"""Unit tests for llama_lifecycle."""

from unittest.mock import MagicMock, patch

import httpx

from PdfToMarkdown.llama_lifecycle import (
    check_health,
    is_port_in_use,
    stop_llama_server,
)


def test_is_port_in_use_true():
    with patch("httpx.Client") as mock_client_cls:
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_instance.get.return_value.status_code = 200
        mock_instance.get.return_value.is_success = True

        assert is_port_in_use(8081) is True


def test_is_port_in_use_false_on_connection_error():
    with patch("httpx.Client") as mock_client_cls:
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_instance.get.side_effect = httpx.ConnectError("Connection refused")

        assert is_port_in_use(8081) is False


def test_check_health_success():
    with patch("httpx.Client") as mock_client_cls:
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_instance.get.return_value.status_code = 200

        callback_msgs = []
        result = check_health(
            port=8081,
            timeout_seconds=5.0,
            interval=0.1,
            status_callback=callback_msgs.append,
        )

        assert result is True
        assert len(callback_msgs) >= 1
        assert "pronto" in callback_msgs[-1]


def test_check_health_timeout():
    with patch("httpx.Client") as mock_client_cls:
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_instance.get.side_effect = httpx.RequestError("Server down")

        callback_msgs = []
        result = check_health(
            port=8081,
            timeout_seconds=0.2,
            interval=0.05,
            status_callback=callback_msgs.append,
        )

        assert result is False
        assert any("Timeout" in msg for msg in callback_msgs)


def test_stop_llama_server():
    mock_proc = MagicMock()
    mock_proc.poll.return_value = None
    stop_llama_server(mock_proc)
    mock_proc.terminate.assert_called_once()
