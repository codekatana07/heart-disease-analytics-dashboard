"""Prepare heart disease CSV files for downstream MySQL loading.

This script supports two source formats:
1) A classic heart dataset with fields like age, sex, cp, trestbps, chol, ...
2) The provided Heart_new2 format with lifestyle and health indicators.

For Heart_new2, the script creates a normalized analytics dataset with columns
needed for SQL analysis and Tableau visualizations.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable

EXPECTED_OUTPUT_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "thalach",
    "exang",
    "oldpeak",
    "target",
    "smoking",
    "physical_activity",
    "bmi",
    "age_category",
]


def _yes_no_to_int(value: str) -> int:
    return 1 if str(value).strip().lower() == "yes" else 0


def _age_category_to_age(age_category: str) -> int:
    mapping = {
        "18-24": 21,
        "25-29": 27,
        "30-34": 32,
        "35-39": 37,
        "40-44": 42,
        "45-49": 47,
        "50-54": 52,
        "55-59": 57,
        "60-64": 62,
        "65-69": 67,
        "70-74": 72,
        "75-79": 77,
        "80 or older": 82,
    }
    return mapping.get(str(age_category).strip(), 50)


def _gen_health_to_cp(gen_health: str) -> int:
    lookup = {
        "excellent": 0,
        "very good": 0,
        "good": 1,
        "fair": 2,
        "poor": 3,
    }
    return lookup.get(str(gen_health).strip().lower(), 1)


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _normalize_from_heart_new2(row: Dict[str, str]) -> Dict[str, object]:
    age = _age_category_to_age(row.get("AgeCategory", ""))
    bmi = float(row.get("BMI", 0) or 0)
    smoking = _yes_no_to_int(row.get("Smoking", "No"))
    diabetic = _yes_no_to_int(row.get("Diabetic", "No"))
    diff_walking = _yes_no_to_int(row.get("DiffWalking", "No"))
    physical_activity = _yes_no_to_int(row.get("PhysicalActivity", "No"))
    stroke = _yes_no_to_int(row.get("Stroke", "No"))
    heart_disease = _yes_no_to_int(row.get("HeartDisease", "No"))

    physical_health = float(row.get("PhysicalHealth", 0) or 0)
    mental_health = float(row.get("MentalHealth", 0) or 0)

    # Approximate medical indicators from available lifestyle variables.
    trestbps = round(_clamp(110 + (age - 40) * 0.5 + (bmi - 25) * 1.2 + smoking * 8 + diff_walking * 6, 90, 200))
    chol = round(_clamp(150 + bmi * 2 + age * 0.8 + smoking * 20 + diabetic * 15, 120, 400))
    thalach = round(_clamp(210 - age - physical_health * 0.5 - diff_walking * 10, 60, 202))
    oldpeak = round(_clamp(mental_health / 10 + physical_health / 15 + smoking * 0.8, 0, 6), 2)

    sex = "M" if str(row.get("Sex", "")).strip().lower() == "male" else "F"

    return {
        "age": age,
        "sex": sex,
        "cp": _gen_health_to_cp(row.get("GenHealth", "")),
        "trestbps": trestbps,
        "chol": chol,
        "fbs": diabetic,
        "thalach": thalach,
        "exang": 1 if diff_walking or stroke else 0,
        "oldpeak": oldpeak,
        "target": heart_disease,
        "smoking": smoking,
        "physical_activity": physical_activity,
        "bmi": round(bmi, 2),
        "age_category": row.get("AgeCategory", "Unknown"),
    }


def _normalize_from_classic(row: Dict[str, str]) -> Dict[str, object]:
    return {
        "age": int(float(row.get("age", 0) or 0)),
        "sex": "M" if str(row.get("sex", "0")).strip() in {"1", "M", "m"} else "F",
        "cp": int(float(row.get("cp", 0) or 0)),
        "trestbps": int(float(row.get("trestbps", 0) or 0)),
        "chol": int(float(row.get("chol", 0) or 0)),
        "fbs": int(float(row.get("fbs", 0) or 0)),
        "thalach": int(float(row.get("thalach", 0) or 0)),
        "exang": int(float(row.get("exang", 0) or 0)),
        "oldpeak": float(row.get("oldpeak", 0) or 0),
        "target": int(float(row.get("target", 0) or 0)),
        "smoking": 0,
        "physical_activity": 1,
        "bmi": 0.0,
        "age_category": "Unknown",
    }


def normalize_rows(rows: Iterable[Dict[str, str]], source_type: str):
    for row in rows:
        if source_type == "heart_new2":
            yield _normalize_from_heart_new2(row)
        else:
            yield _normalize_from_classic(row)


def detect_source_type(fieldnames: Iterable[str]) -> str:
    names = {name.strip() for name in fieldnames}
    if {"HeartDisease", "BMI", "Smoking", "AgeCategory"}.issubset(names):
        return "heart_new2"
    if {"age", "sex", "cp", "trestbps", "chol", "target"}.issubset(names):
        return "classic"
    raise ValueError("Unsupported CSV format. Provide Heart_new2.csv or classic heart dataset format.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize heart disease dataset for MySQL and Tableau")
    parser.add_argument("--input", required=True, help="Path to source CSV")
    parser.add_argument("--output", required=True, help="Path to normalized CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", newline="", encoding="utf-8") as src:
        reader = csv.DictReader(src)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row")

        source_type = detect_source_type(reader.fieldnames)
        normalized = list(normalize_rows(reader, source_type))

    with output_path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=EXPECTED_OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(normalized)

    print(f"Source format: {source_type}")
    print(f"Rows processed: {len(normalized)}")
    print(f"Normalized file created at: {output_path}")


if __name__ == "__main__":
    main()
