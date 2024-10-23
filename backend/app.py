"""
As Indústrias Wayne, uma empresa renomada e inovadora liderada pelo
lendário Bruce Wayne (também conhecido como Batman), está buscando
uma solução tecnológica para otimizar seus processos internos e melhorar a
segurança de Gotham City. Como parte de seu projeto final, você irá
desenvolver uma aplicação web full stack que atenda às necessidades
específicas das Indústrias Wayne.
Descrição do Projeto: Sua missão é criar uma plataforma que aborde os
requisitos que são abordados na próxima página do arquivo.

DO PROJETO:
  * Sistema de Gerenciamento de Segurança:
Desenvolva um sistema de controle de acesso que permita apenas
usuários autorizados a acessar áreas restritas das instalações das Indústrias
Wayne.
Implemente autenticação e autorização para diferentes tipos de usuários,
como funcionários, gerentes e administradores de segurança.
  * Gestão de Recursos:
Desenvolva uma interface para gerenciar recursos internos, como
inventário de equipamentos, veículos e dispositivos de segurança.
Permita que os administradores possam adicionar, remover e atualizar
informações sobre esses recursos de forma eficiente.
  * Dashboard de Visualização:
Crie um painel de controle visualmente atraente que exiba dados relevantes
sobre segurança, recursos e atividades dentro das Indústrias Wayne.

  * Entrega:
Apresente um protótipo funcional da aplicação, incluindo código
fonte e documentação detalhada.
Certifique-se de demonstrar a integração eficaz entre o frontend e
o backend, bem como a implementação dos requisitos
mencionados acima.
Use todo e qualquer conhecimento adquirido até aqui. Este projeto
final, além de ser a sua avaliação, também lhe serve como um bom
portfólio.
"""

import bcrypt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importar CORS para permitir solicitações de outras origens
from api.usuarios import router as usuarios_router
from api.veiculos import router as veiculos_router
from api.dispositivos import router as dispositivos_router
import os
import mysql.connector
from mysql.connector import Error
import logging


logging.basicConfig(level=logging.INFO)

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



app = FastAPI()

# Registrar as rotas da API
app.include_router(usuarios_router, prefix="/usuarios")
app.include_router(veiculos_router, prefix="/veiculos")
app.include_router(dispositivos_router, prefix="/dispositivos")

# Configuração CORS
origins = [
    "http://localhost",  # Frontend rodando no localhost
    "http://localhost:8000",  # Backend rodando no localhost
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
