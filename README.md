# UFO Data Pipeline 🛸

● Orchestration: **Dagster** <br>
● Containerization: **Docker** <br><br>
**➜** Scrapping ➜ Duckdb ➜ <u>(dlt)</u> ➜ Snowflake ➜ <u>(DBT)</u> ➜ PowerBI

[![image](https://images.jpost.com/image/upload/f_auto,fl_lossy/c_fill,g_faces:center,h_537,w_822/545260)](https://images.jpost.com/image/upload/f_auto,fl_lossy/c_fill,g_faces:center,h_537,w_822/545260)

-----

### `[ TECHNOLOGY MATRIX ]`

| Category | Technology / Service | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | Dagster | Defining, executing, and visualizing the end-to-end data pipeline. |
| **Containerization** | Docker | Creating a consistent and portable environment for all scripts and dependencies. |
| **Data Ingestion (Extraction)**| Python (Playwright) | Scraping raw UFO sighting data from the NUFORC public website. |
| **Intermediate Storage** | DuckDB | Staging the raw scraped data in a local, file-based analytical database. |
| **Data Ingestion (Loading)**| Python `(dlt)` (Data Load Tool) | Loading data from the intermediate DuckDB database into Snowflake. |
| **Data Warehouse** | Snowflake | Storing raw (Bronze) and transformed (Silver/Gold) data for analysis. |
| **Data Transformation** | DBT | Cleaning, standardizing, and modeling the data directly within Snowflake. |
| **BI & Data Modeling** | Power BI | Building the final dashboards and reports for data analysis. |
| **Programming Language** | Python | The core language used for scripting the scraping, orchestration, and data loading scripts. |
| **Version Control** | Git & GitHub | Managing and tracking changes to the project's source code. |


-----

## Setup

1.  **Clone the project:**
    ```bash
    git clone https://github.com/maher-dataconsult/nuforc_pipeline.git
    ```

2.  **Navigate into the directory:**
    ```bash
    cd nuforc_pipeline
    ```
    
## Build and Run

3.  **Build the Docker image:**
    ```bash
    docker build -t ufo-pipeline .
    ```

4.  **Run the pipeline:**

    **`For Linux:`**
    ```bash
    docker run --rm -v "$(pwd)/.dlt:/root/.dlt" -v "$(pwd)/profiles:/root/.dbt" ufo-pipeline
    ```

    **`For Windows (Command Prompt):`**
    ```cmd
    docker run --rm -v "%cd%\.dlt:/root/.dlt" -v "%cd%\profiles:/root/.dbt" ufo-pipeline
    ```
-----
*Note: Before running, make sure you have created and configured your `.dlt/secrets.toml` and `profiles/profiles.yml` files.*

