# Social Listening
A social listening tool built in python. Makes use of external APIs to pull data from social media.
Using OCR and a multimodal LLM to process the image of a news paper page.

# Running the app

## Prerequisites
- Python 3.14 (see `.python-version`)
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) installed on your system (used by `pytesseract`)
- [Ollama](https://ollama.com/) running locally (used for the multimodal LLM)

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with the required API keys:
```
TWEETAPIIO=<your-key>
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
