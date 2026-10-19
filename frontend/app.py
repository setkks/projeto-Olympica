import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Olympica - Gestão de Ginástica", page_icon="🏅", layout="wide")

# URL Base do Grupo de APIs no Xano (substitua pela URL do seu workspace se for diferente)
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:uXJ4j_28" 

# Inicialização do estado de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Funções auxiliares para requisições à API
def get_headers():
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def fetch_data(endpoint):
    try:
        response = requests.get(f"{XANO_BASE_URL}{endpoint}", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        st.error(f"Erro ao carregar dados ({response.status_code}): {response.text}")
        return []
    except Exception as e:
        st.error(f"Erro na conexão com a API: {e}")
        return []

def post_data(endpoint, payload):
    try:
        response = requests.post(f"{XANO_BASE_URL}{endpoint}", json=payload, headers=get_headers())
        if response.status_code in [200, 201]:
            return True, response.json()
        return False, response.text
    except Exception as e:
        return False, str(e)

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
                # Tenta autenticar na API do Xano
                success, result = post_data("/auth/login", {"email": email, "password": password})
                if success and isinstance(result, dict) and "authToken" in result:
                    st.session_state.token = result.get("authToken")
                    st.session_state.user = {"name": email.split("@")[0].capitalize(), "email": email}
                    st.session_state.authenticated = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    # Fallback / Modo de demonstração local se o login ainda não estiver rodando no Xano
                    st.info("Conectando em modo local / demonstração...")
                    st.session_state.token = "demo_jwt_token"
                    st.session_state.user = {"name": email.split("@")[0].capitalize(), "email": email}
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.warning("Preencha todos os campos.")

# --- TELA PRINCIPAL (DASHBOARD & MÓDULOS) ---
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
        atletas = fetch_data("/atleta")
        turmas = fetch_data("/turma")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Atletas Cadastrados", len(atletas) if isinstance(atletas, list) else 0)
        col2.metric("Turmas Ativas", len(turmas) if isinstance(turmas, list) else 0)
        col3.metric("Matrículas Realizadas", "0")

    elif opcao == "Atletas":
        st.title("🏃‍♂️ Gestão de Atletas")
        
        with st.expander("➕ Cadastrar Novo Atleta", expanded=False):
            with st.form("form_atleta"):
                nome = st.text_input("Nome Completo")
                data_nasc = st.date_input("Data de Nascimento")
                categoria = st.selectbox("Categoria", ["Mirim", "Infantil", "Juvenil", "Adulto"])
                cadastrar = st.form_submit_button("Salvar Atleta")
                
                if cadastrar:
                    payload = {
                        "nome": nome,
                        "data_nascimento": str(data_nasc),
                        "categoria": categoria
                    }
                    ok, res = post_data("/atleta", payload)
                    if ok:
                        st.success(f"Atleta '{nome}' cadastrado no Xano com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao cadastrar atleta: {res}")

        st.subheader("Lista de Atletas Registrados")
        atletas = fetch_data("/atleta")
        if atletas and isinstance(atletas, list):
            st.dataframe(atletas, use_container_width=True)
        else:
            st.info("Nenhum atleta cadastrado ainda.")

    elif opcao == "Turmas":
        st.title("🤸‍♀️ Gestão de Turmas")
        
        with st.expander("➕ Criar Nova Turma"):
            with st.form("form_turma"):
                nome_turma = st.text_input("Nome da Turma (Ex: GA Solo Avançado)")
                horario = st.text_input("Horários (Ex: Seg/Qua 14:00 - 16:00)")
                capacidade = st.number_input("Capacidade Máxima", min_value=1, value=15)
                salvar_turma = st.form_submit_button("Criar Turma")
                
                if salvar_turma:
                    payload = {
                        "nome": nome_turma,
                        "horario": horario,
                        "capacidade": int(capacidade)
                    }
                    ok, res = post_data("/turma", payload)
                    if ok:
                        st.success(f"Turma '{nome_turma}' registrada com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao criar turma: {res}")

        st.subheader("Turmas Ativas")
        turmas = fetch_data("/turma")
        if turmas and isinstance(turmas, list):
            st.dataframe(turmas, use_container_width=True)
        else:
            st.info("Nenhuma turma cadastrada ainda.")

    elif opcao == "Matrículas":
        st.title("📝 Vínculo Atleta-Turma")
        
        atletas = fetch_data("/atleta")
        turmas = fetch_data("/turma")
        
        if atletas and turmas and isinstance(atletas, list) and isinstance(turmas, list):
            dict_atletas = {f"{a.get('nome')} (ID: {a.get('id')})": a.get('id') for a in atletas}
            dict_turmas = {f"{t.get('nome')} (ID: {t.get('id')})": t.get('id') for t in turmas}
            
            col_a, col_b = st.columns(2)
            with col_a:
                atleta_sel = st.selectbox("Selecione o Atleta", list(dict_atletas.keys()))
            with col_b:
                turma_sel = st.selectbox("Selecione a Turma", list(dict_turmas.keys()))
                
            if st.button("Confirmar Matrícula", type="primary"):
                payload = {
                    "atleta_id": dict_atletas[atleta_sel],
                    "turma_id": dict_turmas[turma_sel]
                }
                ok, res = post_data("/matricula", payload)
                if ok:
                    st.success("Matrícula realizada com sucesso!")
                else:
                    st.error(f"Erro ao vincular matrícula: {res}")
        else:
            st.warning("É necessário ter pelo menos um atleta e uma turma cadastrados para realizar matrículas.")

# --- FLUXO PRINCIPAL ---
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()