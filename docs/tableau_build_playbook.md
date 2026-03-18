# Tableau Build Playbook (Connect + Create Everything)

## 1. Connect Tableau to MySQL
1. Open Tableau Desktop.
2. In **Connect**, click **MySQL**.
3. Enter:
   - Server: `localhost`
   - Port: `3306`
   - Username: `user123`
   - Password: `user123`
   - Database: `heart_disease_dashboard`
4. Click **Sign In**.
5. In the Data Source page, select table/view: `vw_heart_disease_enriched`.
6. Click **Sheet 1**.

## 2. Recommended Data Source Setup
- Keep `sex`, `age_group`, `risk_category` as Dimensions.
- Keep `age`, `trestbps`, `chol`, `thalach`, `oldpeak` as Measures.
- Keep `target`, `smoking`, `physical_activity` as Measures (Number - whole).

## 3. Build 8 Required Worksheets

### Sheet 1: Age vs Heart Disease (Bar)
- Name: `Age vs Disease`
- Columns: `age_group`
- Rows: `SUM(target)`
- Marks: Bar
- Sort age groups ascending.

### Sheet 2: Gender vs Disease (Pie)
- Name: `Gender vs Disease`
- Marks: Pie
- Color: `sex`
- Angle: `SUM(target)`
- Label: `SUM(target)` and `% of Total`.

### Sheet 3: Cholesterol Distribution (Histogram)
- Name: `Cholesterol Distribution`
- Option A: Use `chol` -> Create Bins (size 10), then put `chol (bin)` on Columns and `COUNT(id)` on Rows.
- Option B: Use view `vw_cholesterol_distribution` with `chol_bin` on Columns and `patient_count` on Rows.

### Sheet 4: Blood Pressure vs Cholesterol (Scatter)
- Name: `BP vs Cholesterol`
- Columns: `trestbps`
- Rows: `chol`
- Marks: Circle
- Color: `risk_category`
- Detail: `id`
- Add trend line from Analytics pane.

### Sheet 5: Heart Rate vs Disease (Line)
- Name: `Heart Rate vs Disease`
- Columns: `thalach`
- Rows: `AVG(target)`
- Marks: Line
- Format Y-axis as percentage.

### Sheet 6: Lifestyle Risk Heatmap
- Name: `Lifestyle Heatmap`
- Columns: `physical_activity`
- Rows: `smoking`
- Marks: Square
- Color: `AVG(target)`
- Label: `COUNT(id)`.

### Sheet 7: Age Group Risk Comparison
- Name: `Age Group Risk`
- Columns: `age_group`
- Rows: `AVG(target)`
- Marks: Bar
- Color: `age_group`
- Format Y-axis as percentage.

### Sheet 8: High-Risk Distribution
- Name: `High Risk Distribution`
- Filters: `risk_category` = `High`
- Columns: `age_group`
- Rows: `COUNT(id)`
- Color: `sex`
- Marks: Bar (stacked)

## 4. Create Dashboard
1. Click **New Dashboard**.
2. Name it `MainDashboard`.
3. Set Size to `Automatic`.
4. Place sheets in this layout:
   - Top row: `Age vs Disease`, `Gender vs Disease`
   - Middle row: `BP vs Cholesterol`, `Cholesterol Distribution`
   - Bottom row: `Lifestyle Heatmap`, `Age Group Risk`, `Heart Rate vs Disease`, `High Risk Distribution`
5. Add global filters (Apply to Worksheets -> All Using This Data Source):
   - `age`
   - `sex`
   - `chol`
   - `trestbps`
6. Show legends and add a title:
   - `Heart Disease Data Visualization Dashboard`

## 5. Create Story (5 Scenes)
1. Click **New Story**.
2. Name it `Heart Disease Insights Story`.
3. Add 5 story points:
   - Dataset overview
   - Age risk analysis
   - Lifestyle risk factors
   - Cholesterol correlation
   - Preventive insights
4. Attach relevant dashboard/sheets to each story point.

## 6. Publish and Embed
1. In Tableau, publish `MainDashboard` to Tableau Public (or Tableau Server).
2. Copy share URL and ensure `?:showVizHome=no` is appended.
3. Set env variable and run Flask app:

```powershell
$env:TABLEAU_DASHBOARD_URL="https://public.tableau.com/views/HeartDiseasePrediction_17730017390650/HeartDiseaseDataAnalysisKeyInsights?:showVizHome=no"
& "C:/Users/xhgme/AppData/Local/Programs/Python/Python313/python.exe" "flask_app/app.py"
```

4. Open `http://127.0.0.1:5000/`.
