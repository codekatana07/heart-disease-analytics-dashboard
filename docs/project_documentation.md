# Heart Disease Data Visualization Dashboard - Project Documentation

## 1. Objective
Build an end-to-end analytics workflow using Python, MySQL, Tableau, and Flask to identify heart disease risk factors and present them through interactive dashboards.

## 2. Source Dataset
- Raw source file: `data/Heart_new2.csv` (copied from provided `Heart_new2.csv`)
- Normalized output file: `data/heart_disease.csv`
- Target analytics columns:
  - `age, sex, cp, trestbps, chol, fbs, thalach, exang, oldpeak, target`
  - Additional lifestyle fields: `smoking, physical_activity, bmi, age_category`

## 3. Data Preparation (Python)
Use the normalization script to create a MySQL/Tableau-ready dataset.

```bash
python data/load_dataset.py --input data/Heart_new2.csv --output data/heart_disease.csv
```

Notes:
- If input is the provided `Heart_new2.csv`, the script maps and estimates clinical indicators from available lifestyle/health fields.
- If input already matches classic heart disease columns, records are passed through directly.

## 4. Database Layer (MySQL + SQL Workbench)

### 4.1 Create Schema and Table
Open MySQL Workbench and run:
- `database/schema.sql`

This creates:
- Database: `heart_disease_dashboard`
- Table: `heart_disease`

### 4.2 Load Data into MySQL
Run from terminal:

```bash
python database/insert_data.py --csv data/heart_disease.csv --truncate
```

Environment variables (optional overrides):
- `MYSQL_HOST` (default `localhost`)
- `MYSQL_PORT` (default `3306`)
- `MYSQL_USER` (default `root`)
- `MYSQL_PASSWORD` (default `root`)
- `MYSQL_DATABASE` (default `heart_disease_dashboard`)

### 4.3 Core SQL Queries
Run `database/queries.sql` in MySQL Workbench.

Required queries included:
1. Average cholesterol by age
2. Heart disease count by gender
3. High-risk patients (`chol > 240 AND trestbps > 140`)

## 5. Tableau Integration

### 5.1 Connect Tableau to MySQL
1. Open Tableau Desktop.
2. Click **Connect** -> **To a Server** -> **MySQL**.
3. Enter connection details:
   - Server: `localhost`
   - Port: `3306`
   - Database: `heart_disease_dashboard`
   - Table: `heart_disease`
4. Click **Sign In** and load the table.

### 5.2 Data Preparation in Tableau
- Ensure numeric types for: `age, trestbps, chol, thalach, oldpeak, bmi`
- Ensure dimensions for: `sex, age_category, target, smoking, physical_activity`

### 5.3 Calculated Fields

#### Risk Category
```text
IF [chol] > 240 AND [trestbps] > 140 THEN "High" ELSE "Normal" END
```

#### Age Group
```text
IF [age] < 40 THEN "<40"
ELSEIF [age] >= 40 AND [age] < 50 THEN "40-49"
ELSEIF [age] >= 50 AND [age] < 60 THEN "50-59"
ELSEIF [age] >= 60 AND [age] < 70 THEN "60-69"
ELSE "70+"
END
```

## 6. Required Visualizations (8)
Create these Tableau worksheets:

1. **Age vs Heart Disease (Bar Chart)**
   - X: `Age Group` or `age`
   - Y: `SUM(target)`

2. **Gender vs Disease (Pie Chart)**
   - Color: `sex`
   - Angle: `SUM(target)`

3. **Cholesterol Distribution (Histogram)**
   - Bins from `chol`
   - Count of records

4. **Blood Pressure vs Cholesterol (Scatter Plot)**
   - X: `trestbps`
   - Y: `chol`
   - Color: `Risk Category`

5. **Heart Rate vs Disease (Line Chart)**
   - X: `thalach` (binned or grouped)
   - Y: `AVG(target)`

6. **Lifestyle Risk Heatmap**
   - Rows: `smoking`
   - Columns: `physical_activity`
   - Color: `AVG(target)`

7. **Age Group Risk Comparison**
   - X: `Age Group`
   - Y: `AVG(target)`

8. **High-Risk Patient Distribution**
   - Map/Bar by `sex` or `age_category`
   - Filter `Risk Category = "High"`

## 7. Tableau Dashboard Design
Create a dashboard `MainDashboard` with:
- All major worksheets
- Global filters: `age`, `sex`, `chol`, `trestbps`
- Clean responsive layout:
  - Top row: KPI summaries
  - Middle: risk correlation charts
  - Bottom: distribution/lifestyle charts

## 8. Tableau Story (5 Scenes)
Create a story with these points:
1. Dataset overview
2. Age risk analysis
3. Lifestyle risk factors
4. Cholesterol correlation
5. Preventive insights

## 9. Flask Web App Integration
Use `flask_app/app.py` and `flask_app/templates/dashboard.html`.

- Route `/` serves the dashboard page.
- Tableau dashboard is embedded through an iframe using `TABLEAU_DASHBOARD_URL`.

Run:

```bash
python flask_app/app.py
```

Open: `http://127.0.0.1:5000/`

## 10. Suggested Local Execution Order
1. Install dependencies: `pip install -r requirements.txt`
2. Normalize data: `python data/load_dataset.py --input data/Heart_new2.csv --output data/heart_disease.csv`
3. Run schema in MySQL Workbench: `database/schema.sql`
4. Load data: `python database/insert_data.py --csv data/heart_disease.csv --truncate`
5. Validate queries: `database/queries.sql`
6. Build Tableau worksheets, dashboard, and story
7. Publish dashboard to Tableau Public/Server
8. Set `TABLEAU_DASHBOARD_URL` and run Flask app
