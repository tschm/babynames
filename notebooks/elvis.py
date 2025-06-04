import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# The Elvis effect""")
    return


@app.cell
def _(mo, pl):
    # Read CSV with polars
    # Polars handles multi-index differently than pandas
    # We'll read the CSV and then set up the data for filtering
    _us_path = str(mo.notebook_location() / "public" / "us.csv")

    # Read the CSV file
    df = pl.read_csv(_us_path)

    # Create a LazyFrame to allow for more complex operations
    _names = df.lazy()

    # Display the data
    print(_names.collect().head())

    return (df,)


@app.cell
def _(df, go, pl):
    # Filter for Elvis and Male gender
    _f = df.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "M"))

    # Sort by year for plotting
    _f = _f.sort("year")

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f["year"], y=_f["n"], mode="lines"))
    _fig.update_layout(
        title="# Boys named Elvis",
        xaxis_title="Year",
        yaxis_title="Count")
    _fig.show()

    # Show top 10 years
    print("Top 10 years for Elvis:")
    print(_f.sort("n", descending=True).head(10))

    return


@app.cell
def _(df, go, pl):
    # Filter for Elvis and Female gender
    _f_1 = df.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    _f_1 = _f_1.sort("year")

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f_1["year"], y=_f_1["n"], mode="lines"))
    _fig.update_layout(
        title="# Girls named Elvis",
        xaxis_title="Year",
        yaxis_title="Count"
    )
    _fig.show()

    return


@app.cell
def _(df, go, pl):
    # Filter for Nikita and Female gender
    _f_2 = df.filter((pl.col("Name") == "Nikita") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    _f_2 = _f_2.sort("year")

    # Polars doesn't have a built-in plot method, so we'll use plotly
    # import plotly.graph_objects as go

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f_2["year"], y=_f_2["n"], mode="lines"))
    _fig.update_layout(
        title="# Girls named Nikita",
        xaxis_title="Year",
        yaxis_title="Count"
    )
    _fig.show()

    return


@app.cell
def _(df, pl):
    # Group by Name and Gender and sum the counts
    _a = df.group_by(["Name", "Gender"]).agg(pl.sum("n").alias("total"))

    # Sort by total count
    _a = _a.sort("total")

    # Display the results
    print("Names sorted by total count:")
    print(_a.head(20))

    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.graph_objects as go
    return go, mo, pl


if __name__ == "__main__":
    app.run()
