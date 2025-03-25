import streamlit as st
import datetime
from auth_db import init_auth_db
from menu_db import init_menu_db, salvar_cardapio, editar_cardapio
from historico_db import salvar_conta

# Inicializa o banco de dados
init_auth_db()
init_menu_db()

# Inicializa a sessão para armazenar o estado do usuário
if "user" not in st.session_state:
    st.session_state.user = None

st.title("Conta Certa 🍺")

# Obtém o ID do usuário logado
usuario_id = st.session_state.user[0] if st.session_state.user else None

# Inicializa estados da sessão
if "itens" not in st.session_state:
    st.session_state.itens = {}
if "cardapio_atual" not in st.session_state:
    st.session_state.cardapio_atual = None  # Armazena o ID do cardápio carregado
if "nome_cardapio" not in st.session_state:
    st.session_state.nome_cardapio = ""

st.divider()

st.write("##### Insira os itens do cardápio para controlar seu consumo em tempo real.")

st.divider()

# 📌 Formulário para adicionar itens
with st.form("Adicionar Item"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        item = st.text_input("Item")
    with col2:
        preco = st.number_input("Preço", min_value=0.0, format="%.2f")
    
    adicionar = st.form_submit_button("Adicionar")

# Adiciona o item ao dicionário
if adicionar:
    if not item:
        st.warning("Digite o nome do item.")
    elif preco <= 0:
        st.warning("O preço deve ser maior que zero.")
    else:
        if item in st.session_state.itens:
            st.session_state.itens[item]["Qtd"] += 1
        else:
            st.session_state.itens[item] = {"Preço": float(preco), "Qtd": 1}
        st.rerun()

# 📌 Exibir e manipular itens
if st.session_state.itens:
    st.write("## Itens Adicionados")
    total = 0
    
    for item, dados in st.session_state.itens.items():
        with st.container(border=True):
            nova_qtd = st.number_input(
                f"{item} --- R$ {dados['Preço']:.2f}",
                min_value=0,
                step=1,
                value=dados["Qtd"],
                key=f"qtd_{item}",
            )
        
        if nova_qtd != dados["Qtd"]:
            st.session_state.itens[item]["Qtd"] = nova_qtd
            st.rerun()
        
        total += dados["Preço"] * nova_qtd
    
    gorjeta = total * 0.1
    total_com_gorjeta = total + gorjeta
    
    st.write(f"**Total:** R$ {total:.2f}")
    if st.checkbox("Incluir 10%"):
        st.write(f"**Total com 10%:** R$ {total_com_gorjeta:.2f}")

    # 📌 Botão para salvar ou atualizar cardápio
    if usuario_id:
        nome_cardapio = st.text_input("Nome do Cardápio", value=st.session_state.nome_cardapio, key="nome_cardapio")
        
        if st.session_state.cardapio_atual:
            if st.button("📈 Salvar no Histórico", use_container_width=True):                
                data = datetime.date.today()
                itens = st.session_state.itens
                salvar_conta(usuario_id, nome_cardapio, data, total_com_gorjeta, itens)

            if st.button("🔄 Atualizar Cardápio", use_container_width=True):
                for i in st.session_state.itens:
                    st.session_state.itens[i]["Qtd"] = 0
                editar_cardapio(st.session_state.cardapio_atual, st.session_state.itens)
                st.success("Cardápio atualizado!")
        else:
            if st.button("💾 Salvar Cardápio", use_container_width=True):
                if not nome_cardapio:
                    st.warning("Digite um nome para salvar o cardápio!")
                else:
                    if salvar_cardapio(usuario_id, nome_cardapio, st.session_state.itens):
                        st.success("Cardápio salvo com sucesso!")
                        st.rerun()
                    else:
                        st.error("Já existe um cardápio com esse nome!")

# 📌 Limpar conta
with st.expander("🗑️ Limpar Conta"):
    st.warning("Esta ação removerá todos os itens adicionados.")
    if st.button("Confirmar limpeza", use_container_width=True):
        st.session_state.itens = {}
        st.session_state.cardapio_atual = None
        st.session_state.pop("nome_cardapio", None)
        st.rerun()
