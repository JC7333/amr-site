"""Sert le site en local comme Vercel le sert (adresses sans .html, page 404).

    python tools/serve.py [port]      puis ouvrir http://127.0.0.1:8000/
"""

import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Les mêmes en-têtes que la production (vercel.json), pour voir ici ce que la politique de sécurité bloquerait.
HEADERS = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))["headers"][0]["headers"]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_head(self):
        path = self.path.split("?")[0].split("#")[0]
        target = ROOT / path.lstrip("/")
        if not path.endswith("/") and not target.exists() and target.with_suffix(".html").exists():
            self.path = path + ".html"
        elif not target.exists():
            self.send_response(404)
            body = (ROOT / "404.html").read_bytes()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return None
        return super().send_head()

    def end_headers(self):
        for header in HEADERS:
            self.send_header(header["key"], header["value"])
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"http://127.0.0.1:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
