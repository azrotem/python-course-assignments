"""Calculate sequence parameters and concentrations for PTS constructs."""

import csv
import math
from pathlib import Path

import pandas as pd
from Bio.SeqUtils import molecular_weight


INPUT_FILE = Path(__file__).with_name("PTS_proteins.csv")
OUTPUT_FILE = Path(__file__).with_name("PTS_proteins_concentrations.csv")
PLACEHOLDER = "-[PTS]-"
PATH_LENGTH_CM = 1.0
CONSTRUCT_COLUMNS = {"protein name", "scaffold_name", "PTS sequence", "OD280"}
SCAFFOLD_COLUMNS = {"scaffold_name", "scaffold_sequence"}


def calculate_construct(
    scaffold: str, pts_sequence: str, absorbance: float
) -> dict:
    """Build a construct sequence and calculate its parameters and concentration."""
    if not pts_sequence:
        raise ValueError("PTS sequence is empty.")
    placeholder_count = scaffold.count(PLACEHOLDER)
    if placeholder_count != 1:
        raise ValueError(
            f"scaffold must contain exactly one {PLACEHOLDER!r} placeholder "
            f"(found {placeholder_count})."
        )

    full_sequence = scaffold.replace(PLACEHOLDER, pts_sequence).upper()
    if not full_sequence:
        raise ValueError("The constructed protein sequence is empty.")

    try:
        molecular_weight_da = molecular_weight(
            full_sequence, seq_type="protein", monoisotopic=True
        )
    except (ValueError, KeyError) as error:
        raise ValueError(f"invalid protein sequence: {error}") from error

    extinction_coefficient = (
        full_sequence.count("W") * 5500
        + full_sequence.count("Y") * 1490
        + full_sequence.count("C") * 125
    )
    if extinction_coefficient <= 0:
        raise ValueError(
            "sequence has a zero extinction coefficient; concentration "
            "cannot be calculated."
        )

    molar_concentration = absorbance / (
        extinction_coefficient * PATH_LENGTH_CM
    )
    return {
        "Full Sequence": full_sequence,
        "Extinction Coefficient": extinction_coefficient,
        "MW (Da)": round(molecular_weight_da, 2),
        "Concentration (µM)": round(molar_concentration * 1_000_000, 2),
        "Concentration (mg/mL)": round(
            molar_concentration * molecular_weight_da, 2
        ),
    }


def _is_empty_csv_row(row: list[str]) -> bool:
    return not row or all(not cell.strip() for cell in row)


def parse_input_tables(input_file: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a blank-row-separated CSV into construct and scaffold tables."""
    sections: list[list[list[str]]] = []
    current_section: list[list[str]] = []

    try:
        with input_file.open(encoding="utf-8-sig", newline="") as csv_file:
            for row in csv.reader(csv_file):
                if _is_empty_csv_row(row):
                    if current_section:
                        sections.append(current_section)
                        current_section = []
                else:
                    current_section.append(row)
    except csv.Error as error:
        raise ValueError(f"Could not parse CSV: {error}") from error

    if current_section:
        sections.append(current_section)
    if len(sections) != 2:
        raise ValueError(
            "CSV must contain exactly two non-empty tables separated by a blank row."
        )

    dataframes = []
    for section, required_columns, label in (
        (sections[0], CONSTRUCT_COLUMNS, "constructs"),
        (sections[1], SCAFFOLD_COLUMNS, "scaffolds"),
    ):
        header = [column.strip() for column in section[0]]
        if len(header) != len(set(header)):
            raise ValueError(f"The {label} table contains duplicate column names.")
        for row_number, row in enumerate(section[1:], start=2):
            if len(row) != len(header):
                raise ValueError(
                    f"Malformed {label} row {row_number}: expected "
                    f"{len(header)} columns, found {len(row)}."
                )
        table = pd.DataFrame(section[1:], columns=header)
        missing_columns = required_columns - set(table.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"The {label} table is missing column(s): {missing}")
        if table.empty:
            raise ValueError(f"The {label} table contains no data rows.")
        dataframes.append(table)

    constructs, scaffolds = dataframes
    constructs["scaffold_name"] = (
        constructs["scaffold_name"].fillna("").astype(str).str.strip()
    )
    scaffolds["scaffold_name"] = (
        scaffolds["scaffold_name"].fillna("").astype(str).str.strip()
    )
    if constructs["scaffold_name"].eq("").any():
        raise ValueError("The constructs table contains an empty scaffold_name.")
    if scaffolds["scaffold_name"].eq("").any():
        raise ValueError("The scaffolds table contains an empty scaffold_name.")
    if scaffolds["scaffold_name"].duplicated().any():
        duplicate_names = scaffolds.loc[
            scaffolds["scaffold_name"].duplicated(keep=False), "scaffold_name"
        ].unique()
        raise ValueError(
            "The scaffolds table contains duplicate scaffold_name values: "
            + ", ".join(duplicate_names)
        )
    return constructs, scaffolds


def calculate_table(input_file: Path) -> pd.DataFrame:
    """Merge construct/scaffold tables and append calculated parameters."""
    constructs, scaffolds = parse_input_tables(input_file)
    table = constructs.merge(
        scaffolds,
        on="scaffold_name",
        how="left",
        validate="many_to_one",
        indicator=True,
    )
    missing_scaffolds = table.loc[
        table["_merge"] == "left_only", "scaffold_name"
    ].unique()
    if len(missing_scaffolds):
        raise ValueError(
            "No scaffold sequence found for: " + ", ".join(missing_scaffolds)
        )
    table = table.drop(columns="_merge")
    if table["scaffold_sequence"].isna().any():
        raise ValueError("The scaffolds table contains an empty scaffold_sequence.")

    results = []
    for row_number, (_, row) in enumerate(table.iterrows(), start=2):
        protein_name = str(row["protein name"]).strip()
        try:
            if pd.isna(row["protein name"]) or not protein_name:
                raise ValueError("protein name is empty.")

            scaffold = row["scaffold_sequence"]
            pts_sequence = row["PTS sequence"]
            if pd.isna(scaffold) or pd.isna(pts_sequence):
                raise ValueError(
                    "scaffold sequence and PTS sequence must not be empty."
                )
            scaffold = "".join(str(scaffold).split()).upper()
            pts_sequence = "".join(str(pts_sequence).split()).upper()

            absorbance = float(row["OD280"])
            if not math.isfinite(absorbance) or absorbance < 0:
                raise ValueError("OD280 must be a finite, non-negative number.")

            results.append(
                calculate_construct(scaffold, pts_sequence, absorbance)
            )
        except (TypeError, ValueError) as error:
            name = protein_name or "<unnamed protein>"
            raise ValueError(
                f"Invalid data for {name!r} near constructs row "
                f"{row_number}: {error}"
            ) from error

    calculated = pd.DataFrame(results, index=table.index)
    result = pd.concat([table, calculated], axis=1)
    return result.drop(columns=["scaffold_sequence", "Full Sequence"])


def main() -> None:
    try:
        result = calculate_table(INPUT_FILE)
        result.to_csv(OUTPUT_FILE, index=False)
    except FileNotFoundError as error:
        print(f"Error: input file not found: {INPUT_FILE}")
        raise SystemExit(1) from error
    except (OSError, pd.errors.ParserError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error

    print(f"Calculated concentrations for {len(result)} constructs.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

print("Done!")