import duckdb

# Connect to DuckDB (in-memory or file-based; use ':memory:' for temp)
con = duckdb.connect('ufo_reports.duckdb')  # Creates/saves to this file

# Load CSV directly into a table
con.execute("""
    CREATE OR REPLACE TABLE ufo_reports AS
    SELECT * FROM read_csv_auto('ufo_reports.csv', header=true)
""")

# Close connection
con.close()