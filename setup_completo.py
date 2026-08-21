import json
import os
import platform
import sys
import subprocess
import secrets

def criar_estrutura_diretorios():
    """Cria a estrutura de pastas do projeto para manter tudo organizado."""
    pastas = [
        "credentials",
        "workflows",
        "scripts"
    ]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    print("📁 Estrutura de diretórios criada/verificada.")

def criar_pasta_react_e_configurar_permissoes():
    """Cria a pasta C:\React no Windows e configura permissões de Controle Total (icacls)."""
    if platform.system() == "Windows":
        caminho_react = r"C:\React"
        try:
            os.makedirs(caminho_react, exist_ok=True)
            print(f"📁 Pasta '{caminho_react}' criada/verificada com sucesso.")

            # Executa o comando icacls para conceder Controle Total (F) para todos os Usuários
            comando = f'icacls "{caminho_react}" /grant Users:(OI)(CI)F /T'
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

            if resultado.returncode == 0:
                print(f"🔒 Permissões configuradas com sucesso para '{caminho_react}'.")
            else:
                print(f"⚠️ Aviso ao aplicar permissões com icacls: {resultado.stderr.strip()}")
        except Exception as e:
            print(f"❌ Erro ao criar ou configurar a pasta '{caminho_react}': {e}")
    else:
        print("ℹ️ O sistema operacional não é Windows. A criação de 'C:\\React' foi ignorada.")

def gerar_api_key_aleatoria():
    """Gera uma chave HEX aleatória de 32 caracteres em maiúsculas."""
    return secrets.token_hex(16).upper()

def solicitar_dados_usuario():
    print("\n" + "="*60)
    print("CONFIGURAÇÃO AUTOMÁTICA DE AMBIENTE (EVOLUTION + N8N) ")
    print("="*60)
    print("Pressione ENTER para aceitar o [Valor Padrão] indicado nos colchetes.")
    print("-"*60)
    config = {}


    # Autenticação e Portas
    print("[1/4] AUTENTICAÇÃO E CONEXÃO DA EVOLUTION API")
    print("A AUTHENTICATION_API_KEY é a chave de segurança da sua API.")
    print("[1] Gerar chave aleatória automaticamente (Recomendado)")
    print("[2] Digitar/Colar minha própria chave")
    print("[3] Usar chave padrão e altera-la depois [429683C4C977415CAAFCCE10F7D57E11]\n")

    opcao_key = input("Escolha uma opção (1/2/3) [1]: ").strip() or "1"

    if opcao_key == "1":
        config['API_KEY'] = gerar_api_key_aleatoria()
        print(f"Chave gerada automaticamente: {config['API_KEY']}")
    elif opcao_key == "2":
        chave_manual = input("Digite a sua AUTHENTICATION_API_KEY: ").strip()
        config['API_KEY'] = chave_manual if chave_manual else "429683C4C977415CAAFCCE10F7D57E11"
    else:
        config['API_KEY'] = "429683C4C977415CAAFCCE10F7D57E11"
        print(f"Usando chave padrão: {config['API_KEY']}")
    print("."*60)
    print("• No seu PC (testes locais): http://localhost:8080")
    print("• Em VPS / Servidor na nuvem: http://IP_DO_SERVIDOR:8080 (ex: http://192.168.1.10:8080)")
    print("• Entre containers Docker (n8n chamando a API): http://evolution_api:8080")
    print("⚠️  Obsercação: A URL só responderá após você subir os containers executando o arquivo")
    print("   'iniciar_aplicacao.bat' (ou rodando 'docker compose up -d' no terminal).\n")

    config['SERVER_URL'] = input("URL da Evolution API [http://localhost:8080]: ").strip() or "http://localhost:8080"
    print("."*60)

    print("Porta de escuta do container da Evolution API.")
    print("• Padrão recomendado: 8080")
    print("• Só altere se a porta 8080 já estiver em uso por outro aplicativo no seu computador.")
    print("⚠️  Observação: Se alterar aqui, lembre-se de ajustar a porta mapeada no docker-compose.yml.\n")

    config['SERVER_PORT'] = input("🔌 Porta da Evolution API [8080]: ").strip() or "8080"
    print("-"*60)

    # Banco Postgres (Compartilhado)
    print("[2/4] DEFINIR INFORMAÇÕES DO BANCO DE DADOS POSTGRESQL")
    print("• Em testes locais no seu PC: Pode aceitar os valores padrão pressionando ENTER.")
    print("• Em produção (Servidor/VPS): Altere a senha (DB_PASS) por segurança.")
    print("• Host: Mantenha 'postgres' se os containers rodarem juntos na mesma VPS.")
    print("⚠️  Observação: O PostgreSQL é o banco de dados que será criado via Docker.\n")

    config['DB_USER'] = input("Usuário Postgres [n8n]: ").strip() or "n8n"
    config['DB_PASS'] = input("Senha Postgres [n8npass]: ").strip() or "n8npass"
    config['DB_HOST'] = input("Host Postgres [postgres]: ").strip() or "postgres"
    config['DB_PORT'] = input("Porta Postgres [5432]: ").strip() or "5432"
    config['DB_NAME'] = input("Nome Banco [n8n]: ").strip() or "n8n"
    print("-"*60)

    # Redis Cache
    print("[3/4] REDIS CACHE (Memória Rápida para Sessões e Filas)")
    print("• Uso padrão Docker: Mantenha 'redis://redis:6379' (conecta direto ao container Redis).")
    print("• Se não alterou configurações de senha no Docker, basta pressionar ENTER.")
    print("⚠️  Observação: O Redis gerencia o cache das sessões do WhatsApp e filas do n8n.\n")

    config['REDIS_CACHE_URI'] = input("⚡ Redis Cache URI [redis://redis:6379]: ").strip() or "redis://redis:6379"
    print("-"*60)

    # Fuso Horário
    print("[4/4] CONFIGURAÇÃO REGIONAL (Fuso Horário do Sistema)")
    print("• Padrão no Brasil (Horário de Brasília): America/Sao_Paulo")
    print("• Outros exemplos válidos: America/Manaus, America/Sao_Paulo, Europe/Lisbon, Etc/UTC")
    print("⚠️  Observação: Define a hora correta para os agendamentos do n8n e logs do WhatsApp.\n")

    config['TIMEZONE'] = input("Fuso Horário [America/Fortaleza]: ").strip() or "America/Fortaleza"

    return config

def gerar_arquivos_credenciais_google_fake():
    """Gera arquivos de modelo/exemplo na pasta credentials com avisos visíveis."""
    path_service_account = os.path.join("credentials", "google_service_account.json.example")
    path_oauth = os.path.join("credentials", "google_oauth_client.json.example")

    service_account_dummy = {
        "type": "service_account",
        "project_id": "seu-projeto-exemplo-id",
        "private_key_id": "REMPLACE_WITH_YOUR_KEY_ID",
        "private_key": "-----BEGIN PRIVATE KEY-----\nSUBSTITUA_PELA_SUA_CHAVE_PRIVADA_REAL_AQUI\n-----END PRIVATE KEY-----\n",
        "client_email": "sua-conta-de-servico@seu-projeto-exemplo-id.iam.gserviceaccount.com",
        "client_id": "000000000000000000000",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sua-conta-de-servico%40seu-projeto-exemplo-id.iam.gserviceaccount.com"
    }

    oauth_dummy = {
        "web": {
            "client_id": "000000000000-xxx.apps.googleusercontent.com",
            "project_id": "seu-projeto-exemplo-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "SUBSTITUA_PELO_SEU_CLIENT_SECRET",
            "redirect_uris": ["http://localhost:5678/rest/oauth2-credential/callback"]
        }
    }

    with open(path_service_account, "w", encoding="utf-8") as f:
        json.dump(service_account_dummy, f, indent=2, ensure_ascii=False)

    with open(path_oauth, "w", encoding="utf-8") as f:
        json.dump(oauth_dummy, f, indent=2, ensure_ascii=False)

    print(" Modelos de credenciais fictícias do Google gerados na pasta '/credentials/'.")

def gerar_gitignore():
    """Gera o arquivo .gitignore para evitar vazamento acidental de chaves no GitHub."""
    gitignore_content = """# ==========================================
# REGRAS DE PYTHON
# ==========================================
.venv/
venv/
env/
.env
*.env
!*.env.example
__pycache__/
*.pyc
*.pyo
*.egg-info/
build/
dist/
senha.txt
*.log

# ==========================================
# REGRAS DE REACT NATIVE / NODE / JAVASCRIPT
# ==========================================
node_modules/
.expo/
dist/
web-build/
.bundle/
vendor/bundle/
*.metro-health-check*

# Builds e Nativos (se gerados localmente)
android/app/build/
android/.gradle/
ios/Pods/
ios/build/

# ==========================================
# SISTEMA E IDEs
# ==========================================
.DS_Store
Thumbs.db
.vscode/
.idea/

# ==========================================
# DADOS DE CONTAINERS E SETUP AUTOMÁTICO
# ==========================================
credentials/*.json
!credentials/*.json.example
n8n_data/
postgres_data/
redis_data/
evolution_instances/
iniciar_aplicacao.bat
iniciar_aplicacao.sh
docker-compose.yml
"""
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print(" Arquivo '.gitignore' gerado para proteção de dados sensíveis.")

def gerar_arquivos_env(cfg):
    env_content = f"""# =========================================================
# Evolution API & n8n Environment Variables
# =========================================================

SERVER_TYPE=http
SERVER_PORT={cfg['SERVER_PORT']}
SERVER_URL={cfg['SERVER_URL']}

CORS_ORIGIN=*
CORS_METHODS=GET,POST,PUT,DELETE
CORS_CREDENTIALS=true

LOG_LEVEL=ERROR,WARN,DEBUG,INFO,LOG,VERBOSE,DARK,WEBHOOKS,WEBSOCKET
LOG_COLOR=true
LOG_BAILEYS=error

EVENT_EMITTER_MAX_LISTENERS=50
DEL_INSTANCE=false

DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI='postgresql://{cfg['DB_USER']}:{cfg['DB_PASS']}@{cfg['DB_HOST']}:{cfg['DB_PORT']}/{cfg['DB_NAME']}?schema=evolution_api'
DATABASE_CONNECTION_CLIENT_NAME=evolution_exchange

DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
DATABASE_SAVE_MESSAGE_UPDATE=true
DATABASE_SAVE_DATA_CONTACTS=true
DATABASE_SAVE_DATA_CHATS=true
DATABASE_SAVE_DATA_LABELS=true
DATABASE_SAVE_DATA_HISTORIC=true
DATABASE_SAVE_IS_ON_WHATSAPP=true
DATABASE_SAVE_IS_ON_WHATSAPP_DAYS=7
DATABASE_DELETE_MESSAGE=true

CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI={cfg['REDIS_CACHE_URI']}
CACHE_REDIS_TTL=604800
CACHE_REDIS_PREFIX_KEY=evolution

AUTHENTICATION_API_KEY={cfg['API_KEY']}
AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
LANGUAGE=pt-BR

# Configuracoes de Fuso Horario
GENERIC_TIMEZONE={cfg['TIMEZONE']}
TZ={cfg['TIMEZONE']}

# n8n Database & Configs
POSTGRES_DB={cfg['DB_NAME']}
POSTGRES_USER={cfg['DB_USER']}
POSTGRES_PASSWORD={cfg['DB_PASS']}
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

N8N_DB_TYPE=postgresdb
N8N_DB_SCHEMA=public
N8N_RUNNERS_ENABLED=true
"""

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)

    with open(".env.example", "w", encoding="utf-8") as f_ex:
        f_ex.write(env_content.replace(cfg['API_KEY'], "YOUR_API_KEY_HERE"))

    print("📄 Arquivos '.env' e '.env.example' gerados!")

def gerar_docker_compose():
    compose_content = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-n8n}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-n8npass}
      POSTGRES_DB: ${POSTGRES_DB:-n8n}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    container_name: redis_cache
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network

  evolution-api:
    image: atendai/evolution-api:v1.8.2
    container_name: evolution_api
    restart: always
    env_file:
      - .env
    ports:
      - "${SERVER_PORT:-8080}:8080"
    depends_on:
      - postgres
      - redis
    volumes:
      - evolution_instances:/instance
    networks:
      - app-network

  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n_automation
    restart: always
    env_file:
      - .env
    ports:
      - "5678:5678"
    depends_on:
      - postgres
      - redis
    volumes:
      - n8n_data:/home/node/.n8n
      - ./credentials:/home/node/credentials:ro
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  evolution_instances:
  n8n_data:
"""
    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(compose_content)

    print("🐳 Arquivo 'docker-compose.yml' gerado com sucesso!")

def gerar_script_execucao():
    if platform.system() == "Windows":
        script_bat = """@echo off
echo Subindo containers da Evolution API, n8n, Postgres e Redis...
docker compose up -d

echo.
echo =====================================================
echo  Tudo pronto!
echo  - n8n: http://localhost:5678
echo  - Evolution API: http://localhost:8080
echo =====================================================
pause
"""
        with open("iniciar_aplicacao.bat", "w", encoding="utf-8") as f:
            f.write(script_bat)
        print("🚀 Script de execução 'iniciar_aplicacao.bat' gerado!")
    else:
        script_sh = """#!/bin/bash
echo "Subindo containers..."
docker compose up -d
echo "Tudo pronto!"
"""
        with open("iniciar_aplicacao.sh", "w", encoding="utf-8") as f:
            f.write(script_sh)
        os.chmod("iniciar_aplicacao.sh", 0o755)
        print("🚀 Script de execução 'iniciar_aplicacao.sh' gerado!")

    print("\n⏳ Subindo os containers do Docker...")
    os.system("docker compose up -d")

def gerar_workflow_json():
    path_workflow = os.path.join("workflows", "fluxo_start.json")

    workflow = {
        "name": "Fluxo Start",
        "nodes": [
            {
                "parameters": {"path": "Webhook", "options": {}},
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2.1,
                "position": [2192, 3008],
                "id": "70a5fefc-0a72-48cc-95af-832e32dc196f",
                "name": "Webhook"
            },
            {
                "parameters": {
                    "assignments": {
                        "assignments": [
                            {"id": "6bb07214-2ea5-41ca-8457-9e5094db5d22", "name": "Quem mandou", "value": "={{ $json.body.data.key.remoteJid }}", "type": "string"},
                            {"id": "148fe37f-3711-45e7-8ffd-4832869856ab", "name": "Instancia", "value": "={{ $json.body.instance }}", "type": "string"},
                            {"id": "28401675-8843-491a-bb59-cb31a7a627f7", "name": "Mensagem ", "value": "={{ $json.body.data.message?.conversation || $json.body.data.message?.extendedTextMessage?.text || $json.body.data.message?.audioMessage?.contextInfo?.transcription || \"[Mensagem não suportada/Mídia]\" }}", "type": "string"},
                            {"id": "246600e5-6512-47bd-9201-2b4a39b6e793", "name": "Id da mensagem", "value": "={{ $json.body.data.key.id }}", "type": "string"},
                            {"id": "ba4fe8c9-b79d-458b-b7d6-b74913737da4", "name": "Nome da pessoa ", "value": "={{ $json.pushName || 'Amigo' }}", "type": "string"}
                        ]
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [2384, 3008],
                "id": "69c962d9-6543-4e4e-8cf3-179e8e5b4a44",
                "name": "DADOS"
            },
            {
                "parameters": {
                    "promptType": "define",
                    "text": "={{ $json['Mensagem '] }}",
                    "options": {
                        "systemMessage": "=Regra de Ouro (Prioridade Máxima) Se o usuário informar um nome durante a conversa, ignore qualquer nome vindo dos metadados do sistema. A vontade do usuário sobre como quer ser chamado é a prioridade máxima.\n\nMensagem de Saudação (Passo 1) Texto: Olá! Tudo bem? 😊 Seja bem-vindo(a)!\n\nVi que você demonstrou interesse no nosso anúncio e estou aqui para te ajudar a realizar esse sonho. ✨\n\nPara te atender melhor, me conta rapidinho: 👉 Qual o seu nome?\n\n⚠️ Não consigo ouvir áudio ou receber ligação\n\nColeta do Bem (Passo 2) Somente após o usuário responder o nome, armazene na variável nome e pergunte: Texto: Prazer em te conhecer, [nome]! 😊\n\n👉 O que você deseja adquirir: automóvel ou imóvel? 🚗🏡\n\nMensagem de Desenvolvimento (Passo 3) Assim que o lead identificar o que deseja, armazene na variável bem e responda obrigatoriamente: \nO consórcio é uma forma inteligente e econômica de planejar sua compra: ✔️ Sem juros ✔️ Taxa fixa e diluída ✔️ Sem pagar o dobro do valor.\n\nMe conta: qual valor de crédito você tem em mente para o seu [bem]? 💭\n\nValidação de Valor e Ficha (Passo 4) Analise o valor informado com base no [bem] escolhido:\n\nSe for IMÓVEL: O valor mínimo é 100.000. Se for menor, informe que para imóveis o valor mínimo é 100.000 e peça um novo valor.\n\nSe for AUTOMÓVEL: O valor mínimo é 45.000. Se for menor, informe que para automóveis o valor mínimo é 45.000 e peça um novo valor.\n\nSe o valor for válido: Armazene na variável credito e siga para a ficha.\n\nFicha de Cadastro e Regra de Horário (Ação Obrigatória) Envie este texto logo após a validação do crédito. Verifique o horário atual do sistema:\n\nHorário Comercial: Segunda a Sexta (08:00 às 17:30) e Sábado (08:00 às 12:00).\n\nSe estiver DENTRO do horário: Informe que o consultor entrará em contato em poucos minutos.\n\nSe estiver FORA do horário: Informe que nosso horário é de Seg a Sex (08h às 17h30) e Sáb (08h às 12h) e que o consultor entrará em contato assim que iniciarmos o próximo expediente.\n\nTexto da Ficha: \"Ao ser contemplado, você compra o bem à vista e ganha poder de negociação. Além disso, somos fiscalizados pelo Banco Central, o que garante sua segurança. 🤝\n\nÓtimo! Já organizei seus dados para nossa equipe:\n\nArmazena na variável telefone o valor {{ $('Webhook').item.json.body.data.key.remoteJidAlt.replace(/^55/, '').split('@')[0] }}\n\nNome: [nome]\nBem: [bem]\nValor do Crédito: [credito]\nTelefone: [telefone]\n\n[Inserir a frase de contato (poucos minutos ou próximo expediente) de acordo com o horário atual].\""
                    }
                },
                "type": "@n8n/n8n-nodes-langchain.agent",
                "typeVersion": 3.1,
                "position": [2208, 2736],
                "id": "1fcb0daf-177f-4db8-a0d2-2fb58eb26370",
                "name": "AI Agent"
            },
            {
                "parameters": {
                    "sessionIdType": "customKey",
                    "sessionKey": "=chat_Deu7t_{{ $('DADOS').item.json['Quem mandou'] }}",
                    "sessionTTL": 86400
                },
                "type": "@n8n/n8n-nodes-langchain.memoryRedisChat",
                "typeVersion": 1.5,
                "position": [2304, 2528],
                "id": "1b65f645-ef0a-4d3b-81e8-428bb1031ce8",
                "name": "Memória",
                "credentials": {"redis": {"id": "9sybYoSMY1HwwgF9", "name": "Redis account"}}
            },
            {
                "parameters": {"options": {}},
                "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
                "typeVersion": 1,
                "position": [2208, 2528],
                "id": "9f16221b-ec2d-44bc-93a1-9950e23a523a",
                "name": "Gemini",
                "credentials": {"googlePalmApi": {"id": "4xUhXYMnpk3P5ZYQ", "name": "Google Gemini(PaLM) Api account"}}
            },
            {
                "parameters": {
                    "conditions": {
                        "options": {"caseSensitive": False, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [
                            {"id": "b2d16a50-ccd3-4365-ab2a-9ff7b8d73f9f", "leftValue": "={{ $json.output.includes('Nome:') && $json.output.includes('Valor do Crédito:') }}", "rightValue": "", "operator": {"type": "boolean", "operation": "true", "singleValue": True}}
                        ],
                        "combinator": "and"
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.if",
                "typeVersion": 2.3,
                "position": [2768, 2592],
                "id": "f7e99b2d-1b22-418e-9bab-a371efca200e",
                "name": "If_VALIDAR_VARIAVEIS"
            },
            {
                "parameters": {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [
                            {"id": "ae1af507-0ad1-468f-9cf2-2d137cb79cf5", "leftValue": "={{ $json.ficha_pronta }}", "rightValue": True, "operator": {"type": "boolean", "operation": "true", "singleValue": True}}
                        ],
                        "combinator": "and"
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.if",
                "typeVersion": 2.3,
                "position": [3360, 2576],
                "id": "5c766fb8-8e45-4689-b7c2-aef6277a11f5",
                "name": "IF_VERIFICA_FICHA_COMPLETA"
            },
            {
                "parameters": {
                    "authentication": "serviceAccount",
                    "operation": "appendOrUpdate",
                    "documentId": {"__rl": True, "value": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit?gid=0#gid=0", "mode": "url"},
                    "sheetName": {"__rl": True, "value": "gid=0", "mode": "list", "cachedResultName": "Página1", "cachedResultUrl": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit#gid=0"},
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "Nome ": "={{ $json.cliente_nome_final }}",
                            "Bem": "={{ $json.cliente_bem_final }}",
                            "Valor do Crédito": "={{ $json.cliente_credito_final }}",
                            "Telefone": "={{ $json.cliente_telefone_final }}"
                        },
                        "matchingColumns": ["Telefone"],
                        "schema": [
                            {"id": "Nome ", "displayName": "Nome ", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True, "removed": False},
                            {"id": "Bem", "displayName": "Bem", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True, "removed": False},
                            {"id": "Valor do Crédito", "displayName": "Valor do Crédito", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True, "removed": False},
                            {"id": "Telefone", "displayName": "Telefone", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True, "removed": False}
                        ],
                        "attemptToConvertTypes": False,
                        "convertFieldsToString": False
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.googleSheets",
                "typeVersion": 4.7,
                "position": [2976, 2384],
                "id": "79184251-a0a5-442f-9365-782168419a7f",
                "name": "Update_CADASTRO_CLIENTES",
                "credentials": {"googleApi": {"id": "xIPdXlbOLiG3xdV3", "name": "Google Service Account account"}}
            },
            {
                "parameters": {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [
                            {"id": "bc556881-125f-41c3-9a9a-5e6f18c8f119", "leftValue": "={{ $json.body.data.key.fromMe }}", "rightValue": "", "operator": {"type": "boolean", "operation": "false", "singleValue": True}}
                        ],
                        "combinator": "and"
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.if",
                "typeVersion": 2.3,
                "position": [2560, 3008],
                "id": "57ff95fb-7957-4624-b9d3-2f8d062f3fda",
                "name": "If_IDENTIFICAR_QUEM_ENVIA"
            },
            {
                "parameters": {
                    "jsCode": "const aiDados = $(\"AI Agent\").item.json;\nconst respostaIA = aiDados.output || \"\";\n\nfunction extrairFicha(texto) {\n    const nomeMatch = texto.match(/Nome:\\s*([^\\n]+)/i);\n    const bemMatch = texto.match(/Bem:\\s*([^\\n]+)/i);\n    const creditoMatch = texto.match(/Valor do Crédito:\\s*([^\\n]+)/i);\n    const telefoneMatch = texto.match(/Telefone:\\s*([^\\n]+)/i);\n\n    return {\n        nome: nomeMatch ? nomeMatch[1].trim() : \"Não informado\",\n        bem: bemMatch ? bemMatch[1].trim() : \"Consórcio\",\n        credito: creditoMatch ? creditoMatch[1].trim() : \"A combinar\",\n        telefone: telefoneMatch ? telefoneMatch[1].trim() : \"Não informado\"\n    };\n}\n\nconst ficha = extrairFicha(respostaIA);\n\nconst nodeVendedores = $(\"Get_DISTRIBUIR_LEAD\"); \nconst vendedores = nodeVendedores.all().map((v, index) => ({\n  ...v.json,\n  row_number: index + 2\n}));\n\nvendedores.sort((a, b) => (parseInt(a[\"CONTAGEM DE LEADS:\"] || 0) - parseInt(b[\"CONTAGEM DE LEADS:\"] || 0)));\nconst escolhido = vendedores[0] || {};\n\nreturn {\n  ...escolhido,\n  output_limpo: respostaIA, \n  cliente_nome_final: ficha.nome,\n  cliente_bem_final: ficha.bem,\n  cliente_credito_final: ficha.credito,\n  cliente_telefone_final: ficha.telefone,\n  ficha_pronta: respostaIA.toLowerCase().includes(\"nome:\") && respostaIA.toLowerCase().includes(\"valor do crédito:\")\n};"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [3168, 2576],
                "id": "df916df6-4c93-47fd-8da7-2591bb78151b",
                "name": "JS_ORDEM_VENDEDOR"
            },
            {
                "parameters": {
                    "authentication": "serviceAccount",
                    "operation": "update",
                    "documentId": {"__rl": True, "value": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit?usp=sharing", "mode": "url"},
                    "sheetName": {"__rl": True, "value": "gid=0", "mode": "list", "cachedResultName": "Página1", "cachedResultUrl": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit#gid=0"},
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "row_number": "={{ $json.row_number }}",
                            "CONTAGEM DE LEADS:": "={{ Number($json[\"CONTAGEM DE LEADS:\"]) + 1 }}"
                        },
                        "matchingColumns": ["row_number"],
                        "schema": [
                            {"id": "NOME DO VENDEDOR:", "displayName": "NOME DO VENDEDOR:", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True},
                            {"id": "NÚMERO DO VENDEDOR:", "displayName": "NÚMERO DO VENDEDOR:", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True},
                            {"id": "CONTAGEM DE LEADS:", "displayName": "CONTAGEM DE LEADS:", "required": False, "defaultMatch": False, "display": True, "type": "string", "canBeUsedToMatch": True},
                            {"id": "row_number", "displayName": "row_number", "required": False, "defaultMatch": False, "display": True, "type": "number", "canBeUsedToMatch": True, "readOnly": True, "removed": False}
                        ],
                        "attemptToConvertTypes": False,
                        "convertFieldsToString": False
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.googleSheets",
                "typeVersion": 4.7,
                "position": [3552, 2464],
                "id": "4bc52ed2-49fe-4250-98fb-d7606262cc07",
                "name": "Update_DISTRIBUIR_LEAD",
                "credentials": {"googleApi": {"id": "xIPdXlbOLiG3xdV3", "name": "Google Service Account account"}}
            },
            {
                "parameters": {
                    "authentication": "serviceAccount",
                    "documentId": {"__rl": True, "value": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit?usp=sharing", "mode": "url"},
                    "sheetName": {"__rl": True, "value": "gid=0", "mode": "list", "cachedResultName": "Página1", "cachedResultUrl": "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA/edit#gid=0"},
                    "options": {
                        "dataLocationOnSheet": {"values": {"rangeDefinition": "detectAutomatically"}},
                        "outputFormatting": {"values": {"general": "UNFORMATTED_VALUE", "date": "FORMATTED_STRING"}},
                        "returnFirstMatch": False
                    }
                },
                "type": "n8n-nodes-base.googleSheets",
                "typeVersion": 4.7,
                "position": [2976, 2576],
                "id": "327f0ead-58e3-4c28-ba47-cf609dd3dbc0",
                "name": "Get_DISTRIBUIR_LEAD",
                "credentials": {"googleApi": {"id": "xIPdXlbOLiG3xdV3", "name": "Google Service Account account"}},
                "onError": "continueRegularOutput"
            },
            {
                "parameters": {
                    "resource": "messages-api",
                    "instanceName": "=SUA_INSTANCIA",
                    "remoteJid": "={{ $('JS_ORDEM_VENDEDOR').item.json['NÚMERO DO VENDEDOR:'] }}@s.whatsapp.net",
                    "messageText": "=NOVO LEAD! 🚨 \nNome: {{ $json.cliente_nome_final }} \nTelefone: {{ $json.cliente_telefone_final }} \nInteresse: {{ $json.cliente_bem_final }} \nValor do crédito: {{ $json.cliente_credito_final }}",
                    "options_message": {}
                },
                "type": "n8n-nodes-evolution-api.evolutionApi",
                "typeVersion": 1,
                "position": [3552, 2672],
                "id": "f0d05681-32cd-4f39-b1b7-eb13bff2d015",
                "name": "MENSAGEM_VENDEDOR",
                "credentials": {"evolutionApi": {"id": "PiWuJSOAOB3S3UmO", "name": "Evolution account"}}
            },
            {
                "parameters": {
                    "resource": "messages-api",
                    "instanceName": "={{ $('DADOS').item.json.Instancia }}",
                    "remoteJid": "={{ $('DADOS').item.json['Quem mandou'] }}",
                    "messageText": "={{ $('AI Agent').item.json.output }}",
                    "options_message": {"delay": 2000}
                },
                "type": "n8n-nodes-evolution-api.evolutionApi",
                "typeVersion": 1,
                "position": [2992, 2864],
                "id": "0b34063f-91d8-439e-83d4-29dcc48f0595",
                "name": "RESPOSTA_CLIENTE",
                "credentials": {"evolutionApi": {"id": "PiWuJSOAOB3S3UmO", "name": "Evolution account"}}
            },
            {
                "parameters": {
                    "resource": "chat-api",
                    "operation": "read-messages",
                    "instanceName": "={{ $('DADOS').item.json.Instancia }}",
                    "remoteJid": "=",
                    "messageId": "={{ $('DADOS').item.json['Id da mensagem'] }}"
                },
                "type": "n8n-nodes-evolution-api.evolutionApi",
                "typeVersion": 1,
                "position": [2768, 2864],
                "id": "f26a5add-28ab-4309-b161-805c4d8bde43",
                "name": "LER_MENSAGEM",
                "credentials": {"evolutionApi": {"id": "PiWuJSOAOB3S3UmO", "name": "Evolution account"}}
            }
        ],
        "pinData": {},
        "connections": {
            "Webhook": {"main": [[{"node": "DADOS", "type": "main", "index": 0}]]},
            "DADOS": {"main": [[{"node": "If_IDENTIFICAR_QUEM_ENVIA", "type": "main", "index": 0}]]},
            "AI Agent": {"main": [[{"node": "If_VALIDAR_VARIAVEIS", "type": "main", "index": 0}, {"node": "LER_MENSAGEM", "type": "main", "index": 0}]]},
            "Memória": {"ai_memory": [[{"node": "AI Agent", "type": "ai_memory", "index": 0}]]},
            "Gemini": {"ai_languageModel": [[{"node": "AI Agent", "type": "ai_languageModel", "index": 0}]]},
            "If_VALIDAR_VARIAVEIS": {"main": [[{"node": "Update_CADASTRO_CLIENTES", "type": "main", "index": 0}, {"node": "Get_DISTRIBUIR_LEAD", "type": "main", "index": 0}]]},
            "IF_VERIFICA_FICHA_COMPLETA": {"main": [[{"node": "Update_DISTRIBUIR_LEAD", "type": "main", "index": 0}, {"node": "MENSAGEM_VENDEDOR", "type": "main", "index": 0}]]},
            "If_IDENTIFICAR_QUEM_ENVIA": {"main": [[{"node": "AI Agent", "type": "main", "index": 0}]]},
            "JS_ORDEM_VENDEDOR": {"main": [[{"node": "IF_VERIFICA_FICHA_COMPLETA", "type": "main", "index": 0}]]},
            "Get_DISTRIBUIR_LEAD": {"main": [[{"node": "JS_ORDEM_VENDEDOR", "type": "main", "index": 0}]]},
            "LER_MENSAGEM": {"main": [[{"node": "RESPOSTA_CLIENTE", "type": "main", "index": 0}]]}
        },
        "active": True,
        "settings": {"executionOrder": "v1", "availableInMCP": False},
        "versionId": "3795acaf-adfc-48cc-bf25-e6b1062202a6",
        "meta": {"templateCredsSetupCompleted": True, "instanceId": "9112ef9c2aeaf042adbe7c10fc0771a4c8c10b270d2bb899335ae82573ec58a8"},
        "id": "0W0lhZ74rSz8wWkg",
        "tags": []
    }

    with open(path_workflow, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print("Arquivo 'fluxo_start.json' gerado na pasta '/workflows/'.")

if __name__ == "__main__":
    criar_estrutura_diretorios()
    criar_pasta_react_e_configurar_permissoes()
    dados = solicitar_dados_usuario()
    gerar_arquivos_credenciais_google_fake()
    gerar_gitignore()
    gerar_arquivos_env(dados)
    gerar_docker_compose()
    gerar_script_execucao()
    gerar_workflow_json()

    print("\n" + "="*60)
    print("AMBIENTE GERADO E CONFIGURADO COM SUCESSO!")
    print("="*60)
    print("ATENÇÃO SOBRE AS CREDENCIAIS DO GOOGLE:")
    print(" 1. Acesse a pasta '/credentials/'.")
    print(" 2. Renomeie 'google_service_account.json.example' para 'google_service_account.json'.")
    print(" 3. Abra o arquivo e substitua o conteúdo pelo JSON REAL da sua Service Account do Google Cloud.")
    print(" 4. O arquivo '.gitignore' já foi configurado para impedir a subida de suas chaves reais.")
    print("\nPróximos passos:")
    print(" 1. Execute: iniciar_aplicacao.bat (ou ./iniciar_aplicacao.sh no Linux/Mac)")
    print(" 2. Abra o n8n em: http://localhost:5678")
    print(" 3. Importe o fluxo que está em 'workflows/fluxo_start.json'")
    print("="*60 + "\n")
