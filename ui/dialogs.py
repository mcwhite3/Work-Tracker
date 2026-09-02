from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


def show_not_ready(parent: tk.Widget, feature_name: str) -> None:
    messagebox.showinfo(
        title="Coming Soon",
        message=f"{feature_name} is planned for a future MVP milestone.",
        parent=parent,
    )

