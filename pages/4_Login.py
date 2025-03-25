import streamlit as st
from auth_db import verificar_login, registrar_usuario, usuario_existe

# Inicializa a sessão para armazenar o estado do usuário
if "user" not in st.session_state:
    st.session_state.user = None

# Obtém o ID do usuário logado
usuario_id = st.session_state.user[0] if st.session_state.user else None

if st.session_state.user == None:
    st.title("Login 🔐")
    st.subheader("Entre ou cadastre-se")
else:
    st.title("Login 🔓")

# Função para exibir login e cadastro
def login_form():
    with st.form("login_form"):
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")
        
        if login_button:
            user = verificar_login(email, password)
            if user:
                st.session_state.user = user
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Email ou senha incorretos.")

def register_form():
    with st.form("register_form"):
        st.subheader("Cadastro")
        name = st.text_input("Nome completo")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")
        birth_date = st.date_input("Data de nascimento")
        mother_name = st.text_input("Nome da mãe")
        register_button = st.form_submit_button("Cadastrar")
        
        if register_button:
            if password != confirm_password:
                st.error("As senhas não coincidem.")
            elif usuario_existe(email):
                st.warning("Usuário já cadastrado!")
            else:
                registrar_usuario(name, email, birth_date, mother_name, password)
                st.success("Conta criada com sucesso! Agora você pode fazer login.")
                st.rerun()

# Botão de login/logout
if st.session_state.user:
    st.write(f"#### Bem-vindo, {st.session_state.user[1]}!")
    st.success("Você já pode acessar seus restaurantes favoritos")
    if st.button("Sair"):
        st.session_state.user = None
        st.rerun()
else:
    with st.expander("Entrar / Criar Conta"):
        login_form()
        register_form()

# Inicializa estados da sessão
if "itens" not in st.session_state:
    st.session_state.itens = {}
if "cardapio_atual" not in st.session_state:
    st.session_state.cardapio_atual = None  # Armazena o ID do cardápio carregado
if "nome_cardapio" not in st.session_state:
    st.session_state.nome_cardapio = ""