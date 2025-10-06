# UFO Data Pipeline 🛸

This project uses Docker to run a data pipeline that scrapes data, loads it to Snowflake, and transforms it with dbt.

---

## Setup

1.  **Clone the project:**
    ```bash
    git clone https://github.com/maher-dataconsult/nuforc_pipeline.git
    ```

2.  **Navigate into the directory:**
    ```bash
    cd nuforc_pipeline
    ```
*Note: Before running, make sure you have created and configured your `.dlt/secrets.toml` and `profiles/profiles.yml` files.*

---

## How to Run

1.  **Build the Docker image:**
    ```bash
    docker build -t ufo-pipeline .
    ```

2.  **Run the pipeline:**

    **For Linux:**
    ```bash
    docker run --rm -v "$(pwd)/.dlt:/root/.dlt" -v "$(pwd)/profiles:/root/.dbt" ufo-pipeline
    ```

    **For Windows (Command Prompt):**
    ```cmd
    docker run --rm -v "%cd%\.dlt:/root/.dlt" -v "%cd%\profiles:/root/.dbt" ufo-pipeline
    ```
