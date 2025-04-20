import customtkinter as ctk
import mysql.connector
import bcrypt
import re
from tkinter import messagebox
from dotenv import load_dotenv
import os

# ====================== FUNÇÕES UTILITÁRIAS ======================
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
        entry.configure(validatecommand=(
            parent.register(validar_entrada_cpf),
            '%P'
        ))
        entry.bind("<FocusIn>", lambda e: entry.delete(0, "end"))
        entry.bind("<KeyRelease>", formatar_cpf)

    if is_password:
        entry.configure(validate="key")
        entry.configure(validatecommand=(
            parent.register(validar_entrada_senha),
            '%P'
        ))
        entry.configure(show="•")

    return entry

# ====================== VALIDAÇÃO E SEGURANÇA ======================
def formatar_cpf(event):
    widget = event.widget
    texto = ''.join(filter(str.isdigit, widget.get()))[:11]
    novo_texto = []
    
    for i, char in enumerate(texto):
        if i in (3, 6):
            novo_texto.append('.')
        if i == 9:
            novo_texto.append('-')
        novo_texto.append(char)
    
    novo_texto = ''.join(novo_texto)
    widget.delete(0, "end")
    widget.insert(0, novo_texto)
    return True

def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = resto if resto < 10 else 0
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = resto if resto < 10 else 0
    
    return cpf[-2:] == f"{digito1}{digito2}"

def validar_entrada_cpf(texto):
    return len(texto.replace(".", "").replace("-", "")) <= 11 and re.match(r'^[\d\.\-]*$', texto)

def validar_entrada_senha(texto):
    return len(texto) <= 16

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

def verificar_senha(senha, hash_armazenado):
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))

# ====================== HANDLERS DO SISTEMA ======================
class DatabaseHandler:
    def __init__(self):
        self._load_credentials()
        self.connect()
    
    def _load_credentials(self):
        load_dotenv()
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }
    
    def connect(self):
        try:
            self.mydb = mysql.connector.connect(**self.config)
            self.cursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Falha na conexão: {err}")
            raise

    def get_user(self, cpf):
        self.cursor.execute(
            "SELECT hash_senha FROM projeto_financeiro.usuario WHERE cpf = %s",
            (cpf,)
        )
        return self.cursor.fetchone()
    
    def create_user(self, cpf, hash_senha):
        try:
            self.cursor.execute(
                "INSERT INTO projeto_financeiro.usuario (cpf, hash_senha) VALUES (%s, %s)",
                (cpf, hash_senha)
            )
            self.mydb.commit()
        except mysql.connector.IntegrityError:
            raise ValueError("CPF já cadastrado")

class AuthService:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def login(self, cpf, senha):
        if not validar_cpf(cpf):
            raise ValueError("CPF inválido")
        
        user = self.db.get_user(cpf)
        if not user or not verificar_senha(senha, user[0]):
            raise ValueError("Credenciais inválidas")
        return True
    
    def register(self, cpf, senha):
        if not validar_cpf(cpf):
            raise ValueError("CPF inválido")
        
        if len(senha) < 8:
            raise ValueError("Senha deve ter 8+ caracteres")
        
        try:
            hash_senha_db = hash_senha(senha)
            self.db.create_user(cpf, hash_senha_db)
        except ValueError as e:
            raise

class BaseScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._create_ui()

    def _create_ui(self):
        self.container = create_container(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

# ====================== TELAS ESPECIALIZADAS ======================
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

# ====================== APLICAÇÃO PRINCIPAL ======================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Financeiro")
        self.geometry("1280x720")
        self.iconbitmap("assets/icon.ico")
        self._set_appearance_mode("dark")


        self.db = DatabaseHandler()
        self.auth = AuthService(self.db)
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        self.screens = {
            "login": LoginScreen(self.container, self),
            "register": RegisterScreen(self.container, self),
            "main": MainScreen(self.container, self)
        }
        
        self.show_screen("login")

    def show_screen(self, name):
        for screen in self.screens.values():
            screen.pack_forget()
        self.screens[name].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()