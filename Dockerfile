# Step 1: Use a slim Python base image
FROM python:3.11-slim

# Step 2: Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Step 3: Install system dependencies required by Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 4: Set the working directory inside the container
WORKDIR /app

# Step 5: Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Install the Chromium browser for Playwright
RUN playwright install --with-deps chromium

# Step 7: Copy your entire project into the container
COPY . .

# Step 8: Define the command to execute your Dagster job
CMD ["dagster", "job", "execute", "-f", "ufo_pipeline.py"]