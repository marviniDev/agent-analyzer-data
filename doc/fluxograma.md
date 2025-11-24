# 📊 Fluxograma do Agente Analista de Dados

Este documento descreve o fluxo de funcionamento do agente de análise de dados.

## 🔄 Fluxo Principal

```mermaid
flowchart TD
    Start([Início]) --> LoadEnv[Carregar variáveis de ambiente<br/>.env]
    LoadEnv --> LoadCSV[Carregar arquivo CSV<br/>archive/creditcard.csv]
    LoadCSV --> Preprocess[Pré-processar dados<br/>preprocess_csv]
    
    Preprocess --> CreateTools[Criar ferramentas<br/>dataset_overview<br/>code_interpreter]
    CreateTools --> CreateAgent[Criar Agente OpenAI<br/>com ferramentas]
    
    CreateAgent --> WaitQuestion{Aguardar<br/>Pergunta do Usuário}
    
    WaitQuestion --> AnalyzeQuestion{Analisar<br/>Tipo de Pergunta}
    
    AnalyzeQuestion -->|Pergunta Geral| UseOverview[Usar dataset_overview<br/>Retornar metadados e estatísticas]
    AnalyzeQuestion -->|Pergunta Específica| UseInterpreter[Usar code_interpreter<br/>Executar código Python]
    
    UseOverview --> ProcessResult[Processar Resultado]
    UseInterpreter --> CheckResult{Verificar<br/>Resultado}
    
    CheckResult -->|Variável 'result'| ReturnResult[Retornar resultado]
    CheckResult -->|Print output| CaptureOutput[Capturar output]
    CheckResult -->|Erro| ReturnError[Retornar mensagem de erro]
    
    CaptureOutput --> ProcessResult
    ReturnResult --> ProcessResult
    ReturnError --> ProcessResult
    
    ProcessResult --> FormatResponse[Formatar Resposta]
    FormatResponse --> DisplayResponse[Exibir Resposta ao Usuário]
    
    DisplayResponse --> WaitQuestion
    
    style Start fill:#90EE90
    style CreateAgent fill:#87CEEB
    style UseOverview fill:#FFD700
    style UseInterpreter fill:#FFD700
    style DisplayResponse fill:#90EE90
```

## 🔧 Fluxo de Pré-processamento

```mermaid
flowchart LR
    A[CSV File] --> B[Carregar com pandas]
    B --> C[Extrair Metadados]
    B --> D[Calcular Estatísticas]
    B --> E[Amostra de 5 linhas]
    
    C --> F[preprocessed_data]
    D --> F
    E --> F
    
    F --> G[Armazenar em memória]
    
    style A fill:#FFB6C1
    style F fill:#87CEEB
    style G fill:#90EE90
```

## 🛠️ Fluxo da Ferramenta code_interpreter

```mermaid
flowchart TD
    Start([Receber código Python]) --> ExecCode[Executar código<br/>com DataFrame 'df']
    
    ExecCode --> CheckError{Erro na<br/>execução?}
    
    CheckError -->|Sim| ReturnError[Retornar mensagem<br/>de erro]
    CheckError -->|Não| CheckResult{Existe variável<br/>'result'?}
    
    CheckResult -->|Sim| ReturnResult[Retornar str result]
    CheckResult -->|Não| CapturePrint[Capturar output<br/>do print]
    
    CapturePrint --> CheckOutput{Output<br/>vazio?}
    CheckOutput -->|Sim| ReturnEmpty[Mensagem padrão]
    CheckOutput -->|Não| ReturnOutput[Retornar output]
    
    ReturnResult --> End([Fim])
    ReturnOutput --> End
    ReturnEmpty --> End
    ReturnError --> End
    
    style Start fill:#FFB6C1
    style ExecCode fill:#FFD700
    style ReturnError fill:#FF6B6B
    style End fill:#90EE90
```

## 📝 Descrição dos Componentes

### 1. Inicialização
- **Carregamento de ambiente**: Lê a variável `OPENAI_API_KEY` do arquivo `.env`
- **Carregamento de dados**: Lê o arquivo CSV e armazena em `df_global`
- **Pré-processamento**: Gera metadados, estatísticas e amostra dos dados

### 2. Criação do Agente
- **Modelo**: OpenAI GPT-4o
- **Ferramentas**: 
  - `dataset_overview`: Para perguntas gerais
  - `code_interpreter`: Para cálculos específicos
- **Configuração**: `num_history_runs=1` para limitar histórico

### 3. Processamento de Perguntas
- **Análise**: O agente decide qual ferramenta usar baseado na pergunta
- **Execução**: Chama a ferramenta apropriada
- **Resposta**: Formata e retorna o resultado ao usuário

### 4. Tipos de Perguntas

#### Perguntas Gerais → `dataset_overview`
- "Quantas colunas há no dataset?"
- "Quais colunas possuem valores ausentes?"
- "Quais são os tipos de dados?"

#### Perguntas Específicas → `code_interpreter`
- "Qual a média da coluna 'Amount'?"
- "Filtre as transações fraudulentas"
- "Crie um gráfico de barras"

## 🔄 Loop de Interação

O agente funciona em um loop contínuo:
1. Recebe pergunta do usuário
2. Analisa e escolhe ferramenta
3. Executa e processa resultado
4. Retorna resposta formatada
5. Aguarda próxima pergunta

