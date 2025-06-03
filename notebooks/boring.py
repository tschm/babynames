import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import polars as pl
    import numpy as np

    return np, pl


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
    # Polars equivalent of apply and sort_values
    # Apply entropy to each column and sort
    result = girls.select(
        [
            pl.col(col_name).map_elements(entropy).alias(col_name)
            for col_name in girls.columns
        ]
    )
    # Sort the results
    result = result.melt().sort("value")
    print(result)
    return


@app.cell
def _(girls, norm, pl):
    # Polars equivalent of apply and sort_values
    # Apply norm to each column and sort
    result = girls.select(
        [
            pl.col(col_name).map_elements(norm).alias(col_name)
            for col_name in girls.columns
        ]
    )
    # Sort the results
    result = result.melt().sort("value")
    print(result)
    return


@app.cell
def _(boys, entropy, pl):
    # Polars equivalent of apply and sort_values
    # Apply entropy to each column and sort
    result = boys.select(
        [
            pl.col(col_name).map_elements(entropy).alias(col_name)
            for col_name in boys.columns
        ]
    )
    # Sort the results
    result = result.melt().sort("value")
    print(result)
    return


@app.cell
def _(boys, norm, pl):
    # Polars equivalent of apply and sort_values
    # Apply norm to each column and sort
    result = boys.select(
        [
            pl.col(col_name).map_elements(norm).alias(col_name)
            for col_name in boys.columns
        ]
    )
    # Sort the results
    result = result.melt().sort("value")
    print(result)
    return


@app.cell
def _(boys, girls, pl):
    # Polars equivalent of DataFrame creation and plot
    # Filter out null values
    boy_data = boys.filter(pl.col("Thomas").is_not_null()).select(
        pl.col("Thomas").alias("Boy")
    )
    girl_data = girls.filter(pl.col("Charlotte").is_not_null()).select(
        pl.col("Charlotte").alias("Girl")
    )

    # Create a DataFrame with the filtered data
    pair = pl.DataFrame([boy_data.to_series(0), girl_data.to_series(0)])

    # Polars doesn't have a built-in plot method, so we'll use matplotlib or plotly
    import matplotlib.pyplot as plt

    # Convert to pandas for plotting (temporary solution)
    pair_pd = pair.to_pandas()
    pair_pd.plot()
    plt.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
