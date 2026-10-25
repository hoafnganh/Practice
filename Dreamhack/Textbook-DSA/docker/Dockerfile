FROM python:3.6-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# guard: build fail nếu requirements.txt lỡ đổi sang bản đã vá (3.17+)
RUN python -c "from Crypto.Util.number import inverse; assert inverse(7,7)==0, 'pycryptodome da fix bug inverse'"

COPY chall.py flag ./

# TCP forker thay socat — mỗi connection spawn một process chall.py mới
COPY <<'EOF' /app/serve.py
import socketserver, subprocess

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        fd = self.request.fileno()
        subprocess.run(["python", "-u", "chall.py"], stdin=fd, stdout=fd, stderr=fd)

socketserver.ThreadingTCPServer.allow_reuse_address = True
socketserver.ThreadingTCPServer(("0.0.0.0", 1337), Handler).serve_forever()
EOF

EXPOSE 1337
CMD ["python", "-u", "serve.py"]
