# M-03 Evidence Matrix

Status date: 2026-09-09

This document converts Issue #2 into a durable, fail-closed evidence gate. Unknown commercial facts remain unknown; they are not inferred for the prototype.

| Area | Current disposition | Evidence / boundary | Prototype treatment |
|---|---|---|---|
| Business objective | UNKNOWN | Repository identifies a delivery project but does not yet establish the exact customer/problem strongly enough for production assumptions. | Use a generic synthetic delivery request fixture only. |
| Operating model | OWNER DECISION REQUIRED | Owned fleet / marketplace / third-party / hybrid is unresolved. | Do not encode a commercial operating model. Fixture uses a generic operator + courier role. |
| Core workflow | VERIFIED FOR FIXTURE | Issue #2 and current architecture support request → acceptance → assignment → status transitions → completion/exception as a bounded test flow. | Implement only as local/synthetic lifecycle. |
| Actors / permissions | PARTIAL | Customer/operator/courier/admin are candidate roles; production authorization semantics are not yet proven. | Fixture explicitly scopes customer request, operator acceptance/assignment, courier progression, admin read/audit only. |
| System boundary | PARTIAL | Canonical repository is MyPrimeDelivery; live source-of-truth services are not selected. | Local in-memory/file fixture only; no external source of truth claimed. |
| Data boundary | UNKNOWN | Retention, PII and live customer-data requirements unresolved. | Synthetic IDs/addresses only; no real customer data. |
| Integration boundary | UNKNOWN | Payment/maps/messaging/courier providers unresolved. | Mock adapters only; no credentials or network mutation. |
| Acceptance evidence | VERIFIED FOR FIXTURE | Issue #2 defines a minimum non-production end-to-end gate. | Deterministic lifecycle tests below. |

## First safe vertical slice

`synthetic request → operator accepts → synthetic courier assigned → IN_PROGRESS → COMPLETED or EXCEPTION`

The slice is deliberately provider-neutral and commercial-model-neutral. It proves lifecycle/state/permission behavior only.

## Required deterministic acceptance tests

1. Valid happy-path lifecycle reaches COMPLETED.
2. Invalid status transition is rejected.
3. Actor permissions are enforced for accept/assign/progress operations.
4. One assignment is scoped to one delivery job.
5. Completed jobs are immutable except through an explicit correction path.
6. Exception state preserves reason + audit event.
7. No provider credential or live external call is required.
8. Synthetic fixture IDs cannot be mistaken for production customer/order identifiers.

## Blockers that remain external / owner-gated

- exact customer/problem definition
- commercial operating model
- launch geography
- pricing/unit economics
- payment provider
- maps/routing provider
- messaging provider
- courier/fleet provider
- retention/privacy policy for real customer data

These blockers do not prevent the deterministic local lifecycle fixture, but they do prevent production architecture claims.

## Evidence labels

Use only: VERIFIED, PARTIAL, UNKNOWN, OWNER DECISION REQUIRED, FIXTURE-SAFE, EXTERNAL-PRODUCTION BLOCKER.

## Safety boundary

No live dispatch, payments, customer data, provider credentials, deployment, production integration or external-service mutation is authorised by this artifact.
