# Configurando Secrets no Streamlit Cloud

Este guia explica como configurar credenciais de login e outras informações sensíveis de forma segura no Streamlit Cloud usando o recurso de Secrets.

## O que são Secrets no Streamlit Cloud?

Secrets são variáveis seguras que você pode usar para armazenar informações sensíveis como:
- Credenciais de usuários (nome de usuário/senha)
- Chaves de API
- Credenciais de banco de dados
- Configurações de email

Esses dados não ficam expostos no código-fonte e são armazenados de forma segura no servidor.

## Como configurar Secrets no Streamlit Cloud

### Passo 1: Fazer o deploy do aplicativo

Primeiro, faça o deploy inicial do aplicativo conforme explicado no README.md principal.

### Passo 2: Acessar a configuração de Secrets

1. No dashboard do Streamlit Cloud, localize seu aplicativo
2. Clique em ⋮ (três pontos) e selecione "Settings"
3. Na página de configurações, clique na aba "Secrets"
4. Clique em "Edit Secrets"

### Passo 3: Adicionar as configurações

Copie e cole o conteúdo abaixo, modificando as credenciais conforme necessário:

```toml
# Credenciais de admin
[credentials]
username = "admin"
password = "sua_senha_segura"

# Credenciais de cliente (opcional)
[client_users]
cliente1 = "senha_cliente1"
cliente2 = "senha_cliente2"
cliente3 = "senha_cliente3"

# Configurações SMTP para envio de emails (opcional)
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "seu-email@gmail.com"
smtp_password = "sua-senha-ou-app-password"
from_email = "seu-email@gmail.com"

# Configurações Twilio para SMS (opcional)
[twilio]
account_sid = "seu-account-sid"
auth_token = "seu-auth-token"
phone_number = "+1234567890"
```

### Passo 4: Salvar as configurações

1. Clique em "Save" para salvar as configurações
2. Seu aplicativo será automaticamente reiniciado para aplicar as novas configurações

## Como usar os Secrets em desenvolvimento local

Para testar localmente (em seu computador), crie um arquivo `.streamlit/secrets.toml` com o mesmo conteúdo acima.

**IMPORTANTE:** Nunca adicione o arquivo `secrets.toml` ao controle de versão (Git). Certifique-se de que ele está listado no arquivo `.gitignore`.

## Exemplo de configuração mínima

Se você quiser apenas configurar login e senha, pode usar apenas esta parte:

```toml
[credentials]
username = "admin"
password = "sua_senha_segura"
```

## Suporte

Se tiver dúvidas sobre a configuração de Secrets, consulte a [documentação oficial do Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) ou entre em contato com o desenvolvedor.