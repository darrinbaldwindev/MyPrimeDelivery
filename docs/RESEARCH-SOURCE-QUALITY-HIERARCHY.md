# MyPrimeDelivery — Research Source Quality Hierarchy

Date: 2026-09-14
Status: NON-PRODUCTION RESEARCH CONTRACT

## Purpose

Prevent discovery sources, deal trackers and editorial pages from being mistaken for authoritative Amazon product, Prime, ranking or publication evidence.

## Source classes

### A — AUTHORITATIVE AMAZON / AUTHORISED PROVIDER
Examples once explicitly approved:
- Amazon Creators API / Product Advertising API or successor authorised interface;
- other Amazon-authorised provider contractually permitted for the field being consumed.

May potentially support, subject to exact field rights and freshness rules:
- product identity;
- current Prime eligibility;
- permitted offer/deal fields;
- permitted price/availability content;
- outbound Amazon destination;
- provider-backed freshness timestamps.

This class alone does not automatically define MyPrimeDelivery's `top` ranking methodology.

### B — AMAZON FIRST-PARTY PUBLIC INFORMATION
Examples:
- Amazon Australia announcements;
- official Seller Central event/deal documentation;
- public Amazon category/deal surfaces where use is policy-compliant.

May support:
- event existence;
- general Prime/deal programme facts;
- marketplace-level capability evidence.

Must not be treated as product-specific Prime/ranking evidence unless the exact product fact is explicitly supported and use is permitted.

### C — INDEPENDENT PRICE/DEAL TRACKER
Examples:
- Aussie Amazon Deals;
- Keepa where access/licence permits;
- comparable independent tracking services.

May support:
- discovery;
- price-drop/deal research signals;
- historical-price research where methodology is understood.

Cannot alone promote a product to `QUALIFIED` or prove current Prime eligibility.

### D — CURRENT EDITORIAL CURATION
Examples:
- Tom's Guide Australia;
- TechRadar Australia;
- reputable Australian deal/editorial publications.

May support:
- discovery;
- category demand signals;
- candidate prioritisation;
- editorial deal signal.

Cannot alone prove current Prime eligibility, Amazon ranking or canonical price/availability.

### E — PROMO/COUPON AGGREGATOR
May support:
- broad category-sale discovery;
- event/promotion research.

Never authoritative for product qualification, Prime, rank or publication fields.

## Field authority matrix

| Field/claim | Minimum source class for publication |
|---|---|
| Product identity/ASIN | A |
| Marketplace | A or explicit owner configuration backed by provider |
| Prime eligible | A |
| Current price/availability | A and permitted field rights |
| Deal active/expiry | A where displayed publicly; research may use C/D only as candidate signal |
| `Top`/ranking position | Explicit MyPrimeDelivery methodology + supporting authorised evidence |
| Historical-low research | C may inform research; publication requires rights/methodology review |
| Category demand signal | B/C/D may inform planning |
| Affiliate destination | A + approved Associates/publication authority |

## Promotion rule

`DISCOVERED` and `CANDIDATE` may be created from C/D/E evidence.

`QUALIFIED` requires all pipeline gates and cannot be reached merely because multiple weak sources agree.

## Freshness rule

Every time-sensitive source must record `observed_at` or equivalent. Research snapshots age into stale evidence according to source-specific rules once defined. Absence of a configured live freshness policy means the record remains research-only.

## Conflict rule

Higher-authority evidence wins only for the field it actually supports. Conflicting evidence produces `BLOCKED` or explicit UNKNOWN state rather than silent selection.

## No-production boundary

This hierarchy does not authorise credentials, scraping, live API use, affiliate publication, production ingestion or deployment.