# src/app.py
import streamlit as st
from database.connection import conectar

st.set_page_config(page_title="RetroRent 🕹️", layout="wide")

# Sidebar para configurações
with st.sidebar:
    st.header("Configurações do Banco")
    if st.button("Criar Tabelas (Schema)"):
        from database.connection import criar_tabelas
        criar_tabelas()
        st.success("Tabelas criadas!")

    if st.button("Popular Dados Iniciais (Seed)"):
        conn = conectar()
        if conn:
            try:
                cur = conn.cursor()
                with open('seed.sql', 'r') as f:
                    cur.execute(f.read())
                conn.commit()
                st.success("Dados iniciais inseridos!")
            except Exception as e:
                st.error(f"Erro: {e}")
            finally:
                conn.close()

# Função para executar queries genéricas
def executar_query(query, params=None):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query, params or ())
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro: {e}")
            return False
        finally:
            conn.close()
    return False

# Página principal
st.title("RetroRent - Locadora de Video Games Retro 🎮")

# Abas para diferentes funcionalidades
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Consoles", "Jogos", "Clientes", "Aluguel", "Devolução"]
)

# --- ABA 1: Cadastro de Consoles ---
with tab1:
    st.subheader("Cadastrar Novo Console")
    with st.form("console_form"):
        modelo = st.text_input("Modelo (ex: NES)")
        ano = st.number_input("Ano de Lançamento", min_value=1970, max_value=2024)
        if st.form_submit_button("Salvar"):
            if executar_query(
                "INSERT INTO Console (Modelo, Ano_Lancamento) VALUES (%s, %s)",
                (modelo, ano)
            ):
                st.success("Console cadastrado!")

    st.subheader("Consoles Cadastrados")
    conn = conectar()
    if conn:
        consoles = conn.cursor()
        consoles.execute("SELECT * FROM Console")
        resultados = consoles.fetchall()
        st.table(resultados)
        conn.close()

# --- ABA 2: Cadastro de Jogos ---
with tab2:
    st.subheader("Cadastrar Novo Jogo")
    conn = conectar()
    if conn:
        consoles = conn.cursor()
        consoles.execute("SELECT ID_Console, Modelo FROM Console")
        opcoes_consoles = {row[1]: row[0] for row in consoles.fetchall()}
        conn.close()

    with st.form("jogo_form"):
        titulo = st.text_input("Título do Jogo")
        ano = st.number_input("Ano do Jogo", min_value=1970, max_value=2024)
        console = st.selectbox("Console", options=opcoes_consoles.keys())
        preco = st.number_input("Preço Diária (R$)", min_value=0.0, format="%.2f")
        if st.form_submit_button("Salvar"):
            id_console = opcoes_consoles[console]
            if executar_query(
                """INSERT INTO Jogo (Titulo, Ano, ID_Console, Preco_Diaria)
                   VALUES (%s, %s, %s, %s)""",
                (titulo, ano, id_console, preco)
            ):
                st.success("Jogo cadastrado!")

# --- ABA 3: Cadastro de Clientes ---
with tab3:
    st.subheader("Cadastrar Novo Cliente")
    with st.form("cliente_form"):
        nome = st.text_input("Nome Completo")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        if st.form_submit_button("Salvar"):
            if executar_query(
                "INSERT INTO Cliente (Nome, Telefone, Email) VALUES (%s, %s, %s)",
                (nome, telefone, email)
            ):
                st.success("Cliente cadastrado!")

# --- ABA 4: Realizar Aluguel ---
with tab4:
    st.subheader("Realizar Aluguel")
    conn = conectar()
    if conn:
        clientes = conn.cursor()
        clientes.execute("SELECT ID_Cliente, Nome FROM Cliente")
        opcoes_clientes = {row[1]: row[0] for row in clientes.fetchall()}

        jogos = conn.cursor()
        jogos.execute("SELECT ID_Jogo, Titulo FROM Jogo")
        opcoes_jogos = {row[1]: row[0] for row in jogos.fetchall()}

        consoles = conn.cursor()
        consoles.execute("SELECT ID_Console, Modelo FROM Console")
        opcoes_consoles = {row[1]: row[0] for row in consoles.fetchall()}
        conn.close()

    with st.form("aluguel_form"):
        cliente = st.selectbox("Cliente", options=opcoes_clientes.keys())
        jogo = st.selectbox("Jogo (opcional)", options=[""] + list(opcoes_jogos.keys()))
        console = st.selectbox("Console (opcional)", options=[""] + list(opcoes_consoles.keys()))
        if st.form_submit_button("Registrar Aluguel"):
            id_cliente = opcoes_clientes[cliente]
            id_jogo = opcoes_jogos.get(jogo, None)
            id_console = opcoes_consoles.get(console, None)

            if id_jogo or id_console:
                if executar_query(
                    """INSERT INTO Aluguel (ID_Cliente, ID_Jogo, ID_Console)
                       VALUES (%s, %s, %s)""",
                    (id_cliente, id_jogo, id_console)
                ):
                    st.success("Aluguel registrado!")
            else:
                st.error("Selecione pelo menos um jogo ou console.")

# --- ABA 5: Devolução ---
with tab5:
    st.subheader("Registrar Devolução")
    conn = conectar()
    if conn:
        alugueis_ativos = conn.cursor()
        alugueis_ativos.execute("""
            SELECT A.ID_Aluguel, C.Nome, J.Titulo, CO.Modelo, A.Data_Aluguel 
            FROM Aluguel A
            LEFT JOIN Jogo J ON A.ID_Jogo = J.ID_Jogo
            LEFT JOIN Console CO ON A.ID_Console = CO.ID_Console
            JOIN Cliente C ON A.ID_Cliente = C.ID_Cliente
            WHERE A.Data_Devolucao IS NULL
        """)
        opcoes_alugueis = {f"{row[0]} - {row[1]} ({row[2] or row[3]})": row[0] for row in alugueis_ativos.fetchall()}
        conn.close()

    with st.form("devolucao_form"):
        aluguel = st.selectbox("Selecione o Aluguel", options=opcoes_alugueis.keys())
        if st.form_submit_button("Registrar Devolução"):
            id_aluguel = opcoes_alugueis[aluguel]
            if executar_query(
                "UPDATE Aluguel SET Data_Devolucao = CURRENT_DATE WHERE ID_Aluguel = %s",
                (id_aluguel,)
            ):
                st.success("Devolução registrada!")