# MyPrimeDelivery — Architecture Boundary

## Status

**Reconciled:** 2026-09-13  
**Milestone:** M-03  
**Purpose:** Prevent premature implementation while keeping the first product slice and AgentOS Level-2 workload bounded and evidence-driven.

## Current verified boundary

MyPrimeDelivery is an Amazon product/category discovery project intended to surface top products and categories that are eligible for Prime delivery. It is not a courier, driver, dispatch or last-mile delivery system.

The repository currently contains governance/project-definition documentation, marketing notes, and a deterministic non-production AgentOS Level-2 fixture. No verified production application implementation exists.

## Allowed now

- Project-definition and requirements documentation
- Evidence capture and reconciliation
- Synthetic/non-production fixture work
- Non-production architecture sketches explicitly marked provisional
- Testable acceptance-criteria drafting
- Dependency/capability mapping against the wider portfolio
- Bounded AgentOS Level-2 inspect → edit → reread → diff/verify workloads inside approved fixture paths

## Not yet authorised

- Production deployment
- Amazon account access or ordering
- Amazon/affiliate credentials or secret storage
- Live affiliate publication
- Fabricated Prime-eligibility, rank, stock or price claims
- Unapproved scraping or data acquisition
- Production writes to Amazon or any external commerce service
- Claims that a specific Amazon marketplace, API/feed, affiliate program, ranking formula or refresh cadence has been selected unless supported by owner/evidence

## Architecture decision gates

Product implementation may begin only when the following are evidenced:

1. Target Amazon marketplace/region
2. Definition of "top" and ranking methodology
3. Authorised Prime-eligibility evidence source
4. Authorised product-data source and permitted fields
5. Affiliate/commercial model, if applicable
6. First user journey
7. Minimum product/category/evidence data model
8. Freshness/expiry rules
9. First non-production vertical-slice acceptance tests

## Provisional first product slice

Do not treat this as final architecture. Once the evidence gates are satisfied, the first slice should prove one bounded discovery flow using authorised fixture or product data:

`source evidence -> product/category record -> ranking/eligibility evaluation -> discovery result -> provenance/freshness verification`

The slice must preserve explicit UNKNOWN/stale states rather than converting missing evidence into product claims.

## AgentOS Level-2 fixture boundary

The synthetic lifecycle fixture under `fixtures/level2/` is intentionally independent of live Amazon systems. A valid Level-2 acceptance execution may inspect the fixture, make the single authorised state transition, reread/parse it, and prove by exact diff/receipt that no unrelated path changed. Green and PRS remain external assurance gates; this repository does not create substitute governance or execution systems.

## Overseer rule

When new owner or repository evidence arrives, update the project contract/evidence checklist first. Only then promote provisional decisions into implementation requirements.
