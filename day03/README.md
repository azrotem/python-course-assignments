# Day 03 Assignment: Protein Concentration Calculator

## Description
This project automates the calculation of protein concentrations using the Beer-Lambert law. It features a Python script that reads experimental data (OD280 and extinction coefficients) from a structured CSV file using the `pandas` library. The script calculates the concentration for a batch of proteins simultaneously, handling error validation, and outputs the final results in both mol/L and µmol/L. 

The code was developed and refined using GitHub Copilot within Visual Studio Code.

## Files Included
* `protein_concentration.py`: The main Python script that processes the data and performs the batch calculations.
* `test_proteins.csv`: A mock dataset containing four proteins (BSA, IgG, Lysozyme, Mucin) with their respective OD280 and extinction coefficient values.

## Copilot Prompts
To generate and refine this code, the following prompts were used in the GitHub Copilot chat:

1. *"I want to write a code that can measure protein concentration based on OD at 280 and extintion coefficient. I want you to create a new file under day03 folder"*
2. *"I want you to change the code so I will upload a file with a table of protein name, OD at 280 and extintion coefficient and it can read the table and write me the concentration of a specific protein I ask"*
3. *"Can you change the code so it will use file test_proteins.csv? I also want it to reply with a table with the concentrations of all the proteins in the fike"*