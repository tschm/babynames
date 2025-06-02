import marimo
from typing import Tuple, Any

__generated_with = "0.11.7"
app = marimo.App()


@app.cell
def _(mo: Any) -> None:
    mo.md(r"""# The Elvis effect""")
    return


@app.cell
def _(__file__: str) -> Tuple[Any, Any]:
    from pathlib import Path

    path = Path(__file__).parent
    return Path, path


@app.cell
def _() -> Tuple[Any]:
    import pandas as pd

    pd.options.display.max_rows = 20
    return (pd,)


@app.cell
def _(path: Any, pd: Any) -> Tuple[Any]:
    names = pd.read_csv(
        path / "assets" / "us.csv", index_col=["year", "Name", "Gender"]
    )["n"]
    names
    return (names,)


@app.cell
def _(names: Any) -> Tuple[Any]:
    f = names.loc[:, "Elvis", "M"]
    f.plot()
    print(f.sort_values(ascending=False).head(10))
    f.plot(title="# Boys named Elvis")
    # f.sort_values()

    return (f,)


@app.cell
def _(names: Any) -> Tuple[Any]:
    f_1 = names.loc[:, "Elvis", "F"]
    f_1.plot()
    return (f_1,)


@app.cell
def _(names: Any) -> Tuple[Any]:
    f_2 = names.loc[:, "Nikita", "F"]
    f_2.plot()
    return (f_2,)


@app.cell
def _(names: Any) -> Tuple[Any]:
    a = names.groupby(["Name", "Gender"]).sum()
    a.sort_values()
    return (a,)


@app.cell
def _() -> Tuple[Any]:
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
