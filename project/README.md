# Stock Price Prediction  

## Project Overview  
This project aims to build a complete, end-to-end data pipeline for stock price prediction.  
The goal is to predict the next-day closing price of selected stocks using historical price, trading volume, and other available data.  
This aligns with real-world financial data workflows and will be developed step by step through the lifecycle stages taught in the course.  

## Repository Structure  
project/
│
├── README.md
│
├── .env
│
├── .gitignore
│
├── requirements.txt <- Python dependencies
│
├── data/
│ ├── raw/ <- Raw stock data
│ │ ├──api_source-yfinance_symbol-MSFT_*.csv <- raw stock data pulled from yfinance for `SYMBOL=MSFT`
│ │ └──MSFT_raw_*.csv <- versioned copy of the raw CSV for reproducibility
│ └── processed/ <- Cleaned & feature-engineered data
│ │ ├──prices_*.parquet <- processed Parquet version of raw stock data
│ │ └──MSFT_preprocessed.csv <- cleaned data
│
├── notebooks/
│ ├──Stage_3_python_fundamentals_summary.ipynb
│ ├──Stage_4_data_acquisition.ipynb
│ ├──Stage_5_data_storage.ipynb
│ ├──Stage_6_data_processing.ipynb
│ └──Stage_7_outliers_risk_assumptions.ipynb
│
├── src/
│ ├──utils.py
│ ├──cleaning.py
│ └──outliers.py
│
├── docs/
│ ├── stakeholder_memo.md
│ └── README.md

/notebooks/: Jupyter notebooks for EDA & modeling
/src/: Python scripts for data collection & modeling
/data/raw/ and /data/processed/: Input datasets
/docs/: Stakeholder memo and lifecycle documentation


## Data Acquisition & Ingestion

**Data Source:**  
Historical stock price data for Microsoft Corporation (MSFT) was acquired programmatically using the `yfinance` Python package, which provides access to Yahoo Finance data.

**Stock Symbol:**  
`MSFT` (Microsoft Corporation)

**Time Period:**  
The last 6 months of daily trading data were downloaded with a 1-day interval (`period="6mo"`, `interval="1d"`).

**Saved Location:**  
The raw data was validated and saved as a CSV file in the project folder:  
`/data/raw/` with a timestamped filename for reproducibility.  

**Validation:**  
Data was checked for required columns (`date`, `adj_close`) and proper data types using the `validate_df` utility function. This ensures that the dataset is clean and ready for preprocessing in subsequent stages.

## Data Storage

**File Formats:** 

- CSV: raw, human-readable, easy to inspect, used for storing the original downloaded data.
- Parquet: efficient columnar format, faster to read/write for larger datasets, preserves data types.

**Reading Data in Code:**

All code uses **environment-driven paths** to ensure reproducibility:

```python
import os, pathlib, pandas as pd
from dotenv import load_dotenv

load_dotenv()
RAW_DIR = pathlib.Path(os.getenv("DATA_DIR_RAW", "data/raw"))
PROC_DIR = pathlib.Path(os.getenv("DATA_DIR_PROCESSED", "data/processed"))

csv_path = RAW_DIR / "api_source-yfinance_symbol-MSFT_20250820-200354.csv"
df_raw = pd.read_csv(csv_path, parse_dates=['date'])

parq_path = PROC_DIR / "MSFT_raw_20250820-101530.parquet"
df_proc = pd.read_parquet(parq_path)

## Data Preprocessing Assumptions

1. **Missing Values**
   - Numeric columns: missing values filled with the **median**.
     - Rationale: median is robust to outliers and preserves the central tendency.
   - Rows with >50% missing values dropped.
     - Rationale: heavily missing rows are unlikely to contribute useful information.

2. **Currency Columns**
   - Columns like `price` stored as strings with `$` are converted to numeric (float).
     - Rationale: to allow calculations and transformations for modeling.

3. **Date Columns**
   - String dates (`date_str`) are converted to `datetime` objects.
     - Rationale: enables time-based operations and resampling.

4. **Categorical Columns**
   - Standardized to lowercase and converted to `category` dtype.
     - Rationale: ensures consistent labels and reduces memory usage.

5. **Scaling**
   - Numeric columns optionally scaled using **MinMaxScaler** or **StandardScaler**.
     - Rationale: many ML algorithms perform better when features are normalized.

6. **Column Type Correction**
   - Mixed or object columns checked and cast to appropriate types.
     - Rationale: ensures correct dtype for modeling and prevents unexpected errors.

Preprocessing includes:
  - Missing value imputation
  - Scaling numeric columns
  - Converting string columns to numeric or datetime
  - Standardizing categorical columns
  
Code for preprocessing is located in `src/cleaning.py`

## Outlier Assumptions and Implications

1. Outliers

- IQR multiplier k=1.5; Z threshold=3.0; winsor quantiles 5%/95%.
- The stock price columns (open, high, low, close, adj_close) show no significant outliers, indicating that their distributions are relatively concentrated.
- The trading volume column exhibits a few extreme values, but the number is small and both IQR and Z-score methods detect consistent points.
- The Z-score method does not over-identify outliers in practice.
- Always report thresholds and provide results **with and without** outliers.

2. Sensitivity Analysis

- A regression-based sensitivity analysis was performed on adj_close and volume to evaluate the impact of outliers on model results.
- The R² is very low (0.08), indicating that the independent variable x has weak explanatory power for y.
- The slope and intercept change little, suggesting that outliers do not significantly affect the overall trend.
- Winsorization slightly improves the MAE, indicating that it mitigates the impact of a few extreme points.

3. Assumptions

- Extreme values are rare and do not represent valid underlying patterns.
- The IQR and Z-score thresholds are appropriate for detecting meaningful outliers in stock price and volume data.
- Winsorization is sufficient to mitigate extreme values without distorting overall trends.

4. Potential Risks

- Removing or modifying data could hide important market anomalies (e.g., flash crashes or spikes).
- Overly aggressive filtering may reduce model accuracy for rare but significant events.
- Analysts should verify whether flagged outliers correspond to actual market events or data errors.