#!/usr/bin/env python3
"""Mock server mimicking app.py's /secure/decrypt oracle (AES-CBC, key random, IV=0)
plus a /ct endpoint that hands out the target ciphertext. For testing poattack locally."""
import base64
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from Cryptodome.Cipher import AES

KEY = os.urandom(16)
IV = b"\x00" * 16
PASSWORD = "abPz9Q#x"  # 8 ký tự, "bí mật"


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/ct":
            body = json.dumps({"content": f"The password is: {PASSWORD}", "author": "admin"}).encode()
            pad = 16 - len(body) % 16
            body += bytes([pad]) * pad
            ct = AES.new(KEY, AES.MODE_CBC, IV).encrypt(body)
            return self._send({"enc_data": base64.b64encode(ct).decode()})
        if u.path == "/secure/decrypt":
            if "e_data" not in q or "token" not in q or "sig" not in q:
                return self._send({"status": "error"})
            try:
                pt = AES.new(KEY, AES.MODE_CBC, IV).decrypt(base64.b64decode(q["e_data"][0]))
                n = pt[-1]
                if not (1 <= n <= 16) or pt[-n:] != bytes([n]) * n:
                    raise ValueError("Padding is incorrect.")
                pt = pt[:-n]
            except Exception:
                # ValueError / binascii.Error — y hệt nhánh except ValueError của app.py
                return self._send({"status": "error", "result": {"message": "ValueError"}})
            try:
                json.loads(pt.decode("latin-1"))
            except Exception:
                return self._send({"status": "error", "result": {"message": "JSONDecodeError"}})
            return self._send({"status": "error", "result": {"message": "you don't have a permission."}})
        return self._send({"status": "error"})

    def _send(self, obj):
        b = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("mock oracle on http://127.0.0.1:8080  (GET /ct, GET /secure/decrypt)")
    HTTPServer(("127.0.0.1", 8080), H).serve_forever()
