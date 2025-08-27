# Deployment & Monitoring Reflection

Deploying the MSFT next-day stock price prediction model introduces several risks. First, **data drift** could occur if feature distributions shift over time, e.g., sudden changes in volatility or volume, leading to degraded predictive performance. Second, **missing or delayed data** may cause errors in real-time predictions. Third, **model degradation** is possible if relationships between features and target evolve, reducing R² and increasing MAE. Finally, **system failures** such as job timeouts or failed batch updates could disrupt timely predictions.

To monitor these risks, we propose metrics across four layers:

- **Data:** Track null rates for each feature (<5%), schema hashes to detect changes, and latency since last batch (<10 min). Alerts to the data engineer trigger the runbook to validate incoming CSVs.
- **Model:** Monitor rolling MAE and RMSE on a 7-day window, with a threshold of MAE increase >10% from baseline. Model owner receives alerts and first step is to check recent inputs and retraining logs.
- **System:** Track ETL job success rate (>95%) and p95 latency (<2 min). Ops team notified if failures occur, initiating automatic retries.
- **Business:** Monitor predicted vs actual price deviation impact on portfolio decisions; alert portfolio manager if deviation exceeds $1 per share.

Ongoing maintenance is jointly owned: the **data team** ensures feature pipelines remain correct, the **model owner** evaluates drift and triggers retraining, the **ops team** handles system uptime, and the **analyst/business owner** reviews KPIs weekly. Issues are logged in Jira, retraining is triggered by a PSI >5% or 2-week rolling MAE above threshold, and dashboards are updated weekly to reflect current model performance and business impact.
