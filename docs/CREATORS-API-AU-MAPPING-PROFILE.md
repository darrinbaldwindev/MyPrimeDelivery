# MyPrimeDelivery — Amazon Creators API AU Mapping Profile

Date: 2026-09-15
Status: NON-PRODUCTION / PROVIDER PROFILE CANDIDATE

## Purpose

Map documented Amazon Creators API fields for the Australia marketplace into MyPrimeDelivery's provider-neutral evidence adapter without granting live authority.

## Marketplace profile

- provider profile: `amazon-creators-api-au-v1`
- marketplace: `www.amazon.com.au`
- region: FE
- request marketplace and `x-marketplace` must agree
- a valid Partner Tag for the target marketplace and approved Creators API access are required before live use

## Verified documented resources

### Identity
- item `asin` -> canonical `asin`
- `ParentASIN` -> `identity.parent_asin` when returned and semantically applicable
- item title from `ItemInfo.Title` -> `canonical_title`

### Offer/deal evidence
`OffersV2.Listings` may expose:
- `Availability`
- `Condition`
- `DealDetails`
- `IsBuyBoxWinner`
- `MerchantInfo`
- `Price`
- `Type`
- `ViolatesMAP`

`DealDetails` being present indicates an associated deal for that listing. This is a deal signal only; it does not prove Prime eligibility.

### Images
Creators API exposes image resources. Image use, retention and caching are subject to Amazon's licence requirements and therefore remain a separate permissioned display field.

## Explicit non-mappings

The following must NOT be inferred merely from the documented fields above:
- `Prime = VERIFIED` from availability, FBA, buy-box status, merchant identity, offer type or deal presence;
- Amazon Best Seller Rank from SearchItems order unless an explicit documented ranking signal/method supports the claim;
- historical-low status from current price alone;
- publication authority from successful API access;
- unrestricted caching or redistribution rights.

## Canonical mapping envelope

A future mapper emits only fields supported by both provider response and field policy:

- `provider_id = amazon-creators-api`
- `provider_profile_id = amazon-creators-api-au-v1`
- `marketplace`
- `asin`
- `canonical_title`
- `identity.product_kind`
- `identity.parent_asin`
- `identity.variant_key` only when variant semantics are explicit
- optional offer/deal observations
- optional price/image observations where policy allows
- provider snapshot/evidence IDs and checked-at timestamps
- `publication_authority = false`
- `network_io = false`

## Freshness and rights rule

The mapper does not invent a universal cache lifetime. Each field carries a policy state:
`ALLOWED_CURRENT | ALLOWED_WITH_EXPIRY | HOLD_RIGHTS_UNKNOWN | HOLD_UNSUPPORTED`.

Live expiry values remain blocked until the exact Amazon licence/API rules for the intended use are approved in-project.

## Compliance boundary

Amazon's Associates/Creators API licence controls use of Product Advertising Content. MyPrimeDelivery must not use scraping/data-mining as a substitute for authorised provider access and must not treat API access as permission to reuse every returned field indefinitely.
