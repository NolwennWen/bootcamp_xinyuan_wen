# Orchestration Plan — MSFT Stock Prediction Project

## 1. Pipeline Overview
The project for MSFT stock price prediction is divided into the following key tasks:

| Task ID | Task Name | Input | Output | Notes / Idempotency | Logging & Checkpoint |
|---------|-----------|-------|--------|-------------------|--------------------|
| T1 | Data Ingestion | YFinance API / CSV | Raw CSV in `RAW_DIR` | Repeatable | Log API request success/failure; checkpoint raw CSV |
| T2 | Data Cleaning | Raw CSV | Cleaned CSV in `PROC_DIR` | Repeatable, idempotent | Log number of rows/cols before & after cleaning |
| T3 | Feature Engineering | Cleaned CSV | Feature CSV in `PROC_DIR` | Repeatable, idempotent | Log new feature counts & nulls |
| T4 | Outlier Detection & Winsorization | Feature CSV | Outlier mask + winsorized CSV | Repeatable | Log detected outliers per column |
| T5 | Baseline Linear Regression | Feature CSV | Trained model, metrics, residual plots | Idempotent | Log R², RMSE, MAE; save checkpoint model |
| T6 | Extended Regression (RSI² & RSI³) | Feature CSV | Trained model, metrics, residual plots | Idempotent | Log R², RMSE, MAE; save checkpoint model |
| T7 | Model Saving | Trained model object | Pickled model in `MODEL_DIR` | Idempotent | Log save success & path |
| T8 | Reporting / Visualization | Feature CSV + model predictions | Plots in `OUTPUT_DIR` | Idempotent | Log saved figure paths |

---

## 2. DAG Sketch


        T1
        ↓
        T2
        ↓
        T3
        ↓
   ┌─────┴─────┐
   T4          T5
   ↓           ↓
   T6           T7
   ↓           ↓
        T8


- T4 and T5 can be executed in parallel  
- T6 depends on T3 + T4  
- T8 consolidates all model results and predictions

---

## 3. Logging & Checkpoints

- **Data Layer:** Log number of rows, columns, null values, schema hash  
- **Model Layer:** Log R², RMSE, MAE, model coefficients, outlier counts  
- **System Layer:** Log script start/end time, exceptions, file read/write success  
- **Business Layer:** Track predicted vs actual price trends, key KPI plots

Checkpoint files:
- Cleaned CSV (`PROC_DIR/MSFT_preprocessed.csv`)  
- Feature CSV (`PROC_DIR/MSFT_features.csv`)  
- Models (`MODEL_DIR/*.pkl`)  
- Plots (`OUTPUT_DIR/*.png`)

---

## 4. Automation Strategy

- **Automate:** Data ingestion, cleaning, feature generation, model training, saving, plotting  
- **Manual:** Periodic inspection of plots for anomaly detection, review for business relevance  
- **Reasoning:** Automation ensures reproducibility of the data flow and training; manual tasks are for business judgment and model interpretation

---

## 5. Failure Handling & Retry

| Task | Failure Mode | Retry Policy |
|------|-------------|-------------|
| T1 | API failure / network error | Retry up to 3 times with backoff |
| T2 | Missing columns / parse errors | Halt pipeline and notify analyst |
| T3 | Null or infinite values in features | Filter & log; skip model training if too many |
| T5/T6 | Convergence error / NaN predictions | Halt & inspect; may trigger re-cleaning |
| T7 | File write error | Retry 1 time; alert owner |

---

## 6. Ownership

- **Data ingestion & cleaning:** Analyst weekly review  
- **Model training & evaluation:** Data Scientist  
- **System monitoring / logs:** Platform engineer (if available)  
- **Business KPI review:** Product owner  
- **Issue logging:** Shared GitHub issues / Slack channel
