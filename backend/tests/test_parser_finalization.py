"""Original synthetic oracles only. Every ordinary provider call is mocked."""

import importlib.util
import json
from pathlib import Path

from fastapi.testclient import TestClient
import httpx
from pydantic import ValidationError
import pytest

from app.development_env import load_development_env
from app.domain.models import ParseResult, RawTMTSubmission, SourceContext
from app.main import app
from app.parser.certification import certify_markdown, structural_prompt, validate_proposal
from app.parser.cloud import ParserSettings, load_parser_settings
from app.parser.contracts import AssistedSubmission, AutomaticParseResult, StructuralProposal
from app.parser.detection import detect_source
from app.parser.pipeline import automatic_parse
from app.parser.service import parse_table
from app.parser.synthetic import cloud_example_allowed, synthetic_examples
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings
from app.review.service import review_table
from app.semantics.normalization import assess_semantics
from app.semantics.registry import APPROVED_RELEASE_DIGESTS

CATALOG = synthetic_examples()
MARKDOWN = next(f['raw_text'] for f in CATALOG if f['id'] == 'synthetic-markdown-rows')


def submission(raw=MARKDOWN, *, consent=True, **kwargs):
    cls = AssistedSubmission if consent else RawTMTSubmission
    return cls(raw_text=raw, synthetic_data_confirmed=True, **({'cloud_synthetic_consent': True} if consent else {}), **kwargs)


def settings(**kwargs):
    return ParserSettings(api_key='SYNTHETIC_PARSER_KEY', environment='development', synthetic_transmission_enabled=True, **kwargs)


def proposal(raw=MARKDOWN):
    cert = certify_markdown(raw)
    assert cert
    return {'grammar': 'MARKDOWN_PIPE_V1', 'orientation': cert.layout.orientation, 'rows': cert.ids}


def mock_client(config=None, *, raw=MARKDOWN, mutate=None, status=200, captured=None):
    config = config or settings()
    def handler(request):
        if captured is not None: captured.append(request)
        data = proposal(raw)
        if mutate: mutate(data)
        return httpx.Response(status, json={'model': config.model, 'choices': [{'finish_reason': 'stop',
                              'message': {'role': 'assistant', 'content': json.dumps(data)}}],
                              'usage': {'prompt_tokens': 101, 'completion_tokens': 41, 'total_tokens': 142}},
                              headers={'retry-after': '60'})
    return GroqClient(config, transport=httpx.MockTransport(handler))


@pytest.mark.parametrize('fixture', CATALOG, ids=lambda f:f['id'])
def test_independently_specified_original_synthetic_oracles(fixture):
    raw = fixture['raw_text']
    if fixture['cloud_allowed']:
        result = automatic_parse(submission(raw), assisted=True, settings=settings(), client=mock_client(raw=raw))
        assert result.pipeline.assistance.status == 'ACCEPTED'
    else:
        result = automatic_parse(submission(raw, consent=False), settings=ParserSettings())
    expected = fixture['expected']
    assert result.raw_text == raw
    assert result.layout.orientation == expected['orientation']
    assert [m.raw_value for m in result.measurements] == expected['raw_values']
    assert [str(m.signed_decimal) if m.signed_decimal is not None else None for m in result.measurements] == expected['decimals']
    assert result.pipeline.detection.detected_source == expected['detected_source']
    assert result.pipeline.detection.verified_source is None
    assert result.source.verification_status == 'UNVERIFIED'


@pytest.mark.parametrize('text,expected,status', [
    ('Tooth\tRotation (deg)\n13\t1', 'Unknown', 'UNKNOWN'),
    ('# SYNTHETIC ClinCheck\nTooth\tRot (°)\n13\t1', 'ClinCheck', 'DETECTED_UNVERIFIED'),
    ('Source: SureSmile\nMovement\tUR1\nRotation (deg)\t1', 'SureSmile', 'DETECTED_UNVERIFIED'),
    ('Align Final / Doctor Final\nTooth\tRotation (deg)\n13\t1', 'ClinCheck', 'DETECTED_UNVERIFIED'),
    ('Displacement Type: Cusp Tip\nTooth\tRotation (deg)\n13\t1', 'SureSmile', 'DETECTED_UNVERIFIED'),
    ('ClinCheck / SureSmile\nTooth\tRotation (deg)\n13\t1', 'Unknown', 'CONFLICT'),
    ('Source: ClinCheck\nDisplacement Type: Cusp Tip\nTooth\tRot (deg)\n13\t1', 'Unknown', 'CONFLICT'),
    ('Align Final\nTooth\tRotation (deg)\n13\t1', 'Unknown', 'UNKNOWN'),
    ('Cusp Tip\nTooth\tRotation (deg)\n13\t1', 'Unknown', 'UNKNOWN'),
])
def test_deterministic_indicators_never_establish_vendor_semantics(text,expected,status):
    result = automatic_parse(submission(text, consent=False), settings=ParserSettings())
    detection = result.pipeline.detection
    assert (detection.detected_source, detection.status) == (expected, status)
    assert detection.verified_source is None
    assert all(not m.semantics_verified and m.canonical_axis is None for m in result.measurements)
    for indicator in detection.indicators:
        for cell in indicator.evidence:
            assert text[cell.span.start:cell.span.end] == cell.raw


def test_ambiguous_numbering_is_only_syntax_not_an_automatic_context_claim():
    result = automatic_parse(submission('Tooth\tRotation (deg)\n13\t1',consent=False),settings=ParserSettings())
    assert result.pipeline.detection.notation_candidates == ['FDI_SYNTAX','UNIVERSAL_SYNTAX']
    assert result.source.context.notation == 'UNKNOWN'
    assert result.teeth[0].normalized_identifier is None
    assert any(c.field == 'notation' for c in result.pipeline.clarifications)


def test_targeted_clarifications_keep_explicit_metadata_unverified():
    context = SourceContext(notation='FDI',source_version='UNVERIFIED_VERSION',scope='INCREMENTAL',plan_mode='COMPARISON')
    result = automatic_parse(submission('Tooth\tRotation\n13\t?',consent=False,context=context),settings=ParserSettings())
    assert not any(c.field == 'notation' and c.code == 'METADATA_REQUIRED' for c in result.pipeline.clarifications)
    assert result.source.metadata_status == 'USER_CLAIMS_UNVERIFIED'
    assert {'STAGE_REQUIRED','COMPARISON_NOT_ABSOLUTE'} <= {i.code for i in result.issues}
    assert any(c.measurement_ids == ['measurement-1'] for c in result.pipeline.clarifications)


def test_deterministic_first_makes_zero_provider_calls_even_when_configured():
    client=GroqClient(settings(),transport=httpx.MockTransport(lambda _:pytest.fail('Automatic transmission')))
    r=automatic_parse(submission(), settings=settings(), client=client)
    assert r.pipeline.assistance.available and r.pipeline.assistance.attempts == 0
    assert r.status == 'UNSUPPORTED' and not r.measurements
    good=automatic_parse(submission('Tooth\tRotation (deg)\n13\t1'),assisted=True,settings=settings(),client=client)
    assert good.pipeline.assistance.status == 'BLOCKED'
    assert good.pipeline.assistance.reason == 'DETERMINISTIC_RESULT_AVAILABLE'


@pytest.mark.parametrize('config', [ParserSettings(), ParserSettings(api_key='SYNTHETIC'),
    ParserSettings(api_key='SYNTHETIC',environment='development'),
    ParserSettings(api_key='SYNTHETIC',environment='production',synthetic_transmission_enabled=True),
    ParserSettings(api_key='SYNTHETIC',environment='test',synthetic_transmission_enabled=True)])
def test_disabled_or_non_development_cloud_never_calls(config):
    r=automatic_parse(submission(),assisted=True,settings=config,
                      client=GroqClient(config,transport=httpx.MockTransport(lambda _:pytest.fail('Cloud disabled'))))
    assert r.pipeline.assistance.status == 'BLOCKED' and r.pipeline.assistance.attempts == 0
    assert not r.pipeline.assistance.real_patient_transmission_enabled


def test_synthetic_label_or_claim_is_not_enough_to_transmit_arbitrary_content():
    raw=MARKDOWN.replace('−1.2500','2.00')
    assert not cloud_example_allowed(raw)
    r=automatic_parse(submission(raw),assisted=True,settings=settings(),
                      client=GroqClient(settings(),transport=httpx.MockTransport(lambda _:pytest.fail('Noncatalog upload'))))
    assert r.pipeline.assistance.reason == 'SYNTHETIC_CATALOG_ONLY' and r.pipeline.assistance.attempts == 0


def test_missing_or_malformed_synthetic_catalog_disables_cloud_without_breaking_intake(monkeypatch):
    import app.parser.synthetic as catalog
    def unavailable(): raise OSError('PRIVATE_PATH')
    monkeypatch.setattr(catalog,'synthetic_examples',unavailable)
    assert not catalog.cloud_example_allowed(MARKDOWN)
    result=automatic_parse(submission(consent=False),settings=settings())
    assert not result.pipeline.assistance.available and result.raw_text==MARKDOWN
    assert 'PRIVATE_PATH' not in result.model_dump_json()


def test_library_calls_also_require_per_action_cloud_consent():
    r=automatic_parse(submission(consent=False),assisted=True,settings=settings(),
                      client=GroqClient(settings(),transport=httpx.MockTransport(lambda _:pytest.fail('No consent'))))
    assert r.pipeline.assistance.reason == 'CLOUD_CONSENT_REQUIRED'


def test_certified_assistance_reuses_lexical_models_and_exact_provenance():
    requests=[]
    result=automatic_parse(submission(),assisted=True,settings=settings(),client=mock_client(captured=requests))
    assert result.pipeline.assistance.origin == 'GROQ_PROPOSAL_CERTIFIED'
    assert result.pipeline.assistance.certificate == 'MARKDOWN_PIPE_V1'
    assert len(requests)==1
    payload=json.loads(requests[0].content)
    assert requests[0].headers['authorization']=='Bearer SYNTHETIC_PARSER_KEY'
    assert payload['response_format']['json_schema']['strict'] is True
    assert 'tools' not in payload and 'store' not in payload
    assert 'api_key' not in payload['messages'][1]['content']
    for m in result.measurements:
        assert m.raw_value == MARKDOWN[m.span.start:m.span.end]
        assert m.raw_label == MARKDOWN[m.header_span.start:m.header_span.end]
    for tooth in result.teeth:
        assert tooth.raw_identifier == MARKDOWN[tooth.span.start:tooth.span.end]
    assert result.measurements[1].numeric_status == 'EXPLICIT_ZERO'
    assert result.measurements[2].signed_decimal is None and result.measurements[3].signed_decimal is None
    assert AutomaticParseResult.model_validate_json(result.model_dump_json()) == result
    lexical=ParseResult.model_validate(result.model_dump(exclude={'pipeline'}))
    assessment=assess_semantics(lexical)
    assert assessment.status=='DISABLED'
    assert all(not m.canonical_measurement_ready for m in assessment.measurements)
    assert all(c.canonical_value is None for m in assessment.measurements for c in m.components)
    assert APPROVED_RELEASE_DIGESTS == frozenset()
    # Review/report endpoints never consume a returned proposal as semantic authority.
    review=review_table(submission(consent=False))
    assert review.coverage.eligible_positions==0 and not review.clinical_analysis_enabled


@pytest.mark.parametrize('mutation', ['swap_columns','swap_rows','duplicate','omit','invent','wrong_orientation','extra_value','different_grammar'])
def test_valid_json_or_matching_values_do_not_prove_cell_associations(mutation):
    def mutate(data):
        if mutation=='swap_columns': data['rows'][1][1],data['rows'][1][2]=data['rows'][1][2],data['rows'][1][1]
        if mutation=='swap_rows': data['rows'][1:]=list(reversed(data['rows'][1:]))
        if mutation=='duplicate': data['rows'][1][1]=data['rows'][1][2]
        if mutation=='omit': data['rows'].pop()
        if mutation=='invent': data['rows'][1][1]='L999C999'
        if mutation=='wrong_orientation': data['orientation']='TEETH_IN_COLUMNS'
        if mutation=='extra_value': data['value']='999 mm'
        if mutation=='different_grammar': data['grammar']='GUESSED_SPACES'
    r=automatic_parse(submission(),assisted=True,settings=settings(),client=mock_client(mutate=mutate))
    assert r.pipeline.assistance.status=='REJECTED' and not r.measurements
    assert r.raw_text==MARKDOWN and r.status=='UNSUPPORTED'


@pytest.mark.parametrize('content',['{}','[]','null','not json','{"grammar":"MARKDOWN_PIPE_V1","rows":[],"rows":[]}'])
def test_malformed_or_duplicate_key_proposals_fail_closed(content):
    assert not validate_proposal(content,certify_markdown(MARKDOWN))


def test_identical_text_in_different_positions_still_cannot_swap_ids():
    raw=MARKDOWN.replace('−1.2500','0.00')
    cert=certify_markdown(raw)
    p=proposal(raw)
    assert cert.lattice[p['rows'][1][1]].raw == cert.lattice[p['rows'][1][2]].raw
    p['rows'][1][1],p['rows'][1][2]=p['rows'][1][2],p['rows'][1][1]
    assert not validate_proposal(json.dumps(p),cert)


@pytest.mark.parametrize('raw',[
    MARKDOWN.replace('| 13 | −1.2500 | 0.00 |','| 13 | −1.2500 |'),
    MARKDOWN.replace('| --- | --- | --- |\n',''),
    MARKDOWN.replace('−1.2500','−1.25\\|00'),
    MARKDOWN+'unknown footer',
    MARKDOWN+'| --- | --- | --- |\n',
    'Tooth  Rotation (deg)  Extrusion (mm)\n13  1',
    'arbitrary unknown text',
])
def test_corrupt_or_unsupported_alignment_has_no_independent_certificate(raw):
    assert certify_markdown(raw) is None


@pytest.mark.parametrize('ending',['\n','\r\n','\r'])
def test_certificate_spans_use_unicode_codepoints_and_assorted_line_endings(ending):
    raw=MARKDOWN.replace('\n',ending)
    cert=certify_markdown(raw)
    assert cert
    for cell in cert.lattice.values(): assert raw[cell.span.start:cell.span.end]==cell.raw
    assert validate_proposal(json.dumps(proposal(raw)),cert)


@pytest.mark.parametrize('status,code',[(401,'GROQ_HTTP_ERROR'),(429,'GROQ_RATE_LIMIT'),(503,'GROQ_UNAVAILABLE'),(500,'GROQ_HTTP_ERROR')])
def test_provider_failures_are_one_attempt_and_do_not_weaken_abstention(status,code,caplog):
    caplog.set_level('DEBUG'); calls=[]
    r=automatic_parse(submission(),assisted=True,settings=settings(),client=mock_client(status=status,captured=calls))
    assert len(calls)==1 and r.pipeline.assistance.reason==code
    assert r.pipeline.assistance.status=='FAILED' and not r.measurements
    assert MARKDOWN not in caplog.text and 'SYNTHETIC_PARSER_KEY' not in caplog.text
    assert 'SYNTHETIC_PARSER_KEY' not in r.model_dump_json()


@pytest.mark.parametrize('exception,code',[(httpx.ReadTimeout('PRIVATE'),'GROQ_TIMEOUT'),(httpx.ConnectError('PRIVATE'),'GROQ_CONNECTION_ERROR')])
def test_timeout_and_network_diagnostics_do_not_escape(exception,code):
    def handler(_): raise exception
    r=automatic_parse(submission(),assisted=True,settings=settings(),client=GroqClient(settings(),transport=httpx.MockTransport(handler)))
    assert r.pipeline.assistance.reason==code and 'PRIVATE' not in r.model_dump_json()


def test_independent_parser_configuration_and_redaction(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY','SYNTHETIC_COMMENT_SECRET')
    monkeypatch.setenv('GROQ_API_KEY_2','SYNTHETIC_PARSER_SECRET')
    monkeypatch.setenv('FINOVA_ENVIRONMENT','development')
    monkeypatch.setenv('FINOVA_PARSER_GROQ_ENABLED','true')
    monkeypatch.setenv('GROQ_PARSER_MODEL','another-structured-model')
    monkeypatch.setenv('GROQ_PARSER_REASONING_EFFORT','medium')
    config=load_parser_settings()
    assert config.configured and config.model=='another-structured-model' and config.reasoning_effort=='medium'
    assert config.api_key.get_secret_value()=='SYNTHETIC_PARSER_SECRET'
    assert 'SECRET' not in repr(config) and 'SECRET' not in config.model_dump_json()
    assert ReportSettings().api_key.get_secret_value()==''


def test_invalid_configuration_abstains_without_echoing_environment(monkeypatch):
    monkeypatch.setenv('GROQ_PARSER_REASONING_EFFORT','PRIVATE_INVALID')
    r=automatic_parse(submission(),assisted=True)
    assert r.pipeline.assistance.reason=='PARSER_CONFIGURATION_INVALID'
    assert 'PRIVATE_INVALID' not in r.model_dump_json()


@pytest.mark.parametrize('values',[{'timeout_seconds':31},{'reasoning_effort':'none'},{'max_completion_tokens':9000},
    {'max_retries':1},{'environment':'staging'},{'model':'private\nheader'},{'timeout_seconds':float('nan')}])
def test_parser_settings_reject_invalid_options(values):
    with pytest.raises(ValidationError): ParserSettings(**values)


def test_usage_metrics_are_numeric_and_model_mismatch_is_rejected():
    response=mock_client().generate(structural_prompt(certify_markdown(MARKDOWN)))
    assert response.model_matches is True and response.total_tokens==142 and response.elapsed_seconds>=0
    config=settings()
    client=GroqClient(config,transport=httpx.MockTransport(lambda _:httpx.Response(200,json={'model':'another-model','usage':{'prompt_tokens':'PRIVATE'}})))
    response=client.generate([])
    assert response.code=='GROQ_MODEL_MISMATCH' and response.content is None and response.prompt_tokens is None


@pytest.mark.parametrize('envelope',[None,[],{'choices':None},{'choices':[None]},
    {'choices':[{'finish_reason':'stop','message':[]}]},
    {'choices':[{'finish_reason':'stop','message':42}]}])
def test_malformed_provider_envelope_shapes_abstain_instead_of_crashing(envelope):
    client=GroqClient(settings(),transport=httpx.MockTransport(lambda _:httpx.Response(200,content=json.dumps(envelope))))
    result=automatic_parse(submission(),assisted=True,settings=settings(),client=client)
    assert result.pipeline.assistance.status=='FAILED' and not result.measurements
    assert result.pipeline.assistance.reason=='GROQ_MALFORMED_OUTPUT'


def test_explicit_env_loader_has_no_evaluation_no_secret_output_and_process_precedence(tmp_path,monkeypatch):
    p=tmp_path/'private.env'
    p.write_text('GROQ_API_KEY_2="SYNTHETIC_FILE"\nUNKNOWN_VARIABLE=ignored\n',encoding='utf-8')
    monkeypatch.setenv('GROQ_API_KEY_2','SYNTHETIC_PROCESS')
    monkeypatch.delenv('UNKNOWN_VARIABLE',raising=False)
    load_development_env(p)
    import os
    assert os.environ['GROQ_API_KEY_2']=='SYNTHETIC_PROCESS' and 'UNKNOWN_VARIABLE' not in os.environ
    p.write_text('GROQ_API_KEY_2=PRIVATE\nGROQ_API_KEY_2=PRIVATE\n')
    with pytest.raises(ValueError,match='^DEVELOPMENT_ENV_UNAVAILABLE_OR_INVALID$'): load_development_env(p)


client=TestClient(app)


def test_versioned_endpoint_is_additive_and_private():
    data=submission(consent=False).model_dump(mode='json')
    old=client.post('/api/parse',json=data)
    new=client.post('/api/v1/tmt/parse',json=data)
    assert new.status_code==200 and new.headers['cache-control']=='no-store'
    assert 'pipeline' not in old.json()
    assert new.json()['raw_text']==old.json()['raw_text']
    assert new.json()['raw_sha256']==old.json()['raw_sha256']
    assert len(new.json()['measurements'])==4  # Phase 4 recognizes Markdown deterministically.
    assert new.json()['pipeline']['assistance']['attempts']==0


@pytest.mark.parametrize('extra',[{}, {'cloud_synthetic_consent':False},{'cloud_synthetic_consent':1},
                                 {'cloud_synthetic_consent':True,'release_override':True}])
def test_assisted_api_requires_affirmative_consent_and_has_no_trust_overrides(extra):
    r=client.post('/api/v1/tmt/parse/assisted',json={**submission(consent=False).model_dump(mode='json'),**extra})
    assert r.status_code==422 and MARKDOWN not in r.text and r.headers['cache-control']=='no-store'


def test_assisted_endpoint_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv('FINOVA_PARSER_GROQ_ENABLED',raising=False)
    r=client.post('/api/v1/tmt/parse/assisted',json=submission().model_dump(mode='json'))
    assert r.status_code==200 and r.json()['pipeline']['assistance']['status']=='BLOCKED'


def test_new_exported_schemas_match_models():
    directory=Path(__file__).resolve().parents[2]/'schemas'
    for name,model,mode in [('automatic-parse-result.v1.json',AutomaticParseResult,'serialization'),
                            ('assisted-parse-request.v1.json',AssistedSubmission,'validation'),
                            ('groq-structure.v1.json',StructuralProposal,'validation')]:
        assert json.loads((directory/name).read_text(encoding='utf-8'))==model.model_json_schema(mode=mode)


def test_connectivity_probes_are_mocked_in_tests_and_missing_keys_skip(monkeypatch):
    script=Path(__file__).resolve().parents[1]/'scripts'/'check_groq_connectivity.py'
    spec=importlib.util.spec_from_file_location('groq_probe',script)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    for service,key in [('comments','GROQ_API_KEY'),('parser','GROQ_API_KEY_2')]:
        monkeypatch.delenv(key,raising=False)
        assert module.probe(service)['status']=='SKIPPED'
        monkeypatch.setenv(key,'SYNTHETIC_PROBE_KEY')
        def handler(request):
            body=json.loads(request.content)
            if service=='comments':
                item=json.loads(body['messages'][1]['content'])['authorized_findings'][0]
                data={'comments':[{'finding_ids':item['finding_ids'],'text':item['approved_wordings'][0]}]}
            else:
                raw=next(f['raw_text'] for f in CATALOG if f['id']=='synthetic-markdown-columns')
                data=proposal(raw)
            return httpx.Response(200,json={'model':'openai/gpt-oss-120b','usage':{'prompt_tokens':10,'completion_tokens':10,'total_tokens':20},
                                           'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(data)}}]})
        result=module.probe(service,transport=httpx.MockTransport(handler))
        assert result['status']=='PASSED' and result['attempts']==1 and result['total_tokens']==20
        assert 'content' not in result and 'SYNTHETIC_PROBE_KEY' not in json.dumps(result)
