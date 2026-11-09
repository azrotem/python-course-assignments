"""Flask interface for calculating PTS construct concentrations."""

import tempfile
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request

from PTS_constructs_concentration import calculate_table


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.get("/")
def homepage():
    return render_template("index.html")


@app.post("/upload")
def upload():
    uploaded_file = request.files.get("file")
    if uploaded_file is None or not uploaded_file.filename:
        return render_template(
            "index.html", error="Please choose a CSV file to upload."
        ), 400
    if Path(uploaded_file.filename).suffix.casefold() != ".csv":
        return render_template(
            "index.html", error="The uploaded file must be a CSV."
        ), 400

    try:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_file = Path(temporary_directory) / "upload.csv"
            uploaded_file.save(temporary_file)
            result = calculate_table(temporary_file)
            table_html = result.to_html(index=False, classes="results-table")
    except (OSError, UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
        return render_template("index.html", error=str(error)), 400

    return render_template("results.html", table=table_html)


if __name__ == "__main__":
    app.run(debug=True)
