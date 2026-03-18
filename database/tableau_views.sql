USE heart_disease_dashboard;

-- Tableau-ready base view with calculated categories precomputed in SQL.
DROP VIEW IF EXISTS vw_heart_disease_enriched;
CREATE VIEW vw_heart_disease_enriched AS
SELECT
    id,
    age,
    sex,
    cp,
    trestbps,
    chol,
    fbs,
    thalach,
    exang,
    oldpeak,
    target,
    smoking,
    physical_activity,
    bmi,
    age_category,
    CASE
        WHEN chol > 240 AND trestbps > 140 THEN 'High'
        ELSE 'Normal'
    END AS risk_category,
    CASE
        WHEN age < 40 THEN '<40'
        WHEN age >= 40 AND age < 50 THEN '40-49'
        WHEN age >= 50 AND age < 60 THEN '50-59'
        WHEN age >= 60 AND age < 70 THEN '60-69'
        ELSE '70+'
    END AS age_group
FROM heart_disease;

-- 1) Age vs heart disease.
DROP VIEW IF EXISTS vw_age_vs_disease;
CREATE VIEW vw_age_vs_disease AS
SELECT
    age_group,
    COUNT(*) AS patients,
    SUM(target) AS disease_cases,
    ROUND(AVG(target) * 100, 2) AS disease_rate_pct
FROM vw_heart_disease_enriched
GROUP BY age_group;

-- 2) Gender vs disease.
DROP VIEW IF EXISTS vw_gender_vs_disease;
CREATE VIEW vw_gender_vs_disease AS
SELECT
    sex,
    COUNT(*) AS patients,
    SUM(target) AS disease_cases,
    ROUND(AVG(target) * 100, 2) AS disease_rate_pct
FROM vw_heart_disease_enriched
GROUP BY sex;

-- 3) Cholesterol distribution helper.
DROP VIEW IF EXISTS vw_cholesterol_distribution;
CREATE VIEW vw_cholesterol_distribution AS
SELECT
    FLOOR(chol / 10) * 10 AS chol_bin,
    COUNT(*) AS patient_count
FROM vw_heart_disease_enriched
GROUP BY FLOOR(chol / 10) * 10
ORDER BY chol_bin;

-- 4) BP vs cholesterol scatter helper.
DROP VIEW IF EXISTS vw_bp_vs_chol;
CREATE VIEW vw_bp_vs_chol AS
SELECT
    id,
    trestbps,
    chol,
    risk_category,
    target,
    sex,
    age_group
FROM vw_heart_disease_enriched;

-- 5) Heart rate vs disease.
DROP VIEW IF EXISTS vw_heartrate_vs_disease;
CREATE VIEW vw_heartrate_vs_disease AS
SELECT
    FLOOR(thalach / 10) * 10 AS thalach_bin,
    COUNT(*) AS patients,
    ROUND(AVG(target) * 100, 2) AS disease_rate_pct
FROM vw_heart_disease_enriched
GROUP BY FLOOR(thalach / 10) * 10
ORDER BY thalach_bin;

-- 6) Lifestyle risk heatmap.
DROP VIEW IF EXISTS vw_lifestyle_heatmap;
CREATE VIEW vw_lifestyle_heatmap AS
SELECT
    smoking,
    physical_activity,
    COUNT(*) AS patients,
    SUM(target) AS disease_cases,
    ROUND(AVG(target) * 100, 2) AS disease_rate_pct
FROM vw_heart_disease_enriched
GROUP BY smoking, physical_activity;

-- 7) Age-group risk comparison.
DROP VIEW IF EXISTS vw_agegroup_risk;
CREATE VIEW vw_agegroup_risk AS
SELECT
    age_group,
    COUNT(*) AS patients,
    SUM(target) AS disease_cases,
    ROUND(AVG(target) * 100, 2) AS disease_rate_pct
FROM vw_heart_disease_enriched
GROUP BY age_group;

-- 8) High-risk patient distribution.
DROP VIEW IF EXISTS vw_high_risk_distribution;
CREATE VIEW vw_high_risk_distribution AS
SELECT
    age_group,
    sex,
    COUNT(*) AS high_risk_patients,
    ROUND(AVG(chol), 2) AS avg_chol,
    ROUND(AVG(trestbps), 2) AS avg_bp
FROM vw_heart_disease_enriched
WHERE risk_category = 'High'
GROUP BY age_group, sex;
