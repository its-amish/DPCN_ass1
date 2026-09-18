"""Shared cleaning and encoding for the opinion survey.

Usage:
    from clean import load_survey
    responses, statements, log = load_survey()

`responses` is a DataFrame indexed by student ID with one column per statement
(T01..V15), holding integers in -2..+2 (NaN where the student gave no usable
answer). `statements` maps each code to its full statement text.
"""

from pathlib import Path

import numpy as np
import pandas as pd

CSV_PATH = Path(__file__).parent / "Survey_Results_UC.csv"
ID_COL = "id. Response ID"

# Centred Likert encoding: sign = polarity, absolute value = strength.
# Add 3 to get the conventional 1..5 scale.
LIKERT = {
    "Strongly Disagree": -2,
    "Disagree": -1,
    "Neutral": 0,
    "Agree": 1,
    "Strongly Agree": 2,
}

SECTIONS = {
    "T": "Technology",
    "E": "Education",
    "S": "Society & Ethics",
    "V": "Environment",
}


def load_survey(path=CSV_PATH, verbose=False):
    # utf-8-sig strips the byte-order mark at the start of the file
    raw = pd.read_csv(path, encoding="utf-8-sig", dtype=str, keep_default_na=False)

    raw[ID_COL] = raw[ID_COL].str.strip()
    raw = raw.set_index(ID_COL)
    raw.index.name = "student"

    # "T01. Artificial Intelligence will ..." -> code "T01", statement text
    statements = {}
    for col in raw.columns:
        code, text = col.split(".", 1)
        statements[code.strip()] = text.strip()
    raw.columns = list(statements)

    raw_counts = pd.Series(raw.values.ravel()).replace("", "<blank>").value_counts()

    # Blank and "No Comments" (or anything else unexpected) become NaN
    responses = raw.apply(lambda col: col.str.strip().map(LIKERT)).astype(float)

    n_missing = responses.isna().sum(axis=1)
    empty = n_missing[n_missing == responses.shape[1]].index.tolist()
    responses = responses.drop(index=empty)

    log = {
        "n_raw_students": len(raw),
        "n_statements": raw.shape[1],
        "raw_answer_counts": raw_counts.to_dict(),
        "dropped_empty_students": empty,
        "n_students": len(responses),
        "missing_per_student": n_missing.drop(index=empty)[lambda s: s > 0]
        .sort_values(ascending=False)
        .to_dict(),
        "n_missing_cells": int(responses.isna().sum().sum()),
    }

    if verbose:
        print(f"Raw: {log['n_raw_students']} students x {log['n_statements']} statements")
        print("Raw answer counts:", log["raw_answer_counts"])
        print(f"Dropped {len(empty)} completely empty responses: {empty}")
        print(f"Kept {log['n_students']} students, {log['n_missing_cells']} missing answers remain")
        print("Students with missing answers:", log["missing_per_student"])

    return responses, statements, log


def section_of(code):
    return code[0]


if __name__ == "__main__":
    responses, statements, log = load_survey(verbose=True)
    out = Path(__file__).parent / "survey_clean.csv"
    responses.astype("Int64").to_csv(out)
    print(f"Wrote {out}")
