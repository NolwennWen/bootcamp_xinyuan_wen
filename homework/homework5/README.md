
Homework5: Reproducible Data Storage

1. Folder structure
- data/raw: stores raw data files (CSV format)  
- data/processed: stores processed data files (Parquet format)

2. File Formats
- CSV: easy to inspect and share. 
- Parquet: efficient columnar storage, preserves dtypes.

3. Environment Variables
The notebook loads these variables using `python-dotenv` and constructs the full paths using pathlib.  
This approach ensures that file storage is reproducible and portable.
...
