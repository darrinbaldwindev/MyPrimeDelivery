# MyPrimeDelivery — Project Contract

## Status

**Reconciled:** 2026-08-31  
**Milestone:** M-02 — project-definition reconciliation  
**Confidence:** Medium

## Verified identity

- Repository: `darrinbaldwindev/MyPrimeDelivery`
- Portfolio role: **Delivery project**
- Portfolio scheduler tier: **P2 / adaptive**
- Current repository state: governance documentation only; no verified application implementation.

## Purpose boundary

This repository is treated as a delivery-project repository because that role is recorded in the portfolio registry. The specific commercial model, delivery workflow, customer experience, geographic scope, technology stack, external providers, credentials, and production requirements are **not yet verified** in this repository.

No assumption in this contract authorizes external-service access, credential use, customer-data ingestion, payments, dispatch, deployment, or production operation.

## Evidence required before implementation

1. **Business objective** — what delivery problem the project solves and for whom.
2. **Operating model** — owned delivery, marketplace, third-party courier, hybrid, or other verified model.
3. **Core workflow** — order/request intake through fulfilment, dispatch, tracking and completion.
4. **Actors and permissions** — customer, operator, driver/courier, administrator and any other verified roles.
5. **System boundary** — source of truth and any dependent repositories/services.
6. **Data boundary** — minimum data required, retention expectations and sensitive-data handling constraints.
7. **Integration boundary** — approved payment, maps, messaging, courier, commerce or other providers, if applicable.
8. **Acceptance evidence** — testable definition of a first usable vertical slice.

## First implementation target

Do not build a broad platform from assumptions. Once the missing business facts are evidenced, define the smallest non-production vertical slice that proves the critical delivery workflow end-to-end.

## Governance rules

- Keep verified facts separate from claims and assumptions.
- Prefer evidence from repository artifacts, tests and approved owner decisions.
- Do not expose or commit secrets or credentials.
- Do not activate production integrations from this contract.
- Reassess the contract whenever the canonical business purpose or architecture changes.

## Immediate next task — M-03

Produce a bounded evidence checklist from this contract, then identify the minimum missing owner/project evidence required to start implementation without inventing scope.
