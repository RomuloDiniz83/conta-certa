# Conta Certa 🍺

O **Conta Certa** é um aplicativo web desenvolvido com Streamlit para ajudar a gerenciar contas de restaurantes. Ele permite registrar os itens consumidos, calcular valores com ou sem gorjeta, salvar cardápios personalizados, visualizar históricos de consumo e gerar análises gráficas dos gastos.

## 📌 Funcionalidades

✅ **Gerenciamento de Conta**: Adicione e edite itens consumidos, calculando o total com ou sem gorjeta.  
✅ **Cadastro de Restaurantes**: Salve e gerencie cardápios personalizados para cada restaurante que frequenta.  
✅ **Histórico de Consumo**: Visualize registros de contas passadas e gráficos de análise de gastos. 

## 🚀 Tecnologias Utilizadas

- **Python** + **Streamlit** → Interface web interativa.  
- **SQLite** → Banco de dados para armazenamento dos registros.  
- **Pandas** → Manipulação e análise de dados.  

## 📂 Estrutura do Projeto

```
conta-certa/
│── Home.py               # Página principal
│── auth_db.py            # Banco de dados e autenticação
│── historico_db.py       # Banco de dados do histórico de consumo
│── menu_db.py            # Banco de dados dos cardápios
│── requirements.txt      # Dependências do projeto
│
├── pages/                # Páginas adicionais do app
│   ├── 2_Meus_Restaurantes.py   # Gestão de cardápios
│   ├── 3_Historico.py           # Histórico de consumo e gráficos
│   ├── 4_Login.py               # Página de login e autenticação
```

## 🛠️ Instalação e Execução

1️⃣ **Clone o repositório:**  
```bash
git clone https://github.com/seu-usuario/conta-certa.git
cd conta-certa
```

2️⃣ **Crie um ambiente virtual (opcional, mas recomendado):**  
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

3️⃣ **Instale as dependências:**  
```bash
pip install -r requirements.txt
```

4️⃣ **Execute o aplicativo:**  
```bash
streamlit run Home.py
```

## 🌍 Deploy
O aplicativo pode ser implantado no **Streamlit Community Cloud** ou em qualquer outra plataforma que suporte **Python + SQLite**.

---
💡 **Conta Certa** - Controle suas despesas de forma fácil e prática!

