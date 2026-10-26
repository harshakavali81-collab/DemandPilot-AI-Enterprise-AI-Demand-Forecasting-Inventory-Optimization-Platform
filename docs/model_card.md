# Model card — DemandPilot demo-v1

**Intended task:** predict observed daily sales by SKU-store to support example replenishment decisions.

**Inputs:** historical daily units, price, promotion, SKU and store ID, lag 1/7/14/28, trailing 7/28 means, 7-day standard deviation, weekday, month, weekend and elapsed time.

**Validation:** chronological train/validation/test. A weekly seasonal-naive baseline is compared to LightGBM on validation WAPE. LightGBM is retrained on train plus validation. The frozen selection and both candidates are then reported on the out-of-time test set. See generated `artifacts/metrics.json`.

**Important limitations:** The data is synthetic and reported scores apply only to simulated observed sales. The test metrics are **one-step**, not a rolling-origin 30-day validation. Recursive forecasts compound error over the horizon. Future promotions must be known or assumed. The range `forecast ± 1.645 × test_residual_std × sqrt(step)` is an uncalibrated heuristic and uses test residuals: it is NOT a properly held-out calibration method. Stockout probabilities use an approximate Normal independent-daily-error model. These are educational planning indicators, not guaranteed service levels.

**Production upgrades:** real historical sales and inventory feeds with known censoring; proper rolling multi-horizon backtests and calibration split; supplier lead-time uncertainty; access control; monitored retraining and data drift.
