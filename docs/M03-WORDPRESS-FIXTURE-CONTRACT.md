# MyPrimeDelivery M-03 — Synthetic WordPress Fixture Contract

Date: 2026-09-14
Status: NON-PRODUCTION / EVIDENCE-GATED

## Purpose

Define the smallest implementation-ready WordPress product-discovery slice that can be built and tested with synthetic data while preserving the owner-defined product truth: MyPrimeDelivery surfaces top Amazon products and categories that are eligible for Prime delivery.

This contract does not establish any live Amazon ranking, price, stock, Prime eligibility, affiliate entitlement, or marketplace fact.

## Authoritative project decisions used

- Product purpose: Amazon product/category discovery with Prime-delivery eligibility as evidence.
- Delivery surface: WordPress.
- WordPress role: catalogue/discovery surface, not local checkout/order fulfilment.
- Preferred architecture: WordPress + Gutenberg/GenerateBlocks; WooCommerce may supply catalogue primitives; structured evidence fields remain independent of any single Amazon plugin.
- Live Amazon source, target marketplace, ranking method, affiliate account, credentials and freshness cadence remain UNKNOWN / not authorised.

## Synthetic first vertical slice

Render one category page containing three synthetic product records and prove that the UI distinguishes current, stale, and unknown evidence without fabricating unsupported claims.

Required fixture records:

1. `SYNTH-001` — evidence state `CURRENT`
2. `SYNTH-002` — evidence state `STALE`
3. `SYNTH-003` — evidence state `UNKNOWN`

The records are deliberately not real ASINs and must not link to live Amazon product pages.

## Minimum normalized content model

Each fixture product must support these fields:

- `product_id` — synthetic internal fixture identifier
- `asin` — nullable; must remain null in the synthetic fixture
- `marketplace` — `FIXTURE` only
- `category_slug`
- `title`
- `outbound_url` — nullable; null in the first fixture
- `prime_state` — `ELIGIBLE | NOT_ELIGIBLE | UNKNOWN`
- `prime_evidence_source` — fixture evidence identifier or null
- `prime_checked_at` — ISO-8601 timestamp or null
- `ranking_position` — positive integer or null
- `ranking_method` — fixture method identifier or null
- `ranking_checked_at` — ISO-8601 timestamp or null
- `product_refreshed_at` — ISO-8601 timestamp
- `evidence_state` — `CURRENT | STALE | UNKNOWN`
- `evidence_notes` — short fixture-only explanation

Optional commercial fields such as price, rating, stock, image and affiliate URL must remain absent from the first slice unless a future authorised data source explicitly supports them.

## Deterministic render rules

1. `CURRENT` may render fixture Prime/ranking labels only when the matching evidence source and checked-at fields are present.
2. `STALE` must render a visible stale marker and must not be represented as current.
3. `UNKNOWN` must render an explicit unknown/unverified state and must not infer Prime eligibility or ranking.
4. Missing evidence cannot be converted to a positive claim by template defaults.
5. Null `outbound_url` must render no purchase/affiliate CTA.
6. `FIXTURE` marketplace records must display a non-production fixture marker in development/test output.
7. Product ordering in the fixture must be deterministic from the supplied fixture ranking values; it must not imply an Amazon Best Seller rank.

## Fixture ranking rule

For the first slice only, use `ranking_method = FIXTURE_EDITORIAL_ORDER` and fixture ranking positions `1..3`.

This proves sorting/rendering mechanics only. It is not the production definition of “top” and must not be reused as a live ranking methodology without a separate owner/evidence decision.

## Acceptance tests

The slice is acceptable only if deterministic tests prove:

1. three fixture records render in fixture ranking order;
2. CURRENT evidence renders its fixture evidence status and timestamp;
3. STALE evidence is visibly marked stale and cannot render as current;
4. UNKNOWN evidence does not render a Prime-positive or ranking-positive claim;
5. missing outbound URL produces no Amazon/affiliate CTA;
6. no real ASIN, Amazon URL, affiliate tag, credential, customer data, price, stock or payment field exists in the fixture;
7. template/component output includes the fixture/non-production marker;
8. changing a record from CURRENT to STALE changes the rendered state deterministically without changing canonical fixture identity;
9. unsupported evidence-state values fail validation rather than silently degrading to CURRENT;
10. the normalized content model is not coupled to Lasso, AffiliateX, PA-API, Creators API, scraping, or another specific provider.

## Implementation boundary

Permitted next implementation:

- local/non-production WordPress content-type or WooCommerce catalogue field mapping;
- ACF-compatible field specification;
- Gutenberg/GenerateBlocks component specification;
- synthetic fixture import and deterministic rendering tests;
- no-network unit/integration tests.

Not authorised:

- Amazon account or Associates setup;
- Creators API / Product Advertising API credentials;
- scraping;
- live product ingestion;
- live Prime/rank/price/stock claims;
- affiliate publication;
- checkout/payment/order flow;
- production deployment.

## Remaining evidence gates for a live slice

Before replacing synthetic values with real Amazon evidence, resolve and record:

1. target Amazon marketplace/region;
2. authoritative definition of “top” and ranking methodology;
3. authorised product/Prime evidence source and permitted fields;
4. freshness/expiry cadence for each rendered claim;
5. Amazon Associates/commercial model if outbound monetisation is used;
6. compliance rules for images, price, rating, availability, Prime labels and links.

## Exact next safe action

Implement the normalized fixture schema plus a three-record synthetic dataset and deterministic validation/render tests on a non-production branch. Keep all Amazon/provider adapters behind an unimplemented boundary until the remaining live-data gates are resolved.
