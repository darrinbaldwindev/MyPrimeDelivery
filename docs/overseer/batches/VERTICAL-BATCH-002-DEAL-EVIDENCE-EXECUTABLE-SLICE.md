# MyPrimeDelivery — Vertical Batch 002: Executable Deal Evidence Slice

Date: 2026-09-14
Status: ACTIVE
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Fresh scan baseline

Default branch: `agent/overseer/initial-project-timeline`
Exact head at batch creation: `65dc35d34106d4e8081bec037655feca9bb4d920`

The repository already contains:

- owner-approved WordPress direction;
- a 12-category launch taxonomy;
- a documented deal/offer evidence contract;
- a candidate qualification pipeline;
- a deterministic M-03 product/category fixture, validator, renderer and tests;
- GitHub Actions fixture validation;
- a bounded AgentOS Level-2 lifecycle fixture.

The highest-value safe vertical is therefore to convert the deal/offer contract from documentation into executable fail-closed fixture behavior.

## Vertical outcome

Prove, using synthetic data only, that MyPrimeDelivery can distinguish current, stale, expired, unknown and blocked sale evidence without fabricating price urgency or Prime status.

## Task set

### T1 — Deterministic deal fixture

Create a synthetic deal fixture with a fixed `as_of` timestamp and representative offer records covering:

- ACTIVE
- STALE
- EXPIRED
- UNKNOWN
- BLOCKED

No real ASINs, Amazon URLs, affiliate tags, prices copied from Amazon, credentials or production data are permitted.

### T2 — Fail-closed deal validator

Create a standalone validator that enforces:

- synthetic-only identifiers;
- unique offer IDs;
- explicit source/evidence identity;
- no ACTIVE deal without fresh evidence;
- no discount percentage without an evidence-backed current and reference price;
- expiration overrides sale presentation;
- stale evidence cannot remain ACTIVE;
- Prime status is independent from deal status;
- no live Amazon or affiliate URL leakage.

### T3 — Negative assurance tests

Add deterministic tests for malformed or misleading deal records, including:

- ACTIVE without checked-at/source;
- expired offer labelled ACTIVE;
- stale evidence labelled ACTIVE;
- discount without supported reference price;
- reference price not greater than current price;
- duplicate offer identity;
- live Amazon/affiliate destination leakage.

### T4 — Public projection renderer

Create a small renderer/projection that demonstrates public-facing fail-closed behavior:

- ACTIVE evidence may expose a synthetic sale badge/discount only when supported;
- STALE / EXPIRED / UNKNOWN / BLOCKED suppress urgency and discount presentation;
- no fixture record exposes a live outbound destination;
- Prime eligibility is not inferred from sale status.

### T5 — CI integration and regression

Extend the existing fixture-validation workflow so the new deal validator and tests run alongside M-03 checks. Existing M-03 behavior must remain unchanged.

### T6 — Durable result and coordination

Record exact commits, test/CI evidence, preserved UNKNOWNs and no-overall-GREEN status in a Batch 002 result file, then post the substantive result to `darrinbaldwindev/Overseer#49`.

## Preserved UNKNOWNs / boundaries

This batch does not decide or authorise:

- Amazon marketplace/region;
- live Amazon/Creators API/PA API/feed choice;
- Amazon Associates credentials/tag;
- real product prices, reference prices, Prime state or deal state;
- exact production freshness intervals;
- live publication or deployment.

No alternate AgentOS scheduler, registry, ledger, authority, persistence, assurance or source of truth may be created.

## Completion rule

Batch 002 is complete only when the synthetic deal fixture, validator, renderer, negative tests and CI evidence exist durably and the result is reported to the coordination layer. Batch completion is not overall MyPrimeDelivery GREEN.