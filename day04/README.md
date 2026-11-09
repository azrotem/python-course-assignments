# Day 04: PTS Construct Concentration Calculator (Web)

## Overview
This project converts the structural biology business logic from Day 3 into an interactive local web application using Flask. It calculates biophysical parameters (average molecular weight and extinction coefficients) and final molar concentrations for PTS protein constructs using the Beer-Lambert law.

## Architecture
* **`app.py`**: The Flask web server that handles file uploads, routing, and HTML rendering.
* **`PTS_constructs_concentration.py`**: The core computational engine. It relies on `pandas` for relational data merging and `Biopython` for molecular weight calculations.
* **`templates/`**: Contains `index.html` (the upload interface) and `results.html` (the dynamically generated data table).

## Requirements
This application requires Python along with the following libraries:
* Flask
* pandas
* biopython

## How to Run the Application
1. Open a terminal in the `day04` directory.
2. Start the local Flask server by running:
   ```bash
   python app.py