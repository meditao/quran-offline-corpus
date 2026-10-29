"""Kur'an araştırma uygulamasını üretip yalnız bu bilgisayarda sunar."""

from __future__ import annotations

import argparse
import functools
import json
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from build import build
from tezgah.veri import VeriHatasi


class LocalHandler(SimpleHTTPRequestHandler):
    """Statik dosyalar; veri veya araştırma kayıtlarına yazan bir uç yoktur."""

    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".html": "text/html; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".md": "text/plain; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
    }

    def end_headers(self):
        # Tarayıcı önbelleğinin yeni bir üretimi eski dosyalarla karıştırmasını önler.
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "Dizin listesi sunulmuyor")
        return None


def create_server(directory: Path, port: int = 8765) -> ThreadingHTTPServer:
    handler = functools.partial(LocalHandler, directory=str(directory.resolve()))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    return server


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Offline Kur'an araştırma uygulaması")
    parser.add_argument("--port", type=int, default=8765, help="Yerel port (varsayılan: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma")
    parser.add_argument("--no-build", action="store_true", help="Mevcut dist çıktısını kullan")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("Port 1–65535 arasında olmalıdır")
    directory = Path(__file__).resolve().parent / "dist"
    try:
        if args.no_build:
            with (directory / "manifest.json").open(encoding="utf-8") as source:
                manifest = json.load(source)
            if not manifest.get("files") or not (directory / "index.html").is_file():
                raise ValueError("Üretilmiş uygulama eksik; --no-build olmadan başlatın")
        else:
            print("Yerel korpustan uygulama hazırlanıyor…", flush=True)
            directory = build()
        server = create_server(directory, args.port)
    except (OSError, ValueError, KeyError, VeriHatasi) as exc:
        print(f"Başlatılamadı: {exc}", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Kur'an Araştırma Masası: {url}", flush=True)
    print("İnternet gerekmez. Kapatmak için Ctrl+C.", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nYerel sunucu kapatıldı.", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
