"""Independent source-cell oracles for final ranking, partition and output QA."""
from collections import Counter, defaultdict
from decimal import Decimal
import logging
import re

import httpx
import pytest

from app.interactive.service import generate_interactive
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings
from test_analytical_pipeline import RAW, mock_provider
from test_interactive import submission

FAMILIES = ('rotation', 'angulation', 'inclination', 'vertical', 'relative_vertical', 'buccolingual', 'mesiodistal')


def raw_oracle():
    result = {}
    for line in RAW.splitlines():
        cells = [c.strip() for c in line.strip('|').split('|')]
        if not re.fullmatch(r'\d{2}', cells[0]):
            continue
        for family, cell in zip(FAMILIES, cells[1:], strict=True):
            match = re.fullmatch(r'([+-]?\d+(?:\.\d+)?)(?: ([DMBLEI]))?', cell)
            result[cells[0], family] = (Decimal(match[1]), match[2], cell) if match else None
    return result


@pytest.mark.parametrize('module', ['macro', 'micro', 'nano'])
def test_every_source_scalar_direction_zero_missing_and_reference_is_preserved(module):
    oracle = raw_oracle()
    r = generate_interactive(submission(RAW, module), settings=ReportSettings())
    tokens = {t.id: t.token for t in r.parsed.teeth}
    assert len(oracle) == len(r.parsed.measurements) == 105
    assert sum(v is None for v in oracle.values()) == 2
    assert sum(v is not None and v[0] == 0 for v in oracle.values()) == 6
    for m in r.parsed.measurements:
        expected = oracle[tokens[m.tooth_ref], m.recognized_label]
        assert m.span and RAW[m.span.start:m.span.end] == m.raw_value
        if expected is None:
            assert m.signed_decimal is None and m.numeric_status == 'MISSING'
        else:
            scalar, label, source = expected
            assert str(m.signed_decimal) == str(scalar)
            assert m.raw_direction == label and m.raw_value.strip() == source
            assert m.unit == ('deg' if m.recognized_label in FAMILIES[:3] else 'mm')
    assert r.parsed.status == 'PARTIAL'  # underlying classification is unchanged
    assert 'Successfully parsed with 2 missing values' in r.summary
    assert all(s.text in r.export_text for s in r.sections)


@pytest.mark.parametrize('reverse', [False, True])
def test_every_upper_half_entry_in_every_family_is_grouped_exactly_once(reverse):
    lines = RAW.splitlines()
    raw = '\n'.join(lines[:4] + list(reversed(lines[4:]))) if reverse else RAW
    r = generate_interactive(submission(raw, 'nano'), settings=ReportSettings())
    oracle = raw_oracle()
    tokens = {t.id: t.token for t in r.parsed.teeth}
    measurements = {m.id: m for m in r.parsed.measurements}
    for family in FAMILIES[3:]:
        source = {token: v for (token, field), v in oracle.items() if field == family and v and abs(v[0]) > 0}
        ranked = sorted((abs(v[0]) for v in source.values()), reverse=True)
        cutoff = ranked[(len(ranked)-1)//2]
        expected = {token for token, v in source.items() if abs(v[0]) >= cutoff}
        groups = [f for f in r.analytical_findings if f.kind == 'CONCENTRATION'
                  and measurements[f.selected_refs[0]].recognized_label == family]
        counts = Counter(tokens[measurements[ref].tooth_ref] for f in groups for ref in f.selected_refs)
        assert counts == Counter({token: 1 for token in expected})
        for f in groups:
            own = [measurements[ref] for ref in f.selected_refs]
            assert len({m.raw_direction for m in own}) == 1
            assert len({('upper' if tokens[m.tooth_ref][0] in '12' else 'lower', 'anterior' if tokens[m.tooth_ref][1] in '123' else 'posterior') for m in own}) == 1
            assert len(f.source_refs) == len(source)
        if family == 'buccolingual':
            assert cutoff == Decimal('0.40')
            assert expected == {'11', '12', '13', '21', '22', '24', '26'}
            f24 = next(f for f in groups if any(tokens[measurements[ref].tooth_ref] == '24' for ref in f.selected_refs))
            assert 'Tooth 24 in upper-arch posterior, L source label, 0.40 mm' in f24.text
    assert not re.search(r'(\d+(?:\.\d+)?)–\1 mm', '\n'.join(s.text for s in r.sections))


@pytest.mark.parametrize('transposed', [False, True])
def test_boundary_ties_across_eight_groups_are_not_truncated(transposed):
    teeth = ['11', '14', '21', '24', '31', '34', '41', '44']
    values = ['0.400 L', '0.40 B', '0.400 B', '0.40 L', '0.400 B', '0.40 L', '0.400 L', '0.40 B']
    raw = ('Movement\t'+'\t'.join(teeth)+'\nTranslation B / L (mm)\t'+'\t'.join(values)) if transposed else (
        'Tooth\tTranslation B / L (mm)\n'+'\n'.join(t+'\t'+v for t,v in zip(teeth, values)))
    r = generate_interactive(submission(raw, 'nano'), settings=ReportSettings())
    by_ref = {m.id: m for m in r.parsed.measurements}
    tokens = {t.id: t.token for t in r.parsed.teeth}
    groups = [f for f in r.analytical_findings if f.kind == 'CONCENTRATION']
    assert len(groups) == 8
    assert Counter(tokens[by_ref[ref].tooth_ref] for f in groups for ref in f.selected_refs) == Counter(teeth)
    assert all('–' not in f.text for f in groups)


def test_macro_maxima_ranges_and_direction_counts_match_independent_source_cells():
    r = generate_interactive(submission(RAW), settings=ReportSettings())
    oracle = raw_oracle()
    by_ref = {m.id: m for m in r.parsed.measurements}
    tokens = {t.id: t.token for t in r.parsed.teeth}
    for f in r.analytical_findings:
        if f.kind not in {'MAXIMUM', 'RANGE', 'DIRECTION_DISTRIBUTION'}:
            continue
        family = by_ref[f.source_refs[0]].recognized_label
        source = {t: v for (t, field), v in oracle.items() if field == family and v is not None}
        assert {tokens[by_ref[ref].tooth_ref] for ref in f.source_refs} == set(source)
        if f.kind == 'MAXIMUM':
            maximum = max(abs(v[0]) for v in source.values())
            expected = {t for t, v in source.items() if abs(v[0]) == maximum}
            # Different source precision/directions can have separate tied facts.
            all_maxima = [g for g in r.analytical_findings if g.kind == 'MAXIMUM' and by_ref[g.source_refs[0]].recognized_label == family]
            assert {tokens[by_ref[ref].tooth_ref] for g in all_maxima for ref in g.selected_refs} == expected
        elif f.kind == 'RANGE':
            low, high = min(abs(v[0]) for v in source.values()), max(abs(v[0]) for v in source.values())
            assert f'{low}–{high}' in f.text
        else:
            for label, count in Counter(v[1] or 'unlabelled' for v in source.values()).items():
                assert f'{label}: {count}' in f.text


def test_micro_priority_and_demo_choices_match_independent_angular_ranks():
    oracle = raw_oracle()
    ranks, maxima = defaultdict(set), defaultdict(set)
    for family in FAMILIES[:3]:
        source = {t: v for (t, field), v in oracle.items() if field == family and v and v[0] != 0}
        levels = sorted({abs(v[0]) for v in source.values()}, reverse=True)
        for token, value in source.items():
            if abs(value[0]) in levels[:2]:
                ranks[token].add(family)
            if abs(value[0]) == levels[0]:
                maxima[token].add(family)
    expected = sorted(ranks, key=lambda t: (-len(maxima[t]), -len(ranks[t]), t))[:5]
    r = generate_interactive(submission(RAW, 'micro'), settings=ReportSettings())
    by_ref = {m.id: m for m in r.parsed.measurements}
    tokens = {t.id: t.token for t in r.parsed.teeth}
    profiles = [f for f in r.analytical_findings if f.kind == 'ANGULAR_PRIORITY']
    assert [tokens[by_ref[f.selected_refs[0]].tooth_ref] for f in profiles] == expected == ['11', '12', '15', '21', '23']
    for f in profiles:
        own = [by_ref[ref] for ref in f.selected_refs]
        token = tokens[own[0].tooth_ref]
        assert {m.recognized_label for m in own} == ranks[token]
        assert {tokens[m.tooth_ref] for m in own} == {token}
    for f in r.analytical_findings:
        if f.kind in {'CANDIDATE', 'ALTERNATIVE'}:
            token = tokens[by_ref[f.selected_refs[0]].tooth_ref]
            assert f.kind == ('CANDIDATE' if maxima[token] else 'ALTERNATIVE')
        if f.kind == 'NO_CANDIDATE':
            token = tokens[by_ref[f.selected_refs[0]].tooth_ref]
            assert token == '18' and all(oracle[token, field][0] == 0 for field in FAMILIES[:3])


def test_nano_component_shortlist_and_arch_quantities_match_independent_source_cells():
    oracle = raw_oracle()
    notable = defaultdict(set)
    for family in FAMILIES:
        source = {t: v for (t, field), v in oracle.items() if field == family and v and v[0] != 0}
        magnitudes = sorted((abs(v[0]) for v in source.values()), reverse=True)
        cutoff = magnitudes[(len(magnitudes)-1)//4]
        for token, value in source.items():
            if abs(value[0]) >= cutoff:
                notable[token].add(family)
    expected = [t for t in sorted(notable, key=lambda t: (-len(notable[t]), t))[:4] if len(notable[t]) >= 2]
    r = generate_interactive(submission(RAW, 'nano'), settings=ReportSettings())
    by_ref = {m.id: m for m in r.parsed.measurements}
    tokens = {t.id: t.token for t in r.parsed.teeth}
    profiles = [f for f in r.analytical_findings if f.kind == 'MULTI_COMPONENT']
    assert [tokens[by_ref[f.selected_refs[0]].tooth_ref] for f in profiles] == expected == ['12', '11', '13', '21']
    for f in profiles:
        own = [by_ref[ref] for ref in f.selected_refs]
        assert {m.recognized_label for m in own} == notable[tokens[own[0].tooth_ref]]
    for f in [f for f in r.analytical_findings if f.kind == 'TOKEN_GROUP']:
        group = [by_ref[ref] for ref in f.selected_refs]
        tooth_count = len({m.tooth_ref for m in group})
        numerical = sum(oracle[tokens[m.tooth_ref], m.recognized_label] is not None for m in group)
        assert f'{tooth_count} tooth tokens, {numerical} available numerical entries across {len(group)} positions' in f.text


@pytest.mark.parametrize('outcome', ['success', 'rate_limit', 'rejected', 'missing_key', 'connection_error'])
def test_diagnostics_distinguish_requested_attempted_succeeded_and_fallback(outcome, caplog):
    settings, client, calls = mock_provider(status=429 if outcome == 'rate_limit' else 200,
        mutate=(lambda x: x['sections'][0].update(text='Unsafe 999 mm')) if outcome == 'rejected' else None)
    if outcome == 'missing_key':
        settings = ReportSettings()
    if outcome == 'connection_error':
        def fail(request):
            calls.append({})
            raise httpx.ConnectError('PRIVATE_KEY and source details must not escape')
        client = GroqClient(settings, transport=httpx.MockTransport(fail))
    with caplog.at_level(logging.INFO, logger='finova.analysis'):
        r = generate_interactive(submission(RAW), settings=settings, client=client)
    success = outcome == 'success'
    assert len(calls) == (0 if outcome == 'missing_key' else 1)
    assert r.generation.used_mode == ('GROQ_AI' if success else 'STANDARD_TEMPLATES')
    assert 'requested=True' in caplog.text
    assert f"attempted={outcome != 'missing_key'}" in caplog.text
    assert f'succeeded={success}' in caplog.text and f'fallback={not success}' in caplog.text
    if outcome in {'rate_limit', 'rejected'}:
        assert 'provider_responded=True' in caplog.text
    assert all(secret not in caplog.text for secret in ['PRIVATE', '18.90', RAW, r.parsed.raw_sha256])
