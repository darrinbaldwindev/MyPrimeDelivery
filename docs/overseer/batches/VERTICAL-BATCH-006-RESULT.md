# MyPrimeDelivery — Vertical Batch 006 Result

Date: 2026-09-14
Status: COMPLETE (BOUNDED NON-PRODUCTION IDENTITY/RANKING SLICE)
Canonical batch: `docs/overseer/batches/VERTICAL-BATCH-006-IDENTITY-DEDUPE-AND-RANKING.md`
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Outcome

Batch 006 converted the growing research pool into an identity-aware, deduplicated and deterministically rankable non-production foundation without inventing ASINs, Prime status or Amazon ranking authority.

## Durable artifacts

- `docs/PRODUCT-IDENTITY-CONTRACT.md`
- `docs/RANKING-METHODOLOGY-PROVISIONAL.md`
- `fixtures/candidates/analyze_candidate_collection.py`
- `fixtures/candidates/test_identity_analysis.py`
- `fixtures/ranking/provisional-ranking.synthetic.json`
- `fixtures/ranking/validate_provisional_ranking.py`
- `fixtures/ranking/test_provisional_ranking.py`
- `.github/workflows/fixture-validation.yml` extended without removing source-rights/provider-authority checks
- `docs/overseer/M-04-IMPLEMENTATION-READINESS.md` reconciled

## Cross-tranche identity result

The current research collection contains:
- 58 evidence rows;
- 57 exact normalized-title concepts;
- 1 exact duplicate-title evidence group;
- all 12 launch categories represented.

Known duplicate-title group:
- `cand-030` — Ninja Woodfire Outdoor Oven
- `cand-058` — Ninja Woodfire Outdoor Oven

These remain separate evidence observations. Normalized-title equality is a review signal only and does not prove identical ASIN/variant identity.

## Identity contract

Identity states are now explicit:
`UNRESOLVED -> TITLE_ONLY -> MARKETPLACE_PRODUCT -> ASIN_VERIFIED`

An ASIN must never be guessed. Product-family/range records cannot become concrete catalogue products until exact identity is resolved. ASIN verification does not by itself prove Prime, rank, deal, price, stock or affiliate rights.

## Provisional ranking

A staging-only deterministic `provisional-v1` method now exists with 100 total possible points:
- selection strength 40;
- evidence confidence 25;
- freshness strength 20;
- deal relevance 10;
- editorial utility 5.

For Prime-focused public lists, current verified Prime evidence is a hard gate rather than a score bonus. Unknown Prime, stale freshness or unresolved identity makes the item ineligible regardless of score. Tie-breaking is deterministic.

This method is explicitly **not Amazon Best Seller Rank** and is not authorised as the final production definition of `top`.

## Failure found and corrected

The first Batch 006 CI run `34850492282` failed a normalization test because Unicode decomposition converted the trademark symbol into `tm`. The analyzer itself had already found the expected 58 -> 57 result, but the test exposed an unstable normalization edge.

The normalizer was corrected to remove trademark/registered/copyright symbols before ASCII normalization. This was a bounded code fix; assurance was not weakened.

## Verified CI evidence

Exact-head validation after the fix:
- head: `92909897c8940950b5faeb84270a36d83fca8035`
- workflow run: `34850571826`
- result: SUCCESS

All steps passed, including:
- prior M-03 product validation/rendering;
- deal evidence validation/negative assurance;
- all three candidate tranche validations;
- cross-tranche identity/dedupe analysis;
- candidate + identity assurance tests;
- provisional ranking validation/tests;
- source-rights/provider-authority tests.

A later documentation-only readiness/result commit will receive its own normal workflow run; no code behavior is claimed from documentation alone.

## Remaining blockers / UNKNOWNs

- canonical live marketplace promotion;
- owner-approved production definition of `top`;
- authorised Amazon product/identity/Prime/rank/deal provider;
- real source-backed ASIN resolution;
- Amazon Associates publication authority;
- provider-specific freshness/expiry policy;
- production WordPress publication/deployment.

## Next batch priority

1. define a provider-neutral Amazon identity/evidence adapter contract;
2. model authoritative response -> canonical product identity -> Prime/freshness/ranking inputs;
3. add negative fixtures for ASIN mismatch, marketplace mismatch, stale provider evidence and conflicting variant identity;
4. keep live credentials/network/publication owner-gated.

## Result

Batch 006 is complete as a bounded identity/ranking increment. It materially reduces false duplicate and false ranking risk, but it does not make any live Amazon product QUALIFIED and does not imply overall MyPrimeDelivery GREEN.