# 🧠 Agente Genérico de Análise Exploratória de Dados (EDA)

Este projeto cria um **agente genérico de análise exploratória de dados** utilizando a biblioteca **Agno** e o modelo **OpenAI GPT-4o**. O agente é capaz de analisar **qualquer arquivo CSV**, gerar gráficos, detectar padrões, anomalias e apresentar conclusões baseadas nas análises realizadas.

---

## 📁 Estrutura do Projeto

```
agent-ia-EDA/
├── archive/
│   └── creditcard.csv       # Dataset de exemplo (fraudes de cartão de crédito)
├── doc/
│   └── fluxograma.md        # Fluxograma do projeto
├── graficos/                # Diretório criado automaticamente para gráficos e conclusões
├── .env                     # Contém sua chave da API da OpenAI (OPENAI_API_KEY)
├── .gitignore               # Arquivos ignorados pelo Git
├── eda_agent.py             # Agente genérico de EDA (NOVO - solução completa)
├── main_agent.py            # Código original (exemplo anterior)
├── requirements.txt         # Dependências do projeto
├── README.md                # Este arquivo
└── LICENSE                  # Licença MIT
```

---

## ⚙️ Funcionalidades Principais

### 🔹 1. Carregamento Dinâmico de CSVs (`load_csv`)

Carrega qualquer arquivo CSV e o armazena na memória para análise. Não é necessário modificar o código para usar diferentes datasets.

### 🔹 2. Informações do Dataset (`get_dataset_info`)

Retorna informações completas sobre o dataset:
- Dimensões (linhas x colunas)
- Tipos de dados
- Valores ausentes
- Estatísticas descritivas
- Amostra dos dados

### 🔹 3. Execução de Análises (`execute_analysis`)

Executa código Python para realizar análises específicas:
- Cálculos estatísticos
- Filtros e agregações
- **Geração de gráficos** (salvos automaticamente em `graficos/`)
- Detecção de padrões e anomalias

### 🔹 4. Sistema de Memória (`save_conclusion` / `get_conclusions`)

Salva conclusões importantes das análises e permite recuperá-las posteriormente. As conclusões são salvas tanto na memória quanto em arquivo JSON.

---

## 🎯 Tipos de Análises Suportadas

O agente é capaz de responder perguntas sobre:

### 📊 Descrição dos Dados
- Tipos de dados (numéricos, categóricos)
- Distribuições (histogramas, boxplots)
- Intervalos (mínimo, máximo, quartis)
- Medidas de tendência central (média, mediana, moda)
- Variabilidade (desvio padrão, variância, IQR)

### 🔍 Identificação de Padrões e Tendências
- Padrões temporais (se houver coluna de tempo/data)
- Valores mais/menos frequentes
- Agrupamentos ou clusters visuais

### ⚠️ Detecção de Anomalias (Outliers)
- Identificação de valores atípicos
- Análise do impacto dos outliers
- Sugestões de tratamento

### 🔗 Relações entre Variáveis
- Gráficos de dispersão
- Matriz de correlação
- Tabelas cruzadas
- Identificação de variáveis mais/menos correlacionadas

### 💡 Conclusões e Insights
- Resumo das descobertas
- Insights baseados nas análises
- Recomendações

---

## 🚀 Como Usar

### 1. Instalação das Dependências

```bash
# Criar ambiente virtual (se ainda não criou)
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=your_api_key_here
```

> **Como obter sua chave API**: Acesse [platform.openai.com](https://platform.openai.com/api-keys) para criar uma conta e gerar sua chave de API.

### 3. Executar o Agente

```bash
python eda_agent.py
```

O agente irá:
1. Solicitar o caminho do arquivo CSV (ou usar o padrão `./archive/creditcard.csv`)
2. Carregar o dataset
3. Entrar em modo interativo para receber suas perguntas

### 4. Fazer Perguntas

Exemplos de perguntas que você pode fazer:

```
❓ Quais são os tipos de dados de cada coluna?
❓ Qual a distribuição da coluna 'Amount'?
❓ Existem valores atípicos na coluna 'Amount'?
❓ Qual a correlação entre as variáveis numéricas?
❓ Crie um gráfico mostrando a distribuição de fraudes (Class) por valor (Amount)
❓ Quais são as principais conclusões que podemos tirar dos dados?
```

Digite `conclusoes` para ver um resumo de todas as análises realizadas.

Digite `sair` para encerrar o programa.

## 📈 Gráficos Gerados

Todos os gráficos são salvos automaticamente no diretório `graficos/` com nomes descritivos. O agente informa quais gráficos foram gerados após cada análise.

---

## 💾 Memória de Conclusões

O agente mantém um histórico de todas as conclusões importantes encontradas durante as análises. Essas conclusões são:
- Armazenadas na memória durante a sessão
- Salvas em `graficos/conclusions.json` para persistência
- Recuperáveis a qualquer momento com o comando `conclusoes`

---

## 🎓 Exemplo de Uso Completo

```bash
$ python eda_agent.py

======================================================================
🤖 AGENTE DE ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
======================================================================

📁 Digite o caminho do arquivo CSV (ou Enter para usar './archive/creditcard.csv'): 

⏳ Carregando dataset: ./archive/creditcard.csv
✅ Dataset carregado com sucesso!

======================================================================
💬 Agora você pode fazer perguntas sobre os dados!
   Digite 'sair' para encerrar
   Digite 'conclusoes' para ver um resumo das análises
======================================================================

❓ Sua pergunta: Qual a distribuição de fraudes no dataset?

🔍 Analisando...

💡 Resposta:
[Análise completa com gráficos e estatísticas]

📈 Gráficos recentes salvos em: graficos/distribuicao_fraudes.png
```

---

## 🔐 Segurança

> **Importante**: Não commite o arquivo `.env` no controle de versão. Ele contém informações sensíveis.

O arquivo `.gitignore` já está configurado para ignorar:
- `.env`
- `graficos/` (gráficos e conclusões)
- `.venv/` (ambiente virtual)

---

## ⚙️ Configuração do VSCode

O projeto já inclui um arquivo `.vscode/settings.json` que configura o VSCode para usar o ambiente virtual automaticamente.

**Se o VSCode ainda não reconhecer as dependências:**

1. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
2. Digite "Python: Select Interpreter"
3. Selecione o interpretador do ambiente virtual: `.venv/bin/python`

---

## 📚 Sobre o Dataset de Exemplo

O arquivo `creditcard.csv` contém dados de transações de cartão de crédito com indicação de fraude:
- **Time**: Número de segundos desde a primeira transação
- **V1 a V28**: Variáveis transformadas por PCA (privacidade)
- **Amount**: Valor da transação
- **Class**: 1 = fraude, 0 = normal

---

## 💡 Observações Técnicas

- O agente usa `matplotlib` com backend não-interativo para salvar gráficos
- Todos os gráficos são salvos em formato PNG no diretório `graficos/`
- O sistema de memória permite que o agente "lembre" de análises anteriores
- O código é executado em um ambiente isolado com acesso apenas ao DataFrame
- O agente é genérico e funciona com qualquer CSV, não apenas o exemplo fornecido

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.  
Sinta-se à vontade para usar, modificar e compartilhar!

**Copyright (c) 2025 Marcos Vinícius**
