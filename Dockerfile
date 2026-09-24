# Stage 1: Build
FROM python:3.13-slim AS build
WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.13-slim AS final
WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app/src /app/src

ENV PYTHONUNBUFFERED=1

CMD ["python", "-c", "import PdfToMarkdown; print(f'PdfToMarkdown {PdfToMarkdown.__version__}')"]
