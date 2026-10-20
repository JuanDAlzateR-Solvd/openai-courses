"""A learning API using only Python's standard library.

Use fictional or sanitized ticket text. This app does not store tickets.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class TicketAPI(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):
        """Send a JSON response with an HTTP status code."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "Endpoint not found."})

    def do_POST(self):
        if self.path != "/triage-ticket":
            self.send_json(404, {"error": "Endpoint not found."})
            return

        # Read the JSON request body. No ticket text is saved or logged.
        try:
            body_length = int(self.headers.get("Content-Length", "0"))
            if body_length < 0:
                raise ValueError("Invalid body length")
            body = self.rfile.read(body_length)
            data = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            self.send_json(400, {"error": "Request body must be valid JSON."})
            return

        # A JSON object must contain a non-empty string named ticket_text.
        if not isinstance(data, dict):
            self.send_json(400, {"error": "Request body must be a JSON object."})
            return

        ticket_text = data.get("ticket_text")
        if not isinstance(ticket_text, str) or not ticket_text.strip():
            self.send_json(
                400,
                {"error": "ticket_text is required and must be a non-empty string."},
            )
            return

        # Fixed placeholders: no AI model or external service is called.
        self.send_json(
            200,
            {
                "category": "general",
                "summary": "Placeholder summary for this learning ticket.",
            },
        )


if __name__ == "__main__":
    # Listen only on this computer, so the API is local by default.
    server = ThreadingHTTPServer(("127.0.0.1", 8000), TicketAPI)
    print("Learning API running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping API.")
    finally:
        server.server_close()
