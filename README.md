# docling-pdf-api

FastAPI service that converts a remote PDF URL (for example arXiv PDFs) into Markdown using Docling.

## API

### Health

```bash
curl http://localhost:8000/healthz
```

### Convert PDF URL to Markdown

```bash
curl -G "http://localhost:8000/convert" \
  --data-urlencode "url=https://arxiv.org/pdf/2602.05868"
```

Successful responses are raw Markdown with `Content-Type: text/markdown`.

## Docker builds

### CPU image

```bash
docker build --target cpu -t docling-pdf-api:cpu .
```

### NVIDIA image (Grace Blackwell / GPU hosts)

```bash
docker build --target nvidia -t docling-pdf-api:nvidia .
```

Default NVIDIA base image is pinned in `Dockerfile`:

- `nvcr.io/nvidia/pytorch:26.01-py3`

Override it if needed:

```bash
docker build \
  --target nvidia \
  --build-arg NVIDIA_PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:<tag>-py3 \
  -t docling-pdf-api:nvidia .
```

## Docker run

### CPU

```bash
docker run --rm -p 8000:8000 docling-pdf-api:cpu
```

### CPU with Docker Compose

```bash
docker compose up --build
```

### GPU

```bash
docker run --rm --gpus all -p 8000:8000 docling-pdf-api:nvidia
```

## GitHub Actions and GHCR

Manual publish workflow: `.github/workflows/publish.yml`

### Inputs

- `version`: required release version (`X.Y.Z` or `vX.Y.Z`)
- `publish_latest`: boolean, default `true`

### Published image

- `ghcr.io/<owner>/docling-pdf-api`

### Tags

- CPU:
  - `<version>-cpu`
  - `<shortsha>-cpu`
  - `latest-cpu` (when `publish_latest=true`)
- NVIDIA:
  - `<version>-nvidia`
  - `<shortsha>-nvidia`
  - `latest-nvidia` (when `publish_latest=true`)

Example pulls:

```bash
docker pull ghcr.io/<owner>/docling-pdf-api:1.2.3-cpu
docker pull ghcr.io/<owner>/docling-pdf-api:1.2.3-nvidia
```
