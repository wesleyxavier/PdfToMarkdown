"""Lifecycle management for local llama-server."""

import atexit
import logging
import os
import subprocess
import time
from collections.abc import Callable

import httpx

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = r"C:\LLamaModels\Qwen3-VL-4B-Instruct-Q4_K_M.gguf"
DEFAULT_PORT = 8081
HEALTH_URL_TEMPLATE = "http://localhost:{port}/health"

_current_server_process: subprocess.Popen | None = None


def is_port_in_use(port: int) -> bool:
    """Check if the given port is already in use locally."""
    try:
        with httpx.Client(timeout=1.0) as client:
            resp = client.get(f"http://localhost:{port}/health")
            return resp.status_code == 200 or resp.is_success
    except Exception:
        return False


def start_llama_server(
    model_path: str = DEFAULT_MODEL_PATH,
    port: int = DEFAULT_PORT,
    executable: str = "llama-server",
    extra_args: list[str] | None = None,
) -> subprocess.Popen:
    """Start the llama-server subprocess and register automatic cleanup."""
    global _current_server_process

    if _current_server_process is not None and _current_server_process.poll() is None:
        logger.info("llama-server is already running.")
        return _current_server_process

    cmd = [
        executable,
        "--model",
        model_path,
        "--port",
        str(port),
        "--embedding",
        "-b",
        "2048",
        "-c",
        "32768",
        "-np",
        "1",
        "--tools",
        "all",
        "-fa",
        "on",
        "-ctk",
        "q4_0",
        "-ctv",
        "q4_0",
        "--parallel",
        "1",
    ]
    if extra_args:
        cmd.extend(extra_args)

    logger.info("Starting llama-server: %s", " ".join(cmd))

    # On Windows, create subprocess with creationflags to handle signals properly if needed
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    except FileNotFoundError as err:
        logger.error("llama-server executable not found: %s", err)
        raise RuntimeError(
            f"O executável '{executable}' não foi encontrado no PATH do sistema. "
            "Certifique-se de instalar o llama.cpp localmente."
        ) from err

    _current_server_process = proc
    atexit.register(stop_llama_server, proc)
    return proc


def check_health(
    port: int = DEFAULT_PORT,
    timeout_seconds: float = 60.0,
    interval: float = 1.0,
    status_callback: Callable[[str], None] | None = None,
) -> bool:
    """Poll http://localhost:{port}/health until healthy or timeout expires."""
    url = HEALTH_URL_TEMPLATE.format(port=port)
    start_time = time.time()

    with httpx.Client(timeout=2.0) as client:
        while time.time() - start_time < timeout_seconds:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    if status_callback:
                        status_callback("llama-server pronto para receber requisições.")
                    return True
            except httpx.RequestError:
                pass

            elapsed = int(time.time() - start_time)
            if status_callback:
                status_callback(f"Carregando modelo no llama-server... ({elapsed}s)")
            time.sleep(interval)

    if status_callback:
        status_callback("Timeout aguardando inicialização do llama-server.")
    return False


def stop_llama_server(proc: subprocess.Popen | None = None) -> None:
    """Gracefully terminate or kill the llama-server subprocess."""
    global _current_server_process

    target = proc or _current_server_process
    if target is None:
        return

    if target.poll() is None:
        logger.info("Stopping llama-server process pid=%s...", target.pid)
        try:
            target.terminate()
            target.wait(timeout=5)
        except Exception:
            try:
                target.kill()
            except Exception:
                pass

    if target == _current_server_process:
        _current_server_process = None
