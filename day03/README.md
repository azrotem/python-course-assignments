# Day 03 Assignment: Protein Concentration Calculators

## Description
For this assignment, I initially developed a basic script to calculate protein concentrations using the Beer-Lambert law. To make the project more specific to my structural biology research, I then created an advanced tool tailored to my daily lab work with modular mucin PTS constructs. The final script reads a uniquely formatted CSV containing two separate tables (a construct list and a scaffold dictionary), merges the data, performs biophysical math, and exports a clean summary. Both scripts were developed and refined using GitHub Copilot.

## Files Included

**1. The Basic Calculator**
- `protein_concentration.py`: Processes batch OD280 data from a standard CSV and outputs molarity.
- `test_proteins.csv`: Mock dataset containing proteins like BSA and IgG.

**2. The Advanced PTS Tool**
- `PTS_constructs_concentration.py`: Parses a CSV containing two blank-row-separated tables. It maps a `scaffold_name` to its full sequence, dynamically inserts the `PTS sequence` into a `-[PTS]-` placeholder, uses `Biopython` to calculate exact molecular weights and extinction coefficients, and computes final concentrations (µM and mg/mL).
- `PTS_proteins.csv`: The input dataset containing the constructs table and the scaffold dictionary.
- *Output:* Generates a clean `PTS_proteins_concentrations.csv` file without cluttering it with the massive scaffold sequences.

## Copilot Prompts

**Initial Basic Code:**
1. *"I want to write a code that can measure protein concentration based on OD at 280 and extintion coefficient. I want you to create a new file under day03 folder"*
2. *"I want you to change the code so I will upload a file with a table of protein name, OD at 280 and extintion coefficient and it can read the table and write me the concentration of a specific protein I ask"*
3. *"Can you change the code so it will use file test_proteins.csv? I also want it to reply with a table with the concentrations of all the proteins in the fike"*

**Advanced PTS Code & File Formatting:**
4. *"Create a new Python file named PTS_constructs_concentration.py. Write a script using pandas and Biopython that reads PTS_proteins.csv. For each row, replace '-[PTS]-' in the scaffold with the PTS sequence. Calculate the extinction coefficient, molecular weight (Da), and concentration in µM and mg/mL, then save to a new CSV."*
5. *"Update my PTS_constructs_concentration.py script to handle a new layout inside my existing `PTS_proteins.csv` file. The CSV now contains two tables separated by an empty row... Please write a robust parsing function that reads this single CSV file, splits it into two separate pandas DataFrames... and merges them based on the 'scaffold_name' column."*
6. *"Update the calculate_table function. Before returning the final concatenated DataFrame, please drop the 'scaffold_sequence' column so it does not appear in the exported CSV file."*

## Usage
To run the advanced PTS calculator from the repository folder, use:
```powershell
python .\day03\PTS_constructs_concentration.py