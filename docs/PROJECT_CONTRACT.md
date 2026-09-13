# MyPrimeDelivery — Project Contract

## Status

**Reconciled:** 2026-09-13  
**Milestone:** M-03 — owner-purpose reconciliation  
**Confidence:** High for product purpose; lower for implementation details

## Verified identity

- Repository: `darrinbaldwindev/MyPrimeDelivery`
- Owner-defined purpose: surface **top Amazon products and categories that are eligible for Prime delivery**.
- Current repository state: governance/documentation plus a bounded synthetic AgentOS Level-2 fixture; no verified production application implementation.

## Purpose boundary

MyPrimeDelivery is an Amazon-focused product/category discovery project. It is **not** a courier, dispatch, driver-management or last-mile delivery platform.

The project should help users discover leading Amazon products/categories where Prime-delivery eligibility is part of the selection/filtering evidence. The repository must not fabricate live Amazon ranking, price, stock or Prime-eligibility claims.

## Verified facts

1. The project focuses on Amazon products and categories.
2. Prime-delivery eligibility is part of the intended product-selection boundary.
3. The goal is product/category discovery, not operating a delivery network.
4. A deterministic synthetic Level-2 fixture exists for bounded AgentOS inspect → modify → reread → verify work.
5. No production Amazon access, affiliate publication, ordering, credentials or live data writes are authorised by this contract.

## Remaining evidence required before product implementation

1. **Target marketplace/region** — e.g. Amazon AU, US, UK, multi-marketplace, or another owner-approved scope.
2. **Ranking methodology** — what "top" means and how products/categories are ranked or selected.
3. **Prime-eligibility evidence source** — authorised and compliant source for proving Prime eligibility.
4. **Product-data source** — approved API/feed/manual workflow and its permitted fields/refresh behaviour.
5. **Affiliate/commercial model** — if affiliate links or monetisation are used, the exact approved account/program and compliance rules.
6. **User journey** — browse/search/filter/category/product-detail/outbound-click behaviour for the first usable slice.
7. **Minimum data model** — identifiers, category, title, evidence timestamps/status, eligibility and ranking evidence, plus any permitted price/image/link fields.
8. **Freshness/expiry rules** — when product, rank and Prime evidence becomes stale and must be revalidated.
9. **Acceptance evidence** — testable definition of a first non-production discovery vertical slice.

## First implementation target

Do not build a broad Amazon site from assumptions. Once the remaining evidence gates are satisfied, define the smallest non-production vertical slice that can ingest or use authorised fixture/product data, apply an explicit ranking/eligibility rule, render a bounded category/product discovery result, and prove the data provenance and freshness state.

## AgentOS Level-2 contribution

`docs/level2/AGENTOS-WORKLOAD-2026-09-13.md` and `fixtures/level2/myprime-product-lifecycle.json` are intentionally synthetic acceptance material. They exist to exercise governed file inspection, bounded mutation, reread, diff verification, receipts, replay protection and Green/PRS gates without touching Amazon or production systems.

## Governance rules

- Keep verified facts separate from claims and assumptions.
- Owner direction overrides stale repository interpretations.
- Prefer repository evidence, approved owner decisions and compliant external-data evidence.
- Never fabricate Prime eligibility, Amazon rank, stock or price.
- Do not expose or commit secrets or credentials.
- Do not activate production Amazon/affiliate integrations from this contract.
- Reassess the contract whenever the canonical product purpose or architecture changes.

## Immediate next task

Reconcile the remaining architecture/overseer evidence documents to this owner-defined Amazon/Prime discovery purpose, then identify the minimum authoritative evidence needed for the first real non-production product-discovery slice.
