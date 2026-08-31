# MyPrimeDelivery — Architecture Boundary

## Status

**Created:** 2026-08-31  
**Milestone:** M-03  
**Purpose:** Prevent premature implementation while making the next implementation decision deterministic.

## Current verified boundary

MyPrimeDelivery is recorded in the portfolio as a **Delivery project**. The repository currently contains governance/project-definition documentation and no verified application implementation.

## Allowed now

- Project-definition and requirements documentation
- Evidence capture and reconciliation
- Non-production architecture sketches that are explicitly marked provisional
- Testable acceptance-criteria drafting once authoritative workflow evidence exists
- Dependency/capability mapping against the wider portfolio

## Not yet authorised

- Production deployment
- Payment processing
- Real customer-data ingestion
- Driver/courier operational dispatch
- Credential or secret storage
- Activation of external delivery, maps, messaging or commerce services
- Claims that a specific provider or operating model has been selected

## Architecture decision gate

Implementation may begin only when the following are evidenced:

1. Business objective and target user
2. Operating model
3. End-to-end primary workflow
4. Actor/permission model
5. Canonical source of truth
6. Minimum data entities
7. Required integrations and authority boundary
8. First vertical-slice acceptance tests

## Provisional vertical-slice shape

Do not implement this as fact. Once the eight evidence gates are satisfied, the first slice should normally prove one complete delivery journey end-to-end, from a valid request/order through fulfilment state changes to completion, with actor permissions and auditable state transitions. Exact workflow, entities and integrations remain evidence-dependent.

## Overseer rule

When new evidence arrives, update the project contract and checklist first. Only then promote provisional architecture into implementation requirements.
