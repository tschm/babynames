import marimo
from typing import Optional, Any

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl
    import numpy as np
    import plotly.graph_objects as go
    import scipy.stats as st
    from typing import Optional, Any

    path = mo.notebook_location()

    g = pl.read_csv(str(path / "public" / "girls.csv"))
    b = pl.read_csv(str(path / "public" / "boys.csv"))


@app.cell
def _(mo: Any) -> None:
    mo.md(
        r"""
    ## Definition:
    ### A name is boring if it's associated discrete distribution is close to a uniform distribution.

    ### The Shannon-entropy $\sum p_i \times \log p_i$ is maximal for the uniform distribution. Dangerous! (Kullback-Leibler)

    ### The Euclidean norm $\sqrt{\sum p_i^2}$ is is minimal for the uniform distribution.
    """
    )
    return


@app.function
def entropy(ts: pl.Series, base: Optional[float] = None) -> float:
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return st.entropy(ts_normalized, base=base)


@app.function
def norm(ts: pl.Series) -> float:
    # Polars equivalent of dropna and sum
    ts_filtered = ts.drop_nulls().to_numpy()
    ts_normalized = ts_filtered / ts_filtered.sum()
    return np.linalg.norm(ts_normalized, 2)


@app.function
def calculate_entropy(frame: pl.DataFrame) -> pl.DataFrame:
    _d = {col: entropy(frame[col]) for col in frame.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_entropy = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "entropy": list(_sorted_d.values())
    })

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
    _d = {col: norm(frame[col]) for col in frame.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_norm = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "norm": list(_sorted_d.values())
    })

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
    #pair = boys_thomas.join(girls_charlotte, on="year", how="outer")

    # Outer join from both sides to ensure all years included
    all_years = (
        pl.concat([boys_thomas.select("year"), girls_charlotte.select("year")])
        .unique()
        .sort("year")
    )

    print(all_years)

    # Left-join each side onto the full year range, then combine
    boys_filled = all_years.join(boys_thomas, on="year", how="left")
    girls_filled = all_years.join(girls_charlotte, on="year", how="left")

    print(boys_filled)
    print(girls_filled)

    # Merge both into one DataFrame and fill nulls with 0
    pair = (
        boys_filled.join(girls_filled, on="year", how="full")
        .fill_null(0)
        .sort("year")
    )

    print(pair)

    # Create a line chart with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pair["year"], y=pair["Boy"], mode="lines", name="Thomas"))
    fig.add_trace(go.Scatter(x=pair["year"], y=pair["Girl"], mode="lines", name="Charlotte"))

    fig.update_layout(
        title="Name Popularity Over Time",
        xaxis_title="Year",
        yaxis_title="Count"
    )

    fig
    return


if __name__ == "__main__":
    app.run()
