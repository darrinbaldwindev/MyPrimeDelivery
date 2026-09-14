# Overseer Project Log

## Repository

`darrinbaldwindev/MyPrimeDelivery`

## Current canonical product truth — 2026-09-14

MyPrimeDelivery is an Amazon-focused product/category discovery website for top products/categories eligible for Prime delivery.

Owner direction also establishes WordPress as the site platform.

The project is **not** a courier, dispatch, driver-management, maps/routing or last-mile logistics system. Earlier portfolio/log references to a generic "Delivery project" are stale historical classifications and must not control implementation.

## Current repository state

The repository is no longer documentation-only. It contains:
- governance/project contracts;
- WordPress stack/taxonomy/data-model specifications;
- synthetic product/category fixture + fail-closed validator/render tests;
- executable deal-state fixture + tests;
- real research-only Amazon-Australia candidate datasets;
- candidate fail-closed validation;
- GitHub Actions fixture validation.

No live Amazon product is currently qualified for publication from repository evidence alone.

## Historical baseline — 2026-08-26 to 2026-08-31

Earlier work lacked authoritative product-purpose evidence and temporarily reconciled the repository against a generic portfolio "Delivery project" label. That label generated speculative courier/commerce dependency assumptions. Owner direction has superseded that interpretation.

Historical references are retained only as provenance, not as current architecture.

## Current active milestones

### M-03 — Evidence and non-production vertical slice

**Status:** ACTIVE / synthetic slice established.

Maintain the evidence checklist and fail closed on live Amazon claims until marketplace, `top` methodology, authorised data/Prime/deal provider, publication authority and freshness rules are established.

### M-04 — Implementation readiness

**Status:** NON-PRODUCTION WORDPRESS/DISCOVERY SLICE READY; LIVE AMAZON INTEGRATION BLOCKED.

Synthetic data, rendering, deal states, research-candidate validation and CI can progress safely.

### M-05 — Dependency reconciliation

**Status:** RECONCILED TO AMAZON DISCOVERY MODEL.

Current dependency model is:

`authorised Amazon/provider evidence -> normalised MyPrimeDelivery record -> evidence/ranking evaluation -> WordPress/WooCommerce presentation -> governed Amazon outbound CTA`

Courier, dispatch, driver, maps, local checkout/payment/shipping/order dependencies are not part of the current product model.

## Current research state

A first 30-record Amazon-Australia research tranche exists under `fixtures/candidates/first-100-research.json`.

Batch 004 adds a second gap-closing tranche under `fixtures/candidates/research-tranche-004.json` and introduces `docs/RESEARCH-SOURCE-QUALITY-HIERARCHY.md` so discovery evidence cannot be mistaken for Prime/ranking/publication authority.

Research records may be `DISCOVERED` or `CANDIDATE`; `QUALIFIED` remains evidence-gated.

## AgentOS Level-2 alignment

MyPrimeDelivery retains the bounded non-production Level-2 fixture at `fixtures/level2/myprime-product-lifecycle.json`.

Do not create an alternate scheduler, mission ledger, worker registry, authority, persistence, governance, Green or PRS system.

## Hard boundaries

No merge/approve/ready/rebase/deploy authority, production writes, credential changes, Amazon ordering/account actions, purchases, affiliate publication, live scraping, or production autonomy without explicit owner authorization.

## Reassessment triggers

Reassess immediately when any of the following become authoritative:
- target Amazon marketplace;
- ranking/selection methodology for `top`;
- authorised Amazon product/Prime/deal interface;
- Amazon Associates/publication authority;
- live freshness/expiry requirements;
- staging/production hosting authority.

**Current confidence:** High on product purpose, WordPress direction, synthetic/readiness architecture and research boundaries; low/blocked on live Amazon integration/publication authority.
