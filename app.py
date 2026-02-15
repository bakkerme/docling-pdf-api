import logging
import time

from docling.document_converter import DocumentConverter
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import HttpUrl


logger = logging.getLogger("docling_pdf_api")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Docling PDF API", version="0.1.0")
converter = DocumentConverter()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/convert", response_class=PlainTextResponse)
def convert(url: HttpUrl) -> PlainTextResponse:
    start = time.perf_counter()
    logger.info("conversion_requested url=%s", url)

    try:
        result = converter.convert(str(url))
        markdown = result.document.export_to_markdown()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("conversion_failed url=%s", url)
        raise HTTPException(status_code=502, detail=f"Conversion failed: {exc}") from exc

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    logger.info("conversion_completed url=%s elapsed_ms=%.2f", url, elapsed_ms)
    return PlainTextResponse(content=markdown, media_type="text/markdown")
