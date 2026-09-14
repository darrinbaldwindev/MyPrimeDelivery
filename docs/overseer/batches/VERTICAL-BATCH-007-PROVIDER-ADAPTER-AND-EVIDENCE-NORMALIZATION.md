# MyPrimeDelivery — Vertical Batch 007: Provider Adapter and Evidence Normalization

Date: 2026-09-14
Status: ACTIVE
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Fresh-scan baseline

Branch: `agent/overseer/initial-project-timeline`
Exact head at batch creation: `6ff43782b4f86214ebc0b0466ce710910fe915dd`

Current verified foundation:
- synthetic product/category, deal, candidate, identity/dedupe and provisional-ranking slices are executable in CI;
- source-rights/provider-authority checks already fail closed;
- 58 research evidence rows remain non-production inputs;
- no live Amazon provider, credentials, affiliate publication or deployment authority exists.

## ACTIVE NOW

### T1 — Provider-neutral evidence adapter contract
Define a provider-independent boundary between an authorised Amazon data provider and MyPrimeDelivery canonical product evidence.

Acceptance:
- provider payload is not trusted implicitly;
- source/rights/provider authority must be explicit;
- marketplace and ASIN identity must be explicit;
- Prime, freshness, selection/rank and deal evidence remain independent fields;
- adapter output carries provenance and checked-at metadata;
- no provider-specific credential or network logic enters the canonical contract.

### T2 — Executable synthetic adapter
Implement a pure local adapter over synthetic records only.

Acceptance:
- authoritative, current, identity-consistent fixture can normalize to an evidence packet;
- ASIN mismatch fails closed;
- marketplace mismatch fails closed;
- stale provider evidence fails closed for current claims;
- conflicting parent/variant identity fails closed;
- unknown provider authority or reuse rights fails closed;
- no network or publication authority.

### T3 — Negative assurance
Add tests proving a high-confidence or high-score payload cannot bypass identity, authority, marketplace or freshness gates.

### T4 — CI integration
Run adapter checks alongside all existing product/deal/candidate/identity/ranking/source-rights checks without deleting or weakening prior assurance.

### T5 — Readiness reconciliation and durable result
Update M-04 with exact evidence and preserve live-integration blockers.

## NEXT

- map an owner-approved authorised Amazon provider onto this adapter contract;
- add provider-specific field-permission/freshness policy only after the provider is selected;
- resolve real ASIN identities from authorised evidence;
- feed normalized packets into staging WordPress components without live publication.

## BLOCKED / HOLD / UNKNOWN

- canonical live Amazon marketplace promotion;
- owner-approved production definition of `top`;
- authorised Amazon product/Prime/rank/deal provider and credentials;
- real source-backed ASIN resolution;
- provider-specific freshness/expiry policy;
- Amazon Associates publication authority;
- production deployment/publication.

## Protected boundary

No credentials, network calls, scraping, live Amazon writes, affiliate publication or production deployment are authorised. The adapter is a validation/normalization boundary, not a new authority source. It must consume authority proven elsewhere and fail closed when evidence is incomplete or contradictory.

## Completion rule

Batch 007 completes when the provider-neutral contract, synthetic adapter fixture, negative tests, CI integration, readiness update and durable result are committed and exact-head CI succeeds.