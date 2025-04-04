import customtkinter as ctk
import mysql.connector

# ----------------- Estilização ------------------

STYLES = {
    "container": {
        "fg_color": ("#F0FFF4", "#327F16"),  
        "corner_radius": 15
    },
    "title": {
        "font": ("Trebuchet MS", 24),
        "text_color": ("#1F1F1F", "#A4E786")
    },
    "input": {
        "width": 300,
        "height": 40,
        "border_width": 0,
        "corner_radius": 10,
        "fg_color": ("#A4E786", "#4CAF50"),  
        "text_color": ("#1A1A1A", "#177D1F"),  
        "placeholder_text_color": ("#3B3B3B", "#177D1F")  
    },
    "button": {
        "fg_color": "#4CAF50",       
        "hover_color": "#79CE51",  
        "text_color": ("#FFFFFF", "#0F3B08"),  
        "width": 120,
        "height": 40
    },
    "link": {
        "text_color": ("#1E88E5", "#A4E786"),  
        "cursor": "hand2",
        "font": ("Arial", 12)
    }
}

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def create_container(parent):
    return ctk.CTkFrame(parent, **STYLES["container"])

def create_title(parent, text):
    return ctk.CTkLabel(parent, text=text, **STYLES["title"])

def create_input(parent, placeholder):
    return ctk.CTkEntry(parent, placeholder_text=placeholder, **STYLES["input"])

def create_button(parent, text, command):
    return ctk.CTkButton(parent, text=text, command=command, **STYLES["button"])

def create_link(parent, text, command):
    label = ctk.CTkLabel(parent, text=text, **STYLES["link"])
    label.bind("<Button-1>", lambda e: command())
    return label

# ----------------- Funções de Login / Cadastro ------------------

def login_screen(window):
    clear_window(window)
    main_container = create_container(window)
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    title = create_title(main_container, "Login")
    cpf_input = create_input(main_container, "CPF")
    password_input = create_input(main_container, "Senha")
    password_input.configure(show="•")

    login_btn = create_button(main_container, "Entrar", lambda: login_function(cpf_input, password_input))
    register_link = create_link(main_container, "Criar conta", lambda: register_screen(window))

    for row, widget in enumerate([title, cpf_input, password_input, login_btn, register_link]):
        widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

def register_screen(window):
    clear_window(window)
    main_container = create_container(window)
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    title = create_title(main_container, "Cadastro")
    cpf_input = create_input(main_container, "CPF")
    password_input = create_input(main_container, "Senha")
    password_input.configure(show="•")

    register_btn = create_button(main_container, "Cadastrar", lambda: register_function(cpf_input, password_input))
    login_link = create_link(main_container, "Já tem conta? Login", lambda: login_screen(window))

    for row, widget in enumerate([title, cpf_input, password_input, register_btn, login_link]):
        widget.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

# ----------------- Banco de Dados ------------------

def login_function(cpf_entry, password_entry):
    cpf = cpf_entry.get()
    password = password_entry.get()

    query = "SELECT * FROM usuarios WHERE cpf = %s AND senha = %s"
    cursor.execute(query, (cpf, password))
    result = cursor.fetchone()

    if result:
        print("Login bem-sucedido!")
    else:
        print("Usuário ou senha incorretos.")

def register_function(cpf_entry, password_entry):
    cpf = cpf_entry.get()
    password = password_entry.get()

    query = "INSERT INTO usuarios (cpf, senha) VALUES (%s, %s)"
    cursor.execute(query, (cpf, password))
    mydb.commit()

    print("Cadastro bem-sucedido!")

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
        print(f"Erro ao conectar ao banco de dados: {err}")
        return

    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("Sistema Financeiro")
    app.iconbitmap("assets/icon.ico")
    app.configure(fg_color="#4caf50")  
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    login_screen(app)
    app.mainloop()

if __name__ == "__main__":
    main()
