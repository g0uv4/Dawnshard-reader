#!/usr/bin/env python3
"""Serve a Snippet Reader data folder locally so dashboard.html can fetch state.json.

Usage: python3 scripts/serve_dashboard.py [folder] [port]
"""
import functools, http.server, sys, pathlib

folder = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".snippet-reader").resolve()
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(folder))
print(f"Dashboard: http://localhost:{port}/dashboard.html  (serving {folder})")
http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
