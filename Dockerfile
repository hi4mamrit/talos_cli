FROM python:3.12-slim

# Install curl and uv, then add uv to global PATH
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml ./
COPY .lock ./
RUN uv pip install --system --no-cache -r .lock

# Copy source code
COPY . .

# Run using uv
CMD ["uv", "run", "main.py"]
