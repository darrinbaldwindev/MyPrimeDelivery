# MyPrimeDelivery — Product Identity Contract

Date: 2026-09-14
Status: NON-PRODUCTION / EVIDENCE CONTRACT

## Purpose

Separate research observations from stable product identity. A research row is evidence that a product or product family was observed; it is not automatically a canonical product record.

## Identity states

`UNRESOLVED -> TITLE_ONLY -> MARKETPLACE_PRODUCT -> ASIN_VERIFIED`

### UNRESOLVED
The record describes a product family, range, slot, or otherwise unresolved identity. It may remain research evidence but cannot be promoted to a concrete catalogue product.

### TITLE_ONLY
A concrete named product appears identifiable by title, but no source-backed marketplace identifier has been verified.

### MARKETPLACE_PRODUCT
The exact product has been resolved to the intended Amazon marketplace by an authorised or otherwise accepted identity source, but ASIN verification is still pending or separately controlled.

### ASIN_VERIFIED
The exact ASIN has been source-backed for the intended marketplace and retained with provenance and checked-at metadata.

## Canonical identity fields

A future canonical product identity should include:
- `product_id` — MyPrimeDelivery stable ID;
- `marketplace`;
- `asin` — nullable until verified;
- `asin_source`;
- `asin_checked_at`;
- `canonical_title`;
- `category_id`;
- `identity_state`;
- `identity_evidence_refs` — one or more research/evidence-row IDs;
- `variant_or_parent_state`;
- `identity_notes`.

## Rules

1. Never infer or guess an ASIN from a title.
2. An ASIN is marketplace-specific evidence and must retain provenance.
3. Multiple research rows may map to one canonical product identity.
4. Exact normalized-title matches are duplicate candidates for identity review, not automatic deletion.
5. Product-family/range rows containing unresolved exact SKU identity remain `UNRESOLVED` and cannot become a publishable product.
6. Conflicting categories for the same verified identity are a hard review failure.
7. Variants must not be silently collapsed unless parent/variant semantics are explicit.
8. A verified ASIN does not prove Prime eligibility, ranking, deal state, price, stock, affiliate rights or freshness.

## Promotion gate

`CANDIDATE` or `QUALIFIED` public-product promotion requires at minimum a concrete product identity. `QUALIFIED` additionally requires the separate Prime, selection/ranking, freshness, rights and outbound-destination gates in `docs/PRODUCT-CANDIDATE-QUALIFICATION-PIPELINE.md`.

## Current research pool

Current research rows are evidence inputs. Unless a row already contains source-backed marketplace identity, its ASIN remains UNKNOWN. The repository must prefer an explicit unresolved identity over a fabricated exact match.
