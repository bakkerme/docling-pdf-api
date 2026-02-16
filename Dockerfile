ARG NVIDIA_PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:26.01-py3

FROM python:3.12-slim AS cpu
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
EXPOSE 8000

COPY pyproject.toml README.md ./
COPY app.py ./

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install .

RUN apt update && apt install -y \
    build-essential \
    libxcb1 libgl1 libglib2.0-0

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

FROM ${NVIDIA_PYTORCH_IMAGE} AS nvidia
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
EXPOSE 8000

COPY pyproject.toml README.md ./
COPY app.py ./

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install .

RUN apt update && apt install -y \
    build-essential \
    libxcb1 libgl1 libglib2.0-0

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
