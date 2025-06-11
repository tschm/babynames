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
import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl
    import plotly.graph_objects as go
    import numpy as np
    from typing import Any

    path = mo.notebook_location()

    g = pl.read_csv(str(path / "public" / "girls.csv"))
    b = pl.read_csv(str(path / "public" / "boys.csv"))


@app.function
def age(ts: pl.Series) -> int:
    # Polars equivalent of dropna and sum
    # Convert to numpy for easier manipulation
    ts_filtered = ts.drop_nulls().to_numpy()

    # Get into probabilities
    p = ts_filtered / ts_filtered.sum()

    # Accumulate all the probabilities
    a = np.cumsum(p)

    # Get the first index where at least 50% of the babies have been born
    # This is a bit more complex in polars than pandas
    # We need to find the first index where the cumulative sum is >= 0.5
    first_idx = np.where(a >= 0.5)[0][0]

    # Return the year (assuming the first column is the year)
    # This might need adjustment based on the actual data structure
    return first_idx + 1



@app.cell
def _(mo: Any) -> None:
    # Polars equivalent of apply and sort_values
    # Apply age function to each column3 and sort
    _result = pl.DataFrame(
        {
            "column": b.columns,
            "age": [age(b[col]) for col in b.columns],
        }
    ).sort("age")

    print(_result)


@app.cell
def _(mo: Any) -> None:
    # Polars equivalent of apply and sort_values
    # Apply age function to each column3 and sort
    _result = pl.DataFrame(
        {
            "column": g.columns,
            "age": [age(g[col]) for col in g.columns],
        }
    ).sort("age")

    print(_result)


@app.cell
def _() -> None:
    # Extract the Adolf column and filter out null values
    adolf_data = b.select(["year", "Adolf"]).filter(pl.col("Adolf").is_not_null())

    # Convert to lists
    x = adolf_data["year"].to_list()
    y = adolf_data["Adolf"].to_list()

    # Create line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Adolf"))

    # Add trace for Adolf data
    # fig.add_trace(go.Scatter(y=adolf_data, mode="lines", name="Adolf"))

    # Update layout
    fig.update_layout(
        title="Adolf", xaxis_title="Index", yaxis_title="Value", width=800, height=600
    )

    fig


@app.cell
def _() -> None:
    # Polars equivalent of truncate and sum
    # Filter the data to include only years after 1946
    # Assuming the first column is the year column
    year_col = b.columns[0]

    # Filter the Adolf column for years after 1946
    adolf_after_1946 = b.filter(pl.col(year_col) > 1946).select("Adolf")

    # Sum the values
    adolf_sum = adolf_after_1946.select(pl.sum("Adolf")).item()

    print(f"Sum of Adolf after 1946: {adolf_sum}")
    return


if __name__ == "__main__":
    app.run()
