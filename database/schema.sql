-- Create database and analytics table for heart disease data.
CREATE DATABASE IF NOT EXISTS heart_disease_dashboard;
USE heart_disease_dashboard;

DROP TABLE IF EXISTS heart_disease;

CREATE TABLE heart_disease (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    sex ENUM('M', 'F') NOT NULL,
    cp TINYINT NOT NULL,
    trestbps INT NOT NULL,
    chol INT NOT NULL,
    fbs TINYINT NOT NULL,
    thalach INT NOT NULL,
    exang TINYINT NOT NULL,
    oldpeak DECIMAL(4,2) NOT NULL,
    target TINYINT NOT NULL,
    smoking TINYINT NOT NULL DEFAULT 0,
    physical_activity TINYINT NOT NULL DEFAULT 1,
    bmi DECIMAL(5,2) NOT NULL DEFAULT 0,
    age_category VARCHAR(20) DEFAULT 'Unknown',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_age (age),
    INDEX idx_sex (sex),
    INDEX idx_target (target),
    INDEX idx_risk (chol, trestbps)
);
