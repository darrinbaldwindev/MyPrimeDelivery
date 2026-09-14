# MyPrimeDelivery — M-05 Portfolio Dependency Reconciliation

## Date

2026-09-14

## Verified portfolio position

MyPrimeDelivery is an Amazon-focused product/category discovery website for top products/categories eligible for Prime delivery. WordPress is the owner-selected site platform.

The project is **not** a courier, dispatch, driver-management, maps/routing or last-mile logistics platform.

The repository now contains governance, WordPress architecture/data-model documentation, synthetic product/deal fixtures, candidate-research datasets, validators/tests and CI evidence. Live Amazon-backed publication remains blocked on authorised data/Prime/ranking/freshness and affiliate-publication decisions.

## Dependency status

| Dependency category | Current evidence | Status |
|---|---|---|
| Site/presentation platform | WordPress owner decision | VERIFIED |
| Catalogue presentation | WooCommerce external/affiliate catalogue model recommended/provisional | PROVISIONAL |
| Product/category source | Amazon-focused by owner direction; authorised live provider not selected | BLOCKED FOR LIVE |
| Prime eligibility evidence | Must come from authorised Amazon/provider evidence | BLOCKED FOR LIVE |
| Ranking / definition of `top` | MyPrimeDelivery methodology not yet selected | BLOCKED FOR LIVE CLAIMS |
| Deal/offer evidence | Synthetic contract executable; live provider not selected | PARTIAL |
| Product identity/ASIN | Required for live qualification; research candidates do not yet establish authoritative identity | OPEN |
| Affiliate destination/publication | Amazon Associates/tag/publication authority not established in repo | BLOCKED |
| Freshness/expiry policy | Synthetic state rules exist; provider-specific intervals unknown | PARTIAL |
| Search/filter presentation | WordPress/WooCommerce + evidence-aware filtering recommended | PROVISIONAL |
| CDN/cache | Cloudflare/APO recommended, not production-authorised | PROVISIONAL |
| Checkout/payment/shipping/orders | Explicitly outside current product model | NOT REQUIRED |
| Courier/dispatch/maps/driver systems | Stale historical assumption; no longer applicable | NOT REQUIRED |
| Shared AgentOS capability | Bounded Level-2 fixture exists; no alternate control plane | AVAILABLE FOR ACCEPTANCE WORKLOAD |

## Dependency authority rule

Theme/plugin choices are presentation/adapters, not canonical product truth.

Target data flow remains:

`authorised Amazon/provider evidence -> normalised MyPrimeDelivery product record -> evidence/ranking evaluation -> WordPress/WooCommerce presentation -> governed outbound Amazon CTA`

No source may be promoted beyond the exact field authority it supports. `docs/RESEARCH-SOURCE-QUALITY-HIERARCHY.md` controls discovery-source versus publication-authority distinctions.

## Safe autonomous continuation

Continue:
- research candidate collection with explicit provenance;
- synthetic product/deal/freshness testing;
- WordPress component/content modelling;
- source-authority and ranking-method preparation;
- repository/CI reconciliation;
- bounded AgentOS Level-2 fixture work.

Do not activate credentials, scrape Amazon outside authorised mechanisms, publish affiliate links, deploy production, or claim live Prime/ranking/price/deal facts without the required evidence and authority.

## Unlock condition for live integration

Live Amazon integration can advance when all are explicit:
1. target marketplace;
2. definition/methodology for `top`;
3. authorised product + Prime/deal evidence provider and field rights;
4. Amazon Associates publication authority where applicable;
5. freshness/expiry rules;
6. staging negative tests and fail-closed behavior.

No overall GREEN is implied by this dependency reconciliation.
