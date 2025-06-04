import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import polars as pl
    import numpy as np
    import plotly.graph_objects as go
    return go, np, pl


@app.cell
def _(mo, pl):
    print(mo.notebook_location())
    # In polars, we read the CSV and then set the first column as index
    boys_path = str(mo.notebook_location() / "public" / "boys.csv")
    girls_path = str(mo.notebook_location() / "public" / "girls.csv")

    # Read CSVs with polars
    boys = pl.read_csv(boys_path)
    girls = pl.read_csv(girls_path)

    # Convert first column to index (polars doesn't have index like pandas)
    # We'll keep the original structure for compatibility with the rest of the code
    return boys, girls


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Definition:
    ### A name is boring if it's associated discrete distribution is close to a uniform distribution.

    ### The Shannon-entropy $\sum p_i \times \log p_i$ is maximal for the uniform distribution. Dangerous! (Kullback-Leibler)

    ### The Euclidean norm $\sqrt{\sum p_i^2}$ is is minimal for the uniform distribution.
    """
    )
    return


@app.cell
def _(np):
    from scipy.stats import entropy as e

    def entropy(ts, base=None):
        # Polars equivalent of dropna and sum
        ts_filtered = ts.drop_nulls().to_numpy()
        ts_normalized = ts_filtered / ts_filtered.sum()
        return e(ts_normalized, base=base)

    def norm(ts):
        # Polars equivalent of dropna and sum
        ts_filtered = ts.drop_nulls().to_numpy()
        ts_normalized = ts_filtered / ts_filtered.sum()
        return np.linalg.norm(ts_normalized, 2)

    return entropy, norm


@app.cell
def _(entropy, girls, pl):
    _d = {col: entropy(girls[col]) for col in girls.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_entropy = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "entropy": list(_sorted_d.values())
    })

    print(_df_entropy)
    return


@app.cell
def _(girls, norm, pl):
    _d = {col: norm(girls[col]) for col in girls.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_norm = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "norm": list(_sorted_d.values())
    })

    print(_df_norm)
    return


@app.cell
def _(boys, entropy, pl):
    _d = {col: entropy(boys[col]) for col in boys.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_entropy = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "entropy": list(_sorted_d.values())
    })

    print(_df_entropy)
    return


@app.cell
def _(boys, norm, pl):
    _d = {col: norm(boys[col]) for col in boys.columns if col != "year"}

    _sorted_d = dict(sorted(_d.items(), key=lambda item: item[1], reverse=True))

    # Convert to Polars DataFrame
    _df_norm = pl.DataFrame({
        "column": list(_sorted_d.keys()),
        "norm": list(_sorted_d.values())
    })

    print(_df_norm)
    return


@app.cell
def _(boys, girls, go, pl):
    # Extract year and name data, drop nulls
    boys_thomas = boys.select(["year", "Thomas"]).drop_nulls()
    girls_charlotte = girls.select(["year", "Charlotte"]).drop_nulls()

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


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
