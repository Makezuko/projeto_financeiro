import mysql.connector
import os
from tkinter import messagebox
from dotenv import load_dotenv

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
