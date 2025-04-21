import re
import bcrypt

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
