"""Pipeline for converting PDF pages to Markdown via local visual OCR."""

import base64
from collections.abc import Callable
from pathlib import Path

import pymupdf as fitz
from openai import OpenAI

DEFAULT_OCR_PROMPT = (
    "Transcreva o conteúdo desta página de documento para Markdown limpo e fiel, "
    "preservando títulos (#, ##), listas, tabelas e formatação original. "
    "Retorne estritamente o conteúdo transcrito em Markdown."
)


def render_page_to_base64(page: fitz.Page, dpi: int = 150) -> str:
    """Render a PDF page to PNG image and encode as base64 string."""
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode("utf-8")


def ocr_page_image(
    client: OpenAI,
    base64_image: str,
    model: str = "Gemma-4-12b-it-qat-q4_0.gguf",
    prompt: str = DEFAULT_OCR_PROMPT,
) -> str:
    """Send base64 image to local vision LLM and return Markdown transcription."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
        temperature=0.1,
    )
    content = response.choices[0].message.content or ""
    return content.strip()


def assemble_markdown(page_results: list[tuple[int, str]]) -> str:
    """Combine page Markdown transcriptions with page indicators."""
    sections = []
    for page_num, text in page_results:
        sections.append(f"<!-- Page {page_num} -->\n\n{text}")
    return "\n\n---\n\n".join(sections)


def convert_pdf_to_markdown(
    pdf_path: str | Path,
    output_path: str | Path | None = None,
    base_url: str = "http://localhost:8081/v1",
    api_key: str = "not-needed",
    model: str = "Gemma-4-12b-it-qat-q4_0.gguf",
    progress_callback: Callable[[str, str], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> str:
    """Execute complete PDF to Markdown conversion pipeline.

    Args:
        pdf_path: Path to the input PDF file.
        output_path: Destination .md path. If None, saves in the same folder as the PDF.
        base_url: OpenAI compatible base URL.
        api_key: API key for client.
        model: Model name.
        progress_callback: Callback(message, message_type) for status reporting.
        should_cancel: Function returning True if execution was cancelled.

    Returns:
        Absolute path to the generated Markdown file.
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_file}")

    if output_path is None:
        output_file = pdf_file.with_suffix(".md")
    else:
        output_file = Path(output_path)

    client = OpenAI(base_url=base_url, api_key=api_key)

    def log(msg: str, msg_type: str = "system") -> None:
        if progress_callback:
            progress_callback(msg, msg_type)

    log(f"Abrindo documento: {pdf_file.name}", "system")
    doc = fitz.open(str(pdf_file))
    total_pages = len(doc)
    log(f"Total de páginas detectadas: {total_pages}", "system")

    page_results: list[tuple[int, str]] = []

    try:
        for idx in range(total_pages):
            if should_cancel and should_cancel():
                log("Processamento cancelado pelo usuário.", "aviso")
                raise InterruptedError("Conversão abortada pelo usuário.")

            page_num = idx + 1
            log(f"Renderizando página {page_num}/{total_pages}...", "system")
            page = doc.load_page(idx)
            b64_img = render_page_to_base64(page)

            log(f"Enviando página {page_num} para o modelo local...", "system")
            try:
                markdown_text = ocr_page_image(client, b64_img, model=model)
            except Exception as exc:
                log(f"Falha ao processar página {page_num}: {exc}", "erro")
                raise RuntimeError(f"Erro na inferência da página {page_num}: {exc}") from exc

            page_results.append((page_num, markdown_text))
            log(f"Página {page_num}/{total_pages} transcrita com sucesso.", "sucesso")

    finally:
        doc.close()

    log("Consolidando Markdown final...", "system")
    final_content = assemble_markdown(page_results)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(final_content, encoding="utf-8")

    abs_path = str(output_file.resolve())
    log(f"Conversão concluída com sucesso! Arquivo salvo em:\n{abs_path}", "sucesso")
    return abs_path
