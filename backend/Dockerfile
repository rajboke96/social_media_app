FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY src/requirements.txt src/auth_app/requirements.txt ./src/
RUN pip install --upgrade pip && \
    pip install -r src/requirements.txt -r src/auth_app/requirements.txt

COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
