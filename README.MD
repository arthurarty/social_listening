# Social Listening
A social listening tool built in python. Makes use of external APIs to pull data from social media.
Using OCR and a multimodal LLM to process the image of a news paper page.

# Running the app

## Prerequisites
- Python 3.14 (see `.python-version`)
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) installed on your system (used by `pytesseract`)
- [Ollama](https://ollama.com/) running locally (used for the multimodal LLM)
- [Docker](https://www.docker.com/) (used to run the Postgres database)

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with the required API keys:
```
TWEET_API_IO=<your-key>
DATABASE_URL="postgresql://social_listening:socialListeningPassword@localhost:5432/social_listening"
```

## Database
A Postgres database is provided via Docker Compose (see `docker-compose.yml`). On first startup it automatically creates a `social_listening` database, owned by the `social_listening` user, via the `POSTGRES_DB`/`POSTGRES_USER` env vars.

Start the database in the background:
```bash
docker compose up -d postgres
```

Check it's running and healthy:
```bash
docker compose ps
```

Stop it (add `-v` to also delete the data volume):
```bash
docker compose down
```

The app connects using the `DATABASE_URL` in `.env`. Once the database is up, apply migrations with:
```bash
alembic upgrade head
```

After changing a model in `app/database/`, generate a new migration:
```bash
alembic revision --autogenerate -m "describe your change"
```
Review the generated file in `app/database/alembic/versions/`, then apply it with:
```bash
alembic upgrade head
```
To roll back a migration you can use the command:
```bash
alembic downgrade -1
```

## Pre-commit hooks
This repo uses [pre-commit](https://pre-commit.com/) to run `black`, `isort`, and `autoflake` before each commit.

`pre-commit` is installed via `requirements.txt`, so after activating your venv, install the git hooks:
```bash
pre-commit install
```

## Run
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

The app will be available at http://127.0.0.1:8000.

# Data sources
## Third Party APIS considered
- Twitter - https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search - pay as you go
- Twitter - https://sorsa.io/ - Starting at $50 a month

- All platforms - https://www.netrows.com/ - starting at $30 a month
