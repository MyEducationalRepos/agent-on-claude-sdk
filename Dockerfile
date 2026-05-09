FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency manifests + source (needed to build the local package)
COPY pyproject.toml uv.lock ./
COPY src/ src/

# Install runtime deps only (no dev extras)
RUN uv sync --frozen --no-dev

# Env vars supplied at runtime via --env or .env mount
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["uv", "run", "python", "-m", "agent_on_claude_sdk.main"]
