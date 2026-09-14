# MyPrimeDelivery — Vertical Batch 003 Result

Date: 2026-09-14
Status: COMPLETE (BOUNDED RESEARCH TRANCHE / NON-PRODUCTION)
Canonical batch: `docs/overseer/batches/VERTICAL-BATCH-003-FIRST-100-RESEARCH-DATASET.md`
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Outcome

Created the first validated research tranche for the planned 100-product candidate pool without promoting public deal/discovery evidence into Prime/ranking authority.

## Durable artifacts

- `fixtures/candidates/first-100-research.json`
- `fixtures/candidates/validate_candidate_research.py`
- `fixtures/candidates/test_candidate_research.py`
- `.github/workflows/fixture-validation.yml` now validates the candidate dataset in addition to existing M-03 and deal fixtures.

## Current tranche

30 distinct real product candidates observed from current public Amazon-Australia deal/discovery sources.

State distribution:
- `CANDIDATE`: research signal strong enough for follow-up, still not qualified;
- `DISCOVERED`: weaker/editorial signal requiring follow-up;
- `QUALIFIED`: 0.

No live Amazon affiliate tags or outbound destinations are stored.

## Category coverage

| Category | Count |
|---|---:|
| Home & Kitchen | 8 |
| Electronics | 6 |
| Baby | 1 |
| Pet Supplies | 0 |
| Health & Household | 4 |
| Beauty & Personal Care | 5 |
| Tools & Home Improvement | 2 |
| Toys & Games | 1 |
| Sports & Outdoors | 1 |
| Office Products | 1 |
| Automotive | 0 |
| Garden & Outdoors | 1 |
| **Total** | **30** |

## Research sources used in this tranche

Public current discovery sources only:
- FreeStuff Amazon Home & Kitchen deal tracker, observed 2026-09-11;
- FreeStuff Amazon Top Deals tracker, observed 2026-09-11;
- FreeStuff Amazon Other Deals tracker, observed 2026-09-12;
- TechRadar Australia Amazon coupon/deal page, observed 2026-09-10.

These sources are candidate-discovery evidence, not authoritative Prime-eligibility or canonical ranking evidence.

## Fail-closed assurance now enforced

Dataset validation rejects:
- duplicate candidate IDs;
- unsupported launch-category IDs;
- missing provenance;
- affiliate-tag / `amzn.to` leakage;
- fabricated `QUALIFIED` state without verified Prime + selection/ranking + current freshness evidence;
- Prime VERIFIED without source + checked-at;
- stale records presented as current candidate/qualified records.

## CI evidence

Candidate-validation workflow change exact head:
`5049581b5743f3637eba46acd2e053bce79d6e01`

GitHub Actions Fixture validation run:
`34810046997`

Conclusion: `SUCCESS`.

The run includes existing M-03 checks, existing deal-evidence checks, candidate research validation and negative assurance tests.

## Next research priority

Do not simply fill to 100 with whatever is easy to find.

Priority order for the next candidate tranche:
1. Pet Supplies — zero current candidates;
2. Automotive — zero current candidates;
3. Baby, Toys & Games, Sports & Outdoors, Office Products, Garden & Outdoors — only one current candidate each;
4. then deepen Electronics / Home / Health / Beauty only where evidence quality remains strong.

The dataset can reach 100 progressively, but `QUALIFIED` must remain zero until authoritative Prime/ranking/freshness sources are available.

## Remaining blockers / UNKNOWNs

- canonical marketplace promotion (Australia is research direction, not yet canonical live scope);
- exact definition of `top`;
- authorised Amazon product/Prime/ranking/deal provider;
- Amazon Associates publication authority;
- live commercial-field rights and refresh cadence;
- production publication/deployment.

## Result

Batch 003 is complete as a bounded research/data-validation increment. It proves that real candidate discovery can feed the MyPrimeDelivery evidence model while remaining fail-closed. It does not prove Prime eligibility, current Amazon ranking, production freshness, affiliate publication rights, or overall MyPrimeDelivery GREEN.
