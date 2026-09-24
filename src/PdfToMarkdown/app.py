"""Modern CustomTkinter desktop interface for PdfToMarkdown."""

import os
import threading
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from PdfToMarkdown.llama_lifecycle import (
    check_health,
    start_llama_server,
    stop_llama_server,
)
from PdfToMarkdown.pdf_pipeline import convert_pdf_to_markdown

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_MAP = {
    "sistema": ("#1e293b", "#334155"),  # bg, border
    "aviso": ("#78350f", "#b45309"),
    "sucesso": ("#064e3b", "#059669"),
    "erro": ("#7f1d1d", "#dc2626"),
}


class PdfToMarkdownApp(ctk.CTk):
    """Main application window with dark mode, chat bubbles, and permission gates."""

    def __init__(self) -> None:
        super().__init__()

        self.title("PdfToMarkdown — OCR Visual com LLM Local")
        self.geometry("860x680")
        self.minsize(700, 520)

        self.selected_pdf_path: str | None = None
        self.is_converting = False
        self.permission_event = threading.Event()
        self.permission_granted = False
        self.server_ready = False

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Start llama-server and health-check in background
        self._start_server_background()

    def _build_ui(self) -> None:
        # Header / File selection section
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(fill="x", padx=16, pady=(16, 8))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Conversor de PDF para Markdown",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.pack(anchor="w", padx=16, pady=(12, 4))

        self.btn_row = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btn_row.pack(fill="x", padx=16, pady=(0, 12))

        self.btn_select_file = ctk.CTkButton(
            self.btn_row,
            text="📄 Selecionar PDF",
            command=self._choose_file,
            width=160,
            height=34,
        )
        self.btn_select_file.pack(side="left", padx=(0, 8))

        self.btn_select_dir = ctk.CTkButton(
            self.btn_row,
            text="📁 Buscar em Pasta",
            command=self._choose_directory,
            width=160,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
        )
        self.btn_select_dir.pack(side="left", padx=(0, 12))

        self.lbl_selected_file = ctk.CTkLabel(
            self.btn_row,
            text="Nenhum arquivo selecionado",
            text_color="#94a3b8",
            anchor="w",
        )
        self.lbl_selected_file.pack(side="left", fill="x", expand=True)

        # Log / Chat bubbles area
        self.chat_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=10,
            fg_color="#0f172a",
        )
        self.chat_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Action / Permission Gate Section
        self.footer_frame = ctk.CTkFrame(self, corner_radius=10)
        self.footer_frame.pack(fill="x", padx=16, pady=(8, 16))

        self.btn_start = ctk.CTkButton(
            self.footer_frame,
            text="🚀 Iniciar Conversão",
            command=self._start_conversion,
            width=180,
            height=38,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.btn_start.pack(side="left", padx=16, pady=12)

        # Permission Gate buttons (initially hidden/disabled)
        self.gate_container = ctk.CTkFrame(self.footer_frame, fg_color="transparent")

        self.lbl_gate = ctk.CTkLabel(
            self.gate_container,
            text="Confirmar envio das páginas para o modelo?",
            font=ctk.CTkFont(weight="bold"),
            text_color="#f59e0b",
        )
        self.lbl_gate.pack(side="left", padx=(0, 12))

        self.btn_allow = ctk.CTkButton(
            self.gate_container,
            text="✓ Permitir e Continuar",
            fg_color="#059669",
            hover_color="#047857",
            command=self._on_allow,
            height=34,
        )
        self.btn_allow.pack(side="left", padx=(0, 8))

        self.btn_deny = ctk.CTkButton(
            self.gate_container,
            text="✗ Recusar / Abortar",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self._on_deny,
            height=34,
        )
        self.btn_deny.pack(side="left")

    def add_bubble(self, message: str, msg_type: str = "sistema") -> None:
        """Post a status message bubble to the chat feed on the UI thread."""
        self.after(0, self._render_bubble, message, msg_type)

    def _render_bubble(self, message: str, msg_type: str) -> None:
        bg_color, border_color = COLOR_MAP.get(msg_type, COLOR_MAP["sistema"])

        bubble = ctk.CTkFrame(
            self.chat_frame,
            fg_color=bg_color,
            border_color=border_color,
            border_width=1,
            corner_radius=10,
        )
        bubble.pack(fill="x", padx=8, pady=4, anchor="w")

        lbl = ctk.CTkLabel(
            bubble,
            text=message,
            justify="left",
            wraplength=760,
            font=ctk.CTkFont(size=13),
            padx=12,
            pady=8,
        )
        lbl.pack(anchor="w")

        # Scroll to bottom
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def _choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")],
        )
        if path:
            self._set_selected_pdf(path)

    def _choose_directory(self) -> None:
        folder = filedialog.askdirectory(title="Selecione uma pasta contendo PDFs")
        if not folder:
            return

        pdf_files = list(Path(folder).glob("*.pdf"))
        if not pdf_files:
            self.add_bubble(f"Nenhum arquivo PDF encontrado em: {folder}", "aviso")
            return

        # Let user select one of the found PDFs via open dialog in that folder
        selected = filedialog.askopenfilename(
            initialdir=folder,
            title=f"Encontrados {len(pdf_files)} PDFs — selecione um para converter",
            filetypes=[("Arquivos PDF", "*.pdf")],
        )
        if selected:
            self._set_selected_pdf(selected)

    def _set_selected_pdf(self, path: str) -> None:
        self.selected_pdf_path = path
        filename = Path(path).name
        self.lbl_selected_file.configure(
            text=f"{filename} ({path})",
            text_color="#f8fafc",
        )
        self.add_bubble(f"PDF selecionado: {filename}", "sistema")

    def _start_server_background(self) -> None:
        """Launch llama-server and monitor health in a daemon thread."""
        def run():
            self.add_bubble("Iniciando llama-server local com Gemma-4-12B Vision...", "sistema")
            model_dir = r"C:\LLamaModels"
            if os.path.exists(model_dir):
                has_mmproj = any("mmproj" in f.lower() and f.endswith(".gguf") for f in os.listdir(model_dir))
                if not has_mmproj:
                    self.add_bubble(
                        "Aviso: Nenhum arquivo 'mmproj-*.gguf' encontrado em C:\\LLamaModels. "
                        "Modelos de visão necessitam do projector multimodal (mmproj) para processar imagens.",
                        "aviso",
                    )

            try:
                start_llama_server()
            except Exception as err:
                self.add_bubble(f"Falha ao iniciar processo llama-server: {err}", "erro")
                return


            healthy = check_health(status_callback=lambda msg: self.add_bubble(msg, "sistema"))
            if healthy:
                self.server_ready = True
                self.add_bubble("Servidor local pronto! Selecione um PDF para começar.", "sucesso")
            else:
                self.add_bubble(
                    "O servidor local não respondeu dentro do tempo limite. Verifique se o modelo está baixado.",
                    "erro",
                )

        threading.Thread(target=run, daemon=True).start()

    def _start_conversion(self) -> None:
        if not self.selected_pdf_path:
            self.add_bubble("Por favor, selecione um arquivo PDF antes de iniciar.", "aviso")
            return

        if self.is_converting:
            self.add_bubble("Uma conversão já está em andamento.", "aviso")
            return

        self.is_converting = True
        self.btn_start.configure(state="disabled")

        # Run conversion pipeline in a worker thread
        threading.Thread(target=self._run_pipeline_worker, daemon=True).start()

    def _run_pipeline_worker(self) -> None:
        self.add_bubble("Aguardando verificação do gate de permissão...", "aviso")

        # Show permission gate buttons on main thread
        self.after(0, self._show_permission_gate)

        # Wait for user permission
        self.permission_event.clear()
        self.permission_event.wait()

        self.after(0, self._hide_permission_gate)

        if not self.permission_granted:
            self.add_bubble("Conversão cancelada pelo usuário no gate de permissão.", "aviso")
            self._finish_conversion()
            return

        self.add_bubble("Permissão concedida. Iniciando renderização e OCR...", "sucesso")

        try:
            convert_pdf_to_markdown(
                pdf_path=self.selected_pdf_path,
                progress_callback=self.add_bubble,
                should_cancel=lambda: not self.permission_granted,
            )
        except Exception as exc:
            self.add_bubble(f"Erro durante a execução do pipeline: {exc}", "erro")
        finally:
            self._finish_conversion()

    def _show_permission_gate(self) -> None:
        self.gate_container.pack(side="left", padx=16, pady=12)

    def _hide_permission_gate(self) -> None:
        self.gate_container.pack_forget()

    def _on_allow(self) -> None:
        self.permission_granted = True
        self.permission_event.set()

    def _on_deny(self) -> None:
        self.permission_granted = False
        self.permission_event.set()

    def _finish_conversion(self) -> None:
        self.is_converting = False
        self.after(0, lambda: self.btn_start.configure(state="normal"))

    def _on_close(self) -> None:
        """Handle window close event and stop server."""
        try:
            stop_llama_server()
        except Exception:
            pass
        self.destroy()


def main() -> None:
    """Application entrypoint."""
    app = PdfToMarkdownApp()
    app.mainloop()


if __name__ == "__main__":
    main()
