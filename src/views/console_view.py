import streamlit as st
from database.connection import conectar
from database.database_manager import DatabaseManager

def consoles_view():
    
    # Controles de Ordenação
    ordem = st.radio("Ordenar por:", ["Mais Recente", "Mais Antigo"], horizontal=True)

    # Formulário de Cadastro de Consoles
    with st.expander("Cadastrar Novo Console"):
        with st.form("console_form"):
            modelo = st.text_input("Modelo (ex: NES)")
            ano = st.number_input("Ano de Lançamento", min_value=1970, max_value=2024)
            if st.form_submit_button("Salvar"):
                if DatabaseManager.execute_query(
                    "INSERT INTO Console (Modelo, Ano_Lancamento) VALUES (%s, %s)",
                    (modelo, ano)
                ):
                    st.success("Console cadastrado!")
                    st.rerun()

    # Lista de Consoles Cadastrados
    st.subheader("Consoles Cadastrados")
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            order = "DESC" if ordem == "Mais Recente" else "ASC"
            cur.execute(f"SELECT * FROM Console ORDER BY ID_Console {order}")  # Consulta para listar consoles ordenados
            consoles = cur.fetchall()

            # Exibir cada console
            for console in consoles:
                id_console, modelo_console, ano_console = console
                
                # Layout em colunas
                col1, col2, col3 = st.columns([4, 2, 1])
                
                with col1:
                    st.markdown(f"**{modelo_console}** ({ano_console})")
                
                with col2:
                    # Botão de Edição
                    if st.button("✏️ Editar", key=f"edit_{id_console}"):
                        st.session_state['editando_console'] = id_console
                
                with col3:
                    # Botão de Exclusão
                    if st.button("🗑️ Excluir", key=f"del_{id_console}"):
                        conn_check = conectar()
                        if conn_check:
                            try:
                                cur_check = conn_check.cursor()
                                cur_check.execute(
                                    "SELECT COUNT(*) FROM Jogo WHERE ID_Console = %s",  # Verifica se há jogos vinculados ao console
                                    (id_console,)
                                )
                                total_jogos = cur_check.fetchone()[0]
                                
                                if total_jogos > 0:
                                    st.error("Não é possível excluir: existem jogos vinculados!")
                                else:
                                    if executar_query(
                                        "DELETE FROM Console WHERE ID_Console = %s",  # Exclui o console se não houver jogos vinculados
                                        (id_console,)
                                    ):
                                        st.success("Console excluído!")
                                        st.rerun()
                                        
                            except Exception as e:
                                st.error(f"Erro: {e}")
                            finally:
                                conn_check.close()

                # Formulário de Edição
                if st.session_state.get('editando_console') == id_console:
                    with st.form(key=f"editar_console_{id_console}"):
                        novo_modelo = st.text_input("Modelo", value=modelo_console)
                        novo_ano = st.number_input("Ano", value=ano_console, 
                                                 min_value=1970, max_value=2024)
                        
                        col_salvar, col_cancelar = st.columns(2)
                        with col_salvar:
                            if st.form_submit_button("💾 Salvar"):
                                if executar_query(
                                    "UPDATE Console SET Modelo = %s, Ano_Lancamento = %s WHERE ID_Console = %s",  # Atualiza o console
                                    (novo_modelo, novo_ano, id_console)
                                ):
                                    del st.session_state['editando_console']
                                    st.rerun()
                        
                        with col_cancelar:
                            if st.form_submit_button("❌ Cancelar"):
                                del st.session_state['editando_console']
                                st.rerun()

        except Exception as e:
            st.error(f"Erro ao carregar consoles: {e}")
        finally:
            conn.close()