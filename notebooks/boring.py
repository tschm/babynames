import marimo
from typing import Tuple, Any, Callable, Optional

__generated_with = "0.10.7"
app = marimo.App()


@app.cell
def _() -> Tuple[Any, Any]:
    import pandas as pd
    import numpy as np

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
        ## Definition:
        ### A name is boring if it's associated discrete distribution is close to a uniform distribution.

        ### The Shannon-entropy $\sum p_i \times \log p_i$ is maximal for the uniform distribution. Dangerous! (Kullback-Leibler)

        ### The Euclidean norm $\sqrt{\sum p_i^2}$ is is minimal for the uniform distribution.
        """
    )
    return


@app.cell
def _(np: Any) -> Tuple[Any, Callable, Callable]:
    from scipy.stats import entropy as e

    def entropy(ts: Any, base: Optional[int] = None) -> Any:
        ts = ts.dropna() / ts.sum()
        return e(ts, base=base)

    def norm(ts: Any) -> Any:
        ts = ts.dropna() / ts.sum()
        return np.linalg.norm(ts, 2)

    return e, entropy, norm


@app.cell
def _(entropy: Callable, girls: Any) -> None:
    girls.apply(entropy).sort_values()
    return


@app.cell
def _(girls: Any, norm: Callable) -> None:
    girls.apply(norm).sort_values()
    return


@app.cell
def _(boys: Any, entropy: Callable) -> None:
    boys.apply(entropy).sort_values()
    return


@app.cell
def _(boys: Any, norm: Callable) -> None:
    boys.apply(norm).sort_values()
    return


@app.cell
def _(boys: Any, girls: Any, pd: Any) -> Tuple[Any]:
    pair = pd.DataFrame(
        {"Boy": boys["Thomas"].dropna(), "Girl": girls["Charlotte"].dropna()}
    )
    pair.plot()
    return (pair,)


@app.cell
def _() -> Tuple[Any]:
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
