import marimo

__generated_with = "0.10.7"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np

    pd.options.display.max_rows = 20
    return np, pd


@app.cell
def _(__file__):
    from pathlib import Path

    path = Path(__file__).parent
    return Path, path


@app.cell
def _(path, pd):
    boys = pd.read_csv(path / "assets" / "boys.csv", index_col=0)
    girls = pd.read_csv(path / "assets" / "girls.csv", index_col=0)
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
def _(np):
    # project to unit-simplex
    def proj_simplex(ts):
        return ts.fillna(0) / ts.sum()

    # project to unit-sphere
    def proj_sphere(ts):
        return np.sqrt(proj_simplex(ts))

    return proj_simplex, proj_sphere


@app.cell
def _(pd, proj_sphere):
    def match(body1, body2):
        if isinstance(body1, pd.Series):
            body1 = body1.to_frame()
        if isinstance(body2, pd.Series):
            body2 = body2.to_frame()
        x = body1.apply(proj_sphere)
        y = body2.apply(proj_sphere)
        x = pd.DataFrame({key: x[key].dot(y) for key in x.keys()}).stack().sort_values()
        x.index.names = ["Name A", "Name B"]
        return x

    return (match,)


@app.cell
def _(boys, girls, match):
    x = match(boys["Thomas"], girls)
    print(x)
    return (x,)


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
def _(match, pd, proj_simplex):
    def pair_plot(ts1, ts2, project=True):
        if project:
            ts1 = proj_simplex(ts1)
            ts2 = proj_simplex(ts2)
        print(match(ts1, ts2))

        x = pd.DataFrame({ts1.name: ts1, ts2.name: ts2})
        return x.plot()

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
def _(boys, girls, match):
    match(boys["Thomas"], girls).mean()
    return


@app.cell
def _(boys, girls, match):
    # which girl has the best matching with the boys, e.g. we match each girl against all boys and compute the mean
    # for each girl. A high number indicates that the girl would be very compatible
    match(boys, girls).reset_index().groupby(by="Name A")[0].mean().sort_values()
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
