# MyPrimeDelivery — Vertical Batch 008: Creators API Mapping, Evidence Lineage and WordPress Staging

Date: 2026-09-15
Status: ACTIVE
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Fresh-scan baseline

Branch: `agent/overseer/initial-project-timeline`
Exact head at batch creation: `e3f841293f5174d2ff988bc040580f3df1e9475e`

Verified foundation:
- provider-neutral evidence adapter exists and is fail-closed;
- exact-head CI for Batch 007 succeeded;
- source-rights/provider-authority checks remain independent;
- no live provider credentials, publication authority, production writes or deployment authority.

## Current external provider evidence

Amazon Creators API official documentation currently exposes identity/product resources including ASIN, ParentASIN, ItemInfo, Images and OffersV2. Australia targets `www.amazon.com.au`; requests require a valid Partner Tag for the target marketplace and approved Creators API access. License and cache rules remain separate compliance gates.

This batch treats Creators API as a provider-profile candidate only. It does not claim account approval, credentials, production rights, or that every required MyPrimeDelivery field is available from the API.

## ACTIVE NOW

### T1 — Provider-specific mapping profile
Define a bounded Creators API AU profile mapping only verified documented fields into the existing provider-neutral contract.

### T2 — Field rights/freshness policy
Keep identity/title/parent/offer/deal/price/image fields separately permissioned and freshness-scoped. Unknown or unsupported field policy fails closed.

### T3 — Snapshot lineage and replay
Create deterministic synthetic lineage rules for repeated provider snapshots:
- stable snapshot identity;
- source/evidence version lineage;
- duplicate replay is idempotent;
- older snapshot cannot overwrite newer evidence;
- conflicting same-version snapshot is rejected.

### T4 — WordPress staging projection
Project accepted normalized evidence into a synthetic WordPress-facing product card/category payload with all outbound/publication controls disabled.

### T5 — CI/readiness/result closure
Wire all new checks into existing Fixture validation without removing previous assurance, reconcile M-04, verify exact-head CI, record result, and report to Overseer #49.

## BLOCKED / HOLD / UNKNOWN

- real Creators API account approval and credentials;
- owner promotion of Amazon AU as canonical live marketplace;
- final production definition of `top`;
- whether Creators API exposes a sufficiently authoritative Prime-eligibility signal for MyPrimeDelivery's exact Prime claim;
- Amazon Associates publication/tag authority;
- production freshness windows after exact license/field requirements are approved;
- live WordPress publication/deployment.

## Protected boundary

No network calls, credentials, account mutation, scraping, affiliate publication, production write or deployment. Provider documentation informs mapping only; it does not self-authorize live use.
