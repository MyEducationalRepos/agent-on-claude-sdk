FROM python:3.12-slim

WORKDIR /app

# Non-root runtime user (architecture §5)
RUN addgroup --system agent && adduser --system --ingroup agent agent

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency manifests + source (needed to build the local package)
COPY pyproject.toml uv.lock ./
COPY src/ src/

# Install runtime deps only (no dev extras)
RUN uv sync --frozen --no-dev

# Env vars supplied at runtime via --env or .env mount
ENV PYTHONUNBUFFERED=1

# Drop to non-root before running
USER agent

ENTRYPOINT ["uv", "run", "python", "-m", "agent_on_claude_sdk.main"]
