"""Calculate and display concentrations for proteins in test_proteins.csv."""

import math
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).with_name("test_proteins.csv")
PATH_LENGTH_CM = 1.0
REQUIRED_COLUMNS = {"Protein Name", "OD280", "Extinction Coefficient"}


def calculate_concentration(
    absorbance: float, extinction_coefficient: float
) -> float:
    """Return protein concentration in mol/L using a 1 cm path length."""
    if not math.isfinite(absorbance) or absorbance < 0:
        raise ValueError("Absorbance must be a finite, non-negative number.")
    if not math.isfinite(extinction_coefficient) or extinction_coefficient <= 0:
        raise ValueError("Extinction coefficient must be a finite, positive number.")

    return absorbance / (extinction_coefficient * PATH_LENGTH_CM)


def load_protein_table(file_path: Path) -> pd.DataFrame:
    """Load and validate the protein table from a CSV file."""
    table = pd.read_csv(file_path)
    missing_columns = REQUIRED_COLUMNS - set(table.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"The file is missing required column(s): {missing}")

    table["OD280"] = pd.to_numeric(table["OD280"], errors="raise")
    table["Extinction Coefficient"] = pd.to_numeric(
        table["Extinction Coefficient"], errors="raise"
    )
    protein_names = table["Protein Name"].fillna("").astype(str).str.strip()
    if protein_names.eq("").any():
        raise ValueError("The file contains a row with an empty Protein Name.")

    for absorbance, coefficient in zip(
        table["OD280"], table["Extinction Coefficient"]
    ):
        calculate_concentration(absorbance, coefficient)
    return table


def main() -> None:
    table = load_protein_table(DATA_FILE)
    table["Concentration (mol/L)"] = [
        calculate_concentration(absorbance, coefficient)
        for absorbance, coefficient in zip(
            table["OD280"], table["Extinction Coefficient"]
        )
    ]
    table["Concentration (µmol/L)"] = (
        table["Concentration (mol/L)"] * 1_000_000
    )
    print(f"Concentrations from {DATA_FILE.name} (path length: {PATH_LENGTH_CM:g} cm)")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()