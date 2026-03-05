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

## Additional Information

- **How to run the project:** Run locally via `uvicorn` on port `5555`. See _Start the app locally with_ session.
- **Time spent building the project:** _3 hours_
- **Assumptions made:** I assumed the project would be local and intended for a single user offline, simulating an app installed on a phone or a computer. Additionally, I assumed that the player would play directly through the API, using only requests to interact with the game.
- **Trade-offs:**
  - Used uv for simplicity instead of Docker. It's good enough for demos and prototypes, but Docker with Docker Compose would be a better choice for a real product.
  - I used SQLite programming instead of Postgres or MySQL. Adding a relational database would have added an unnecessary layer of complexity to the project.
  - Synchronous programming instead of asynchronous. I could get stuck on an issue that I wouldn’t be able to solve quickly due to my lack of experience with FastAPI, which could delay the project."

- **Special / unique features:**
  - auto-migration with Alembic
  - integrated coverage reports
  - added status/health routes
  - api documentation (due Fast API)
  - AscII board to play on request
  - added test coverage over 80%
  - added layer of separation of concerns (repositories and services)
  - added ruff as a linter and formatter helpping the code quality
