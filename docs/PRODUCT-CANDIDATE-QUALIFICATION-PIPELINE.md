# MyPrimeDelivery — Product Candidate Qualification Pipeline

Date: 2026-09-14
Status: NON-PRODUCTION RESEARCH/INTAKE CONTRACT

## Purpose

Define how candidate Amazon products move from discovery into a displayable MyPrimeDelivery catalogue without confusing research findings, popularity claims, Prime eligibility or live deal evidence.

## States

`DISCOVERED -> CANDIDATE -> QUALIFIED | REJECTED | STALE | BLOCKED`

### DISCOVERED

A product was found in an approved research source or future authorised Amazon source. Discovery alone authorises no public claim.

### CANDIDATE

The product appears relevant to an approved category and is worth evidence collection. Prime, ranking and freshness may still be incomplete.

### QUALIFIED

Minimum requirements:

- product identity is stable (including ASIN or equivalent Amazon identifier);
- target marketplace is explicit;
- category mapping is valid;
- Prime-eligibility evidence is current and source-backed;
- ranking/selection rationale is explicit and evidence-backed;
- product evidence is within the configured freshness window;
- any displayed commercial fields are permitted by and traceable to the authorised source;
- outbound destination is separately verified before a public CTA is enabled.

A current sale/deal is **not** required for evergreen qualification.

### REJECTED

Product fails a durable criterion. Record a rejection reason, such as:

- category mismatch;
- weak/unsupported ranking evidence;
- unavailable or unverifiable Prime eligibility;
- misleading/unsupported discount evidence;
- low-quality/unsafe/irrelevant product;
- duplicate variant/listing;
- data-rights or compliance issue;
- insufficient evidence after review.

### STALE

Previously useful evidence is outside the configured freshness interval. Public Prime/rank/deal claims must fail closed until refreshed.

### BLOCKED

Conflicting evidence, provider failure, identity ambiguity, policy uncertainty or another hard dependency prevents a safe qualification decision.

## Candidate intake record

Minimum research/intake fields:

- `candidate_id`
- `asin`
- `marketplace`
- `category_id`
- `title`
- `discovered_from`
- `discovered_at`
- `qualification_state`
- `prime_state`
- `prime_evidence_source`
- `prime_checked_at`
- `ranking_method_id`
- `ranking_evidence_source`
- `ranking_checked_at`
- `product_data_refreshed_at`
- `deal_state`
- `deal_evidence_ref`
- `outbound_destination_state`
- `evidence_status`
- `freshness_state`
- `rejection_reason`
- `notes`

## First-100 research batch rule

The planned first 100 Amazon Australia research candidates should be collected as candidate records, not automatically published products.

Target distribution may be adjusted as evidence density emerges, but the research batch should favour the 12 approved launch categories and maintain category diversity rather than filling the list with one high-volume vertical.

Every candidate must end the batch with one explicit state: `CANDIDATE`, `QUALIFIED`, `REJECTED`, `STALE`, or `BLOCKED`. UNKNOWN evidence remains visible in the record.

## Public-display separation

Research intake state must not directly control publication.

Public display additionally requires:

- approved WordPress publication workflow;
- evidence-aware rendering rules;
- permitted product content rights;
- verified outbound destination if a CTA is shown;
- any required affiliate disclosure;
- no stale/unknown field rendered as current fact.

## Deal interaction

Deal evidence follows `docs/DEAL-OFFER-EVIDENCE-CONTRACT.md`.

- `ACTIVE` deal may increase ranking/presentation priority only if the chosen ranking method explicitly allows it.
- expired/stale deal removes urgency but does not automatically reject an evergreen qualified product.
- deal evidence does not prove Prime eligibility.

## WordPress mapping

When candidates become approved catalogue records:

- WooCommerce Product provides product presentation/content identity;
- WooCommerce Product Category uses the stable taxonomy from `docs/WORDPRESS-CATEGORY-TAXONOMY.md`;
- evidence, freshness, ranking, Prime and deal fields remain namespaced MyPrimeDelivery metadata;
- GenerateBlocks/Gutenberg renders state-aware components;
- FacetWP filters only on explicit state fields.

## No-production boundary

This pipeline does not authorise live Amazon access, scraping, credentials, affiliate publication, checkout, production ingestion or deployment.