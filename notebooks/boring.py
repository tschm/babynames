import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np

    return np, pd


@app.cell
def _(mo, pd):
    boys = pd.read_csv(mo.notebook_location() / "public" / "boys.csv", index_col=0)
    girls = pd.read_csv(mo.notebook_location() / "public" / "girls.csv", index_col=0)
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
        ts = ts.dropna() / ts.sum()
        return e(ts, base=base)

    def norm(ts):
        ts = ts.dropna() / ts.sum()
        return np.linalg.norm(ts, 2)

    return entropy, norm


@app.cell
def _(entropy, girls):
    girls.apply(entropy).sort_values()
    return


@app.cell
def _(girls, norm):
    girls.apply(norm).sort_values()
    return


@app.cell
def _(boys, entropy):
    boys.apply(entropy).sort_values()
    return


@app.cell
def _(boys, norm):
    boys.apply(norm).sort_values()
    return


@app.cell
def _(boys, girls, pd):
    pair = pd.DataFrame(
        {"Boy": boys["Thomas"].dropna(), "Girl": girls["Charlotte"].dropna()}
    )
    pair.plot()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
