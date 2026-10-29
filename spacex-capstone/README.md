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

The historical Wikipedia revision returned HTTP 403. The current launch-list page was successfully retrieved on 29 October 2026 and parsed into 285 distinct dated records (2025-2026), demonstrating the complete scraping workflow. These records are not merged into the historical modeling cohort. See 02_Web_Scraping.ipynb and evidence/scraping_evidence.json. Independent supplied lab snapshots support the historical analyses.

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

## Evidence added after report review

- 01_Data_Collection_API.ipynb verifies the 107 -> 95 -> 94 -> 90 filter counts.
- 02_Web_Scraping.ipynb executes the BeautifulSoup workflow and displays current-page output.
- folium_site_records.py and 06_Folium_Map.ipynb render all 56 records in four site maps; saved HTML views are in evidence/.
- evidence/test_prediction_audit.csv lists every held-out prediction. All four models use 18 test records (6 Class 0, 12 Class 1). Training contains 72 records (24 Class 0, 48 Class 1).
- SVM false positives are flights 75, 14 and 12; TN=3, FP=3, FN=0, TP=12.
- The SQL notebook includes every required query and output, using its separate 101-record snapshot.
