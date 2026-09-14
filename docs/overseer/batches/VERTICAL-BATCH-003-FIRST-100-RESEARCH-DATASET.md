# MyPrimeDelivery — Vertical Batch 003: First-100 Research Dataset

Date: 2026-09-14
Status: ACTIVE
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Fresh scan baseline

Default branch: `agent/overseer/initial-project-timeline`
Exact head at batch creation: `3dc8de70c03d561c93e11b293f99d8c629e5235f`

Current verified foundation:
- owner-corrected Amazon/Prime discovery contract;
- WordPress stack, taxonomy and synthetic product slice;
- candidate qualification contract;
- executable deal-evidence fixture/validator/tests;
- current fixture-validation CI green on prior exact head;
- no production Amazon credentials/data-provider authority.

## Vertical outcome

Create a research-ready, fail-closed first-100 candidate dataset structure and populate a bounded evidence-backed initial tranche from current public Amazon-Australia deal/discovery sources without promoting any record to `QUALIFIED` unless Prime/ranking/freshness requirements are met by authoritative evidence.

## Task set

### T1 — Candidate research schema
Create executable validation for a research candidate dataset.

Acceptance:
- states limited to `DISCOVERED | CANDIDATE | QUALIFIED | REJECTED | STALE | BLOCKED`;
- each record has stable candidate ID, title, category ID, marketplace research direction, source URL/domain, observed-at date/time or explicit UNKNOWN, Prime evidence state, ranking/selection evidence state, freshness state and rejection/block reason where applicable;
- `QUALIFIED` is impossible without Prime + selection/ranking + freshness evidence;
- public web/deal-tracker evidence cannot silently become Amazon-authoritative Prime evidence;
- live affiliate URLs/tags are prohibited in this research dataset.

### T2 — Initial real-candidate tranche
Research current Amazon-Australia candidate products across the 12 launch categories using public sources.

Acceptance:
- target at least 30 distinct real candidates this batch, spread across as many launch categories as evidence allows;
- source and evidence timestamp recorded;
- no copied price/rating/stock claims unless source is cited in the record and state remains research-only;
- no `QUALIFIED` state unless all qualification gates are satisfied.

### T3 — Category coverage analysis
Produce category counts and gaps against the 12-category launch taxonomy.

Acceptance:
- exact candidate counts per category;
- identify weak/empty categories;
- propose next research priority by evidence gap, not by arbitrary quota.

### T4 — Validation and negative tests
Add tests that fail on:
- fake QUALIFIED records;
- missing provenance;
- live Amazon affiliate-tag leakage;
- duplicate candidate IDs;
- unsupported category IDs;
- Prime VERIFIED without authoritative source + checked-at;
- stale evidence presented as current.

### T5 — CI integration
Add candidate dataset checks alongside existing M-03 and deal checks without removing or weakening them.

### T6 — Durable result / coordination
Record exact commits, CI run evidence, candidate counts, coverage gaps and blockers; report substantive outcome to `darrinbaldwindev/Overseer#49`.

## Preserved blockers / UNKNOWNs

- canonical marketplace remains not formally promoted despite Australia being the current research direction;
- definition of `top` remains unselected;
- authoritative Prime/ranking/product source remains unselected;
- Amazon Associates publication authority remains absent;
- source-specific refresh cadence remains unknown;
- production publication/deployment remains unauthorised.

## Completion rule

Batch 003 is complete when schema + initial real-candidate tranche + validation/tests + CI + category coverage/result are durable. This batch may create `DISCOVERED`/`CANDIDATE` research records but must not fabricate `QUALIFIED` live products or imply production readiness.
