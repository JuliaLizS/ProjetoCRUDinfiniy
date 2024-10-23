from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
import logging
import traceback
import os

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

# Modelo Pydantic para Veículo
class Veiculo(BaseModel):
    placa: str
    modelo: str
    marca: str
    cor: str

# Rota para adicionar um veículo (somente POST)
@router.post("/adicionar")
async def adicionar_veiculo(veiculo: Veiculo, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()

        # Verifica se a placa já está cadastrada
        cursor.execute("SELECT id FROM veiculo WHERE placa = %s", (veiculo.placa,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Veículo com essa placa já existe")

        # Insere o novo veículo
        cursor.execute(
            "INSERT INTO veiculo (placa, modelo, marca, cor) VALUES (%s, %s, %s, %s)",
            (veiculo.placa, veiculo.modelo, veiculo.marca, veiculo.cor)
        )
        conexao.commit()

        return {"message": "Veículo adicionado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao adicionar veículo: {e}")
        logging.error(traceback.format_exc())  # Loga o erro com detalhes
        raise HTTPException(status_code=500, detail="Erro ao adicionar veículo no banco de dados.")
    finally:
        if cursor:
            cursor.close()


# Rota para listar todos os veículos
@router.get("/listar")
async def listar_veiculos(db: mysql.connector.connection = Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, placa, modelo, marca, cor FROM veiculo")
        veiculos = cursor.fetchall()
        return {"veiculos": veiculos}
    except Exception as e:
        logging.error(f"Erro ao listar veículos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar veículos")
    finally:
        cursor.close()


# Rota para editar um veículo
@router.put("/alterar/{veiculo_id}")
async def editar_veiculo(veiculo_id: int, veiculo: Veiculo, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        query = """
            UPDATE veiculo 
            SET placa = %s, modelo = %s, marca = %s, cor = %s 
            WHERE id = %s
        """
        cursor.execute(query, (veiculo.placa, veiculo.modelo, veiculo.marca, veiculo.cor, veiculo_id))
        conexao.commit()
        return {"message": "Veículo atualizado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao atualizar veículo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar veículo no banco de dados.")
    finally:
        if cursor:
            cursor.close()


# Rota para excluir um veículo
@router.delete("/excluir/{veiculo_id}")
async def excluir_veiculo(veiculo_id: int, conexao=Depends(get_db)):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM veiculo WHERE id = %s", (veiculo_id,))
        conexao.commit()
        return {"message": "Veículo excluído com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao excluir veículo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir veículo")
    finally:
        if cursor:
            cursor.close()
