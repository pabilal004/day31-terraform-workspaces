"""Small dependency-free application used by the Day 54 CI/CD security lab."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def calculate_total(price: float, quantity: int) -> float:
    """Return a simple order total after validating input."""
    if price < 0 or quantity < 0:
        raise ValueError("price and quantity must not be negative")
    return round(price * quantity, 2)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_error(404, "Not found")
            return

        body = json.dumps({"status": "ok"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        # Keep the demo server's output concise.
        print("%s - %s" % (self.address_string(), format_string % args))


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), RequestHandler).serve_forever()
