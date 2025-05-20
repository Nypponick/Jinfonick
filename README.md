# JGR Broker - Sistema de Acompanhamento de Processos

Este é o sistema de acompanhamento de processos de importação e exportação da JGR Broker.

## Como fazer o Deploy no Streamlit Cloud

### Passo 1: Criar repositório no GitHub
1. Acesse [GitHub](https://github.com) e faça login
2. Crie um novo repositório (pode ser privado)
3. Faça upload de todos estes arquivos para o repositório, mantendo a estrutura de pastas

### Passo 2: Conectar no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io/)
2. Faça login com sua conta do GitHub
3. Clique em "New app"
4. Selecione o repositório que você criou
5. Configure a implantação:
   - **Main file path**: app.py
   - **Python version**: 3.11
6. Clique em "Deploy!"

### Passo 3: Acesse seu aplicativo
Após o deploy, você receberá um link para seu aplicativo no formato:
https://[seu-usuario]-[nome-repositorio].streamlit.app

## Estrutura de Arquivos

- `app.py` - Arquivo principal do aplicativo
- `data.py` - Gerenciamento de dados
- `utils.py` - Funções utilitárias
- `components/` - Componentes da interface
- `assets/` - Recursos (CSS, imagens, etc.)
- Arquivos HTML e JavaScript para exportação de relatórios

## Observações Importantes

- No Streamlit Cloud, os dados em arquivos JSON serão resetados a cada nova implantação.
- A pasta `html_exports` é temporária e os relatórios gerados não ficarão permanentes.
- Para atualizar o aplicativo, basta fazer commit das alterações no repositório GitHub.