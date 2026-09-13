# MyPrimeDelivery — M-03 WordPress Data Model & First Non-Production Slice

Date: 2026-09-14  
Status: IMPLEMENTATION-READY SPEC / SYNTHETIC DATA ONLY

## Purpose

Define the smallest reusable WordPress product-discovery slice for MyPrimeDelivery without requiring live Amazon credentials, production ingestion, scraping, affiliate publication, or assumptions about the final marketplace/ranking method.

This specification implements the next step from `docs/WORDPRESS-STACK-DECISION.md` and remains subordinate to `docs/PROJECT_CONTRACT.md`.

## Product boundary

MyPrimeDelivery surfaces top Amazon products and categories where Prime-delivery eligibility is part of the evidence boundary.

The site is a discovery and outbound-referral surface, not a local checkout, fulfilment, courier, inventory or order-management system.

## First-slice flow

`Homepage -> category landing -> ranked product list -> product detail/editorial view -> governed Amazon outbound CTA`

The first slice must run entirely from local synthetic fixture data until an authorised Amazon/product-data source is selected.

## Canonical content entities

### Category

Required fields:

- `category_id`
- `slug`
- `name`
- `summary`
- `marketplace`
- `ranking_method_id`
- `ranking_checked_at`
- `evidence_status`
- `freshness_state`

### Product

Required fields:

- `product_id`
- `asin`
- `marketplace`
- `category_id`
- `title`
- `summary`
- `prime_state` — `VERIFIED | NOT_VERIFIED | UNKNOWN | STALE`
- `prime_evidence_source`
- `prime_checked_at`
- `ranking_position`
- `ranking_method_id`
- `ranking_evidence_source`
- `ranking_checked_at`
- `product_data_refreshed_at`
- `evidence_status`
- `freshness_state`
- `outbound_destination_state` — `DISABLED | FIXTURE_ONLY | VERIFIED`
- `outbound_url` — absent/null for synthetic fixtures unless a non-live placeholder is explicitly used

Optional fields, rendered only when authorised evidence exists:

- `price`
- `currency`
- `image_url`
- `rating`
- `review_count`
- `availability_state`

No optional commercial field may be invented merely to make the fixture look realistic.

### Ranking Method

Required fields:

- `ranking_method_id`
- `name`
- `description`
- `source_type`
- `effective_at`
- `review_at`
- `status` — `FIXTURE | VERIFIED | STALE | BLOCKED`

A product may not be presented as "top" unless it references an explicit ranking method and fresh supporting evidence.

## WordPress mapping

Use the owner-approved stack from `docs/WORDPRESS-STACK-DECISION.md`.

Recommended mapping:

- WooCommerce Product -> MyPrimeDelivery Product
- WooCommerce Product Category -> Category
- ACF field group -> evidence/provenance/freshness fields
- GenerateBlocks/Gutenberg -> reusable discovery/card/detail components
- FacetWP -> evidence-aware filtering

WooCommerce remains catalogue-only for this project. Do not enable local payment, shipping or checkout as part of this slice.

## Reusable component contract

### `mpd-category-card`

Displays:

- category name
- category summary
- marketplace state
- ranking evidence state
- last checked/freshness

### `mpd-product-card`

Displays only evidence-backed fields:

- title
- category
- Prime state
- ranking position when valid
- evidence/freshness badge
- optional price/image/rating only when supported
- outbound CTA only when destination state is `VERIFIED`

For fixture data the CTA must remain disabled or clearly fixture-only.

### `mpd-evidence-badge`

States:

- `VERIFIED`
- `UNKNOWN`
- `STALE`
- `FIXTURE`
- `BLOCKED`

The UI must not convert `UNKNOWN` or `STALE` into a positive claim.

### `mpd-product-detail`

Must expose:

- ASIN/marketplace identifier
- Prime state and evidence timestamp
- ranking method and evidence timestamp
- product-data refresh timestamp
- current freshness state
- commercial fields only when authorised
- disclosure/outbound state

## Synthetic fixture rules

Create initial fixtures with obviously synthetic identifiers such as:

- `TEST-ASIN-001`
- `TEST-ASIN-002`
- `TEST-ASIN-003`

Fixture records must:

- use `marketplace = UNKNOWN` until owner scope is confirmed;
- use `prime_state = UNKNOWN` or clearly synthetic `FIXTURE` evidence;
- never contain copied Amazon prices, ratings, stock, images or Prime claims;
- never contain live affiliate IDs or links;
- never be published to a production WordPress site.

## Freshness contract

Until a live authorised source exists, fixtures use `freshness_state = FIXTURE`.

Future live records must fail closed:

- missing checked-at timestamp -> `UNKNOWN`
- evidence past configured review interval -> `STALE`
- missing ranking evidence -> ranking hidden / not "top"
- missing Prime evidence -> Prime claim hidden / `UNKNOWN`
- source conflict -> `BLOCKED`

Exact live refresh intervals remain UNKNOWN until the Amazon/product-data source and applicable terms are selected.

## First acceptance fixture

Use one synthetic category containing three synthetic products.

Required deterministic behavior:

1. category page renders exactly three fixture products;
2. each card visibly identifies fixture/evidence state;
3. no card claims verified Prime eligibility;
4. no live price, stock, image, rating or affiliate link is rendered;
5. ranking order comes from an explicit fixture ranking method;
6. changing one product's evidence state to `STALE` changes its badge and suppresses any positive Prime/ranking presentation;
7. changing destination state from `FIXTURE_ONLY` to `DISABLED` removes the outbound CTA;
8. no local checkout/add-to-cart flow is exposed.

## Negative acceptance cases

The slice must fail closed when:

- ASIN/product identifier is missing;
- category reference is invalid;
- ranking method is missing;
- Prime state is `VERIFIED` but evidence source or checked-at is absent;
- ranking position is present without ranking evidence;
- a commercial field is rendered while its source/evidence state is unknown;
- outbound destination is not `VERIFIED` but a live CTA is attempted;
- stale evidence is presented as current.

## Still owner/evidence gated

This specification intentionally does not decide:

- Amazon AU/US/UK/multi-marketplace scope;
- definition of "top";
- authoritative ranking methodology;
- Product Advertising API / Creators API / feed / manual source;
- Amazon Associates account/affiliate tag;
- live price/image/rating rights;
- production refresh cadence;
- live publication/deployment.

## Completion gate for M-03 first slice

The project may move from documentation-only toward a non-production WordPress prototype when:

- this schema is represented in synthetic fixture data;
- one category/three-product fixture renders through reusable templates/components;
- evidence/freshness fail-closed rules are demonstrably enforced;
- live Amazon credentials/data are not required;
- automated/static checks confirm no live affiliate URL or unsupported commercial claim is present.

No production launch or Amazon integration is implied by completion of this slice.
