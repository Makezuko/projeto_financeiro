import customtkinter as ctk
import re
from tkinter import messagebox
from ui.widgets import create_container, create_title, create_button, create_link, create_input, clear_window

class BaseScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.container = None    

    def _create_ui(self):
        if self.container is not None:
            self.container.destroy()

        self.configure(fg_color="#42a603")
        self.container = create_container(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")



class LoginScreen(BaseScreen):
    def _create_ui(self):
        super()._create_ui()
        title = create_title(self.container, "Login")
        self.cpf_input = create_input(self.container, "CPF", is_cpf=True)
        self.password_input = create_input(self.container, "Senha", is_password=True)

        login_btn = create_button(self.container, "Entrar", self._on_login)
        register_link = create_link(self.container, "Criar conta", lambda: self.controller.show_screen("register"))

        for row, widget in enumerate([title, self.cpf_input, self.password_input, login_btn, register_link]):
            widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

    def _on_login(self):
        try:
            cpf = re.sub(r'[^0-9]', '', self.cpf_input.get())
            senha = self.password_input.get()
            self.controller.auth.login(cpf, senha)
            self.controller.show_screen("main")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

class RegisterScreen(BaseScreen):
    def _create_ui(self):
        super()._create_ui()
        title = create_title(self.container, "Cadastro")
        self.cpf_input = create_input(self.container, "CPF", is_cpf=True)
        self.password_input = create_input(self.container, "Senha", is_password=True)

        register_btn = create_button(self.container, "Cadastrar", self._on_register)
        login_link = create_link(self.container, "Voltar ao login", lambda: self.controller.show_screen("login"))

        for row, widget in enumerate([title, self.cpf_input, self.password_input, register_btn, login_link]):
            widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

    def _on_register(self):
        try:
            cpf = re.sub(r'[^0-9]', '', self.cpf_input.get())
            senha = self.password_input.get()
            self.controller.auth.register(cpf, senha)
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.controller.show_screen("login")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

class MainScreen(BaseScreen):
    def _create_ui(self):
        super()._create_ui()
        self.container = ctk.CTkFrame(
            self,
            fg_color=("#00FF00", "#327F16")
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.container,
            text="Dashboard",
            font=("Trebuchet MS", 28, "bold"),
            text_color=("#1F1F1F", "#A4E786")
        )
        title.pack(pady=20, anchor="n")

        logout_link = ctk.CTkLabel(
            self.container,
            text="Sair",
            cursor="hand2",
            text_color=("#1E88E5", "#A4E786"),
            font=("Arial", 12)
        )
        logout_link.bind("<Button-1>", lambda e: self.controller.show_screen("login"))
        logout_link.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
