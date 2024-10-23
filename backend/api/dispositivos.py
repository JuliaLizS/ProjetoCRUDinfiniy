from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from conexao import get_db
import os
import logging
import mysql

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

class Dispositivo(BaseModel):
    nome: str
    tipo: str
    quantidade: int

# Rota para criar um novo dispositivo
@router.post("/adicionar")
async def criar_dispositivo(dispositivo: Dispositivo, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO dispositivo (nome, tipo, quantidade) VALUES (%s, %s, %s)",
            (dispositivo.nome, dispositivo.tipo, dispositivo.quantidade)
        )
        conexao.commit()
        return {"success": True, "message": "Dispositivo adicionado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao adicionar dispositivo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao adicionar dispositivo")
    finally:
        if cursor:
            cursor.close()

# Rota para listar todos os dispositivos
@router.get("/listar")
async def listar_dispositivos(conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, tipo, quantidade FROM dispositivo")
        dispositivos = cursor.fetchall()
        return {"dispositivos": dispositivos}
    except Exception as e:
        logging.error(f"Erro ao listar dispositivos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar dispositivos")
    finally:
        if cursor:
            cursor.close()


# Rota para editar um dispositivo
@router.put("/alterar/{dispositivo_id}")
async def alterar_dispositivo(dispositivo_id: int, dispositivo: Dispositivo, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE dispositivo SET nome = %s, tipo = %s, quantidade = %s WHERE id = %s",
            (dispositivo.nome, dispositivo.tipo, dispositivo.quantidade, dispositivo_id)
        )
        conexao.commit()
        return {"message": "Dispositivo atualizado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao atualizar dispositivo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar dispositivo")
    finally:
        if cursor:
            cursor.close()


# Rota para excluir um dispositivo
@router.delete("/excluir/{dispositivo_id}")
async def excluir_dispositivo(dispositivo_id: int, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM dispositivo WHERE id = %s", (dispositivo_id,))
        conexao.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado.")
        
        return {"message": "Dispositivo excluído com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao excluir dispositivo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir dispositivo")
    finally:
        if cursor:
            cursor.close()
