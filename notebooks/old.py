import marimo

__generated_with = "0.10.7"
app = marimo.App()


@app.cell
def _():
    import pandas as pd

    pd.options.display.max_rows = 20
    return (pd,)


@app.cell
def _(__file__):
    from pathlib import Path

    path = Path(__file__).parent
    return Path, path


@app.cell
def _(path, pd):
    boys = pd.read_csv(path / "data" / "boys.csv", index_col=0)
    girls = pd.read_csv(path / "data" / "girls.csv", index_col=0)
    return boys, girls


@app.cell
def _(boys):
    boys
    return


@app.cell
def _(girls):
    girls
    return


@app.cell
def _():
    # write a function for the age of a name
    def age(ts):
        # get into probabilities
        p = ts.dropna() / ts.sum()
        # accumulate all the probabilities
        a = p.cumsum()
        # get the first index where at least 50% of the babies have been boren
        return a[a >= 0.5].index[0]

    return (age,)


@app.cell
def _(age, girls):
    girls.apply(age).sort_values()
    return


@app.cell
def _(age, boys):
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
