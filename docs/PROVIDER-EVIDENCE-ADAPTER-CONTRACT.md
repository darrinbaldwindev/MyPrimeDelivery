# MyPrimeDelivery — Provider Evidence Adapter Contract

Date: 2026-09-14
Status: NON-PRODUCTION / PROVIDER-NEUTRAL CONTRACT

## Purpose

Define the boundary between an authorised Amazon product-data provider and MyPrimeDelivery canonical evidence. This contract does not choose a provider, grant provider authority, permit network access, or authorize publication.

The adapter consumes evidence whose authority/rights are proven separately, validates identity/freshness consistency, and produces a normalized evidence packet suitable for staging logic.

## Input requirements

A provider record must identify:
- `provider_id`
- `provider_authority` — `PROVEN` for authoritative claims
- `rights_to_use` — `PROVEN` for fields consumed by MyPrimeDelivery
- `evidence_id`
- `marketplace`
- `asin`
- `canonical_title`
- `checked_at`
- `freshness_state`
- `identity` object
- optional independent claim objects for Prime, selection/rank and deal evidence

## Identity object

Required fields:
- `marketplace`
- `asin`
- `product_kind` — `PRODUCT`, `PARENT`, or `VARIANT`
- `parent_asin` — nullable
- `variant_key` — nullable

Rules:
1. outer and identity marketplace must match;
2. outer and identity ASIN must match;
3. `VARIANT` requires explicit `parent_asin` and `variant_key`;
4. `PARENT` must not masquerade as a concrete variant;
5. conflicting identity is HOLD, never auto-corrected.

## Claim objects

Each claim is independent. One valid claim must not silently authorize another.

### Prime
- `state`: `VERIFIED`, `NOT_VERIFIED`, or `UNKNOWN`
- `evidence_id`
- `checked_at`

### Selection / rank
- `state`: `VERIFIED`, `UNKNOWN`, or `NOT_APPLICABLE`
- `method_id`
- `position` — optional; must be positive integer when present
- `evidence_id`
- `checked_at`

A provider rank is not automatically Amazon Best Seller Rank. `method_id` must disclose what the position means.

### Deal
- `state`: `ACTIVE`, `INACTIVE`, `UNKNOWN`, `STALE`, or `EXPIRED`
- `evidence_id`
- `checked_at`
- optional `ends_at`

A deal claim cannot imply Prime eligibility.

## Freshness rule

The adapter only accepts `freshness_state=CURRENT` for current public-facing claim inputs. `STALE`, `EXPIRED`, `UNKNOWN`, or missing freshness causes a HOLD for current-claim normalization. Provider-specific maximum ages remain blocked until a real provider is selected.

## Normalized packet

Accepted records normalize to:
- `product_identity`
- `provider_id`
- `marketplace`
- `asin`
- `title`
- `identity_state=ASIN_VERIFIED`
- `prime_state`
- `selection_state`
- `ranking_method_id`
- `ranking_position`
- `deal_state`
- `freshness_state`
- `checked_at`
- `evidence_refs`
- `publication_authority=false`
- `network_io=false`

## Fail-closed outcomes

The adapter returns HOLD for:
- unproven provider authority;
- unproven rights-to-use;
- missing evidence identity;
- ASIN mismatch;
- marketplace mismatch;
- stale/unknown top-level freshness;
- conflicting variant/parent identity;
- malformed claim evidence;
- claim timestamps later than the provider checked-at time;
- any attempt to embed publication or network authority.

## Authority separation

This adapter is not an authority source. It does not decide whether a provider is contractually/compliantly authorised. That decision belongs to the source-rights/provider-authority gate. The adapter only normalizes evidence after those facts are explicitly present.

## Production gate

Before connecting a live provider, owner approval/evidence is required for:
1. provider identity and authorised API/feed;
2. target marketplace;
3. permitted fields and display rights;
4. provider-specific freshness/expiry rules;
5. credentials handling;
6. affiliate/publication authority;
7. staging validation with no production publication.