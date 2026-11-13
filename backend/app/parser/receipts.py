"""Short-lived stateless original-association receipts, never clinical authority.

No raw text/values are stored. Restart/expiry invalidates receipts. Every use also
recomputes the independent proofs from exact raw text and checks all associations.
"""

import base64
import hashlib
import hmac
import json
import secrets
import time

from app.domain.models import ParseIssue
from app.parser.contracts import Association
from app.parser.recovery import assemble, prove, validate
from app.parser.service import parse_table

_KEY=secrets.token_bytes(32)
TTL=900


def binding(submission):
    data={'raw':submission.raw_text,'source':submission.source_claim,'context':submission.context.model_dump(mode='json')}
    return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest()


def issue(submission, associations: list[Association], *, now=None) -> str:
    payload=json.dumps({'v':1,'binding':binding(submission),'expires':int(time.time() if now is None else now)+TTL,
                        'associations':[a.model_dump() for a in associations]},separators=(',',':')).encode()
    body=base64.urlsafe_b64encode(payload).decode().rstrip('=')
    return body+'.'+hmac.new(_KEY,body.encode(),hashlib.sha256).hexdigest()


def resolve(submission, *, now=None):
    from app.parser.phase4 import deterministic
    baseline=deterministic(submission)
    receipt=getattr(submission,'recovery_receipt',None)
    if receipt is None: return baseline
    try:
        if len(receipt)>100_000: raise ValueError()
        body,signature=receipt.split('.')
        if not hmac.compare_digest(hmac.new(_KEY,body.encode(),hashlib.sha256).hexdigest(),signature): raise ValueError()
        payload=json.loads(base64.urlsafe_b64decode(body+'='*(-len(body)%4)))
        if payload['v']!=1 or payload['binding']!=binding(submission) or not (int(time.time() if now is None else now)<payload['expires']<=int(time.time() if now is None else now)+TTL): raise ValueError()
        proofs=prove(submission.raw_text)
        accepted,rejected=validate(json.dumps({'associations':payload['associations']}),proofs)
        if rejected or not accepted: raise ValueError()
        return assemble(submission,baseline,proofs,accepted)
    except (ValueError,TypeError,KeyError,UnicodeError):
        baseline.issues.append(ParseIssue(code='RECOVERY_RECEIPT_INVALID',severity='ERROR',message='Recovery evidence expired or did not match this exact input/context. Reparse the unchanged source.'))
        baseline.status='PARTIAL' if baseline.measurements else 'INVALID'
        return baseline
