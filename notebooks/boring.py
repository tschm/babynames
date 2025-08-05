# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "polars==1.30.0",
#     "numpy==2.2.3",
#     "plotly==6.1.2",
#     "scipy==1.15.3",
# ]
# ///
"""Module for analyzing the 'boringness' of baby names using entropy and norm metrics."""

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import polars as pl
    import scipy.stats as st

    path = mo.notebook_location()

    g = pl.read_csv(str(path / "public" / "girls.csv"))
    b = pl.read_csv(str(path / "public" / "boys.csv"))


@app.cell
def _() -> None:
    mo.md(
        r"""
    ## Definition:
    ### A name is boring if it's associated discrete distribution is close to a uniform distribution.

    ### The Shannon-entropy $\sum p_i \times \log p_i$ is maximal for the uniform distribution.

    ### The Euclidean norm $\sqrt{\sum p_i^2}$ is minimal for the uniform distribution.
    """
    )


@app.function
def entropy(ts: pl.Series, base: float | None = None) -> float:
    """Calculate the Shannon entropy of a name's distribution.

    Args:
        ts: Time series data for a name
        base: The logarithm base to use for the calculation

    Returns:
        The Shannon entropy value
    """
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return st.entropy(ts_normalized, base=base)


@app.function
def norm(ts: pl.Series) -> float:
    """Calculate the Euclidean norm of a name's distribution.

    Args:
        ts: Time series data for a name

    Returns:
        The Euclidean norm value
    """
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return np.linalg.norm(ts_normalized, 2)


@app.function
def calculate_entropy(frame: pl.DataFrame) -> pl.DataFrame:
    """Calculate entropy for all names in the dataset.

    Args:
        frame: DataFrame containing name data

    Returns:
        DataFrame with name columns and their entropy values, sorted by entropy
    """
    _d = {col: entropy(frame[col]) for col in frame.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_entropy = pl.DataFrame({"column": list(_sorted_d.keys()), "entropy": list(_sorted_d.values())})

    return _df_entropy


@app.cell
def _() -> None:
    _df_entropy_girls = calculate_entropy(g)
    _df_entropy_boys = calculate_entropy(b)
    print(_df_entropy_girls)
    print(_df_entropy_boys)


@app.function
def calculate_norm(frame: pl.DataFrame) -> pl.DataFrame:
    """Calculate norm for all names in the dataset.

    Args:
        frame: DataFrame containing name data

    Returns:
        DataFrame with name columns and their norm values, sorted by norm
    """
    _d = {col: norm(frame[col]) for col in frame.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_norm = pl.DataFrame({"column": list(_sorted_d.keys()), "norm": list(_sorted_d.values())})

    return _df_norm


@app.cell
def _() -> None:
    _df_norm_girls = calculate_norm(g)
    _df_norm_boys = calculate_norm(b)
    print(_df_norm_girls)
    print(_df_norm_boys)


@app.cell
def _() -> None:
    # Extract year and name data, drop nulls
    boys_thomas = b.select(["year", "Thomas"]).drop_nulls()
    girls_charlotte = g.select(["year", "Charlotte"]).drop_nulls()

    print(boys_thomas)
    print(girls_charlotte)

    # Rename columns to a common structure
    boys_thomas = boys_thomas.rename({"Thomas": "Boy"})
    girls_charlotte = girls_charlotte.rename({"Charlotte": "Girl"})

    # Outer join from both sides to ensure all years included

    # Outer join from both sides to ensure all years included
    all_years = pl.concat([boys_thomas.select("year"), girls_charlotte.select("year")]).unique().sort("year")

    print(all_years)

    # Left-join each side onto the full year range, then combine
    boys_filled = all_years.join(boys_thomas, on="year", how="left")
    girls_filled = all_years.join(girls_charlotte, on="year", how="left")

    print(boys_filled)
    print(girls_filled)

    # Merge both into one DataFrame and fill nulls with 0
    pair = boys_filled.join(girls_filled, on="year", how="full").fill_null(0).sort("year")

    print(pair)

    # Create a line chart with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pair["year"], y=pair["Boy"], mode="lines", name="Thomas"))
    fig.add_trace(go.Scatter(x=pair["year"], y=pair["Girl"], mode="lines", name="Charlotte"))

    fig.update_layout(title="Name Popularity Over Time", xaxis_title="Year", yaxis_title="Count")

    fig


if __name__ == "__main__":
    app.run()
