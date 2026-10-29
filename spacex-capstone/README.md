# Data Science Capstone Project: SpaceX Falcon 9

Author: Isse Abdallah Mohamoud

This project analyzes historical Falcon 9 first-stage landing outcomes using the IBM Applied Data Science Capstone snapshots. It covers data acquisition, wrangling, EDA, SQL, Folium, Dash, and classification.

## Reproduce

```bash
pip install -r requirements.txt
python collect_data.py
python analyze.py
python create_assets.py
python spacex_dashboard.py
```

Run the notebook from this project folder. The Dash app opens at http://127.0.0.1:8052.

## Scope and results

- API-derived model snapshot: 90 Falcon 9 records, 2010-2020. Label 1 appears in 60 records.
- SQL snapshot: 101 rows. Strings are stripped before aggregation.
- Dash and geospatial snapshots: 56 records. Site labels differ across snapshots.
- Model split: 72 training, 18 test, random_state=2. Five-fold stratified validation fits scaling within each training fold.
- SVM and KNN tie at 84.76% validation accuracy and 83.33% test accuracy. Logistic regression also reaches 83.33% test accuracy. Decision tree reaches 72.22% with the stated grid.
- Separate lab-style global scaling reproduces sigmoid SVM with C=1, gamma=0.0316228, validation=84.82%, test=83.33%. This comparison is not a leakage-free validation protocol.

## Important limits

Labels follow the course convention and include successful ocean outcomes. They do not prove recovery, future reuse, or launch costs. ReusedCount and booster metadata can reflect information accumulated after the event. The tiny random test split is not evidence of future operational performance.

The historical Wikipedia revision returned HTTP 403 during preparation. collect_data.py includes the parsing workflow and records failures explicitly. No fresh historical scrape is claimed. Independent supplied lab snapshots support the remaining analyses.

Proximity map points are manually selected illustrative references, not surveyed or verified nearest roads, railways, or coastline points. Distances are haversine straight-line distances.

## Files

- collect_data.py: source downloads, API inspection, historical HTML parsing workflow.
- SpaceX_Capstone_Analysis.ipynb: EDA and SQL results.
- analyze.py / analysis_results.json: reproducible model grids and computed results.
- sql_analysis.sql: required SQL queries.
- create_assets.py: Folium site, record, and proximity maps.
- spacex_dashboard.py: site dropdown, payload slider, pie and scatter charts.
- data/: original course CSV snapshots.

Data source: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/
