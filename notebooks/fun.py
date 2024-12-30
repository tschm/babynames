import marimo

__generated_with = "0.10.7"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# Fun with the SMI""")
    return


@app.cell
def _(__file__):
    from pathlib import Path

    path = Path(__file__).parent
    return Path, path


@app.cell
def _():
    import pandas as pd
    import cvxpy as cvx

    pd.options.display.max_rows = 20
    return cvx, pd


@app.cell
def _(path, pd):
    prices = pd.read_csv(path / "data" / "prices.csv", index_col=0)

    returns = prices.pct_change().fillna(0.0)
    returns
    return prices, returns


@app.cell
def _(returns):
    print(100 * 16 * returns.std().sort_values())
    return


@app.cell
def _(prices):
    # Severe problems with data quality here...
    prices["UBS Group AG"].plot()
    return


@app.cell
def _(cvx, pd, returns):
    def min_var(matrix):
        w = cvx.Variable(matrix.shape[1])

        cvx.Problem(
            cvx.Minimize(cvx.norm(matrix.values @ w, 2)), [0 <= w, cvx.sum(w) == 1]
        ).solve()

        return 100 * pd.Series(index=matrix.keys(), data=w.value).sort_values()

    min_var(returns).map("{:,.2f}%".format)
    return (min_var,)


@app.cell
def _(cvx, pd, returns):
    def ridge(matrix, lamb_balance=0):
        def __objective():
            return cvx.Minimize(
                cvx.norm(matrix.values @ w, 2) + lamb_balance * cvx.norm(w, 2)
            )

        w = cvx.Variable(matrix.shape[1])
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()
        return 100 * pd.Series(index=matrix.keys(), data=w.value).sort_values()

    ridge(returns, 1).map("{:,.2f}%".format)
    return (ridge,)


@app.cell
def _(cvx, pd, returns):
    def ElasticNet(matrix, w0, lamb_balance=0, lamb_trades=0):

        def __objective():
            return cvx.Minimize(
                cvx.norm(matrix.values @ w, 2)
                + lamb_balance * cvx.norm(w, 2)
                + lamb_trades * cvx.norm(w - w0, 1)
            )

        w = cvx.Variable(matrix.shape[1])
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()
        return 100 * pd.Series(index=matrix.keys(), data=w.value).sort_values()

    ElasticNet(returns, w0=0.05, lamb_balance=1, lamb_trades=0.03).map(
        "{:,.2f}%".format
    )
    return (ElasticNet,)


@app.cell
def _(cvx, pd):
    def ElasticNet_1(matrix, w0, lamb_balance=0, lamb_trades=0):

        def __objective():
            return cvx.Minimize(
                cvx.norm(matrix.values @ w, 2)
                + lamb_balance * cvx.norm(w, 2)
                + lamb_trades * cvx.norm(w - w0, 1)
            )

        w = cvx.Variable(matrix.shape[1])
        cvx.Problem(__objective(), [0 <= w, cvx.sum(w) == 1]).solve()
        return 100 * pd.Series(index=matrix.keys(), data=w.value).sort_values()

    return (ElasticNet_1,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
