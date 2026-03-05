# Project README

## Prerequisites

Make sure you have `uv` installed.

### Install `uv`

**Linux, macOS, Windows (WSL):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Setup

Create a virtual environment and synchronize dependencies:

```bash
uv venv      # creates .venv/
uv sync      # syncs dependencies
```

---

## Database Migrations

### Generate a new migration

```bash
uv run alembic revision --autogenerate -m "describe your changes here"
```

### Apply migrations

```bash
uv run alembic upgrade head
```

---

## Running the Application

Start the app locally with:

```bash
uv run uvicorn app.main:app --reload --port 5555
```

- The app will be accessible at `http://localhost:5555\`.
- Documentation at `http://localhost:5555\docs`.

---

## Testing

Run the full test suite with coverage:

```bash
uv run pytest --cov=app -vv
```

Generate an HTML coverage report:

```bash
uv run coverage html
```

---

## Linting and Formatting

Check for linting issues:

```bash
uv run ruff check . && uv run ruff check . --diff
```

Auto-format and fix issues:

```bash
uv run ruff check . --fix && uv run ruff format .
```
