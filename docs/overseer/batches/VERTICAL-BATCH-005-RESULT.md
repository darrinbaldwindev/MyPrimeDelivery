# MyPrimeDelivery — Vertical Batch 005 Result

Date: 2026-09-14
Status: COMPLETE (BOUNDED RESEARCH / NON-PRODUCTION)
Canonical batch: `docs/overseer/batches/VERTICAL-BATCH-005-WEAK-CATEGORY-DEPTH-AND-MARKETING-RECON.md`
Canonical coordination: `darrinbaldwindev/Overseer#49`

## Outcome

Deepened the six weakest launch categories, added explicit historical/snapshot evidence semantics, wired the new tranche into CI, and reconciled the Marketing Overseer brief to the verified Amazon/Prime discovery proposition.

## Fresh scan finding

Batch creation observed exact head:
`0be405b64eb539476dbd89c5fcfb499355578709`

The scan confirmed the Batch 004 source-quality hierarchy and 40-record cumulative research foundation. It also showed marketing documentation still in generic DISCOVERY REQUIRED state despite the now-verified product proposition.

## Durable artifacts

- `docs/overseer/batches/VERTICAL-BATCH-005-WEAK-CATEGORY-DEPTH-AND-MARKETING-RECON.md`
- `fixtures/candidates/research-tranche-005.json`
- `.github/workflows/fixture-validation.yml` now validates Batch 005 alongside all prior candidate/product/deal checks
- `docs/MARKETING-ROLE-AND-NEXT-ACTIONS.md` reconciled to current product truth

## Research tranche

18 additional research records were added, targeted exactly at the six weakest categories:

| Category | Added records |
|---|---:|
| Baby | 3 |
| Pet Supplies | 3 |
| Toys & Games | 3 |
| Office Products | 3 |
| Automotive | 3 |
| Garden & Outdoors | 3 |
| **Total rows** | **18** |

Evidence discipline:
- official Amazon Australia 2026 Prime Day product examples are `OFFICIAL_AMAZON_EVENT_HISTORICAL`; the event has ended and no current deal is implied;
- Amazon bestseller/category snapshots are `AMAZON_BESTSELLER_SNAPSHOT` and are not treated as current ranking authority where crawl freshness is inadequate;
- older official Amazon category/product-family signals remain `DISCOVERED`, with exact SKU/ASIN unresolved where appropriate;
- one Automotive slot is intentionally `BLOCKED` rather than inventing a current exact product from a category-level event signal;
- Prime evidence remains `UNKNOWN` throughout;
- `QUALIFIED` remains zero.

## Duplicate-awareness note

`Ninja Woodfire Outdoor Oven` appears as an additional official-Amazon historical evidence row in Batch 005 but was already present in the original first-30 research dataset. It therefore must not be counted twice when measuring unique product concepts. Batch 005 contributes 18 evidence rows but 17 new unique product concepts relative to prior tranches.

Cumulative after this batch:
- research evidence rows: 58;
- unique product concepts: at least 57 after known duplicate suppression;
- live `QUALIFIED` products: 0.

A later portfolio-level dedupe validator should enforce normalized-title/ASIN uniqueness across tranche files once stable identifiers are available.

## Marketing reconciliation

The Marketing Overseer brief now explicitly states:
- MyPrimeDelivery is an Amazon-focused product/category discovery site, not logistics/courier software;
- WordPress is the owner-selected platform;
- Prime, rank and deal claims are evidence-gated;
- deals are a freshness-aware discovery/repeat-visit layer;
- buying guides, category pages and comparison content are safe planning targets;
- marketing cannot become source of truth for eligibility/ranking/price/stock/deal status;
- no traction/revenue/savings/market-leadership claims without evidence.

## Current external evidence used

Research used current/recent and official Amazon evidence including:
- Amazon Australia Prime Day 2026 product examples across Toys & Kids, Baby/essentials and other categories;
- Amazon AU Dogs bestseller snapshot for pet-product discovery;
- Amazon AU Baby health/category bestseller snapshot;
- official historical Amazon Australia Prime Day/Boxing Day/Prime Big Deal Days category signals for Office, Automotive and Garden where fresh exact-product evidence was insufficient;
- Amazon Seller Central AU confirmation that Best Deals, Lightning Deals and Prime Exclusive Price Discounts are supported around 2026 peak events.

None of this public research substitutes for authorised current Prime/product/ranking data.

## Exact-head CI evidence

Workflow change was included before final documentation head:
`ce5f11bc26421712a7d8b47dc48164c9a9b239ab`

GitHub Actions run:
`34827072786`

Job `validate-m03-fixture` conclusion: `SUCCESS`.

Successful steps included:
- M-03 synthetic product validation/tests/rendering;
- deal evidence validation/rendering/negative assurance;
- first-100 candidate dataset validation;
- Batch 004 tranche validation;
- Batch 005 tranche validation;
- candidate negative assurance tests.

## Remaining blockers / UNKNOWNs

- canonical live marketplace/region decision;
- definition and evidence method for `top`;
- authorised Amazon product/Prime/deal/ranking provider;
- stable ASIN identity for all research records;
- Amazon Associates publication authority;
- allowed commercial fields and source-specific freshness/expiry cadence;
- public WordPress publication workflow and deployment authority.

## Result

Batch 005 is complete as a bounded research and documentation increment. Weak launch categories now have substantially more research depth, and the marketing brief no longer lags behind the product contract. No overall GREEN and no live product qualification is claimed.
