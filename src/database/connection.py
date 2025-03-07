# src/database/connection.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    """Conecta ao PostgreSQL e retorna a conexão e cursor."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def criar_tabelas():
    """Executa o script SQL de criação de tabelas."""
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            with open('schema.sql', 'r') as f:
                cur.execute(f.read())
            conn.commit()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            conn.close()