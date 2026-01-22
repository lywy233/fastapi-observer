import json
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
import uvicorn

BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"

app = FastAPI(title="HTTP Request Observer")


def safe_decode(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="ignore")


@app.api_route("/{path:path}", methods=[
    "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"
])
async def observe(request: Request, path: str):
    # ---- basic info ----
    request_id = str(uuid.uuid4())
    now = datetime.utcnow()

    # ---- body ----
    body_bytes = await request.body()
    body_text = safe_decode(body_bytes)

    # try parse json
    parsed_json = None
    try:
        parsed_json = json.loads(body_text)
    except Exception:
        pass

    # ---- headers ----
    headers = dict(request.headers)

    # ---- full url ----
    full_url = str(request.url)

    # ---- client info ----
    client = request.client.host if request.client else None

    # ---- assemble record ----
    record = {
        "request_id": request_id,
        "timestamp": now.isoformat() + "Z",
        "method": request.method,
        "path": "/" + path,
        "url": full_url,
        "client_ip": client,
        "headers": headers,
        "body": {
            "raw": body_text,
            "json": parsed_json
        }
    }

    # ---- write to file ----
    date_dir = STORAGE_DIR / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)

    filename = f"req-{now.strftime('%H%M%S')}-{request_id[:8]}.json"
    filepath = date_dir / filename

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    # ---- response ----
    return {
        "status": "ok",
        "request_id": request_id
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=False,   # 本地调试可改为 True
        log_level="info",
    )
