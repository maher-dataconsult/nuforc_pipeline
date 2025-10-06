import subprocess
import sys
from dagster import job, op

@op
def scrape_ufo_data(context):
    """Scrape UFO data to CSV."""
    result = subprocess.run(
        [sys.executable, "1.scrape.py"],
        capture_output=True,
        text=True,
        cwd="."
    )
    if result.returncode != 0:
        raise Exception(f"Scraping failed: {result.stderr}")
    context.log.info("Scraping completed successfully.")
    return result.stdout

@op
def load_to_duckdb(context, scraped):
    """Load CSV to DuckDB."""
    # The 'scraped' input is not used directly but ensures dependency
    result = subprocess.run(
        [sys.executable, "2.csv_to_duckdb.py"],
        capture_output=True,
        text=True,
        cwd="."
    )
    if result.returncode != 0:
        raise Exception(f"DuckDB load failed: {result.stderr}")
    context.log.info("DuckDB load completed successfully.")
    return result.stdout

@op
def load_to_snowflake(context, duckdb_loaded):
    """Load DuckDB to Snowflake."""
    # The 'duckdb_loaded' input is not used directly but ensures dependency
    result = subprocess.run(
        [sys.executable, "3.duckdb_to_snowflake_raw.py"],
        capture_output=True,
        text=True,
        cwd="."
    )
    if result.returncode != 0:
        raise Exception(f"Snowflake load failed: {result.stderr}")
    context.log.info("Snowflake load completed successfully.")
    return result.stdout

@op
def run_dbt_transform(context, snowflake_loaded):
    """Run dbt transformations."""
    # The 'snowflake_loaded' input is not used directly but ensures dependency
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "ufo_dbt"],
        capture_output=True,
        text=True,
        cwd="."
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    context.log.info("dbt run completed successfully.")
    return result.stdout

@job
def ufo_pipeline():
    """Orchestrate the full UFO data pipeline."""
    scraped = scrape_ufo_data()
    duckdb_loaded = load_to_duckdb(scraped)
    snowflake_loaded = load_to_snowflake(duckdb_loaded)
    run_dbt_transform(snowflake_loaded)