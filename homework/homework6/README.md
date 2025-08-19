- Cleaning Strategy

1. Fill Missing Values
   Numeric columns are filled with the median using `fill_missing_median()`.

2. Drop Missing Values  
   Rows with too many missing values are removed using `drop_missing()` with a threshold.

3. Normalization
   Numeric columns are scaled using MinMaxScaler or StandardScaler via `normalize_data()`.

4. Column Type Correction  
   - `price` → float  
   - `date_str` → datetime (`date`)  
   - `category` → lowercase categorical  

- How to Run

1. Load the raw data from `data/raw/instructor_dirty.csv`.
2. Apply functions from `src/cleaning.py` in your notebook.
3. Save the cleaned data to `data/processed/combined_cleaned_data.csv`.
