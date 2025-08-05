# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "polars==1.30.0",
#     "numpy==2.2.3",
#     "plotly==6.1.2"
# ]
# ///
"""Module for analyzing geometric relationships between baby names using vector projections."""

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import numpy as np
    import polars as pl

    path = mo.notebook_location()

    g = pl.read_csv(str(path / "public" / "girls.csv"))
    b = pl.read_csv(str(path / "public" / "boys.csv"))


@app.cell
def _() -> None:
    mo.md(
        r"""
    ## Each name can be projected to the unit-sphere

    ## We compute the Bhattacharyya angle (correlation)
    """
    )


@app.function
def match(body1: pl.DataFrame, body2: pl.DataFrame) -> pl.DataFrame:
    """Match names between two datasets based on their geometric similarity.

    Args:
        body1: First DataFrame containing name data
        body2: Second DataFrame containing name data

    Returns:
        DataFrame with pairs of names and their similarity scores, sorted by score
    """
    # Polars equivalent of Series and DataFrame operations
    # Convert to DataFrame if it's a Series
    merged = body1.join(body2, on="year", how="left")

    # Identify all value columns (exclude 'year')
    value_cols = [col for col in merged.columns if col != "year"]

    # Normalize each value column (e.g., L1 normalization to unit simplex)
    merged = merged.with_columns(
        [(pl.col(col).fill_null(0) / (pl.col(col).fill_null(0) ** 2).sum().sqrt()).alias(col) for col in value_cols]
    )

    # Apply proj_sphere to each column
    x_cols = [col for col in body1.columns if col != "year"]
    y_cols = [col for col in body2.columns if col != "year"]

    a = merged.select(x_cols).fill_null(0).to_numpy()
    b = merged.select(y_cols).fill_null(0).to_numpy()

    scores = np.transpose(a) @ b

    # Create result as list of dicts
    result_data = [
        {"Name A": x, "Name B": y, "value": scores[i, j]}
        for i, x in enumerate(x_cols)
        for j, y in enumerate(y_cols)
        if x != y
    ]

    return pl.DataFrame(result_data).sort("value", descending=True)


@app.cell
def _() -> None:
    match(b.select(["year", "Thomas"]).drop_nulls(), g)
    return


@app.cell
def _() -> None:
    match(b.select(["year", "Urs"]).drop_nulls(), b)


@app.cell
def _() -> None:
    match(b, g)


@app.cell
def _() -> None:
    # Polars equivalent of reset_index, groupby, and mean
    result = match(b, g)

    # Group by Name A and calculate mean of value
    grouped_result = result.group_by("Name A").agg(pl.mean("value")).sort("value")

    print(grouped_result)


if __name__ == "__main__":
    app.run()
