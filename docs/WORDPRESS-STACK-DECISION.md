# MyPrimeDelivery — WordPress Stack Decision

Date: 2026-09-13
Status: OWNER-APPROVED DIRECTION

## Product context

MyPrimeDelivery is an Amazon-focused product/category discovery site intended to surface top Amazon products and categories that are eligible for Prime delivery. It is not a courier, driver, dispatch or last-mile delivery platform.

## Owner decision

The site will use **WordPress**.

## Recommended site architecture

Use WordPress as a fast affiliate/product-discovery catalogue rather than a conventional ecommerce checkout site.

### Core stack

- **WordPress** — CMS/application surface.
- **GeneratePress Premium** — preferred lightweight theme.
- **GenerateBlocks** — preferred block/layout system with native Gutenberg.
- **WooCommerce** — catalogue/product/category infrastructure, configured for external/affiliate products rather than on-site checkout.
- **ACF Pro** — structured MyPrimeDelivery evidence fields such as marketplace, Prime evidence status/source, ranking evidence, freshness timestamps and stale/unknown states.
- **FacetWP** — product/category filtering.
- **Rank Math** — SEO/schema layer.
- **Cloudflare + APO** — preferred caching/CDN/performance layer.

### Amazon / affiliate presentation layer

Preferred current direction:

- Evaluate **Lasso / Lasso Lite** as the first Amazon affiliate display/link-management option.
- Evaluate **AffiliateX** or custom Gutenberg blocks for comparison tables, top-product grids, pros/cons and editorial buying-guide components.
- Do **not** make any single Amazon plugin the canonical product-data source or source of truth.

Amazon product data should pass through a MyPrimeDelivery-normalised product/evidence model so upstream Amazon data-source changes do not require a theme/site rebuild.

## WooCommerce operating model

WooCommerce should be used primarily as a catalogue. Products that send users to Amazon should use the External/Affiliate product model where appropriate.

The first site architecture should not depend on:

- local checkout
- shipping calculation
- payment processing
- customer orders
- inventory fulfilment

Those features are outside the current MyPrimeDelivery purpose unless later owner direction changes the product.

## Product/evidence data model direction

The WordPress product model should be capable of storing, subject to final approved Amazon data-source rules:

- ASIN
- Amazon marketplace
- category
- title
- affiliate/outbound URL
- Prime-eligibility state
- Prime evidence source
- Prime evidence checked-at timestamp
- ranking position/state
- ranking method/evidence
- ranking checked-at timestamp
- product-data refreshed-at timestamp
- evidence status
- stale/unknown state

Price, stock, rating, image and Prime claims must only be rendered when supported by an authorised/compliant Amazon data source and applicable usage rules. Missing or expired evidence must remain UNKNOWN/STALE rather than being fabricated.

## Page/template direction

Initial reusable templates should support:

- homepage discovery surface
- top categories
- category landing/archive pages
- top products by category
- product cards
- product-detail/editorial pages where useful
- comparison/top-list pages
- buying guides
- trending/newly-verified surfaces only where evidence supports the claim

The site should prioritise discovery and outbound Amazon conversion rather than behaving like a normal cart/checkout store.

## Performance/design rule

Prefer Gutenberg + GenerateBlocks over Elementor unless a later requirement proves Elementor necessary. Keep the frontend lean because the site may contain a large product/category catalogue.

Avoid overlapping cache/security/plugin stacks where one clearly owned layer is sufficient.

## Still UNKNOWN / not authorised by this decision

This architecture decision does **not** yet select or authorise:

- target Amazon marketplace/region
- exact definition of "top"
- ranking methodology
- Creators API / Product Advertising API / feed / manual ingestion choice
- Amazon Associates account or affiliate IDs
- live Amazon credentials
- scraping
- exact refresh/freshness cadence
- production product ingestion
- live affiliate publication
- production deployment

Those remain evidence-gated and owner/compliance dependent.

## Next implementation step

Define the WordPress content/data model and reusable template/component specification against synthetic fixture data first. Keep live Amazon integration behind a provider boundary until the authorised data source, marketplace, ranking method and affiliate rules are confirmed.
