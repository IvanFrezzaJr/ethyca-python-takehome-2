
## Setup
Install uv
```bash
# Linux, macOS, Windows (WSL)
curl -LsSf https://astral.sh/uv/install.sh | sh


# Windows (Powershell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Run:
```bash
uv venv  # create .venv/

uv sync
```

## run migration


### generate migrations
```bash
uv run alembic revision --autogenerate -m "add your message here"
```

### appling migration
```bash
uv run alembic upgrade head
```


## Running Aplication

Run:
```bash
uv run uvicorn app.main:app --reload --port 5555
```

## Running tests

Run the full test suite with coverage:

```bash
 uv run pytest --cov=app -vv
```

## lint
```bash
uv run ruff check . && ruff check . --diff
```

## format
```bash
uv run ruff check . --fix && ruff format .
```


## generate coverage report in HTML
```bash
uv run coverage html
```
