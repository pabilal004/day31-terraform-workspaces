FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --no-compile -r requirements.txt \
    && groupadd --system app \
    && useradd --system --uid 10001 --gid app --home-dir /app app
COPY --chown=10001:app app/ .
USER 10001:app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "app:app"]
