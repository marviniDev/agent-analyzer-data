# 🏗️ Arquitetura do Agente Genérico de EDA

Este documento descreve a arquitetura técnica do agente genérico de análise exploratória de dados.

## 📐 Visão Geral

O agente é construído sobre a biblioteca **Agno**, que fornece uma abstração para criar agentes de IA com ferramentas customizadas. O modelo de linguagem utilizado é o **OpenAI GPT-4o**.

## 🔧 Componentes Principais

### 1. Camada de Ferramentas (Tools Layer)

As ferramentas são funções Python decoradas com `@tool` que o agente pode chamar. Elas fornecem:

- **Acesso a dados**: Carregamento e consulta de datasets
- **Execução de código**: Ambiente Python isolado para análises
- **Persistência**: Sistema de memória para conclusões

```
┌─────────────────────────────────────┐
│      Camada de Ferramentas          │
├─────────────────────────────────────┤
│  load_csv                            │
│  check_dataset_loaded                │
│  get_dataset_info                    │
│  execute_analysis                    │
│  save_conclusion                     │
│  get_conclusions                     │
└─────────────────────────────────────┘
```

### 2. Camada de Estado (State Layer)

O estado é mantido em variáveis globais Python:

```python
datasets = {}              # Dicionário de DataFrames
current_dataset_name = None # Nome do dataset atual
conclusions_memory = []    # Lista de conclusões
```

**Vantagens:**
- Acesso rápido aos dados
- Persistência durante a sessão
- Compartilhamento entre ferramentas

**Limitações:**
- Estado perdido ao reiniciar programa
- Não compartilhado entre processos

### 3. Camada de Execução (Execution Layer)

A ferramenta `execute_analysis` cria um ambiente Python isolado:

```python
exec_globals = {
    'df': df.copy(),      # DataFrame disponível
    'pd': pd,             # Pandas
    'np': np,             # NumPy
    'plt': plt,           # Matplotlib
    'sns': sns,           # Seaborn
    'output_dir': output_dir
}
exec(code, exec_globals, exec_locals)
```

**Segurança:**
- Código executado em contexto controlado
- Acesso apenas a bibliotecas permitidas
- Erros capturados e retornados

### 4. Camada de Persistência (Persistence Layer)

**Gráficos:**
- Salvos em `output/*.png`
- Nomes descritivos gerados pelo agente
- Formato PNG para compatibilidade

**Conclusões:**
- Memória: `conclusions_memory` (lista)
- Arquivo: `output/conclusions.json`
- Formato JSON para fácil leitura

## 🔄 Fluxo de Dados

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ Pergunta
       ▼
┌─────────────────┐
│  Agente Agno    │
│  (GPT-4o)       │
└──────┬──────────┘
       │ Escolhe ferramenta
       ▼
┌─────────────────┐
│   Ferramenta    │
│   (Tool)        │
└──────┬──────────┘
       │ Executa
       ▼
┌─────────────────┐
│  Estado Global  │
│  (datasets,     │
│   conclusions)  │
└──────┬──────────┘
       │ Retorna resultado
       ▼
┌─────────────────┐
│   Resposta      │
│   ao Usuário    │
└─────────────────┘
```

## 🗂️ Estrutura de Arquivos

```
agent-ia-EDA/
├── eda_agent.py          # Código principal do agente
├── main_agent.py         # Versão anterior (referência)
├── requirements.txt      # Dependências
├── .env                 # Variáveis de ambiente
│
├── archive/             # Datasets
│   └── creditcard.csv
│
├── output/              # Gerado automaticamente
│   ├── *.png           # Gráficos
│   └── conclusions.json # Conclusões
│
└── doc/                 # Documentação
    ├── fluxograma.md
    ├── ferramentas.md
    └── arquitetura.md
```

## 🔌 Integração com OpenAI

### Configuração
```python
model = OpenAIChat(
    id="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Comunicação
1. Agente recebe pergunta do usuário
2. GPT-4o analisa e decide qual ferramenta usar
3. Ferramenta é executada
4. Resultado retornado ao GPT-4o
5. GPT-4o formata resposta final

## 🧠 Sistema de Memória

### Memória de Curto Prazo
- **Histórico de conversa**: Mantido pelo Agno
- **Estado global**: Variáveis Python
- **Duração**: Durante a sessão

### Memória de Longo Prazo
- **Conclusões**: Salvas em JSON
- **Gráficos**: Salvos como PNG
- **Duração**: Persistem entre sessões

## 🔒 Segurança e Isolamento

### Isolamento de Código
- Código executado em contexto controlado
- Acesso apenas a bibliotecas permitidas
- Sem acesso a sistema de arquivos (exceto output/)
- Sem acesso a rede

### Tratamento de Erros
- Todas as ferramentas capturam exceções
- Mensagens de erro amigáveis
- Não interrompe execução do agente

## 📊 Geração de Gráficos

### Pipeline
```
Código Python
    │
    ├─→ plt.figure()
    ├─→ sns.plot() / plt.plot()
    ├─→ plt.savefig('output/nome.png')
    ├─→ plt.close()
    └─→ Retorna resultado
```

### Backend
- `matplotlib.use('Agg')`: Backend não-interativo
- Permite salvar gráficos sem display
- Funciona em servidores sem GUI

## 🎯 Decisões de Design

### Por que variáveis globais?
- **Simplicidade**: Fácil acesso entre ferramentas
- **Performance**: Sem overhead de serialização
- **Compatibilidade**: Funciona com Agno sem modificações

### Por que exec() em vez de subprocess?
- **Contexto compartilhado**: Acesso ao mesmo DataFrame
- **Performance**: Mais rápido que subprocess
- **Simplicidade**: Menos código de infraestrutura

### Por que JSON para conclusões?
- **Legibilidade**: Fácil de ler e editar
- **Portabilidade**: Pode ser usado por outros sistemas
- **Simplicidade**: Sem necessidade de banco de dados

## 🔄 Ciclo de Vida do Agente

### 1. Inicialização
```python
# Carrega variáveis de ambiente
load_dotenv()

# Configura matplotlib
matplotlib.use('Agg')

# Cria agente
eda_agent = Agent(...)
```

### 2. Carregamento de Dataset
```python
# Usuário informa CSV
# Agente chama load_csv
# DataFrame armazenado em datasets dict
```

### 3. Análise
```python
# Usuário faz pergunta
# Agente escolhe ferramenta
# Ferramenta executa
# Resultado retornado
```

### 4. Persistência
```python
# Conclusões salvas automaticamente
# Gráficos salvos em output/
```

## 🚀 Otimizações

### Performance
- DataFrame mantido em memória (não recarregado)
- Gráficos fechados após salvar (libera memória)
- Código executado diretamente (sem compilação)

### Escalabilidade
- Suporta datasets grandes (limitado por memória)
- Múltiplos datasets podem ser carregados
- Conclusões acumuladas sem limite

## 🔮 Possíveis Melhorias Futuras

### 1. Cache de Análises
- Armazenar resultados de análises comuns
- Evitar recalcular estatísticas

### 2. Banco de Dados
- Substituir JSON por SQLite
- Consultas mais eficientes

### 3. Paralelização
- Executar múltiplas análises simultaneamente
- Processar datasets grandes em chunks

### 4. Interface Web
- Substituir CLI por interface web
- Visualização interativa de gráficos

### 5. Suporte a Outros Formatos
- Excel, Parquet, JSON
- APIs e bancos de dados

## 📚 Dependências Principais

```
agno              # Framework de agentes
openai            # Cliente OpenAI
pandas            # Manipulação de dados
numpy             # Computação numérica
matplotlib        # Gráficos básicos
seaborn           # Gráficos estatísticos
python-dotenv     # Variáveis de ambiente
```

## 🎓 Padrões Utilizados

### 1. Tool Pattern
- Ferramentas como funções isoladas
- Interface clara e documentada
- Fácil adicionar novas ferramentas

### 2. Global State Pattern
- Estado compartilhado entre ferramentas
- Simples e eficiente
- Adequado para aplicações single-threaded

### 3. Command Pattern
- Código Python como comandos
- Execução dinâmica
- Flexibilidade máxima

### 4. Memory Pattern
- Conclusões como memória persistente
- Histórico de descobertas
- Contexto entre sessões

