# Deliverables README

## Chosen Audience and Rationale
The primary audience for these deliverables are **portfolio managers, investment analysts, and traders** who need quick, actionable insights on predicted next-day stock prices.  
- **Decision-makers:** Portfolio managers decide on trade execution and portfolio allocation based on predictions.  
- **End-users:** Traders and retail investors use predictions to guide daily trading decisions.  

## Format Choice
The deliverable is provided in **Markdown format** with embedded visualizations:  
- Markdown is lightweight, easily version-controlled, and displays well on **GitHub**.  
- Visualizations (line plots, scatter plots, residual charts) are integrated directly with explanations, ensuring stakeholders can review both the results and the context without switching applications.  
- This format allows **quick updates** and reproducibility: charts can be regenerated daily as new data arrives.

## Alignment with Project Goals
- **Transparency:** All model assumptions, risks, and sensitivity analyses are documented in plain language.  
- **Reproducibility:** Figures and tables are generated from code in `/notebooks/` using processed data in `/data/processed/`.  
- **Decision-oriented:** Each chart is accompanied by concise interpretation and practical takeaway, enabling stakeholders to make informed trading and portfolio allocation decisions.  

## Folder Structure Overview
- `/data/`: Raw and processed stock data.  
- `/src/`: Python scripts for data collection, feature engineering, and modeling.  
- `/notebooks/`: Jupyter notebooks with modeling, evaluation, and scenario analysis.  
- `/deliverables/images/`: Final visualizations exported for stakeholder review.  
- `/deliverables/`: Markdown report and README for stakeholders.  
