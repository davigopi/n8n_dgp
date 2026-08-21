# 🚀 Stack N8N + Evolution API + Redis + Postgres (Docker Starter)

Um guia completo, prático e estruturado em ordem cronológica para instalação, configuração e execução da stack completa de automação (n8n, Evolution API, Postgres, Redis), além de tutoriais de integração (Google Service Account) e prompt base para assistente de IA.

---

## 📋 Sumário
1. [Pré-requisitos e Preparação do Ambiente](#1-pré-requisitos-e-preparação-do-ambiente)
2. [Obtenção e Estrutura do Projeto](#2-obtenção-e-estrutura-do-projeto)
3. [Instalação Rápida Via Script Python (Recomendado)](#3-instalação-rápida-via-script-python-recomendado)
4. [Configuração Manual das Variáveis de Ambiente (.env)](#4-configuração-manual-das-variáveis-de-ambiente-env)
5. [Execução da Stack Docker](#5-execução-da-stack-docker)
6. [Primeiro Acesso e Ativação do n8n](#6-primeiro-acesso-e-ativação-do-n8n)
7. [Instalação do Nó da Evolution API no n8n](#7-instalação-do-nó-da-evolution-api-no-n8n)
8. [Configuração de IA Gratuita (OpenRouter)](#8-configuração-de-ia-gratuita-openrouter)
9. [Regras de Comunicação Interna no Docker (DNS Interno)](#9-regras-de-comunicação-interna-no-docker-dns-interno)
10. [Integração Extra: Google Service Account no n8n](#10-integração-extra-google-service-account-no-n8n)
11. [Bônus: Fluxo de Prompt do Agente de Vendas (Consórcio)](#11-bônus-fluxo-de-prompt-do-agente-de-vendas-consórcio)
12. [Comandos Úteis do Docker](#12-comandos-úteis-do-docker)
13. [Estrutura dos Serviços](#13-estrutura-dos-serviços)
14. [Solução de Problemas](#14-solução-de-problemas)
15. [Suporte e Licença](#15-suporte-e-licença)

---

## 1. Pré-requisitos e Preparação do Ambiente

Siga a ordem dos passos abaixo para preparar seu sistema Windows:

1. Windows Terminal:
   - Abra a Microsoft Store, pesquise por Windows Terminal e instale-o.
2. Instalação do WSL2 (Windows Subsystem for Linux):
   - Abra o Windows Terminal como Administrador e execute:
     wsl --install
3. Reinicialização:
   - REINICIE o computador para finalizar a instalação do subsistema Linux.
4. Instalação do Docker Desktop:
   - Baixe e instale o Docker Desktop para Windows (versão AMD64).
   - Obrigatório: Marque a opção "Use WSL 2 instead of Hyper-V" durante a instalação.
   - Certifique-se de que o Docker Desktop esteja aberto com o status **`Engine running`** (canto inferior esquerdo) e que os containers da aplicação estejam iniciados (status **Running** na aba Containers).
5. Python 3.x:
   - Baixe e instale o Python (versão 3.8 ou superior) para utilizar o assistente automático de configuração.
6. Git (Opcional, mas recomendado):
   - Baixe e instale o Git caso deseje clonar o repositório via linha de comando.

---

## 2. Obtenção e Estrutura do Projeto

Escolha uma das opções abaixo para obter os arquivos do projeto:

### Opção A: Via Git (Recomendado)
1. git clone https://github.com/davigopi/n8n_dgp
2. cd n8n_dgp

### Opção B: Via Download do ZIP
1. Acesse o repositório no GitHub (davigopi/n8n_dgp).
2. Clique em Code > Download ZIP.
3. Extraia o arquivo ZIP no local desejado.
4. Abra o terminal na pasta extraída do projeto.

---

## 3. Instalação Rápida Via Script Python (Recomendado)

Para automatizar a criação da estrutura de pastas, chaves de exemplo, .env, docker-compose.yml, atalhos de execução e a criação automática do workflow inicial (workflows/fluxo_start.json).

1. No terminal, dentro da pasta do projeto, execute:
   python setup_completo.py

2. Responda às perguntas interativas no terminal ou pressione ENTER para aceitar os valores padrão.

3. Para subir a aplicação com 1 clique:
   - Windows: Dê um duplo clique no arquivo iniciar_aplicacao.bat ou rode no terminal:
     iniciar_aplicacao.bat
   - Linux / Mac: Execute no terminal:
     ./iniciar_aplicacao.sh

---

## 4. Configuração Manual das Variáveis de Ambiente (.env)

Caso prefira configurar tudo manualmente sem o script Python:

1. Localize o arquivo .env.example na raiz do projeto.
2. Renomeie o arquivo .env.example para .env:
   - No Linux/macOS/Bash:
     cp .env.example .env
   - No Windows PowerShell:
     Rename-Item -Path .env.example -NewName .env
   - No CMD do Windows:
     copy .env.example .env
3. Ajustes necessários no .env:
   - Abra o arquivo .env em um editor de texto (VS Code, Bloco de Notas, etc.).
   - Altere obrigatoriamente a chave de autenticação da Evolution API:
     AUTHENTICATION_API_KEY=SuaChaveSeguraAqui
   - Revise o fuso horário (TZ, GENERIC_TIMEZONE) e as senhas do PostgreSQL/Redis, se desejar.

⚠️ Atenção nas Variáveis do .env:
1. Chave Global da Evolution API: Altere a variável AUTHENTICATION_API_KEY para uma chave forte e pessoal. Nunca mantenha o valor padrão 429683C4C977415CAAFCCE10F7D57E11.
2. DNS Interno dos Serviços: Garanta que as URIs de banco e cache no .env apontem para os nomes dos containers Docker (postgres e redis), em vez de localhost ou host.docker.internal.

---

## 5. Execução da Stack Docker

Se você optou pela configuração manual (sem usar o iniciar_aplicacao.bat):

1. Abra o terminal dentro da pasta do projeto (onde fica o arquivo docker-compose.yml).
2. Suba todos os contêineres (n8n, Evolution API, Postgres, Redis):
   docker compose up -d
3. Mantenha o Docker rodando em segundo plano:
   - Certifique-se de que o Docker Desktop exiba **`Engine running`** (verde) no canto inferior esquerdo.
   - Abra a aba **Containers** e verifique se todos os serviços (`n8n`, `evolution-api`, `postgres`, `redis`) estão com status **Running** (ícone verde).

ℹ️ Nota: O arquivo docker-compose.yml orquestra os serviços na rede isolada app-network e mapeia o acesso externo para as portas 5678 (n8n) e 8080 (Evolution).

---

## 6. Primeiro Acesso e Ativação do n8n

1. Acesse o n8n no seu navegador: http://localhost:5678
2. Crie a conta de administrador preenchendo seu nome, e-mail e senha.
3. Ativação da Licença Comunitária:
   - Na tela inicial, solicite a chave gratuita da comunidade por e-mail.
   - Abra a caixa de entrada do seu e-mail e COPIE a chave alfanumérica recebida (Atenção: não clique no link, apenas copie o código).
   - Cole o código no painel do n8n para concluir a ativação.

---

## 7. Instalação do Nó da Evolution API no n8n

1. No painel do n8n, navegue até Settings > Community Nodes.
2. Clique em Install a community node.
3. No campo de nome do pacote, insira:
   n8n-nodes-evolution-api
4. Marque a caixa de seleção de ciência de riscos e clique em Install.

---

## 8. Configuração de IA Gratuita (OpenRouter)

1. Acesse https://openrouter.ai e crie uma conta.
2. Acesse Keys > Create Key e copie a chave gerada.
3. No n8n, crie uma nova credencial do tipo OpenRouter/OpenAI Header Auth e insira sua chave.
4. Nos nós de linguagem/IA do n8n, utilize modelos gratuitos marcados com o sufixo :free (ex: google/gemma-2-9b-it:free).

---

## 9. Regras de Comunicação Interna no Docker (DNS Interno)

⚠️ REGRA CRÍTICA DE REDE: Quando os serviços conversam entre si no Docker, NUNCA utilize localhost. Utilize o nome do serviço registrado no Docker Compose.

### URLs de Acesso Externo (Navegador do seu PC):
* Painel do n8n: http://localhost:5678
* Manager da Evolution API: http://localhost:8080/manager

### Configuração de Credenciais na Rede Interna do Docker:

#### 1. Credencial da Evolution API no n8n:
* Server URL: http://evolution-api:8080

#### 2. Credencial do Redis no n8n:
* Host: redis
* Porta: 6379
* (Usuário e Senha podem ficar em branco)

#### 3. Configuração do Webhook do n8n na Evolution API:
* Webhook URL: http://n8n:5678/webhook/seu-id-de-webhook

---

## 10. Integração Extra: Google Service Account no n8n

Para conectar o n8n ao Google Sheets, Drive ou outras APIs do Google sem erros de conexão (ex: 403 Forbidden ou 404 Not Found):

### Passo 1: Gerar a Chave JSON no Google Cloud
1. Acesse o Google Cloud Console (https://console.cloud.google.com/).
2. Vá em **IAM e Administrador > Contas de serviço**.
3. Selecione ou crie um projeto.
4. Clique na conta de serviço desejada e acesse a aba **Chaves (Keys)**.
5. Clique em **Adicionar chave > Criar nova chave**, selecione o formato **JSON** e confirme.
6. O arquivo JSON será baixado automaticamente. Guarde-o em local seguro na pasta `/credentials/`.

### Passo 2: Configurar Credencial no n8n
1. Abra o arquivo JSON baixado e copie as informações para o n8n:
   * **Service Account Email:** Copie o valor de `client_email`.
   * **Private Key:** Copie todo o conteúdo começando em `-----BEGIN PRIVATE KEY-----` até `-----END PRIVATE KEY-----`.
   * **Atenção:** Remova aspas extras e evite quebras de linha indevidas (`\n`).

### Passo 3: Ativar APIs e Compartilhar Permissões
1. No Google Cloud Console, vá em **APIs e Serviços > Biblioteca** e ative as APIs necessárias (ex: Google Sheets API, Google Drive API).
2. **Importante:** Abra a planilha ou pasta no Google Drive, clique em **Compartilhar** e adicione o e-mail da Service Account (`client_email`) com permissão de Editor.

### Passo 4: Sanitização de Dados Fictícios e Segurança no Git
Para versionar modelos no repositório sem expor suas chaves privadas reais:

* **Modificações Recomendadas no JSON de Modelo:**
  * **Chave Privada (`private_key`):** Remova a chave de criptografia RSA real e insira uma instrução clara no lugar.
  * **Identificadores Únicos (`private_key_id`, `client_id`, `project_id`):** Substitua por textos indicativos.
  * **E-mails de Serviço (`client_email`, `client_x509_cert_url`):** Trocados por um formato genérico (`seu-servico@seu-projeto.iam.gserviceaccount.com`).
* **Boas Práticas de Segurança:**
  * Como a chave privada RSA original foi exposta em commits passados ou ambientes não seguros, **recomenda-se revogá-la imediatamente** no Google Cloud Console e gerar um novo arquivo de credencial para o ambiente de produção.
  * Adicione o nome do arquivo original (ex: `credentials.json` ou `select-whatshapp-*.json`) ao seu arquivo `.gitignore` para evitar o envio acidental da chave real no futuro, mantendo apenas um arquivo de modelo (ex: `credentials.example.json`) versionado no Git.

---

## 11. Bônus: Fluxo de Prompt do Agente de Vendas (Consórcio)

💡 **Importação Prática: Ao executar o script python setup_completo.py, este fluxo pré-configurado já é gerado automaticamente no arquivo workflows/fluxo_start.json. Basta acessar o n8n, clicar em Workflows > Import from File e selecionar o arquivo.

Instruções para estruturar um nó de IA/Webhook no n8n para atendimento automático da Select Consórcio:

### Regras Gerais & Prioridades:
* Nome do Usuário: Se o usuário se identificar na conversa, a vontade dele sobre como quer ser chamado é prioridade absoluta.

### Passo a Passo do Atendimento:

1. Passo 1 — Saudação Inicial:
   > "Olá! Tudo bem? 😊 Seja bem-vindo(a) ao Select Consórcio! Vi que você demonstrou interesse no nosso anúncio e estou aqui para te ajudar a realizar esse sonho. ✨ Para te atender melhor, me conta rapidinho: 👉 Qual o seu nome? ⚠️ Não consigo ouvir áudio ou receber ligação."

2. Passo 2 — Coleta do Bem:
   * Após a resposta, armazene a variável nome e pergunte:
   > "Prazer em te conhecer, [nome]! 😊 👉 O que você deseja adquirir: automóvel ou imóvel? 🚗🏡"

3. Passo 3 — Mensagem de Desenvolvimento:
   * Armazene a variável bem e responda:
   > "O consórcio é uma forma inteligente e econômica de planejar sua compra: ✔️ Sem juros ✔️ Taxa fixa e diluída ✔️ Sem pagar o dobro do valor. Me conta: qual valor de crédito você tem em mente para o seu [bem]? 💭"

4. Passo 4 — Validação do Valor:
   * IMÓVEL: Crédito mínimo de R$ 100.000.
   * AUTOMÓVEL: Crédito mínimo de R$ 45.000.
   * Se o valor for inferior, solicite o reajuste. Se válido, armazene na variável credito.

5. Passo 5 — Ficha de Cadastro e Checagem de Horário:
   * Obtenha o telefone do payload do Webhook:
     {{ $('Webhook').item.json.body.data.key.remoteJidAlt.replace(/^55/, '').split('@')[0] }}
   * Verifique o horário do sistema:
     * Horário Comercial: Segunda a Sexta (08:00 às 17:30) e Sábado (08:00 às 12:00).
   * Texto de Envio:
     > "Ao ser contemplado, você compra o bem à vista e ganha poder de negociação. Além disso, somos fiscalizados pelo Banco Central, o que garante sua segurança. 🤝 Ótimo! Já organizei seus dados para nossa equipe:
     >
     > Nome: [nome]
     > Bem: [bem]
     > Valor do Crédito: [credito]
     > Telefone: [telefone]
     >
     > [Frase de Contato: 'Nosso consultor entrará em contato em poucos minutos' OU 'Nosso horário de atendimento é de Seg a Sex (08h às 17h30) e Sáb (08h às 12h). Seu consultor entrará em contato logo no início do próximo expediente.']"

---

## 12. Comandos Úteis do Docker

Execute estes comandos no terminal dentro da pasta do projeto:
```shell
# Ver status dos contêineres
docker compose ps

# Ver logs em tempo real da Evolution API
docker compose logs -f evolution-api

# Ver logs do n8n
docker compose logs -f n8n

# Reiniciar todos os serviços
docker compose restart

# Parar os contêineres sem apagar dados
docker compose stop

# Parar e remover contêineres (preserva os volumes)
docker compose down

# Atualizar imagens e recriar contêineres
docker compose pull && docker compose up -d --remove-orphans

# REMOVER TUDO (ATENÇÃO: Apaga dados persistidos nos volumes)
docker compose down -v
```
---

## 13. Estrutura dos Serviços

* evolution-api: API da Evolution exposta na porta 8080. Persiste dados no volume evolution_instances.
* postgres: Banco de dados PostgreSQL compartilhado para Evolution API e n8n.
* redis: Instância do Redis para cache da Evolution API e filas do n8n.
* n8n: Ferramenta de automação de workflows exposta na porta 5678.

---

## 14. Solução de Problemas

* Erro de permissão no .env: Garanta que o arquivo se chame exatamente .env e não .env.txt.
* Conflito de Portas: Caso as portas 5678 ou 8080 já estejam em uso na sua máquina, edite o mapeamento de portas no arquivo docker-compose.yml.
* Problemas no Windows/WSL2: Verifique no Docker Desktop se a opção WSL2 Backend está ativa.
* Comunicação entre serviços falhando: Confirme se está utilizando os nomes do Docker (ex: http://evolution-api:8080) e não localhost.
* Aplicação/Serviços fora do ar: Certifique-se de que o Docker Desktop está aberto com a mensagem `Engine running` no canto inferior esquerdo e que os containers estão com status `Running` na aba **Containers** (se estiverem parados, execute `iniciar_aplicacao.bat` ou `docker compose up -d`).

---

## 15. Suporte e Licença

Mantido por: Davi Pinheiro
* LinkedIn: https://www.linkedin.com/in/davigopi/
* GitHub: https://github.com/davigopi

Créditos do projeto base original: Yami Renato (https://github.com/rgvieiraoficial)

Sinta-se livre para utilizar, modificar e adaptar este projeto conforme suas necessidades.
