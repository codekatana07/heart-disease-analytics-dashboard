USE heart_disease_dashboard;

-- 1) Average cholesterol by age
SELECT age, ROUND(AVG(chol), 2) AS avg_cholesterol
FROM heart_disease
GROUP BY age
ORDER BY age;

-- 2) Heart disease count by gender
SELECT sex, COUNT(*) AS disease_count
FROM heart_disease
WHERE target = 1
GROUP BY sex;

-- 3) High risk patients (cholesterol > 240 and BP > 140)
SELECT id, age, sex, chol, trestbps, target
FROM heart_disease
WHERE chol > 240
  AND trestbps > 140
ORDER BY chol DESC, trestbps DESC;

-- Optional: lifestyle risk segmentation used by Tableau heatmaps
SELECT
    smoking,
    physical_activity,
    COUNT(*) AS patients,
    SUM(target) AS disease_cases,
    ROUND(SUM(target) / COUNT(*) * 100, 2) AS disease_rate_pct
FROM heart_disease
GROUP BY smoking, physical_activity;
