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


@app.cell
def _():
    import polars as pl
    import marimo as mo
    import plotly.graph_objects as go

    # Polars doesn't have the same display options as pandas
    # We'll use the default display settings
    return go, mo, pl


@app.cell
def _(mo, pl):
    # Read CSV with polars
    boys_path = str(mo.notebook_location() / "public" / "boys.csv")
    girls_path = str(mo.notebook_location() / "public" / "girls.csv")

    # Read CSVs with polars
    boys = pl.read_csv(boys_path)
    girls = pl.read_csv(girls_path)

    # In polars, we need to handle the index differently
    # We'll assume the first column is the index (year)

    return boys, girls


@app.cell
def _(boys):
    boys
    return


@app.cell
def _(girls):
    girls
    return


@app.function
# write a function for the age of a name
def age(ts):
    import numpy as np

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
def _(girls, pl):
    # Polars equivalent of apply and sort_values
    # Apply age function to each column and sort
    _result = pl.DataFrame(
        {
            "column": girls.columns,
            "age": [age(girls.select(col).to_series()) for col in girls.columns],
        }
    ).sort("age")

    print(_result)
    return


@app.cell
def _(boys, pl):
    # Polars equivalent of apply and sort_values
    # Apply age function to each column and sort
    _result = pl.DataFrame(
        {
            "column": boys.columns,
            "age": [age(boys.select(col).to_series()) for col in boys.columns],
        }
    ).sort("age")

    print(_result)
    return


@app.cell
def _(boys):
    boys
    return


@app.cell
def _(boys, go, pl):
    # Extract the Adolf column and filter out null values
    adolf_data = boys.select(["year", "Adolf"]).filter(pl.col("Adolf").is_not_null())

    # Convert to lists
    x = adolf_data["year"].to_list()
    y = adolf_data["Adolf"].to_list()

    # Create line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Adolf"))

    # Add trace for Adolf data
    #fig.add_trace(go.Scatter(y=adolf_data, mode="lines", name="Adolf"))

    # Update layout
    fig.update_layout(
        title="Adolf", xaxis_title="Index", yaxis_title="Value", width=800, height=600
    )

    fig
    return


@app.cell
def _(boys, pl):
    # Polars equivalent of truncate and sum
    # Filter the data to include only years after 1946
    # Assuming the first column is the year column
    year_col = boys.columns[0]

    # Filter the Adolf column for years after 1946
    adolf_after_1946 = boys.filter(pl.col(year_col) > 1946).select("Adolf")

    # Sum the values
    adolf_sum = adolf_after_1946.select(pl.sum("Adolf")).item()

    print(f"Sum of Adolf after 1946: {adolf_sum}")
    return


if __name__ == "__main__":
    app.run()
