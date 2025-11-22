# 🧠 Agente Analista de Dados com Gemini e Agno

Este projeto cria um **agente de análise de dados** utilizando a biblioteca **Agno** e o modelo **Gemini** da Google AI. O agente é capaz de responder perguntas gerais sobre um dataset (ex: estatísticas, colunas, tipos de dados) e também executar **códigos Python dinâmicos** para realizar cálculos, filtros ou agregações sobre o DataFrame carregado.

---

## 📁 Estrutura do Projeto

```
agent-ia-EDA/
├── archive/
│   └── creditcard.csv       # Dataset utilizado (exemplo)
├── .env                     # Contém sua chave da API da Google (GOOGLE_API_KEY)
├── main_agent.py            # Código principal do agente
├── README.md                # Este arquivo
└── LICENSE                  # Licença MIT
```

---

## ⚙️ Funcionalidades Principais

### 🔹 1. Pré-processamento de Dados (`preprocess_csv`)

Carrega um arquivo CSV e gera um resumo com:
- **Metadados**: linhas, colunas, tipos de dados, valores nulos
- **Estatísticas descritivas** resumidas
- **Pequena amostra** de 5 linhas para referência

### 🔹 2. Ferramenta `dataset_overview`

Retorna o resumo pré-processado do dataset.  
Ideal para perguntas **gerais** como:
- "Quantas colunas há no dataset?"
- "Quais colunas possuem valores ausentes?"
- "Quais são os tipos de dados de cada coluna?"

### 🔹 3. Ferramenta `code_interpreter`

Executa código Python diretamente no contexto do dataset (`df`).  
Ideal para perguntas **específicas** que exigem cálculo, como:
- "Qual a média da coluna 'Amount'?"
- "Filtre as transações fraudulentas e conte quantas existem."
- "Crie um gráfico de barras mostrando a média de 'Amount' para cada valor de 'Class'."

**Nota**: Se o código definir uma variável `result`, ela será retornada. Caso contrário, o resultado impresso no console é capturado e exibido.

---

## 🤖 Criação do Agente

O agente é criado com duas ferramentas e o modelo Gemini:

```python
analyst_agent = Agent(
    tools=[dataset_overview, code_interpreter],
    model=Gemini(
        id="gemini-2.0-flash-001",
        api_key=os.getenv("GOOGLE_API_KEY")
    ),
    num_history_runs=1,
    description="Você é um assistente de IA que tem acesso a DUAS ferramentas e NADA MAIS.",
    instructions=[
        "Sua única tarefa é responder perguntas sobre um dataset usando as ferramentas disponíveis."
    ],
)
```

---

## 🚀 Exemplo de Uso

```python
print("\n--- Pergunta 2: Cálculo Específico (Média) ---")
analyst_agent.print_response(
    "Selecione a coluna 'Amount' e 'Class' e crie um gráfico de barras mostrando a média de 'Amount' para cada valor de 'Class'."
)
```

O agente entende o contexto e gera o código necessário para calcular e exibir o gráfico, utilizando `pandas` e `matplotlib` internamente.

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
GOOGLE_API_KEY=your_api_key_here
```

> **Importante**: Não commite o arquivo `.env` no controle de versão. Ele contém informações sensíveis.

---

## 🧩 Requisitos

Instale as dependências necessárias com:

```bash
pip install agno pandas python-dotenv
```

> **Nota**: Certifique-se de também ter o dataset (exemplo: `creditcard.csv`) na pasta `archive/`.

---

## 💡 Observações

- A função `preprocess_csv` limita o tamanho dos dados para não ultrapassar o limite de tokens do modelo.
- O `code_interpreter` é protegido contra erros e retorna mensagens amigáveis em caso de exceção.
- O projeto é facilmente adaptável para outros datasets - basta modificar o caminho do arquivo CSV em `main_agent.py`.
- O agente está configurado com `num_history_runs=1` para limitar o histórico de conversas.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.  
Sinta-se à vontade para usar, modificar e compartilhar!

**Copyright (c) 2025 Marcos Vinícius**
