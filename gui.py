"""
GUI for the HIBP tool
---------------------

Uses existing modules:
- api_client: API calls + error classes
- data_processing: dataclasses + parsers + risk score
- ui_format: formatting functions (ANSI will be stripped)
- utils_and_tests: validate_email

The backend remains unchanged. This GUI is only a visual layer on top.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox

from api_client import (
    get_breached_account,
    get_paste_account,
    get_all_breaches,
    get_data_classes,
    ApiError,
    RateLimitError,
)
from data_processing import (
    parse_breach_list,
    parse_paste_list,
    build_breach_summary,
)
from ui_format import (
    format_breach_list,
    format_paste_list,
    format_breach_summary,
    format_info,
    format_warning,
)
from utils_and_tests import validate_email


# ==== Color definitions in HIBP style ====

HIBP_PRIMARY = "#1A8CFF"   # main blue
BG_MAIN = "#0F1626"        # main background (dark, but not pure black)
BG_PANEL = "#172235"       # header / panels
BG_OUTPUT = "#111C2E"      # output text area
FG_TEXT = "#E8ECF2"        # normal text
FG_MUTED = "#9CA3AF"       # subtle text (status bar etc.)


# ==== Remove ANSI/colorama escape sequences from strings ====

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string."""
    return ANSI_ESCAPE_RE.sub("", text)


# ==== GUI class ====

class HibpGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Have I Been Pwned – Checker (GUI)")
        self.configure(bg=BG_MAIN)
        self.geometry("950x620")

        # ttk styles
        style = ttk.Style(self)
        style.theme_use("clam")

        # Frames
        style.configure(
            "Main.TFrame",
            background=BG_MAIN,
        )
        style.configure(
            "Header.TFrame",
            background=BG_PANEL,
        )

        # Labels
        style.configure(
            "TLabel",
            background=BG_MAIN,
            foreground=FG_TEXT,
        )
        style.configure(
            "Header.TLabel",
            background=BG_PANEL,
            foreground=FG_TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background=BG_MAIN,
            foreground=FG_MUTED,
            font=("Segoe UI", 9),
        )

        # Buttons
        style.configure(
            "Accent.TButton",
            background=HIBP_PRIMARY,
            foreground="white",
            padding=8,
            borderwidth=0,
            focusthickness=0,
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[
                ("active", "#4EA3FF"),
                ("pressed", "#1664C5"),
            ],
            foreground=[("disabled", "#D1D5DB")],
        )

        # ----- Header area -----
        header_frame = ttk.Frame(self, style="Header.TFrame")
        header_frame.pack(side=tk.TOP, fill=tk.X)

        header_label = ttk.Label(
            header_frame,
            text="Have I Been Pwned – Checker",
            style="Header.TLabel",
        )
        header_label.pack(side=tk.LEFT, padx=16, pady=10)

        subtitle_label = ttk.Label(
            header_frame,
            text="Check email addresses for data breaches and pastes (HIBP API v3)",
            background=BG_PANEL,
            foreground=FG_MUTED,
            font=("Segoe UI", 9),
        )
        subtitle_label.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        # ----- Input area -----
        input_frame = ttk.Frame(self, style="Main.TFrame")
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=16, pady=(12, 4))

        email_label = ttk.Label(input_frame, text="Email address:")
        email_label.grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(input_frame, textvariable=self.email_var, width=40)
        email_entry.grid(row=0, column=1, sticky="w")
        email_entry.bind("<Return>", lambda event: self.on_check_breaches())

        hint_label = ttk.Label(
            input_frame,
            text="Press Enter to run “Check Email for breaches”.",
            style="SubHeader.TLabel",
        )
        hint_label.grid(row=1, column=1, sticky="w", pady=(4, 0))

        # ----- Button area -----
        button_frame = ttk.Frame(self, style="Main.TFrame")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=16, pady=(4, 8))

        btn_breaches = ttk.Button(
            button_frame,
            text="Check Email for breaches",
            style="Accent.TButton",
            command=self.on_check_breaches,
        )
        btn_breaches.grid(row=0, column=0, padx=5, pady=4, sticky="w")

        btn_pastes = ttk.Button(
            button_frame,
            text="Show Pastes for email",
            style="Accent.TButton",
            command=self.on_show_pastes,
        )
        btn_pastes.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        btn_all_breaches = ttk.Button(
            button_frame,
            text="Show all breaches",
            style="Accent.TButton",
            command=self.on_show_all_breaches,
        )
        btn_all_breaches.grid(row=0, column=2, padx=5, pady=4, sticky="w")

        btn_data_classes = ttk.Button(
            button_frame,
            text="Show data classes",
            style="Accent.TButton",
            command=self.on_show_data_classes,
        )
        btn_data_classes.grid(row=0, column=3, padx=5, pady=4, sticky="w")

        button_frame.grid_columnconfigure(4, weight=1)

        # ----- Output area (Text + Scrollbar) -----
        output_frame = ttk.Frame(self, style="Main.TFrame")
        output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.output_text = tk.Text(
            output_frame,
            wrap="word",
            bg=BG_OUTPUT,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            font=("Consolas", 10),
            relief="flat",
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            output_frame,
            orient=tk.VERTICAL,
            command=self.output_text.yview,
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        self.output_text.configure(state=tk.DISABLED)

        # ----- Status bar -----
        status_frame = ttk.Frame(self, style="Main.TFrame")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=(0, 8))

        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            foreground=FG_MUTED,
        )
        self.status_label.pack(side=tk.LEFT)

    # ---------- Helper methods ----------

    def set_output(self, text: str) -> None:
        """Replace the entire content of the output text widget."""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state=tk.DISABLED)

    def set_status(self, text: str) -> None:
        """Set the status bar text (ANSI codes will be removed)."""
        self.status_var.set(strip_ansi(text))

    def _get_valid_email(self) -> str | None:
        """
        Read the email address from the input field and validate it.
        Returns the cleaned email or None if invalid.
        """
        email = self.email_var.get().strip()

        if not email:
            self.set_status("Email address must not be empty.")
            return None

        if not validate_email(email):
            self.set_status(strip_ansi(format_warning("Invalid email address.")))
            return None

        return email

    def _handle_api_errors(self, exc: Exception) -> None:
        """
        Central error handler for all API-related calls.
        Shows a message box and updates the status bar.
        """
        if isinstance(exc, RateLimitError):
            msg = "HIBP API rate limit reached. Please try again later."
        elif isinstance(exc, ApiError):
            msg = f"API error: {exc}"
        elif isinstance(exc, RuntimeError):
            # e.g. missing API key from load_api_key_from_env
            msg = str(exc)
        else:
            msg = f"Unexpected error: {exc}"

        self.set_status(msg)
        messagebox.showerror("Error", msg)

    # ---------- Button callbacks ----------

    def on_check_breaches(self) -> None:
        """Check the given email address for breaches."""
        print("DEBUG: on_check_breaches clicked")
        email = self._get_valid_email()
        if email is None:
            print("DEBUG: _get_valid_email returned None")
            return

        try:
            raw = get_breached_account(email)
            print("DEBUG: get_breached_account returned", type(raw), "len:",
                  len(raw))
            breaches = parse_breach_list(raw)
            print("DEBUG: parse_breach_list returned", len(breaches),
                  "breaches")

            if not breaches:
                text = strip_ansi(
                    format_info("No breaches found for this email."))
                self.set_output(text)
                self.set_status("No breaches found.")
                return

            breach_text = strip_ansi(format_breach_list(breaches))
            summary = build_breach_summary(breaches)
            summary_text = strip_ansi(format_breach_summary(summary))

            full_text = breach_text + "\n\n" + summary_text
            self.set_output(full_text)
            self.set_status("Breaches loaded successfully.")

        except Exception as exc:
            print("DEBUG: exception in on_check_breaches:", repr(exc))
            self._handle_api_errors(exc)

    def on_show_pastes(self) -> None:
        """Show pastes for the given email address."""
        email = self._get_valid_email()
        if email is None:
            return

        try:
            raw = get_paste_account(email)
            pastes = parse_paste_list(raw)

            text = strip_ansi(format_paste_list(pastes))
            self.set_output(text)

            if pastes:
                self.set_status("Pastes loaded successfully.")
            else:
                self.set_status("No pastes found.")

        except Exception as exc:
            self._handle_api_errors(exc)

    def on_show_all_breaches(self) -> None:
        """Show all known breaches (may be a large list)."""
        try:
            raw = get_all_breaches()
            breaches = parse_breach_list(raw)

            if not breaches:
                text = strip_ansi(format_info("No breaches available."))
                self.set_output(text)
                self.set_status("No breaches available.")
                return

            text = strip_ansi(format_breach_list(breaches))
            self.set_output(text)
            self.set_status(f"All breaches loaded (count: {len(breaches)}).")

        except Exception as exc:
            self._handle_api_errors(exc)

    def on_show_data_classes(self) -> None:
        """Show the list of HIBP data classes."""
        try:
            data_classes = get_data_classes()

            if not data_classes:
                text = strip_ansi(format_info("No data classes available."))
                self.set_output(text)
                self.set_status("No data classes available.")
                return

            lines = ["Available Data Classes:\n"]
            for dc in data_classes:
                lines.append(f" • {dc}")

            self.set_output("\n".join(lines))
            self.set_status(f"Data classes loaded (count: {len(data_classes)}).")

        except Exception as exc:
            self._handle_api_errors(exc)


def main() -> None:
    app = HibpGui()
    app.mainloop()


if __name__ == "__main__":
    main()
