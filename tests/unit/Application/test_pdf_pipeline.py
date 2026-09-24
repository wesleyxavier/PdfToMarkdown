"""Unit tests for PDF pipeline functions."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import fitz
import pytest

from PdfToMarkdown.pdf_pipeline import (
    assemble_markdown,
    convert_pdf_to_markdown,
    ocr_page_image,
)


def test_assemble_markdown_single_page():
    page_results = [(1, "# Título da Página 1\n\nConteúdo transcrito.")]
    result = assemble_markdown(page_results)
    assert "<!-- Page 1 -->" in result
    assert "# Título da Página 1" in result


def test_assemble_markdown_multiple_pages():
    page_results = [
        (1, "Texto Página 1"),
        (2, "Texto Página 2"),
        (3, "Texto Página 3"),
    ]
    result = assemble_markdown(page_results)
    assert "<!-- Page 1 -->" in result
    assert "<!-- Page 2 -->" in result
    assert "<!-- Page 3 -->" in result
    assert "---\n\n<!-- Page 2 -->" in result


def test_ocr_page_image_calls_openai_correctly():
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "## Markdown Mockado da Imagem"
    mock_response = MagicMock(choices=[mock_choice])
    mock_client.chat.completions.create.return_value = mock_response

    output = ocr_page_image(
        client=mock_client,
        base64_image="fake_base64_string",
        model="test-model",
    )

    assert output == "## Markdown Mockado da Imagem"
    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "test-model"
    assert "fake_base64_string" in str(call_kwargs["messages"])


def test_convert_pdf_to_markdown_file_not_found():
    with pytest.raises(FileNotFoundError):
        convert_pdf_to_markdown("caminho_inexistente.pdf")


def test_convert_pdf_to_markdown_success(tmp_path: Path):
    # Criar um PDF real pequeno
    pdf_file = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_text((20, 20), "Hello Test PDF")
    doc.save(str(pdf_file))
    doc.close()

    output_file = tmp_path / "output.md"

    with patch("PdfToMarkdown.pdf_pipeline.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "# Página Transcrita"
        mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
        mock_openai_cls.return_value = mock_client

        logs = []
        result_path = convert_pdf_to_markdown(
            pdf_path=pdf_file,
            output_path=output_file,
            progress_callback=lambda msg, t: logs.append((msg, t)),
        )

        assert Path(result_path).exists()
        content = Path(result_path).read_text(encoding="utf-8")
        assert "<!-- Page 1 -->" in content
        assert "# Página Transcrita" in content
        assert any("sucesso" in t for _, t in logs)


def test_convert_pdf_to_markdown_cancellation(tmp_path: Path):
    pdf_file = tmp_path / "sample.pdf"
    doc = fitz.open()
    doc.new_page(width=200, height=200)
    doc.save(str(pdf_file))
    doc.close()

    with patch("PdfToMarkdown.pdf_pipeline.OpenAI"), pytest.raises(InterruptedError):
        convert_pdf_to_markdown(
            pdf_path=pdf_file,
            should_cancel=lambda: True,
        )

