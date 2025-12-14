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
"""Analysis of baby name distributions to identify 'boring' names.

This module analyzes baby name distributions to identify names that have
uniform distributions over time, which are considered 'boring'. It uses
entropy and Euclidean norm calculations to measure the uniformity of name
distributions.
"""

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    from pathlib import Path

    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import polars as pl
    import scipy.stats as st

    path = Path(__file__).parent

    g = pl.read_csv(str(path / "public" / "girls.csv"))
    b = pl.read_csv(str(path / "public" / "boys.csv"))


@app.cell
def _() -> None:
    mo.md(
        r"""
    ## Definition:
    ### a name is boring if it's associated discrete distribution is close to a uniform distribution.

    ### The Shannon-entropy $\sum p_i \times \log p_i$ is maximal for the uniform distribution.
    ### Note: Be careful with Kullback-Leibler divergence!

    ### The Euclidean norm $\sqrt{\sum p_i^2}$ is is minimal for the uniform distribution.
    """
    )
    return


@app.function
def entropy(ts: pl.Series, base: float | None = None) -> float:
    """Calculate the Shannon entropy of a probability distribution.

    The entropy is maximal for a uniform distribution and minimal for a
    distribution where all mass is concentrated at one point.

    Args:
        ts: a polars Series containing the distribution values
        base: The logarithm base to use (default: e)

    Returns:
        The entropy value as a float
    """
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return st.entropy(ts_normalized, base=base)


@app.function
def norm(ts: pl.Series) -> float:
    """Calculate the Euclidean (L2) norm of a probability distribution.

    The Euclidean norm is minimal for a uniform distribution and maximal
    for a distribution where all mass is concentrated at one point.

    Args:
        ts: a polars Series containing the distribution values

    Returns:
        The Euclidean norm as a float
    """
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return np.linalg.norm(ts_normalized, 2)


@app.function
def calculate_entropy(frame: pl.DataFrame) -> pl.DataFrame:
    """Calculate entropy for all name columns in a DataFrame and sort by entropy value.

    This function computes the Shannon entropy for each name column in the input
    DataFrame, sorts the results by entropy value in descending order (most uniform
    distributions first), and returns a new DataFrame with the results.

    Args:
        frame: a polars DataFrame with year and name columns

    Returns:
        a polars DataFrame with columns 'column' (name) and 'entropy' (entropy value),
        sorted by entropy in descending order
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
    return


@app.function
def calculate_norm(frame: pl.DataFrame) -> pl.DataFrame:
    """Calculate Euclidean norm for all name columns in a DataFrame and sort by norm value.

    This function computes the Euclidean (L2) norm for each name column in the input
    DataFrame, sorts the results by norm value in descending order (least uniform
    distributions first), and returns a new DataFrame with the results.

    Args:
        frame: a polars DataFrame with year and name columns

    Returns:
        a polars DataFrame with columns 'column' (name) and 'norm' (norm value),
        sorted by norm in descending order
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
    return


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

    # Outer join on year
    # pair = boys_thomas.join(girls_charlotte, on="year", how="outer")

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
    return


if __name__ == "__main__":
    app.run()
