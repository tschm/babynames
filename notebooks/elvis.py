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
    us_path = str(mo.notebook_location() / "public" / "us.csv")

    # Read the CSV file
    df = pl.read_csv(us_path)

    # Create a LazyFrame to allow for more complex operations
    names = df.lazy()

    # Display the data
    print(names.collect().head())

    return (df, names)


@app.cell
def _(df, pl):
    # Filter for Elvis and Male gender
    f = df.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "M"))

    # Sort by year for plotting
    f = f.sort("year")

    # Polars doesn't have a built-in plot method, so we'll use plotly
    import plotly.graph_objects as go

    # Create a plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f["year"], y=f["n"], mode="lines"))
    fig.update_layout(
        title="# Boys named Elvis",
        xaxis_title="Year",
        yaxis_title="Count",
        width=1000,
        height=600,
    )
    fig.show()

    # Show top 10 years
    print("Top 10 years for Elvis:")
    print(f.sort("n", descending=True).head(10))

    return f


@app.cell
def _(df, pl):
    # Filter for Elvis and Female gender
    f_1 = df.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    f_1 = f_1.sort("year")

    # Polars doesn't have a built-in plot method, so we'll use plotly
    import plotly.graph_objects as go

    # Create a plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f_1["year"], y=f_1["n"], mode="lines"))
    fig.update_layout(
        title="# Girls named Elvis",
        xaxis_title="Year",
        yaxis_title="Count",
        width=1000,
        height=600,
    )
    fig.show()

    return f_1


@app.cell
def _(df, pl, go):
    # Filter for Nikita and Female gender
    f_2 = df.filter((pl.col("Name") == "Nikita") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    f_2 = f_2.sort("year")

    # Polars doesn't have a built-in plot method, so we'll use plotly
    # import plotly.graph_objects as go

    # Create a plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f_2["year"], y=f_2["n"], mode="lines"))
    fig.update_layout(
        title="# Girls named Nikita",
        xaxis_title="Year",
        yaxis_title="Count",
        width=1000,
        height=600,
    )
    fig.show()

    return f_2


@app.cell
def _(df, pl):
    # Group by Name and Gender and sum the counts
    a = df.group_by(["Name", "Gender"]).agg(pl.sum("n").alias("total"))

    # Sort by total count
    a = a.sort("total")

    # Display the results
    print("Names sorted by total count:")
    print(a.head(20))

    return a


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return (mo, pl)


if __name__ == "__main__":
    app.run()
