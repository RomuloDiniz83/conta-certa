import streamlit as st
from menu_db import carregar_cardapios, carregar_cardapio_por_id, excluir_cardapio

# Inicializa a sessão para armazenar o estado do usuário
if "user" not in st.session_state:
    st.session_state.user = None

# Obtém o ID do usuário logado
usuario_id = st.session_state.user[0] if st.session_state.user else None

if usuario_id:
    st.header("Cardápios Salvos 🗒️")
    cardapios = carregar_cardapios(usuario_id)
    
    for cardapio_id, nome in cardapios:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            if col1.button(nome, key=f"load_{cardapio_id}"):            
                st.session_state.itens = carregar_cardapio_por_id(cardapio_id)
                st.session_state.cardapio_atual = cardapio_id
                st.session_state.nome_cardapio = nome
                for i in st.session_state.itens:
                    st.session_state.itens[i]["Qtd"] = 0
                st.success(f"Cardápio '{nome}' carregado!")
                st.success("Retorne para a página inicial")                
                    
            if col2.button("🗑️", key=f"delete_{cardapio_id}"):
                with st.expander(f"Excluir {nome}?"):
                    st.warning("Esta ação é irreversível!")
                    if st.button("Confirmar exclusão", key=f"confirm_delete_{cardapio_id}"):
                        excluir_cardapio(cardapio_id)
                        st.rerun()
else:
    st.title("Meus Cardápios 🗒️")
    st.warning("Faça login para acessar seus cardápios salvos.")