# MyPrimeDelivery — AgentOS Level-2 bounded acceptance workload

Status: READY AS NON-PRODUCTION FIXTURE
Date: 2026-09-13

## Product truth
MyPrimeDelivery is intended to surface top Amazon products/categories that are eligible for Prime delivery. This fixture does not claim current Amazon ranking, price, stock or Prime eligibility.

## Exact workload
1. Create or update only `fixtures/level2/myprime-product-lifecycle.json`.
2. Use deterministic synthetic data only:
```json
{
  "schema": "myprime.level2.fixture.v1",
  "asin": "FIXTURE-ASIN-001",
  "category": "fixture-category",
  "prime_eligible": false,
  "evidence_status": "SYNTHETIC_ONLY",
  "state": "CANDIDATE",
  "production_write": false
}
```
3. Reread and parse the JSON.
4. Change `state` from `CANDIDATE` to `REVIEWED` in the same fixture only.
5. Reread again and produce a diff proving no other path changed.

## Acceptance
PASS requires bounded-root enforcement, valid JSON after both reads, exactly one permitted state transition, exact task/mission/result correlation, mutation receipt, replay protection, and Green then PRS verification. Any live Amazon write/scrape claim, fabricated Prime eligibility, extra file mutation, or missing receipt is FAIL/BLOCKED.

## Authority boundary
No Amazon account access, ordering, affiliate publication, price/stock claim, credentials or production changes are authorized by this workload.