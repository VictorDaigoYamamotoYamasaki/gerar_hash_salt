import sqlite3
import bcrypt


def criar_banco_dados():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        print("Banco de dados e tabela criados com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        conn.close()

criar_banco_dados()



def registrar_usuario(username, password):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    if cursor.fetchone():
        print("Erro: Nome de usuário já existe.")
        conn.close()
        return
    

    salt = bcrypt.gensalt()
    

    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    print(f"SALT gerado: {salt.decode('utf-8')}")
    print(f"Hash da senha gerado: {password_hash.decode('utf-8')}")
    

    cursor.execute('''
    INSERT INTO usuarios (username, password_hash) 
    VALUES (?, ?)
    ''', (username, password_hash))
    

    conn.commit()
    conn.close()
    print("Usuário registrado com sucesso.")


username = input("Digite o nome de usuário: ")
password = input("Digite a senha: ")
registrar_usuario(username, password)