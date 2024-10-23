import os
import mysql.connector
from mysql.connector import Error
import logging

# Configurar o log para exibir informações no console
logging.basicConfig(level=logging.INFO)

def conexao_banco():
    con = None
    try:
        # Pegar informações de usuário e senha do ambiente
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '1234')

        logging.info("Tentando conectar ao banco de dados...")

        # Tentar conectar ao banco de dados
        con = mysql.connector.connect(
            host='localhost',
            database='industria_wayne',
            user=db_user,
            password=db_password
        )

        if con.is_connected():
            db_info = con.get_server_info()
            logging.info(f"Conectado ao servidor MySQL versão {db_info}")
            cursor = con.cursor()
            cursor.execute("SELECT DATABASE();")
            linha = cursor.fetchone()
            logging.info(f"Conectado ao banco de dados: {linha}")
            return con
        else:
            logging.error("Falha na conexão.")
            return None

    except mysql.connector.ProgrammingError as e:
        logging.error(f"Erro de programação no MySQL: {e}")
        return None

    except mysql.connector.DatabaseError as e:
        logging.error(f"Erro relacionado ao banco de dados: {e}")
        return None

    except mysql.connector.Error as e:
        logging.error(f"Erro genérico no MySQL: {e}")
        return None

    finally:
        if con is not None and con.is_connected():
            con.close()
            logging.info("Conexão com o banco de dados foi fechada.")

# Função para uso no backend (por exemplo, FastAPI)
def get_db():
    con = conexao_banco()
    try:
        yield con
    finally:
        if con and con.is_connected():
            con.close()
