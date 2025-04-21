from core.validators import validar_cpf, hash_senha, verificar_senha

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

        hash_senha_db = hash_senha(senha)
        self.db.create_user(cpf, hash_senha_db)
