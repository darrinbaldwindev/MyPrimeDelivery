# MyPrimeDelivery — Vertical Batch 001: WordPress Discovery Foundation

Date: 2026-09-14
Status: ACTIVE
Trigger: owner request for high-yield vertical batching
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Operating protocol for future `cont` / `continue autonomously`

For this MyPrimeDelivery Overseer context, every owner instruction `cont` or `continue autonomously` means:

1. fresh-scan the current default branch, recent commits, relevant active branches and current coordination evidence;
2. identify the highest-value vertical that can be advanced safely without inventing requirements or creating duplicate AgentOS control-plane systems;
3. create a new numbered vertical batch file before execution;
4. pack the batch with multiple coherent tasks that share one outcome, rather than one tiny task per batch;
5. execute all safe bounded tasks in that batch during the current turn;
6. verify exact repository state, tests/CI evidence where available, and every durable mutation;
7. record blockers/UNKNOWNs explicitly instead of filling gaps with assumptions;
8. report substantive results durably back to the established coordination layer when they affect portfolio/AgentOS work;
9. do not claim overall GREEN from worker self-report.

Hard boundaries remain: no merge, deploy, credentials, production writes, Amazon account actions, supplier contact, purchases, production autonomy, or alternate scheduler/registry/ledger/authority/governance/persistence/assurance/source-of-truth systems without explicit owner authority.

## Fresh scan baseline

Current default branch: `agent/overseer/initial-project-timeline`.

Observed current foundation:

- owner-corrected Amazon/Prime product-discovery project contract;
- WordPress stack decision;
- M-03 WordPress data model and first non-production slice;
- deterministic synthetic product/category fixture;
- renderer and validator implementation with tests;
- fixture-validation GitHub Actions workflow;
- AgentOS Level-2 bounded lifecycle fixture/workload.

Current exact head at batch creation scan: `a0791c11624d751e36abc2d7d4c5b793b568c760`.

## Vertical outcome

Turn the owner-approved WordPress/Amazon discovery direction into a coherent, implementation-ready non-production product-discovery foundation that supports:

- launch category structure;
- time-sensitive deal/sale evidence without fabricated urgency;
- candidate-product intake and qualification states;
- evidence/freshness fail-closed behavior;
- future WordPress templates/components;
- continued use as a bounded AgentOS Level-2 acceptance workload.

## Task set

### T1 — Launch taxonomy

Create a bounded 12-category launch taxonomy with expansion rules and subcategory policy. Categories are planning architecture, not claims that Amazon currently supplies qualified inventory.

Acceptance:
- exactly 12 initial top-level categories;
- category IDs/slugs are stable and WordPress/WooCommerce-friendly;
- subcategories are only created when evidence/product density justifies them;
- no empty SEO-category proliferation.

### T2 — Deal/time-sensitive evidence contract

Define a deal/offer record and fail-closed freshness model for sale products.

Acceptance:
- separate product identity from offer/deal evidence;
- support ACTIVE / STALE / UNKNOWN / EXPIRED / BLOCKED states;
- never infer a discount from an unsupported reference price;
- expired/stale deals automatically lose current-sale presentation;
- no scraping or live Amazon credentials authorised.

### T3 — Product-candidate qualification pipeline

Define the intake states used for the planned first 100 Amazon AU candidates:

`DISCOVERED -> CANDIDATE -> QUALIFIED | REJECTED | STALE | BLOCKED`

Acceptance:
- QUALIFIED requires marketplace, Prime evidence, ranking/selection evidence and freshness evidence;
- deal status is optional for evergreen products;
- rejection reason is durable;
- public display and outbound CTA remain gated from research/intake status.

### T4 — WordPress mapping alignment

Map taxonomy, product evidence and deal evidence to the existing WooCommerce + ACF + GenerateBlocks/Gutenberg + FacetWP design without making a plugin the canonical data source.

Acceptance:
- WooCommerce remains catalogue-only;
- Prime/ranking/deal evidence fields remain explicit;
- checkout/shipping/payment/order flows remain out of scope;
- live Amazon provider remains behind a replaceable data-provider boundary.

### T5 — Verification / regression review

Re-read current M-03 validator/renderer/test/workflow evidence and verify this batch does not weaken fail-closed behavior or Level-2 fixture isolation.

Acceptance:
- no live Amazon links or credentials added;
- synthetic fixture rules remain intact;
- no alternate AgentOS control plane introduced;
- batch artifacts are durable and exact paths are verified.

### T6 — Coordination report

Post one concise substantive report to `darrinbaldwindev/Overseer#49` after execution, including exact head/commits, bounded contribution, verified evidence, remaining blockers and no-overall-GREEN statement.

## Known UNKNOWNs preserved

- target Amazon marketplace/region is not yet owner-confirmed in the canonical contract (AU is the current research direction, not silently promoted here);
- exact definition of `top` / ranking methodology;
- authorised Amazon product/Prime/deal data source;
- Amazon Associates account/tag and rights;
- live price/image/rating/reference-price permissions;
- exact freshness/refresh intervals;
- production deployment and publishing authority.

## Batch completion rule

Batch 001 is complete only when T1–T6 have durable repository/coordination evidence. Completion of the batch is not overall MyPrimeDelivery GREEN and does not authorise production Amazon integration.