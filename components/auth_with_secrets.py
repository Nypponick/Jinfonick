import streamlit as st
import json
import os
import hashlib
from datetime import datetime, timedelta
import uuid

# Caminho para o arquivo de usuários
USERS_FILE = 'users.json'

def init_auth_state():
    """Inicializa o estado de autenticação na sessão"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'client_processes' not in st.session_state:
        st.session_state.client_processes = []

def get_password_hash(password):
    """Criar hash seguro da senha"""
    # Método mais seguro usando hash SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Carregar usuários do arquivo ou usar secrets do Streamlit Cloud"""
    # Tentar carregar usuários do arquivo
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Se o arquivo não existir ou der erro, tentar usar secrets
    try:
        # Verificar se temos secrets configurados
        if hasattr(st, 'secrets') and 'credentials' in st.secrets:
            admin_username = st.secrets.credentials.username
            admin_password = get_password_hash(st.secrets.credentials.password)
            
            default_users = {
                "users": [
                    {
                        "id": "admin",
                        "name": "Administrador",
                        "email": "admin@jgr.com.br",
                        "password": admin_password,
                        "role": "admin",
                        "created_at": datetime.now().isoformat()
                    }
                ]
            }
            
            # Adicionar clientes configurados nos secrets
            if hasattr(st.secrets, 'client_users'):
                client_id = 1
                for username, password in st.secrets.client_users.items():
                    default_users["users"].append({
                        "id": f"client_{client_id}",
                        "name": username,
                        "email": f"{username}@cliente.com",
                        "password": get_password_hash(password),
                        "role": "client",
                        "client_id": f"cliente_{client_id}",
                        "created_at": datetime.now().isoformat()
                    })
                    client_id += 1
            
            # Usar os users configurados no secrets.toml
            return default_users
    except Exception as e:
        st.error(f"Erro ao carregar secrets: {e}")
    
    # Criar arquivo com usuário admin padrão se não existir
    admin_password = get_password_hash("admin123")
    default_users = {
        "users": [
            {
                "id": "admin",
                "name": "Administrador",
                "email": "admin@jgr.com.br",
                "password": admin_password,
                "role": "admin",
                "created_at": datetime.now().isoformat()
            }
        ]
    }
    
    # Salvar o arquivo para futuros usos
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)
    except Exception as e:
        st.warning(f"Não foi possível salvar o arquivo de usuários: {e}")
    
    return default_users

def save_users(users_data):
    """Salvar usuários no arquivo"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar usuários: {e}")
        return False

def check_login(username, password):
    """Verificar login"""
    # Carregar usuários
    users_data = load_users()
    
    # Verificar se é um usuário no arquivo
    for user in users_data.get('users', []):
        if user.get('email') == username:
            if user.get('password') == get_password_hash(password):
                return user
            else:
                # Verificar senhas sem hash para compatibilidade
                if user.get('password') == password:
                    return user
    
    # Verificar diretamente no secrets (verificação adicional)
    try:
        if hasattr(st, 'secrets') and 'credentials' in st.secrets:
            if username == st.secrets.credentials.username and password == st.secrets.credentials.password:
                # Retornar usuário admin do secrets
                return {
                    "id": "admin",
                    "name": "Administrador",
                    "email": st.secrets.credentials.username,
                    "role": "admin"
                }
            
            # Verificar clientes nos secrets
            if hasattr(st.secrets, 'client_users'):
                for client_name, client_pwd in st.secrets.client_users.items():
                    if username == client_name and password == client_pwd:
                        client_id = f"cliente_{list(st.secrets.client_users.keys()).index(client_name) + 1}"
                        return {
                            "id": f"client_{client_id}",
                            "name": client_name,
                            "email": f"{client_name}@cliente.com",
                            "role": "client",
                            "client_id": client_id
                        }
    except Exception as e:
        st.warning(f"Erro ao verificar secrets: {e}")
    
    return None

def display_login():
    """Mostrar tela de login"""
    init_auth_state()
    
    if st.session_state.authenticated:
        st.success(f"Login realizado com sucesso como {st.session_state.user_name}")
        st.button("Logout", on_click=logout)
        return True
    
    st.title("Acesso ao Sistema")
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("E-mail", placeholder="Digite seu e-mail")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            user = check_login(username, password)
            if user:
                # Autenticar usuário
                st.session_state.authenticated = True
                st.session_state.user_id = user.get('id')
                st.session_state.user_role = user.get('role')
                st.session_state.user_name = user.get('name')
                st.session_state.user_email = user.get('email')
                
                # Se for cliente, definir os processos associados
                if user.get('role') == 'client' and 'client_id' in user:
                    st.session_state.client_id = user.get('client_id')
                
                st.success(f"Login realizado com sucesso como {user.get('name')}")
                st.rerun()
            else:
                st.error("Credenciais inválidas. Tente novamente.")
    
    # Mostrar informações sobre os secrets (apenas em modo desenvolvedor)
    if st.checkbox("Modo desenvolvedor"):
        st.write("Verifique secrets.toml para configurar usuários")
        
        # Verificar se secrets estão configurados
        if hasattr(st, 'secrets') and 'credentials' in st.secrets:
            st.success("✅ Secrets estão configurados")
        else:
            st.warning("⚠️ Secrets não estão configurados. O sistema usará o arquivo users.json local.")
    
    return False

def logout():
    """Fazer logout do sistema"""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.client_processes = []
    st.session_state.client_id = None
    st.rerun()

def display_user_management():
    """Mostrar gerenciamento de usuários"""
    if not st.session_state.authenticated or st.session_state.user_role != 'admin':
        st.error("Acesso não autorizado")
        return
    
    st.title("Gerenciamento de Usuários")
    
    # Carregar usuários
    users_data = load_users()
    users = users_data.get('users', [])
    
    # Interface para adicionar usuário
    with st.expander("Adicionar Novo Usuário", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Nome", key="add_name")
                new_email = st.text_input("E-mail", key="add_email")
                new_password = st.text_input("Senha", type="password", key="add_password")
            
            with col2:
                new_role = st.selectbox("Função", ["admin", "client"], key="add_role")
                new_client_id = st.text_input("ID Cliente (apenas para clientes)", key="add_client_id", 
                                             disabled=new_role != "client")
                
                # Upload de logo do cliente
                client_logo = st.file_uploader("Logo do Cliente (opcional)", type=["png", "jpg", "jpeg"], key="add_logo")
                
            submit_add = st.form_submit_button("Adicionar Usuário")
            
            if submit_add:
                if not new_name or not new_email or not new_password:
                    st.error("Preencha todos os campos obrigatórios")
                elif new_role == "client" and not new_client_id:
                    st.error("ID do Cliente é obrigatório para usuários do tipo client")
                else:
                    # Verificar se e-mail já existe
                    exists = False
                    for user in users:
                        if user.get('email') == new_email:
                            exists = True
                            break
                    
                    if exists:
                        st.error("Usuário com este e-mail já existe")
                    else:
                        # Gerar ID único para o usuário
                        user_id = str(uuid.uuid4())
                        
                        # Criar novo usuário
                        new_user = {
                            "id": user_id,
                            "name": new_name,
                            "email": new_email,
                            "password": get_password_hash(new_password),
                            "role": new_role,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        # Adicionar ID do cliente se for cliente
                        if new_role == "client":
                            new_user["client_id"] = new_client_id
                        
                        # Salvar logo se fornecido
                        if client_logo:
                            try:
                                logo_dir = "assets/client_logos"
                                os.makedirs(logo_dir, exist_ok=True)
                                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                                logo_path = f"{logo_dir}/logo_{timestamp}.png"
                                with open(logo_path, "wb") as f:
                                    f.write(client_logo.getbuffer())
                                new_user["logo_path"] = logo_path
                            except Exception as e:
                                st.warning(f"Erro ao salvar logo: {e}")
                        
                        # Adicionar usuário à lista
                        users.append(new_user)
                        users_data['users'] = users
                        
                        # Salvar usuários
                        if save_users(users_data):
                            st.success(f"Usuário {new_name} adicionado com sucesso")
                            st.rerun()
                        else:
                            st.error("Erro ao salvar usuário")
    
    # Listar usuários
    st.subheader("Lista de Usuários")
    
    if not users:
        st.info("Nenhum usuário cadastrado")
    else:
        for i, user in enumerate(users):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Nome:** {user.get('name')}")
                st.write(f"**E-mail:** {user.get('email')}")
                st.write(f"**Função:** {user.get('role')}")
                if user.get('role') == 'client':
                    st.write(f"**ID Cliente:** {user.get('client_id', 'Não definido')}")
                    if user.get('logo_path'):
                        st.write("**Logo:** Definido")
            
            with col2:
                # Formulário de edição
                with st.form(f"edit_user_{i}", clear_on_submit=False):
                    st.write("**Editar**")
                    edit_password = st.text_input("Nova senha", type="password", key=f"edit_password_{i}")
                    if user.get('role') == 'client':
                        edit_client_id = st.text_input("Novo ID Cliente", 
                                                      value=user.get('client_id', ''),
                                                      key=f"edit_client_id_{i}")
                    else:
                        edit_client_id = None
                        
                    edit_logo = st.file_uploader("Nova logo", type=["png", "jpg", "jpeg"], key=f"edit_logo_{i}")
                    
                    submit_edit = st.form_submit_button("Atualizar")
                    
                    if submit_edit:
                        updated = False
                        
                        # Atualizar senha
                        if edit_password:
                            user['password'] = get_password_hash(edit_password)
                            updated = True
                        
                        # Atualizar ID do cliente
                        if edit_client_id is not None and edit_client_id != user.get('client_id', ''):
                            user['client_id'] = edit_client_id
                            updated = True
                        
                        # Atualizar logo
                        if edit_logo:
                            try:
                                logo_dir = "assets/client_logos"
                                os.makedirs(logo_dir, exist_ok=True)
                                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                                logo_path = f"{logo_dir}/logo_{timestamp}.png"
                                with open(logo_path, "wb") as f:
                                    f.write(edit_logo.getbuffer())
                                user['logo_path'] = logo_path
                                updated = True
                            except Exception as e:
                                st.warning(f"Erro ao salvar logo: {e}")
                        
                        # Salvar alterações
                        if updated:
                            if save_users(users_data):
                                st.success("Usuário atualizado com sucesso")
                                st.rerun()
                            else:
                                st.error("Erro ao atualizar usuário")
            
            with col3:
                # Botão de exclusão
                if st.button(f"Excluir", key=f"delete_{i}"):
                    if user.get('role') == 'admin' and len([u for u in users if u.get('role') == 'admin']) <= 1:
                        st.error("Não é possível excluir o último administrador")
                    else:
                        # Perguntar confirmação
                        if st.checkbox(f"Confirmar exclusão de {user.get('name')}", key=f"confirm_delete_{i}"):
                            users.remove(user)
                            users_data['users'] = users
                            
                            if save_users(users_data):
                                st.success(f"Usuário {user.get('name')} excluído com sucesso")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir usuário")
            
            st.markdown("---")