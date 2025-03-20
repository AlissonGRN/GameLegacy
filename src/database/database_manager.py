from database.connection import conectar
import streamlit as st

class DatabaseManager:
    @staticmethod
    def execute_query(query, params=None, return_results=False):
        """
        Executa uma query no banco de dados
        Args:
            query: SQL query
            params: Parâmetros para query parametrizada
            return_results: Se True, retorna resultados da consulta
        """
        conn = None
        try:
            conn = conectar()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                
                if return_results:
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        results = [dict(zip(columns, row)) for row in cur.fetchall()]
                        return results
                    return None
                    
                conn.commit()
                return True
                
        except Exception as e:
            if conn:
                conn.rollback()
            st.error(f"Database error: {e}")
            return None
            
        finally:
            if conn:
                conn.close()