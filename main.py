import customtkinter as ctk
import mysql.connector
import bcrypt
import re
from tkinter import messagebox


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

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

def create_input(parent, placeholder, is_cpf=False, is_password=False):
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
        entry.bind("<KeyRelease>", formatar_cpf)
    
    if is_password:
        entry.configure(validate="key")
        entry.configure(validatecommand=(
            parent.register(validar_entrada_senha),
            '%P'
        ))
        entry.configure(show="•")
    
    return entry

# ----------------- Funções de Validação ------------------
def formatar_cpf(event):
    widget = event.widget
    texto = widget.get().replace(".", "").replace("-", "")[:11]
    novo_texto = ""
    
    for i, char in enumerate(texto):
        if i in [3, 6]:
            novo_texto += "."
        if i == 9:
            novo_texto += "-"
        novo_texto += char
    
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
    if len(texto.replace(".", "").replace("-", "")) > 11:
        return False
    return re.match(r'^[\d\.\-]*$', texto) is not None

def validar_entrada_senha(texto):
    return len(texto) <= 16

# ----------------- Funções de Segurança ------------------
def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

def verificar_senha(senha, hash_armazenado):
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))

# ----------------- Funções de Banco de Dados ------------------
def login_function(cpf_entry, password_entry, window):  
    cpf_formatado = cpf_entry.get()
    cpf_numeros = re.sub(r'[^0-9]', '', cpf_formatado)
    senha = password_entry.get()

    if not validar_cpf(cpf_numeros):
        messagebox.showerror("Erro", "CPF inválido!")
        return

    try:
        cursor.execute(
            "SELECT hash_senha FROM projeto_financeiro.usuario WHERE cpf = %s",
            (cpf_numeros,)
        )
        resultado = cursor.fetchone()

        if resultado and verificar_senha(senha, resultado[0]):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            main_screen(window)  
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no login: {str(e)}")

def register_function(cpf_entry, password_entry):
    cpf_formatado = cpf_entry.get()
    cpf_numeros = re.sub(r'[^0-9]', '', cpf_formatado)
    senha = password_entry.get()

    if not validar_cpf(cpf_numeros):
        messagebox.showerror("Erro", "CPF inválido!")
        return

    if len(senha) < 8:
        messagebox.showerror("Erro", "A senha deve ter no mínimo 8 caracteres!")
        return

    try:
        hash_senha_db = hash_senha(senha)
        cursor.execute(
            "INSERT INTO projeto_financeiro.usuario (cpf, hash_senha) VALUES (%s, %s)",
            (cpf_numeros, hash_senha_db)
        )
        mydb.commit()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Erro", "CPF já cadastrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no cadastro: {str(e)}")

# ----------------- Telas ------------------
def login_screen(window):
    clear_window(window)
    main_container = create_container(window)
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    title = create_title(main_container, "Login")
    cpf_input = create_input(main_container, "CPF", is_cpf=True)
    password_input = create_input(main_container, "Senha", is_password=True)

    login_btn = create_button(main_container, "Entrar", 
                            lambda: login_function(cpf_input, password_input, window))
    register_link = create_link(main_container, "Criar conta", 
                              lambda: register_screen(window))

    for row, widget in enumerate([title, cpf_input, password_input, login_btn, register_link]):
        widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

def register_screen(window):
    clear_window(window)
    main_container = create_container(window)
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    title = create_title(main_container, "Cadastro")
    cpf_input = create_input(main_container, "CPF", is_cpf=True)
    password_input = create_input(main_container, "Senha", is_password=True)

    register_btn = create_button(main_container, "Cadastrar",
                               lambda: register_function(cpf_input, password_input))
    login_link = create_link(main_container, "Voltar ao login",
                           lambda: login_screen(window))

    for row, widget in enumerate([title, cpf_input, password_input, register_btn, login_link]):
        widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

def main_screen(window):
    clear_window(window)
    
    main_container = ctk.CTkFrame(
        window,
        fg_color=("#F0FFF4", "#327F16")
    )
    main_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    title = ctk.CTkLabel(
        main_container,
        text="Dashboard",
        font=("Trebuchet MS", 28, "bold"),
        text_color=("#1F1F1F", "#A4E786")
    )
    title.pack(pady=20, anchor="n")

    logout_link = ctk.CTkLabel(
        main_container,
        text="Sair",
        cursor="hand2",
        text_color=("#1E88E5", "#A4E786"),
        font=("Arial", 12)
    )
    logout_link.bind("<Button-1>", lambda e: login_screen(window))
    logout_link.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)      

# ----------------- App Principal ------------------
def main():
    global mydb, cursor
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="rootroot",
            database="projeto_financeiro"
        )
        cursor = mydb.cursor()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Não foi possível conectar ao banco de dados: {err}")
        return

    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("Sistema Financeiro")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")  
    app.configure(fg_color="#4caf50")
    app.iconbitmap("assets/icon.ico")
    login_screen(app)
    app.mainloop()

if __name__ == "__main__":
    main()