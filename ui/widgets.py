import customtkinter as ctk
from core.validators import validar_entrada_cpf, validar_entrada_senha, formatar_cpf

def create_container(parent):
    return ctk.CTkFrame(
        parent,
        fg_color=("#F0FFF4", "#327F16"),
        corner_radius=15
    )

def create_title(parent, text):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=("Trebuchet MS", 24),
        text_color=("#1F1F1F", "#A4E786")
    )

def create_button(parent, text, command):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color="#4CAF50",
        hover_color="#79CE51",
        text_color=("#FFFFFF", "#0F3B08"),
        width=120,
        height=40
    )

def create_link(parent, text, command):
    label = ctk.CTkLabel(
        parent,
        text=text,
        text_color=("#1E88E5", "#A4E786"),
        cursor="hand2",
        font=("Arial", 12)
    )
    label.bind("<Button-1>", lambda e: command())
    return label

def create_input(parent, placeholder: str, is_cpf=False, is_password=False):
    entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=300,
        height=40,
        border_width=0,
        corner_radius=10,
        fg_color=("#A4E786", "#4CAF50"),
        text_color=("#FFFFFF", "#0F3B08"),
        placeholder_text_color=("#FFFFFF", "#0F3B08")
    )

    if is_cpf:
        entry.configure(validate="key")
        entry.configure(validatecommand=(parent.register(validar_entrada_cpf), '%P'))
        entry.bind("<FocusIn>", lambda e: entry.delete(0, "end"))
        entry.bind("<KeyRelease>", formatar_cpf)

    if is_password:
        entry.configure(validate="key")
        entry.configure(validatecommand=(parent.register(validar_entrada_senha), '%P'))
        entry.configure(show="•")

    return entry

def clear_window(widget):
    for child in widget.winfo_children():
        child.destroy()
