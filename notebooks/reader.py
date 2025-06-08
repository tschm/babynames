import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import polars as pl
    import marimo as mo

@app.function
def boys():
    # In polars, we read the CSV and then set the first column as index
    boys_path = str(mo.notebook_location() / "public" / "boys.csv")

    # Read CSVs with polars
    boys = pl.read_csv(boys_path)

    # Convert first column to index (polars doesn't have index like pandas)
    # We'll keep the original structure for compatibility with the rest of the code
    return boys

@app.function
def girls():
    # In polars, we read the CSV and then set the first column as index
    girls_path = str(mo.notebook_location() / "public" / "girls.csv")

    # Read CSVs with polars
    girls = pl.read_csv(girls_path)

    # Convert first column to index (polars doesn't have index like pandas)
    # We'll keep the original structure for compatibility with the rest of the code
    return girls

@app.function
def us():
    us_path = str(mo.notebook_location() / "public" / "us.csv")

    # Read the CSV file
    dframe = pl.read_csv(us_path)

    return dframe
