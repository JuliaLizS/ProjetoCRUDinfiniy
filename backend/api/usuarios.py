import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from conexao import get_db
import traceback
import logging
from enum import Enum
import mysql.connector
from mysql.connector import Error
import os
from typing import Optional

def conexao_banco():
    try:
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '1234')

        logging.info("Tentando conectar ao banco de dados...")

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

    except mysql.connector.Error as e:
        logging.error(f"Erro no MySQL: {e}")
        return None


def get_db():
    con = conexao_banco()
    try:
        yield con
    finally:
        if con and con.is_connected():
            con.close()
            logging.info("Conexão com o banco de dados foi fechada.")


router = APIRouter()

class TipoUsuario(str, Enum):
    administrador = 'administrador'
    funcionario = 'funcionario'
    gerente = 'gerente'


# Modelo para representar um usuário (Pydantic)
class Usuario(BaseModel):
    nome: str
    email: str
    tipo: TipoUsuario
    senha: str

# Modelo de Atualização de Usuário
class UsuarioUpdate(BaseModel):
    nome: str
    email: str
    tipo: TipoUsuario
    senha: Optional[str] = None  



# Rota para listar todos os usuários
@router.get("/listar")
async def listar_usuarios(db: mysql.connector.connection = Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, tipo FROM usuario")
        usuarios = cursor.fetchall()
        return {"usuarios": usuarios}
    except Exception as e:
        logging.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar usuários")
    finally:
        cursor.close()


# Rota para criar um novo usuário (somente POST)
@router.post("/adicionar")
async def criar_usuario(usuario: Usuario, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        senha_hash = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO usuario (nome, email, tipo, senha) VALUES (%s, %s, %s, %s)",
            (usuario.nome, usuario.email, usuario.tipo, senha_hash)
        )
        conexao.commit()
        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao inserir usuário: {e}")
        logging.error(traceback.format_exc())  # Mostra a pilha de rastreamento
        raise HTTPException(status_code=500, detail="Erro ao inserir usuário no banco de dados.")
    finally:
        if cursor:  # Fecha o cursor apenas se ele foi criado
            cursor.close()


#! EDITAR USUARIO

# Rota para alterar os dados do usuário
@router.put("/alterar/{usuario_id}")
async def alterar_usuario(usuario_id: int, usuario: UsuarioUpdate, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        
        # Inicia a query de update
        query = "UPDATE usuario SET nome = %s, email = %s, tipo = %s"
        valores = [usuario.nome, usuario.email, usuario.tipo]
        
        # Se uma nova senha foi fornecida, a criptografa e adiciona à query
        if usuario.senha:
            senha_hash = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
            query += ", senha = %s"
            valores.append(senha_hash)
        
        query += " WHERE id = %s"
        valores.append(usuario_id)
        
        cursor.execute(query, tuple(valores))
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao alterar usuário: {e}")
        logging.error(traceback.format_exc())  # Loga a pilha de rastreamento
        raise HTTPException(status_code=500, detail="Erro ao alterar usuário no banco de dados.")
    finally:
        if cursor:
            cursor.close()















@router.delete("/excluir/{usuario_id}")
async def excluir_usuario(usuario_id: int, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
        conexao.commit()
        return {"message": "Usuário excluído com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao excluir usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir usuário no banco de dados.")
    finally:
        if cursor:
            cursor.close()


