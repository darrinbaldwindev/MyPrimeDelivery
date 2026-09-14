# MyPrimeDelivery — Vertical Batch 006: Identity, Dedupe and Ranking

Date: 2026-09-14
Status: ACTIVE
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Fresh-scan baseline

Branch: `agent/overseer/initial-project-timeline`
Exact head at batch creation: `a2ea8260a47f069794085161c0fad6c530bd2f0a`

Current verified foundation:
- 58 research evidence rows across three candidate tranches;
- all 12 launch categories represented;
- public/editorial research remains non-authoritative for Prime/rank/deal claims;
- source-rights/provider-authority tests are present in CI;
- no production Amazon credentials, affiliate publication or deployment authority.

## ACTIVE NOW

### T1 — Cross-tranche identity/dedupe analyzer
Create deterministic analysis across all research tranches.

Acceptance:
- load all three current candidate files;
- detect exact normalized-title duplicates across tranches;
- distinguish evidence rows from unique product concepts;
- produce machine-readable summary counts;
- fail on duplicate candidate IDs or category conflicts for identical normalized titles;
- do not delete evidence rows automatically.

### T2 — Product identity contract
Define identity states and ASIN readiness without inventing ASINs.

Acceptance:
- `UNRESOLVED`, `TITLE_ONLY`, `MARKETPLACE_PRODUCT`, `ASIN_VERIFIED` states;
- ASIN may only be stored when source-backed for the intended marketplace;
- unresolved product-family/range rows cannot become `CANDIDATE` or `QUALIFIED` product identities;
- evidence rows can map many-to-one into a stable product identity later.

### T3 — Provisional ranking methodology
Define a deterministic non-production ranking model suitable for synthetic/staging validation.

Acceptance:
- ranking is explicitly provisional and not a claim of Amazon Best Seller Rank;
- Prime eligibility is a hard public-display gate, not an invented score;
- freshness and evidence confidence cap ranking eligibility;
- deal signal may boost presentation only after current evidence exists;
- stale/unknown evidence fails closed;
- ties resolve deterministically.

### T4 — Executable ranking fixture/tests
Create a synthetic ranking fixture and validator/calculator proving deterministic ordering and fail-closed handling of stale/unknown evidence.

### T5 — CI + readiness reconciliation
Add identity/dedupe/ranking checks alongside existing checks, then update M-04 with exact evidence.

## BLOCKED / HOLD / UNKNOWN

- authoritative Amazon product/Prime/rank/deal provider;
- canonical live marketplace promotion;
- real ASIN resolution for research rows;
- Amazon Associates publication authority;
- provider-specific refresh windows;
- production deployment/publication.

## Protected boundary

No ASIN may be guessed. No public research source may silently become Prime/rank/deal authority. No live Amazon access, scraping, affiliate publication, credentials, deployment or production write is authorised.

## Completion rule

Batch 006 completes when dedupe/identity analysis, product identity contract, provisional ranking contract, executable synthetic ranking tests, CI evidence, readiness update and durable result are committed and verified on an exact head.