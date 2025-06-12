ARG PYTHON_VERSION=3.11.11

FROM python:${PYTHON_VERSION}-slim AS base
WORKDIR /app

# Install Poetry
FROM base AS base-poetry
RUN pip install --no-cache-dir poetry==1.8.3
COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

# Build the package
FROM base-poetry AS package-builder
COPY ./src /app/src
RUN poetry build --format wheel

# Install dependencies using Poetry
FROM base-poetry AS dependencies-installer
RUN --mount=type=secret,id=poetry_auth_toml,target=/root/.config/pypoetry/auth.toml \
    poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root --no-interaction --no-ansi

# Create the final stage with dependencies and built package
FROM base-poetry AS final
ENV PATH="/app/.venv/bin:${PATH}"
COPY --from=dependencies-installer /app/.venv/ /app/.venv/
COPY --from=package-builder /app/dist/*.whl /app/
RUN pip install --no-cache-dir --no-deps ./*.whl

ENTRYPOINT [ "poetry", "run", "python3", "live_prices_validation/main.py" ]