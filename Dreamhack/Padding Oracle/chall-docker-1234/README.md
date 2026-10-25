# GuestBook Challenge - Docker

## Chạy challenge

```bash
docker compose up -d --build
```

Challenge sẽ chạy tại:

```text
http://localhost:1234
```

Kiểm tra nhanh:

```bash
curl http://localhost:1234/
```

Dừng challenge:

```bash
docker compose down
```

Xem log:

```bash
docker compose logs -f
```
