# Minimal local ticket API

A small learning API with a built-in HTTP server version and a FastAPI version. It listens on
`127.0.0.1` only and returns fixed placeholders. It does not connect to external
systems, store ticket text, or require credentials. Use fictional or sanitized
ticket text only; never send customer data or secrets.

## File structure

```text
api-deployment/
├── app.py            # Original standard-library server
├── fastapi_app.py    # Same API using FastAPI and Uvicorn
├── pyproject.toml    # Project settings and FastAPI dependencies
├── uv.lock           # Exact dependency versions for reproducible installs
├── README.md         # Setup, commands, and contract
└── .gitignore        # Ignore Python cache and virtual environment
```

## Dependency installation

Install Python 3 if it is not already available. Check it with:

```sh
python3 --version
```

The original `app.py` has no third-party dependencies and no `pip install` step.
All its imports come with Python.

## Run

From this directory:

```sh
python3 app.py
```

Leave this terminal running and execute the test commands in another terminal.
Stop the server with `Ctrl+C`. This built-in server is for local learning.

## FastAPI and Uvicorn version

This project uses uv to manage dependencies and its `.venv` environment.
Install uv if needed using the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
The project requires Python 3.14 or newer; uv can download a compatible Python
version if one is not available locally.

From this directory, install the dependencies recorded in `uv.lock`:

```sh
uv sync --locked
```

Run the FastAPI version with Uvicorn:

```sh
uv run uvicorn fastapi_app:app --host 127.0.0.1 --port 8000
```

Alternatively, run `uv run python fastapi_app.py`; it starts Uvicorn with the same local
host and port. Stop the original server first if it is using port 8000.
Leave this terminal running and use the same curl tests below in another terminal.
Both versions share the request/response contract below, including HTTP `400`
validation errors. Ticket text is not stored or logged by either version.

You do not need to activate the virtual environment: `uv run` uses it automatically.
To add another dependency later, use `uv add package-name`. Keep `pyproject.toml`
and `uv.lock` together when sharing the project. Package installation downloads
dependencies; the API itself makes no external connections.

## Health test

```sh
curl -i http://127.0.0.1:8000/health
```

Expected HTTP status: `200`. Response body:

```json
{"status": "ok"}
```

## Success test

```sh
curl -i -X POST http://127.0.0.1:8000/triage-ticket \
  -H 'Content-Type: application/json' \
  -d '{"ticket_text": "Fictional ticket: the demo robot cannot find its imaginary hat."}'
```

Expected HTTP status: `200`. Response body:

```json
{"category": "general", "summary": "Placeholder summary for this learning ticket."}
```

## Error tests

Missing field (a valid JSON body):

```sh
curl -i -X POST http://127.0.0.1:8000/triage-ticket \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Empty field (also a valid JSON body):

```sh
curl -i -X POST http://127.0.0.1:8000/triage-ticket \
  -H 'Content-Type: application/json' \
  -d '{"ticket_text": ""}'
```

Both return HTTP `400` with this controlled response:

```json
{"error": "ticket_text is required and must be a non-empty string."}
```

Whitespace-only strings, `null`, numbers, and other non-string field values
return the same validation error.

## Request/response contract

| Request | Input | Response |
| --- | --- | --- |
| `GET /health` | No body | `200`, `{"status": "ok"}` |
| `POST /triage-ticket` | JSON object with required `ticket_text`: non-empty string | `200`, fixed `category` and `summary` strings shown above |
| `POST /triage-ticket` | Missing, empty, whitespace-only, or non-string `ticket_text` | `400`, `{"error": "ticket_text is required and must be a non-empty string."}` |
| `POST /triage-ticket` | Malformed JSON or no body | `400`, `{"error": "Request body must be valid JSON."}` |
| `POST /triage-ticket` | Valid JSON that is not an object | `400`, `{"error": "Request body must be a JSON object."}` |
| Unknown GET or POST path | Any | `404`, `{"error": "Endpoint not found."}` |

Send POST bodies with `Content-Type: application/json`. Responses for the routes
above use JSON. Extra object fields are ignored. Placeholder output does not
classify or summarize the actual text.
