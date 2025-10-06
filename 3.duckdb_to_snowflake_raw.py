import dlt
import duckdb

# Define the source from DuckDB (native, no SQLAlchemy)
@dlt.source
def ufo_duckdb_source():
    # Connect directly to DuckDB
    con = duckdb.connect('ufo_reports.duckdb')

    # Read the table as a DataFrame (dlt handles it seamlessly)
    df = con.execute("SELECT * FROM ufo_reports").df()
    con.close()

    # Yield as a resource (dlt infers schema from DataFrame/rows)
    @dlt.resource(name="ufo_reports_raw", write_disposition="replace")
    def raw_data():
        yield df  # Or iterate: for _, row in df.iterrows(): yield row.to_dict()

    return raw_data()

if __name__ == "__main__":
    # Create the pipeline to Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="ufo_to_snowflake",
        destination="snowflake",
        dataset_name="raw",  # Changed schema name to "raw" in Snowflake
        progress="log",
    )

    # Load the data
    source = ufo_duckdb_source()
    # CORRECTED LINE: Pass the source object, not the resource
    load_info = pipeline.run(source)
    print(load_info)  # Shows loaded rows, tables, etc.