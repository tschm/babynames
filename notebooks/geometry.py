import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import polars as pl
    import numpy as np

    # Polars doesn't have the same display options as pandas
    # We'll use the default display settings
    return np, pl


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
def _(mo):
    mo.md(
        r"""
    ## Each name lives on the unit-simplex

    ## Each name can be projected to the unit-sphere

    ## We compute the Bhattacharyya angle (correlation)
    """
    )
    return


@app.cell
def _(np, pl):
    # project to unit-simplex
    def proj_simplex(ts):
        # Polars equivalent of fillna and sum
        # If ts is a Series, convert to numpy for easier manipulation
        if hasattr(ts, "to_numpy"):
            ts_array = ts.fill_null(0).to_numpy()
            return ts_array / ts_array.sum()
        # If ts is a DataFrame, apply to each column
        elif hasattr(ts, "fill_null"):
            return ts.fill_null(0).select(
                [(pl.col(col) / pl.col(col).sum()).alias(col) for col in ts.columns]
            )
        # Fallback for numpy arrays
        else:
            return ts / ts.sum()

    # project to unit-sphere
    def proj_sphere(ts):
        return np.sqrt(proj_simplex(ts))

    return proj_simplex, proj_sphere


@app.cell
def _(pl, proj_sphere, np):
    def match(body1, body2, np):
        # Polars equivalent of Series and DataFrame operations
        # Convert to DataFrame if it's a Series
        if hasattr(body1, "to_frame") and not hasattr(body1, "columns"):
            # Assuming body1 is a Series-like object
            col_name = body1.name if hasattr(body1, "name") else "column"
            body1 = pl.DataFrame({col_name: body1})

        if hasattr(body2, "to_frame") and not hasattr(body2, "columns"):
            # Assuming body2 is a Series-like object
            col_name = body2.name if hasattr(body2, "name") else "column"
            body2 = pl.DataFrame({col_name: body2})

        # Apply proj_sphere to each column
        x_cols = body1.columns
        y_cols = body2.columns

        # Create a result DataFrame with all combinations of x and y columns
        result_data = []

        # For each column in body1
        for x_col in x_cols:
            x_sphere = proj_sphere(body1.select(x_col))

            # For each column in body2
            for y_col in y_cols:
                y_sphere = proj_sphere(body2.select(y_col))

                # Calculate dot product (correlation)
                # Convert to numpy for easier manipulation
                x_np = (
                    x_sphere
                    if isinstance(x_sphere, np.ndarray)
                    else x_sphere.to_numpy().flatten()
                )
                y_np = (
                    y_sphere
                    if isinstance(y_sphere, np.ndarray)
                    else y_sphere.to_numpy().flatten()
                )

                # Calculate dot product
                dot_product = np.dot(x_np, y_np)

                # Add to result data
                result_data.append(
                    {"Name A": x_col, "Name B": y_col, "value": dot_product}
                )

        # Create result DataFrame and sort by value
        result = pl.DataFrame(result_data).sort("value")

        return result

    return (match,)


@app.cell
def _(boys, girls, match):
    x = match(boys["Thomas"], girls)
    print(x)
    return


@app.cell
def _(boys, match):
    match(boys, boys["Urs"])
    return


@app.cell
def _(boys, girls, match):
    match(boys, girls)
    # Ruth is amazing!
    return


@app.cell
def _(match, pl, proj_simplex, np):
    def pair_plot(ts1, ts2, project=True):
        # Project to simplex if requested
        if project:
            ts1 = proj_simplex(ts1)
            ts2 = proj_simplex(ts2)

        # Print match results
        print(match(ts1, ts2))

        # Create a DataFrame for plotting
        # Get names for the columns
        name1 = ts1.name if hasattr(ts1, "name") else "Series 1"
        name2 = ts2.name if hasattr(ts2, "name") else "Series 2"

        # Convert to numpy arrays if they're not already
        ts1_np = ts1 if isinstance(ts1, np.ndarray) else ts1.to_numpy().flatten()
        ts2_np = ts2 if isinstance(ts2, np.ndarray) else ts2.to_numpy().flatten()

        # Create a polars DataFrame
        df = pl.DataFrame({name1: ts1_np, name2: ts2_np})

        # Polars doesn't have a built-in plot method, so we'll use matplotlib
        import matplotlib.pyplot as plt

        # Convert to pandas for plotting
        df_pd = df.to_pandas()
        plot = df_pd.plot()
        plt.show()

        return plot

    return (pair_plot,)


@app.cell
def _(boys, girls, pair_plot):
    pair_plot(boys["Gottfried"], girls["Elisabeth"], project=True)
    return


@app.cell
def _(boys, girls, pair_plot):
    pair_plot(boys["Chris"], girls["Rachel"], project=True)
    return


@app.cell
def _(boys, pair_plot):
    pair_plot(boys["Chris"], boys["Christian"], project=False)
    return


@app.cell
def _(boys, pair_plot):
    pair_plot(boys["Urs"], boys["Beat"], project=True)
    return


@app.cell
def _(boys, girls, pair_plot):
    pair_plot(boys["Walter"], girls["Ruth"])
    return


@app.cell
def _(boys, girls, match, pl):
    # Polars equivalent of mean
    # Calculate the mean of the match values
    result = match(boys.select("Thomas"), girls)
    mean_value = result.select(pl.mean("value")).item()

    print(f"Mean match value: {mean_value}")
    return


@app.cell
def _(boys, girls, match, pl):
    # which girl has the best matching with the boys, e.g. we match each girl against all boys and compute the mean
    # for each girl. A high number indicates that the girl would be very compatible

    # Polars equivalent of reset_index, groupby, and sort_values
    result = match(boys, girls)

    # Group by Name A and calculate mean of value
    grouped_result = result.group_by("Name A").agg(pl.mean("value")).sort("value")

    print(grouped_result)
    return


@app.cell
def _(boys, girls, match):
    match(boys, girls).reset_index().groupby(by="Name A")[0].mean().sort_values()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
