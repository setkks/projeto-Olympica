import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Olympica - Gestão de Ginástica", page_icon="🏅", layout="wide")

# URL base do seu backend no Xano (substitua pela sua URL do Xano quando necessário)
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:uXJ4j_28" 

# Inicialização de estado de sessão para autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# --- TELA DE LOGIN ---
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🏅 Sistema Olympica - Acesso")
        st.caption("Insira suas credenciais para acessar o painel de gestão.")
        
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar", type="primary", use_container_width=True):
            if email and password:
                # Simulação / Integração com endpoint /auth/login do Xano
                try:
                    payload = {"email": email, "password": password}
                    # Exemplo de chamada real:
                    # res = requests.post(f"{XANO_BASE_URL}/auth/login", json=payload)
                    # if res.status_code == 200:
                    #     data = res.json()
                    #     st.session_state.token = data.get("authToken")
                    #     st.session_state.authenticated = True
                    
                    # Modo de demonstração local rápido:
                    st.session_state.token = "fake_jwt_token_olympica"
                    st.session_state.user = {"name": "Administrador", "email": email}
                    st.session_state.authenticated = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao conectar com o backend: {e}")
            else:
                st.warning("Preencha todos os campos.")

# --- TELA PRINCIPAL (APÓS LOGIN) ---
def show_dashboard():
    st.sidebar.markdown(f"**Usuário:** {st.session_state.user.get('name', 'Admin')}")
    st.sidebar.caption(f"E-mail: {st.session_state.user.get('email', '')}")
    
    if st.sidebar.button("Sair / Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()

    st.sidebar.divider()
    opcao = st.sidebar.radio("Navegação", ["Dashboard", "Atletas", "Turmas", "Matrículas"])

    if opcao == "Dashboard":
        st.title("📊 Painel Geral")
        col1, col2, col3 = st.columns(3)
        col1.metric("Atletas Cadastrados", "12")
        col2.metric("Turmas Ativas", "4")
        col3.metric("Matrículas Realizadas", "18")
        st.info("Selecione um dos módulos no menu lateral para gerenciar os dados.")

    elif opcao == "Atletas":
        st.title("🏃‍♂️ Gestão de Atletas")
        
        with st.expander("➕ Cadastrar Novo Atleta", expanded=True):
            with st.form("form_atleta"):
                nome = st.text_input("Nome Completo")
                data_nasc = st.date_input("Data de Nascimento")
                categoria = st.selectbox("Categoria", ["Mirim", "Infantil", "Juvenil", "Adulto"])
                cadastrar = st.form_submit_button("Salvar Atleta")
                
                if cadastrar:
                    st.success(f"Atleta '{nome}' cadastrado com sucesso!")

        st.subheader("Lista de Atletas")
        # Exemplo de tabela de listagem
        st.dataframe(
            [
                {"ID": 1, "Nome": "Ana Silva", "Categoria": "Infantil", "Status": "Ativo"},
                {"ID": 2, "Nome": "Lucas Mendes", "Categoria": "Juvenil", "Status": "Ativo"},
            ],
            use_container_width=True
        )

    elif opcao == "Turmas":
        st.title("🤸‍♀️ Gestão de Turmas")
        
        with st.expander("➕ Criar Nova Turma"):
            with st.form("form_turma"):
                nome_turma = st.text_input("Nome da Turma (Ex: GA Solo Avançado)")
                horario = st.text_input("Horários (Ex: Seg/Qua 14:00 - 16:00)")
                capacidade = st.number_input("Capacidade Máxima", min_value=1, value=15)
                salvar_turma = st.form_submit_button("Criar Turma")
                
                if salvar_turma:
                    st.success(f"Turma '{nome_turma}' criada com sucesso!")

    elif opcao == "Matrículas":
        st.title("📝 Vínculo Atleta-Turma")
        st.write("Realize a matrícula de um atleta registrado em uma das turmas ativas.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.selectbox("Selecione o Atleta", ["Ana Silva", "Lucas Mendes"])
        with col_b:
            st.selectbox("Selecione a Turma", ["GA Solo Infantil - Seg/Qua", "GA Trave Juvenil - Ter/Qui"])
            
        if st.button("Confirmar Matrícula", type="primary"):
            st.success("Matrícula realizada com sucesso!")

# --- FLUXO PRINCIPAL ---
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()