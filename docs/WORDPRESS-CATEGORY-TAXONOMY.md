# MyPrimeDelivery — WordPress Launch Category Taxonomy

Date: 2026-09-14
Status: OWNER-DIRECTION ALIGNED / NON-PRODUCTION PLANNING

## Purpose

Define a bounded initial category architecture for the MyPrimeDelivery WordPress discovery site. This is information architecture, not evidence that every category currently has qualified Prime-eligible products.

## Launch top-level categories

Exactly 12 initial top-level categories:

| ID | Slug | Name |
|---|---|---|
| `cat-home-kitchen` | `home-kitchen` | Home & Kitchen |
| `cat-electronics` | `electronics` | Electronics |
| `cat-baby` | `baby` | Baby |
| `cat-pet-supplies` | `pet-supplies` | Pet Supplies |
| `cat-health-household` | `health-household` | Health & Household |
| `cat-beauty-personal-care` | `beauty-personal-care` | Beauty & Personal Care |
| `cat-tools-home-improvement` | `tools-home-improvement` | Tools & Home Improvement |
| `cat-toys-games` | `toys-games` | Toys & Games |
| `cat-sports-outdoors` | `sports-outdoors` | Sports & Outdoors |
| `cat-office-products` | `office-products` | Office Products |
| `cat-automotive` | `automotive` | Automotive |
| `cat-garden-outdoors` | `garden-outdoors` | Garden & Outdoors |

## WordPress mapping

- WooCommerce Product Category is the presentation taxonomy.
- Stable MyPrimeDelivery category ID is stored independently from WordPress term/database IDs.
- Slugs above are canonical unless deliberately migrated.
- Category evidence/freshness metadata is stored through the MyPrimeDelivery evidence layer, not inferred from theme/plugin presentation.

## Subcategory policy

A subcategory should only be created when all are true:

1. it has a clear shopper intent distinct from its parent;
2. enough candidate inventory exists to justify a useful page;
3. qualified inventory can be maintained without fabricating Prime/rank/deal claims;
4. it can support a useful ranked/list/filter experience rather than an empty SEO page;
5. naming maps cleanly to the selected Amazon marketplace/data source once confirmed.

Target planning range after validation: roughly 3–8 useful subcategories per mature top-level category, not a copied Amazon category tree.

## Example future subcategories (provisional)

These are examples only and are not yet canonical:

- Home & Kitchen: storage & organisation, small appliances, cookware, cleaning, bedding, bathroom
- Electronics: headphones & audio, chargers & power, tablets, smart home, computer accessories
- Baby: monitors, feeding, nursery, travel, safety
- Pet Supplies: feeding, beds, grooming, toys, travel
- Health & Household: oral care, vitamins/supplements, household cleaning, personal health
- Beauty & Personal Care: skincare, haircare, fragrance, grooming
- Tools & Home Improvement: power tools, hand tools, lighting, hardware, home safety
- Toys & Games: building sets, educational toys, games, outdoor toys
- Sports & Outdoors: fitness, running, camping, hydration, recovery
- Office Products: chairs, desk accessories, stationery, organisation
- Automotive: car care, accessories, electronics, storage
- Garden & Outdoors: gardening tools, outdoor living, plant care, lighting

## Category publication gate

A category may exist internally before it is public, but a public category landing page should require a configurable minimum number of currently displayable products. Until the marketplace, ranking method and live data source are approved, this threshold remains a product decision rather than a hard-coded number.

## Anti-patterns

Do not:

- copy Amazon's full taxonomy wholesale;
- create hundreds of empty/thin category pages;
- call a category `Top` merely because products exist in it;
- expose a Prime filter if Prime evidence is UNKNOWN/STALE;
- make theme/plugin taxonomy IDs the long-term source of truth;
- use deal availability as a requirement for evergreen category membership.
