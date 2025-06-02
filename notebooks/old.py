import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import pandas as pd

    pd.options.display.max_rows = 20
    return (pd,)


@app.cell
def _(mo, pd):
    boys = pd.read_csv(mo.notebook_location() / "public" / "boys.csv", index_col=0)
    girls = pd.read_csv(mo.notebook_location() / "public" / "girls.csv", index_col=0)
    return boys, girls


@app.cell
def _(boys):
    boys
    return


@app.cell
def _(girls):
    girls
    return


@app.function
# write a function for the age of a name
def age(ts):
    # get into probabilities
    p = ts.dropna() / ts.sum()
    # accumulate all the probabilities
    a = p.cumsum()
    # get the first index where at least 50% of the babies have been boren
    return a[a >= 0.5].index[0]


@app.cell
def _(girls):
    girls.apply(age).sort_values()
    return


@app.cell
def _(boys):
    boys.apply(age).sort_values()
    return


@app.cell
def _(boys):
    boys["Adolf"].dropna().plot()
    return


@app.cell
def _(boys):
    boys["Adolf"].truncate(before=1946).sum()
    return


if __name__ == "__main__":
    app.run()
