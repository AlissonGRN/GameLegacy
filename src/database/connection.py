import psycopg2
from psycopg2 import sql, OperationalError
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

def conectar():
    """Conecta ao PostgreSQL e retorna a conexão."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
    """Executa o script SQL de criação de tabelas."""
    conn = conectar()
    if not conn:
        return
    
    try:
        with conn, conn.cursor() as cur:
            with open('schema.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Divide os comandos SQL caso haja múltiplos comandos
            comandos = sql_script.split(';')
            for comando in comandos:
                if comando.strip():
                    cur.execute(sql.SQL(comando))

            print("Tabelas criadas com sucesso!")
    
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    
    finally:
        conn.close()
