# MyPrimeDelivery — Deal / Offer Evidence Contract

Date: 2026-09-14
Status: NON-PRODUCTION IMPLEMENTATION CONTRACT

## Purpose

Define how MyPrimeDelivery may represent time-sensitive Amazon sale/deal products without fabricating urgency, discount depth, Prime status, availability or expiry.

A product and an offer/deal are separate records. Evergreen product qualification must not depend on a sale being active.

## Deal/offer record

Required fields for any future current-sale presentation:

- `offer_id`
- `product_id`
- `marketplace`
- `source_id`
- `source_type`
- `observed_at`
- `evidence_status`
- `freshness_state`
- `deal_state`

Permitted evidence-backed optional fields:

- `current_price`
- `currency`
- `reference_price`
- `discount_amount`
- `discount_percent`
- `deal_start_at`
- `deal_end_at`
- `availability_state`
- `prime_offer_state`

Optional fields may only be rendered when the selected authorised source permits and supplies them.

## Deal states

- `ACTIVE` — fresh authorised evidence currently supports a deal/sale claim.
- `UNKNOWN` — evidence is insufficient to make a current deal claim.
- `STALE` — evidence existed but exceeded its configured freshness interval.
- `EXPIRED` — authoritative timing/evidence indicates the offer has ended.
- `BLOCKED` — conflicting, invalid or disallowed evidence prevents presentation.

## Fail-closed rules

1. Missing `observed_at` -> `UNKNOWN`.
2. Evidence older than the configured source-specific review interval -> `STALE`.
3. Known `deal_end_at` in the past -> `EXPIRED`.
4. Missing/unsupported reference price -> do not calculate or show percentage/amount discount.
5. Conflicting prices, marketplace or offer identity -> `BLOCKED` until reconciled.
6. `ACTIVE` may not be inferred from editorial wording, cached HTML, a crossed-out price with no authorised source provenance, or a previous observation.
7. A product may remain displayable as an evergreen qualified product after a deal becomes `STALE`/`EXPIRED`, but all current-sale urgency must disappear.
8. Prime eligibility and deal status remain separate evidence dimensions; one does not prove the other.

## WordPress mapping

Recommended architecture:

- WooCommerce Product remains the product/catalogue entity.
- Deal/offer evidence is stored as structured MyPrimeDelivery metadata/history, preferably through a small project-owned data layer or clearly namespaced ACF/custom-table fields once scale requirements are known.
- GenerateBlocks/Gutenberg components render current-deal labels only from `ACTIVE` evidence.
- FacetWP filters such as `Deals now`, `Ending soon`, `Prime eligible`, and `Recently verified` must query explicit evidence states, never visual labels alone.

No theme, affiliate-link plugin or deal widget is the canonical evidence source.

## Safe display examples

Allowed when evidence supports them:

- `Deal active — checked 12 minutes ago`
- `Prime eligibility verified — checked 12 minutes ago`
- `Deal ends 21:00 AEST` only when source evidence supplies that expiry
- `32% off` only when current/reference price evidence is authorised and fresh

Fail-closed display examples:

- `Price unavailable`
- `Deal status unknown`
- `Previously observed deal — recheck required`
- hide current-sale badge after freshness expiry

## Synthetic test cases

Future fixtures/tests should cover:

1. ACTIVE + fresh evidence renders deal badge;
2. ACTIVE + missing timestamp fails to UNKNOWN;
3. past end time becomes EXPIRED;
4. stale observation suppresses urgency;
5. missing reference price suppresses discount percent;
6. conflicting source records become BLOCKED;
7. expired deal does not remove evergreen product qualification;
8. deal evidence does not upgrade UNKNOWN Prime status.

## Not authorised by this contract

- scraping Amazon pages;
- live Amazon credentials;
- claiming a specific API/feed has been approved;
- inventing deal expiry times;
- storing or republishing fields not permitted by the selected data licence;
- production publication/deployment.

Exact source, rate limits, cache/freshness windows and field-retention rules remain gated on the authorised Amazon data-provider decision.