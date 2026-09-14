# MyPrimeDelivery — M-04 Implementation Readiness

Date: 2026-09-14
Status: ACTIVE / NON-PRODUCTION SLICE READY; LIVE AMAZON INTEGRATION BLOCKED

## Current result

MyPrimeDelivery is no longer blocked on basic product identity or on creating synthetic non-production discovery/deal/ranking/provider-normalization slices.

Owner direction establishes the product as an Amazon-focused product/category discovery site for top products/categories eligible for Prime delivery, using WordPress as the site platform. The repository now has a bounded WordPress data model, synthetic product/category fixture, executable time-sensitive deal fixture, candidate-research pipeline, source-rights/provider-authority tests, cross-tranche identity/dedupe analysis, provisional ranking contract, and a provider-neutral evidence adapter with fail-closed normalization tests.

Live Amazon-backed product publication remains blocked until marketplace, ranking policy, authorised data provider, Prime/deal evidence, affiliate/compliance and provider-specific freshness decisions are authorised.

## Readiness matrix

| Requirement | Evidence | Status |
|---|---|---|
| Product identity | Owner direction + `docs/PROJECT_CONTRACT.md` | PASS |
| Site platform | WordPress owner decision + `docs/WORDPRESS-STACK-DECISION.md` | PASS |
| Discovery operating model | Catalogue/outbound-referral; no local checkout | PASS |
| First user journey | Homepage -> category -> ranked list -> detail -> governed outbound CTA | PASS for synthetic slice |
| Launch taxonomy | `docs/WORDPRESS-CATEGORY-TAXONOMY.md` | PASS for planning |
| Synthetic product data model | `docs/M03-WORDPRESS-DATA-MODEL-AND-FIRST-SLICE.md` + fixture | PASS |
| Product fail-closed validation/rendering | `fixtures/m03/` validators, renderer and tests | PASS |
| Deal/time-sensitive evidence | `docs/DEAL-OFFER-EVIDENCE-CONTRACT.md` + `fixtures/deals/` | PASS for non-production |
| Candidate qualification pipeline | `docs/PRODUCT-CANDIDATE-QUALIFICATION-PIPELINE.md` | PASS for research/intake |
| Research source/right-to-use separation | `docs/RESEARCH-SOURCE-QUALITY-HIERARCHY.md` + `fixtures/source_rights/` | PASS for contract/tests |
| Research pool | 58 evidence rows across three tranches | PASS for research only |
| Cross-tranche dedupe | `fixtures/candidates/analyze_candidate_collection.py` | PASS; 58 rows -> 57 normalized-title concepts; one known duplicate pair |
| Stable identity/ASIN contract | `docs/PRODUCT-IDENTITY-CONTRACT.md` | PASS for contract; live ASIN resolution OPEN |
| Provisional ranking method | `docs/RANKING-METHODOLOGY-PROVISIONAL.md` + `fixtures/ranking/` | PASS for synthetic/staging only |
| Provider-neutral evidence adapter | `docs/PROVIDER-EVIDENCE-ADAPTER-CONTRACT.md` + `fixtures/provider_adapter/` | PASS for non-production contract/tests |
| Adapter negative assurance | ASIN mismatch, marketplace mismatch, stale provider evidence, conflicting variant identity, unproven authority/rights, claim-time contradiction, authority-escalation denial | PASS |
| Exact-head CI for adapter code | Fixture validation run `34851885896` on `2214c54eebb98d309332beb5d1d4a617bdaacec0` | PASS / SUCCESS |
| Target marketplace | Amazon Australia is current research direction but not formally promoted as canonical live scope | OPEN |
| Production definition of `top` | Provisional method exists; owner/live provider policy not yet selected | BLOCKED for live claims |
| Authorised live provider | Provider-neutral boundary exists; no provider selected/authorised | BLOCKED |
| Prime evidence source | No authorised live source selected | BLOCKED for live claims |
| Product/deal data source | No authorised live provider selected | BLOCKED for live claims |
| Real ASIN identity resolution | No authorised live identity source integrated | BLOCKED for live catalogue |
| Affiliate account/tag and publication rights | Not authorised in repo | BLOCKED for live outbound publication |
| Live freshness/expiry intervals | Provider/terms dependent | BLOCKED |
| Production deployment | Not authorised | BLOCKED |

## Provider adapter result

The provider adapter now separates four concerns that must not collapse into one another:

1. **source authority / rights** — must already be proven;
2. **identity** — marketplace and ASIN must be internally consistent, with explicit parent/variant semantics;
3. **claims** — Prime, selection/rank and deal states remain independent evidence dimensions;
4. **freshness** — current-claim normalization fails closed when top-level provider evidence is not current.

An accepted packet always carries `publication_authority=false` and `network_io=false`. The adapter cannot promote its own authority and cannot turn an active deal into an implied Prime claim.

## Identity and dedupe finding

The research pool contains 58 evidence rows but 57 exact normalized-title concepts. `cand-030` and `cand-058` both refer to `Ninja Woodfire Outdoor Oven`. They remain separate evidence observations until authoritative identity evidence proves whether they map to the same exact marketplace listing/ASIN. No evidence row was deleted or promoted.

## Provisional ranking rule

The repository has a deterministic staging-only score with hard fail-closed gates. Unknown Prime, stale freshness, unresolved identity or missing marketplace eligibility prevents inclusion regardless of numerical score. The model is explicitly not Amazon Best Seller Rank.

## Safe autonomous work now

Permitted useful work includes:
- provider-specific mapping fixtures without credentials/network I/O;
- product-identity resolution preparation and ASIN evidence schema;
- ranking-mode and freshness-policy tests;
- WordPress presentation/component specification;
- category/subcategory and candidate research;
- Level-2 bounded acceptance workloads;
- repository/CI verification and documentation reconciliation.

Do not turn public web research into `QUALIFIED` product records without authoritative Prime/ranking/freshness/identity evidence.

## Exit condition for live integration readiness

The live Amazon integration gate can advance only when all are evidenced:
1. target marketplace/region;
2. owner-approved live ranking/selection method for `top`;
3. authorised provider identity and permitted product/Prime/deal fields;
4. source-backed ASIN resolution for intended marketplace;
5. provider-specific freshness/expiry rules;
6. Amazon Associates/affiliate publication authority if used;
7. live-data negative tests and fail-closed behavior;
8. non-production staging validation before any production publication.

No overall GREEN is implied by synthetic-slice readiness.