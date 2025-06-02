import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# The Elvis effect""")
    return


@app.cell
def _():
    import pandas as pd

    pd.options.display.max_rows = 20
    return (pd,)


@app.cell
def _(mo, pd):
    names = pd.read_csv(
        mo.notebook_location() / "public" / "us.csv",
        index_col=["year", "Name", "Gender"],
    )["n"]
    names
    return (names,)


@app.cell
def _(names):
    f = names.loc[:, "Elvis", "M"]
    f.plot()
    print(f.sort_values(ascending=False).head(10))
    f.plot(title="# Boys named Elvis")
    # f.sort_values()

    return


@app.cell
def _(names):
    f_1 = names.loc[:, "Elvis", "F"]
    f_1.plot()
    return


@app.cell
def _(names):
    f_2 = names.loc[:, "Nikita", "F"]
    f_2.plot()
    return


@app.cell
def _(names):
    a = names.groupby(["Name", "Gender"]).sum()
    a.sort_values()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
