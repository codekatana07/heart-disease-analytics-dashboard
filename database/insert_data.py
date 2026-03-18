"""Insert normalized heart disease CSV data into MySQL.

Usage (PowerShell):
  python database/insert_data.py --csv data/heart_disease.csv

MySQL connection defaults can be overridden via env vars:
  MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Dict

import mysql.connector
from mysql.connector import Error

INSERT_SQL = """
INSERT INTO heart_disease (
    age, sex, cp, trestbps, chol, fbs, thalach, exang, oldpeak,
    target, smoking, physical_activity, bmi, age_category
) VALUES (
    %(age)s, %(sex)s, %(cp)s, %(trestbps)s, %(chol)s, %(fbs)s, %(thalach)s, %(exang)s, %(oldpeak)s,
    %(target)s, %(smoking)s, %(physical_activity)s, %(bmi)s, %(age_category)s
)
"""


def to_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_record(row: Dict[str, str]) -> Dict[str, object]:
    return {
        "age": to_int(row.get("age")),
        "sex": "M" if str(row.get("sex", "F")).strip().upper().startswith("M") else "F",
        "cp": to_int(row.get("cp")),
        "trestbps": to_int(row.get("trestbps")),
        "chol": to_int(row.get("chol")),
        "fbs": to_int(row.get("fbs")),
        "thalach": to_int(row.get("thalach")),
        "exang": to_int(row.get("exang")),
        "oldpeak": to_float(row.get("oldpeak")),
        "target": to_int(row.get("target")),
        "smoking": to_int(row.get("smoking"), 0),
        "physical_activity": to_int(row.get("physical_activity"), 1),
        "bmi": to_float(row.get("bmi"), 0.0),
        "age_category": str(row.get("age_category", "Unknown"))[:20],
    }


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "heart_disease_dashboard"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Insert normalized heart disease CSV into MySQL")
    parser.add_argument("--csv", default="data/heart_disease.csv", help="Path to normalized CSV")
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate heart_disease table before insert",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    connection = None
    inserted = 0

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if args.truncate:
            cursor.execute("TRUNCATE TABLE heart_disease")

        with csv_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(INSERT_SQL, normalize_record(row))
                inserted += 1

        connection.commit()
        print(f"Inserted {inserted} rows into heart_disease_dashboard.heart_disease")

    except Error as exc:
        if connection:
            connection.rollback()
        raise RuntimeError(f"MySQL insert failed: {exc}") from exc

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()
