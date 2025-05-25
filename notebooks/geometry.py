import marimo
from typing import Tuple, Any, Callable

__generated_with = "0.10.7"
app = marimo.App()


@app.cell
def _() -> Tuple[Any, Any]:
    import pandas as pd
    import numpy as np

    pd.options.display.max_rows = 20
    return np, pd


@app.cell
def _(__file__: str) -> Tuple[Any, Any]:
    from pathlib import Path

    path = Path(__file__).parent
    return Path, path


@app.cell
def _(path: Any, pd: Any) -> Tuple[Any, Any]:
    boys = pd.read_csv(path / "data" / "boys.csv", index_col=0)
    girls = pd.read_csv(path / "data" / "girls.csv", index_col=0)
    return boys, girls


@app.cell
def _(mo: Any) -> None:
    mo.md(
        r"""
        ## Each name lives on the unit-simplex

        ## Each name can be projected to the unit-sphere

        ## We compute the Bhattacharyya angle (correlation)
        """
    )
    return


@app.cell
def _(np: Any) -> Tuple[Callable, Callable]:
    # project to unit-simplex
    def proj_simplex(ts: Any) -> Any:
        return ts.fillna(0) / ts.sum()

    # project to unit-sphere
    def proj_sphere(ts: Any) -> Any:
        return np.sqrt(proj_simplex(ts))

    return proj_simplex, proj_sphere


@app.cell
def _(pd: Any, proj_sphere: Callable) -> Tuple[Callable]:
    def match(body1: Any, body2: Any) -> Any:
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
def _(boys: Any, girls: Any, match: Callable) -> Tuple[Any]:
    x = match(boys["Thomas"], girls)
    print(x)
    return (x,)


@app.cell
def _(boys: Any, match: Callable) -> None:
    match(boys, boys["Urs"])
    return


@app.cell
def _(boys: Any, girls: Any, match: Callable) -> None:
    match(boys, girls)
    # Ruth is amazing!
    return


@app.cell
def _(match: Callable, pd: Any, proj_simplex: Callable) -> Tuple[Callable]:
    def pair_plot(ts1: Any, ts2: Any, project: bool = True) -> Any:
        if project:
            ts1 = proj_simplex(ts1)
            ts2 = proj_simplex(ts2)
        print(match(ts1, ts2))

        x = pd.DataFrame({ts1.name: ts1, ts2.name: ts2})
        return x.plot()

    return (pair_plot,)


@app.cell
def _(boys: Any, girls: Any, pair_plot: Callable) -> None:
    pair_plot(boys["Gottfried"], girls["Elisabeth"], project=True)
    return


@app.cell
def _(boys: Any, girls: Any, pair_plot: Callable) -> None:
    pair_plot(boys["Chris"], girls["Rachel"], project=True)
    return


@app.cell
def _(boys: Any, pair_plot: Callable) -> None:
    pair_plot(boys["Chris"], boys["Christian"], project=False)
    return


@app.cell
def _(boys: Any, pair_plot: Callable) -> None:
    pair_plot(boys["Urs"], boys["Beat"], project=True)
    return


@app.cell
def _(boys: Any, girls: Any, pair_plot: Callable) -> None:
    pair_plot(boys["Walter"], girls["Ruth"])
    return


@app.cell
def _(boys: Any, girls: Any, match: Callable) -> None:
    match(boys["Thomas"], girls).mean()
    return


@app.cell
def _(boys: Any, girls: Any, match: Callable) -> None:
    # which girl has the best matching with the boys, e.g. we match each girl against all boys and compute the mean
    # for each girl. A high number indicates that the girl would be very compatible
    match(boys, girls).reset_index().groupby(by="Name A")[0].mean().sort_values()
    return


@app.cell
def _(boys: Any, girls: Any, match: Callable) -> None:
    match(boys, girls).reset_index().groupby(by="Name A")[0].mean().sort_values()
    return


@app.cell
def _() -> Tuple[Any]:
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
