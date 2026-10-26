# System architecture

```mermaid
flowchart TD
  A[Simulated sales and inventory] --> B[Schema validation]
  B --> C[Daily store-product histories]
  C --> D[Lagged features using earlier days only]
  D --> E[Chronological validation and test]
  E --> F[Seasonal naive compared with LightGBM]
  F --> G[Saved trained model and metrics]
  G --> H[Recursive horizon forecasts]
  H --> I[Lead-time inventory optimization]
  J[Simulated stock and supplier lead times] --> I
  I --> K[Reorder quantities and approximate stockout risk]
  K --> L[FastAPI REST service]
  H --> L
  L --> M[Streamlit dashboard, CSV export and SQLite audit]
```

## API contract

- `GET /health`: API liveness information.
- `GET /catalog`: synthetic store-product catalog.
- `POST /forecast`: forecast 1–90 days for known product and store; optionally set future price and known promotion days.
- `GET /inventory/alerts`: compute sample stockout risk and order recommendation for each store-product.
- `POST /inventory/recommend`: user-provided daily forecast, lead time, review period, stock and service target.
- `GET /metrics`: chronological validation and out-of-time test comparison.

All scores and inventory simulations are demonstration values, not independently validated commercial outcomes. This is a single-user educational app, NOT a multi-tenant authenticated ERP integration.
