"""The learning ticket API, implemented with FastAPI and Uvicorn.

Use fictional or sanitized ticket text. No tickets are stored or sent elsewhere.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


app = FastAPI(title="Local learning ticket API")


@app.exception_handler(HTTPException)
async def handle_http_error(request: Request, error: HTTPException):
    """Keep unknown endpoint responses consistent with the original API."""
    if error.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "Endpoint not found."})
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail},
        headers=error.headers,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/triage-ticket")
async def triage_ticket(request: Request):
    # Validate manually to preserve the original API's 400 error responses.
    try:
        data = await request.json()
    except (ValueError, UnicodeDecodeError):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be valid JSON."},
        )

    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object."},
        )

    ticket_text = data.get("ticket_text")
    if not isinstance(ticket_text, str) or not ticket_text.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "ticket_text is required and must be a non-empty string."},
        )

    # Fixed placeholders: no model, external service, or database is used.
    return {
        "category": "general",
        "summary": "Placeholder summary for this learning ticket.",
    }


if __name__ == "__main__":
    import uvicorn

    # Listen only on this computer.
    uvicorn.run(app, host="127.0.0.1", port=8000)
