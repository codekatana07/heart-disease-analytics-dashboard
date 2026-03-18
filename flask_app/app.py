"""Flask app that hosts an embedded Tableau dashboard."""

from __future__ import annotations

import os

from flask import Flask, render_template

app = Flask(__name__)


def _normalize_tableau_url(url: str) -> str:
    """Convert Tableau public profile share links to embeddable /views links."""
    clean = (url or "").strip()
    if "/app/profile/" in clean and "/viz/" in clean:
        tail = clean.split("/viz/", 1)[1].split("#", 1)[0]
        return f"https://public.tableau.com/views/{tail}?:showVizHome=no"
    if "?:showVizHome=no" not in clean:
        if "?" in clean:
            return f"{clean}&:showVizHome=no"
        return f"{clean}?:showVizHome=no"
    return clean


@app.route("/")
def index():
    # Replace with your Tableau Public or Tableau Server share URL.
    raw_url = os.getenv(
        "TABLEAU_DASHBOARD_URL",
        "https://public.tableau.com/views/HeartDiseasePrediction_17730017390650/HeartDiseaseDataAnalysisKeyInsights?:showVizHome=no",
    )
    tableau_url = _normalize_tableau_url(raw_url)
    return render_template("dashboard.html", tableau_url=tableau_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
