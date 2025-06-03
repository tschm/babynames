import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# Fun with the SMI""")
    return


@app.cell
def _():
    import polars as pl
    import cvxpy as cvx

    # Polars doesn't have the same display options as pandas
    # We'll use the default display settings
    return cvx, pl


@app.cell
def _(mo, pl):
    # Read CSV with polars
    prices = pl.read_csv(str(mo.notebook_location() / "public" / "prices.csv"))

    # In polars, we need to handle the index differently
    # We'll assume the first column is the index (date)
    date_col = prices.columns[0]

    # Calculate percentage change (equivalent to pct_change in pandas)
    # First, we need to convert to a format where we can calculate percentage change
    # Then fill null values with 0.0
    prices.with_row_index(date_col)

    # Calculate returns using polars expressions
    # This is a bit more complex in polars than pandas
    returns = prices.select(
        [
            ((pl.col(col) / pl.col(col).shift(1)) - 1).fill_null(0.0).alias(col)
            for col in prices.columns
            if col != date_col
        ]
    )

    # Display returns
    print(returns)

    return prices, returns


@app.cell
def _(returns, pl):
    # Calculate standard deviation for each column and sort
    # In polars, we need to use a different approach
    std_values = returns.select(
        [pl.col(col).std().alias(col) for col in returns.columns]
    )

    # Convert to a format that can be sorted
    std_series = std_values.melt().sort("value")

    # Scale by 100 * 16 as in the original code
    print(100 * 16 * std_series)
    return


@app.cell
def _(prices):
    # Severe problems with data quality here...
    # Polars doesn't have a built-in plot method, so we'll use matplotlib
    import matplotlib.pyplot as plt

    # Extract the UBS Group AG column and plot it
    ubs_data = prices.select("UBS Group AG").to_pandas()
    ubs_data.plot()
    plt.title("UBS Group AG")
    plt.show()
    return


@app.cell
def _(cvx, pl, returns):
    def min_var(matrix):
        # Get the number of columns in the matrix
        n_cols = len(matrix.columns)

        # Create a variable for optimization
        w = cvx.Variable(n_cols)

        # Convert polars DataFrame to numpy array for optimization
        matrix_values = matrix.to_numpy()

        # Solve the optimization problem
        cvx.Problem(
            cvx.Minimize(cvx.norm(matrix_values @ w, 2)), [0 <= w, cvx.sum(w) == 1]
        ).solve()

        # Create a polars DataFrame with the results
        result = pl.DataFrame({"column": matrix.columns, "value": 100 * w.value}).sort(
            "value"
        )

        return result

    # Format the results
    result = min_var(returns)
    # Polars doesn't have a direct equivalent to pandas' map with format
    # We'll format the values manually
    formatted_result = result.with_columns(
        pl.col("value").map_elements(lambda x: f"{x:,.2f}%").alias("formatted_value")
    )
    print(formatted_result)
    return


@app.cell
def _(cvx, pl, returns):
    def ridge(matrix, lamb_balance=0):
        def __objective():
            # Convert polars DataFrame to numpy array for optimization
            matrix_values = matrix.to_numpy()
            return cvx.Minimize(
                cvx.norm(matrix_values @ w, 2) + lamb_balance * cvx.norm(w, 2)
            )

        # Get the number of columns in the matrix
        n_cols = len(matrix.columns)

        # Create a variable for optimization
        w = cvx.Variable(n_cols)

        # Solve the optimization problem
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()

        # Create a polars DataFrame with the results
        result = pl.DataFrame({"column": matrix.columns, "value": 100 * w.value}).sort(
            "value"
        )

        return result

    # Format the results
    result = ridge(returns, 1)
    # Polars doesn't have a direct equivalent to pandas' map with format
    # We'll format the values manually
    formatted_result = result.with_columns(
        pl.col("value").map_elements(lambda x: f"{x:,.2f}%").alias("formatted_value")
    )
    print(formatted_result)
    return


@app.cell
def _(cvx, pl, returns):
    def ElasticNet(matrix, w0, lamb_balance=0, lamb_trades=0):
        def __objective():
            # Convert polars DataFrame to numpy array for optimization
            matrix_values = matrix.to_numpy()
            return cvx.Minimize(
                cvx.norm(matrix_values @ w, 2)
                + lamb_balance * cvx.norm(w, 2)
                + lamb_trades * cvx.norm(w - w0, 1)
            )

        # Get the number of columns in the matrix
        n_cols = len(matrix.columns)

        # Create a variable for optimization
        w = cvx.Variable(n_cols)

        # Solve the optimization problem
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()

        # Create a polars DataFrame with the results
        result = pl.DataFrame({"column": matrix.columns, "value": 100 * w.value}).sort(
            "value"
        )

        return result

    # Format the results
    result = ElasticNet(returns, w0=0.05, lamb_balance=1, lamb_trades=0.03)
    # Polars doesn't have a direct equivalent to pandas' map with format
    # We'll format the values manually
    formatted_result = result.with_columns(
        pl.col("value").map_elements(lambda x: f"{x:,.2f}%").alias("formatted_value")
    )
    print(formatted_result)
    return


@app.cell
def _(cvx, pl):
    def ElasticNet_1(matrix, w0, lamb_balance=0, lamb_trades=0):
        def __objective():
            # Convert polars DataFrame to numpy array for optimization
            matrix_values = matrix.to_numpy()
            return cvx.Minimize(
                cvx.norm(matrix_values @ w, 2)
                + lamb_balance * cvx.norm(w, 2)
                + lamb_trades * cvx.norm(w - w0, 1)
            )

        # Get the number of columns in the matrix
        n_cols = len(matrix.columns)

        # Create a variable for optimization
        w = cvx.Variable(n_cols)

        # Solve the optimization problem
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()

        # Create a polars DataFrame with the results
        result = pl.DataFrame({"column": matrix.columns, "value": 100 * w.value}).sort(
            "value"
        )

        return result

    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
