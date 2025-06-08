# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "numpy==2.2.5",
#     "plotly==6.1.1",
#     "polars==1.29.0",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import polars as pl
    from reader import boys, girls

    g = girls()
    b = boys()

@app.cell
def _():
    import marimo as mo

    # Polars doesn't have the same display options as pandas
    # We'll use the default display settings
    return mo



@app.cell
def _(mo):
    mo.md(
        r"""
    ## Each name can be projected to the unit-sphere

    ## We compute the Bhattacharyya angle (correlation)
    """
    )
    return


@app.function
def match(body1, body2):
    # Polars equivalent of Series and DataFrame operations
    # Convert to DataFrame if it's a Series
    merged = body1.join(body2, on="year", how="left")

    # Identify all value columns (exclude 'year')
    value_cols = [col for col in merged.columns if col != "year"]

    # Normalize each value column (e.g., L1 normalization to unit simplex)
    merged = merged.with_columns([
        (pl.col(col).fill_null(0) / (pl.col(col).fill_null(0) ** 2).sum().sqrt()).alias(col) for col in value_cols
    ])

    # Apply proj_sphere to each column
    x_cols = [col for col in body1.columns if col != "year"]
    y_cols = [col for col in body2.columns if col != "year"]

    # Create a result DataFrame with all combinations of x and y columns
    # result_data = []

    a = merged.select(x_cols).fill_null(0).to_numpy().transpose()
    b = merged.select(y_cols).fill_null(0).to_numpy()

    scores = (a @ b)

    # Create result as list of dicts
    result_data = [
        {"Name A": x, "Name B": y, "value": scores[i, j]}
        for i, x in enumerate(x_cols)
        for j, y in enumerate(y_cols)
        if x != y
    ]

    return pl.DataFrame(result_data).sort("value", descending=True)



@app.cell
def _():
    match(b.select(["year", "Thomas"]).drop_nulls(), g)
    return


@app.cell
def _():
    match(b.select(["year", "Urs"]).drop_nulls(), b)
    return


@app.cell
def _():
    match(b, g)
    return


@app.cell
def _():
    # Polars equivalent of reset_index, groupby, and mean
    result = match(b, g)

    # Group by Name A and calculate mean of value
    grouped_result = result.group_by("Name A").agg(pl.mean("value")).sort("value")

    print(grouped_result)
    return


if __name__ == "__main__":
    app.run()
