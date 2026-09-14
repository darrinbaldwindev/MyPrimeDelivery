# MyPrimeDelivery — Provisional Ranking Methodology

Date: 2026-09-14
Status: PROVISIONAL / NON-PRODUCTION

## Purpose

Define a deterministic ranking model for synthetic/staging validation while the owner has not yet selected a live definition of `top` and no authorised live Amazon ranking source is integrated.

This methodology is **not Amazon Best Seller Rank** and must never be described as Amazon's ranking.

## Hard eligibility gates

A product is rankable for public presentation only when all required live gates are satisfied:
- concrete product identity;
- intended marketplace explicit;
- Prime eligibility current and source-backed;
- selection evidence permitted and current;
- product evidence within freshness limits;
- required content/display rights present;
- outbound destination separately verified if a CTA is shown.

If a required field is UNKNOWN, STALE, BLOCKED, or expired, the product is not eligible for a live ranked list.

## Provisional score

For synthetic/staging evaluation only, calculate a 0–100 score from explicit evidence dimensions:

- `selection_strength` — 0–40
- `evidence_confidence` — 0–25
- `freshness_strength` — 0–20
- `deal_relevance` — 0–10
- `editorial_utility` — 0–5

`provisional_score = sum(dimensions)`

### Interpretation

`selection_strength` represents the strength of the permitted selection signal, not Amazon BSR.

`evidence_confidence` rewards stronger provenance and penalises indirect/editorial-only evidence.

`freshness_strength` rewards current evidence and must collapse when evidence expires.

`deal_relevance` is optional and cannot rescue an otherwise ineligible product. Evergreen products may rank without a current deal.

`editorial_utility` is a small bounded factor for shopper usefulness such as breadth, comparison value or guide relevance. It must not override evidence gates.

## Deterministic tie-break

Tie order:
1. higher `evidence_confidence`;
2. higher `freshness_strength`;
3. higher `selection_strength`;
4. lexicographically smaller stable `product_id`.

No random tie-breaking.

## Prime rule

Prime eligibility is not a score boost. For any page explicitly claiming Prime eligibility, current source-backed Prime evidence is a hard inclusion gate.

## Deal rule

A current verified deal may add up to 10 points only where the page/ranking mode permits deal relevance. STALE, EXPIRED or UNKNOWN deal state contributes 0 and cannot display urgency.

## Modes

Future production may expose separate methods rather than one universal score:
- `TOP_PRODUCTS` — evergreen quality/selection emphasis;
- `DEALS_NOW` — current deal relevance plus normal eligibility;
- `RECENTLY_VERIFIED` — freshness-first ordering;
- `EDITORIAL_PICK` — explicit editorial list with evidence disclosure.

Each mode must carry a `ranking_method_id` and version so historical outputs can be reproduced.

## Production gate

Before this becomes live ranking logic, the owner must approve:
1. target marketplace;
2. exact definition(s) of `top`;
3. authoritative source/provider fields;
4. source-specific freshness windows;
5. weighting/mode policy;
6. compliance/disclosure wording;
7. negative tests showing stale/unknown evidence fails closed.
