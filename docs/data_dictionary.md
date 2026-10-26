# Dataset and provenance

All demo data is **synthetic**. The seeded generator creates eight fictional product IDs across two fictional stores for 420 consecutive days (6,720 sales rows). This is NOT a real retailer's transaction feed or the M5 dataset.

## Sales columns

| Name | Meaning |
|---|---|
| date | ISO daily date, complete for each SKU-store |
| store_id | Fictional store key |
| product_id | Fictional product key |
| category | Fictional category label |
| price | Simulated sold-unit price in INR |
| units_sold | Simulated nonnegative daily sales |
| promo | Simulated 0/1 promotion flag |

## Inventory columns

| Name | Meaning |
|---|---|
| on_hand | Simulated stock units |
| on_order | Simulated incoming units |
| backorders | Outstanding units |
| lead_time_days | Simulated supplier delay |
| unit_cost | Simulated buying cost in INR |
| service_level | Target service level, NOT achieved service |

Known constraints: sales may be censored by stockouts in real life; the generator does not simulate demand censoring. There are no real customer data, actual ERP feeds, holiday events, returns, supplier delays, or personally identifiable information. Treat price assumptions, independence of errors, and service-level risk estimates as examples only.
