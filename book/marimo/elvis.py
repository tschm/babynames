# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "polars==1.30.0",
#     "numpy==2.2.3",
#     "plotly==6.1.2"
# ]
# ///
"""Analysis of the 'Elvis effect' in baby naming trends.

This module examines the popularity of the name 'Elvis' over time,
showing how cultural events and figures influence baby naming patterns.
It also compares with other names for context.
"""

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    from typing import Any

    import marimo as mo
    import plotly.graph_objects as go
    import polars as pl

    path = mo.notebook_location()

    u = pl.read_csv(str(path / "public" / "us.csv"))


@app.cell
def _(mo: Any) -> None:
    mo.md(r"""# The Elvis effect""")
    return


@app.cell
def _():
    # Filter for Elvis and Male gender

    _f = u.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "M"))

    # Sort by year for plotting
    _f = _f.sort("year")

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f["year"].to_list(), y=_f["n"].to_list(), mode="lines"))
    _fig.update_layout(title="# Boys named Elvis", xaxis_title="Year", yaxis_title="Count")
    _fig.show()

    # Show top 10 years
    print("Top 10 years for Elvis:")
    print(_f.sort("n", descending=True).head(10))

    return


@app.cell
def _() -> None:
    # Filter for Elvis and Female gender
    _f_1 = u.filter((pl.col("Name") == "Elvis") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    _f_1 = _f_1.sort("year")

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f_1["year"].to_list(), y=_f_1["n"].to_list(), mode="lines"))
    _fig.update_layout(title="# Girls named Elvis", xaxis_title="Year", yaxis_title="Count")
    _fig.show()

    return


@app.cell
def _() -> None:
    # Filter for Nikita and Female gender
    _f_2 = u.filter((pl.col("Name") == "Nikita") & (pl.col("Gender") == "F"))

    # Sort by year for plotting
    _f_2 = _f_2.sort("year")

    # Polars doesn't have a built-in plot method, so we'll use plotly
    # import plotly.graph_objects as go

    # Create a plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_f_2["year"].to_list(), y=_f_2["n"].to_list(), mode="lines"))
    _fig.update_layout(title="# Girls named Nikita", xaxis_title="Year", yaxis_title="Count")
    _fig.show()

    return


@app.cell
def _() -> None:
    # Group by Name and Gender and sum the counts
    _a = u.group_by(["Name", "Gender"]).agg(pl.sum("n").alias("total"))

    # Sort by total count
    _a = _a.sort("total")

    # Display the results
    print("Names sorted by total count:")
    print(_a.head(20))

    return


if __name__ == "__main__":
    app.run()
