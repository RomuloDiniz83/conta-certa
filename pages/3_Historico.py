import streamlit as st
import pandas as pd
import plotly.express as px
from historico_db import init_historico_db, carregar_historico

# Inicializa o banco de dados
init_historico_db()

# Obtém o ID do usuário logado
usuario_id = st.session_state.user[0] if "user" in st.session_state and st.session_state.user else None

st.title("Histórico de Consumo 📊")
st.divider()

if usuario_id:
    # Carregar histórico do banco de dados e transformar em Data Frame
    historico = carregar_historico(usuario_id)
    historico_df = pd.DataFrame(historico)
        
    if not historico:
        st.warning("Nenhum histórico encontrado.")
    else:
        # Converter datas        
        historico_df = historico_df.astype({
            'data':'datetime64[ns]'
        })
        # Organizar por data
        historico_df = historico_df.sort_values(by="data")

        # Filtragem
        st.subheader("Filtros")
        col1, col2 = st.columns(2)
        
        with col1:
            data_inicial = st.date_input("Data Inicial", historico_df["data"].min().date())
            data_final = st.date_input("Data Final", historico_df["data"].max().date())
        
        with col2:
            restaurantes = historico_df["restaurante"].unique()
            restaurante_filtro = st.selectbox("Filtrar por restaurante", ["Todos"] + list(restaurantes))
        
        # Aplicar filtros
        df_filtrado = historico_df[(historico_df["data"] >= pd.Timestamp(data_inicial)) & (historico_df["data"] <= pd.Timestamp(data_final))]
        if restaurante_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["restaurante"] == restaurante_filtro]
        
        st.divider()
                
        # Gráficos
        st.subheader("Gráficos")
        
        # Gráfico de gastos mensais
        df_mensal = df_filtrado.drop("itens", axis=1).resample("ME", on="data").sum().reset_index()
        fig_mensal = px.bar(df_mensal, x="data", y='total', title="Gastos Mensais", labels={"data": "Mês", "total": "Total Gasto (R$)"})
        st.plotly_chart(fig_mensal, use_container_width=True)
        
        
        # Gráfico de gastos por restaurante
        df_restaurante = df_filtrado.groupby(["data", "restaurante"]).sum().reset_index()
        fig_restaurante = px.bar(df_restaurante, x="data", y="total", color="restaurante", title="Gasto por Restaurante", labels={"data": "Data", "valor": "Valor (R$)", "restaurante": "Restaurante"})
        st.plotly_chart(fig_restaurante, use_container_width=True)
       
else:
    st.warning("Faça login para acessar seu histórico.")
