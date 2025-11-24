# 📊 Fluxograma do Agente Genérico de EDA

Este documento descreve o fluxo de funcionamento do agente genérico de análise exploratória de dados (EDA).

## 🔄 Fluxo Principal

```mermaid
flowchart TD
    Start([Início]) --> LoadEnv[Carregar variáveis de ambiente<br/>.env]
    LoadEnv --> Init[Inicializar agente<br/>com 6 ferramentas]
    
    Init --> UserInput[Usuário informa<br/>caminho do CSV]
    UserInput --> LoadCSV[load_csv:<br/>Carregar CSV na memória]
    
    LoadCSV --> StoreData[Armazenar DataFrame<br/>em datasets dict]
    StoreData --> Ready[Dataset pronto<br/>para análise]
    
    Ready --> WaitQuestion{Aguardar<br/>Pergunta do Usuário}
    
    WaitQuestion --> CheckDataset[check_dataset_loaded:<br/>Verificar se dataset está carregado]
    
    CheckDataset -->|Dataset carregado| AnalyzeType{Analisar<br/>Tipo de Pergunta}
    CheckDataset -->|Dataset não carregado| LoadCSV
    
    AnalyzeType -->|Info geral| GetInfo[get_dataset_info:<br/>Retornar metadados]
    AnalyzeType -->|Análise específica| ExecuteCode[execute_analysis:<br/>Executar código Python]
    AnalyzeType -->|Salvar conclusão| SaveConclusion[save_conclusion:<br/>Armazenar na memória]
    AnalyzeType -->|Ver conclusões| GetConclusions[get_conclusions:<br/>Recuperar conclusões]
    
    GetInfo --> ProcessResult[Processar Resultado]
    ExecuteCode --> GenerateGraph{Gerar<br/>Gráfico?}
    GenerateGraph -->|Sim| SaveGraph[Salvar gráfico<br/>em graficos/]
    GenerateGraph -->|Não| ProcessResult
    SaveGraph --> ProcessResult
    
    SaveConclusion --> ProcessResult
    GetConclusions --> ProcessResult
    
    ProcessResult --> FormatResponse[Formatar Resposta]
    FormatResponse --> DisplayResponse[Exibir Resposta ao Usuário]
    
    DisplayResponse --> WaitQuestion
    
    style Start fill:#90EE90
    style Init fill:#87CEEB
    style LoadCSV fill:#FFD700
    style ExecuteCode fill:#FFD700
    style SaveGraph fill:#FFB6C1
    style DisplayResponse fill:#90EE90
```

## 🛠️ Ferramentas Disponíveis

### 1. `load_csv`
Carrega um arquivo CSV e o armazena na memória global.

```mermaid
flowchart LR
    A[CSV File Path] --> B[Ler CSV com pandas]
    B --> C[Armazenar em datasets dict]
    C --> D[Definir current_dataset_name]
    D --> E[Retornar resumo JSON]
    
    style A fill:#FFB6C1
    style C fill:#87CEEB
    style E fill:#90EE90
```

### 2. `check_dataset_loaded`
Verifica se há um dataset carregado na memória.

```mermaid
flowchart TD
    Start([Verificar dataset]) --> Check{current_dataset_name<br/>existe?}
    Check -->|Sim| CheckDict{Dataset em<br/>datasets dict?}
    Check -->|Não| ReturnNone[Retornar:<br/>Nenhum dataset carregado]
    
    CheckDict -->|Sim| GetInfo[Obter informações<br/>do DataFrame]
    CheckDict -->|Não| ReturnNone
    
    GetInfo --> ReturnInfo[Retornar:<br/>Dataset carregado + dimensões]
    
    style Start fill:#FFB6C1
    style ReturnInfo fill:#90EE90
    style ReturnNone fill:#FF6B6B
```

### 3. `get_dataset_info`
Retorna informações completas sobre o dataset carregado.

```mermaid
flowchart TD
    Start([get_dataset_info]) --> Validate{Dataset<br/>carregado?}
    Validate -->|Não| Error[Retornar erro]
    Validate -->|Sim| Extract[Extrair informações]
    
    Extract --> Info1[Dimensões]
    Extract --> Info2[Colunas]
    Extract --> Info3[Tipos de dados]
    Extract --> Info4[Valores ausentes]
    Extract --> Info5[Estatísticas descritivas]
    Extract --> Info6[Amostra 5 linhas]
    
    Info1 --> Combine[Combinar em JSON]
    Info2 --> Combine
    Info3 --> Combine
    Info4 --> Combine
    Info5 --> Combine
    Info6 --> Combine
    
    Combine --> Return[Retornar JSON]
    
    style Start fill:#FFB6C1
    style Combine fill:#87CEEB
    style Return fill:#90EE90
```

### 4. `execute_analysis`
Executa código Python para análises específicas e geração de gráficos.

```mermaid
flowchart TD
    Start([Receber código Python]) --> Validate{Dataset<br/>carregado?}
    Validate -->|Não| Error[Retornar erro]
    Validate -->|Sim| PrepareEnv[Preparar ambiente:<br/>df, pd, np, plt, sns]
    
    PrepareEnv --> CaptureStdout[Capturar stdout]
    CaptureStdout --> ExecCode[Executar código<br/>com exec]
    
    ExecCode --> CheckError{Erro na<br/>execução?}
    
    CheckError -->|Sim| RestoreStdout[Restaurar stdout]
    RestoreStdout --> ReturnError[Retornar mensagem<br/>de erro]
    
    CheckError -->|Não| CheckResult{Existe variável<br/>'result'?}
    
    CheckResult -->|Sim| GetResult[Obter resultado]
    CheckResult -->|Não| GetOutput[Obter output<br/>capturado]
    
    GetResult --> RestoreStdout
    GetOutput --> RestoreStdout
    
    RestoreStdout --> FormatReturn[Formatar retorno]
    FormatReturn --> Return[Retornar resultado]
    
    style Start fill:#FFB6C1
    style ExecCode fill:#FFD700
    style ReturnError fill:#FF6B6B
    style Return fill:#90EE90
```

### 5. `save_conclusion`
Salva uma conclusão importante na memória.

```mermaid
flowchart LR
    A[Conclusão texto] --> B[Criar entrada com timestamp]
    B --> C[Adicionar a conclusions_memory]
    C --> D[Salvar em graficos/conclusions.json]
    D --> E[Retornar confirmação]
    
    style A fill:#FFB6C1
    style C fill:#87CEEB
    style D fill:#FFD700
    style E fill:#90EE90
```

### 6. `get_conclusions`
Recupera todas as conclusões salvas.

```mermaid
flowchart TD
    Start([get_conclusions]) --> Check{conclusions_memory<br/>vazio?}
    Check -->|Sim| ReturnEmpty[Retornar:<br/>Nenhuma conclusão]
    Check -->|Não| FormatJSON[Formatar como JSON]
    FormatJSON --> Return[Retornar conclusões]
    
    style Start fill:#FFB6C1
    style Return fill:#90EE90
    style ReturnEmpty fill:#FF6B6B
```

## 📊 Fluxo de Geração de Gráficos

```mermaid
flowchart TD
    Start([execute_analysis recebe código]) --> CodeHasPlot{Código contém<br/>plt.savefig?}
    
    CodeHasPlot -->|Sim| ExecCode[Executar código]
    CodeHasPlot -->|Não| ExecCode
    
    ExecCode --> PlotSaved[Gráfico salvo em<br/>graficos/nome.png]
    PlotSaved --> ClosePlot[plt.close libera memória]
    ClosePlot --> Return[Retornar resultado]
    
    style Start fill:#FFB6C1
    style PlotSaved fill:#FFD700
    style Return fill:#90EE90
```

## 🔄 Fluxo de Memória de Conclusões

```mermaid
flowchart TD
    Analysis[Análise realizada] --> Important{Conclusão<br/>importante?}
    
    Important -->|Sim| Save[save_conclusion]
    Important -->|Não| Continue[Continuar análise]
    
    Save --> Memory[Armazenar em<br/>conclusions_memory]
    Memory --> File[Salvar em<br/>graficos/conclusions.json]
    
    UserRequest[Usuário pede conclusões] --> Get[get_conclusions]
    Get --> Load[Carregar de<br/>conclusions_memory]
    Load --> Format[Formatar e retornar]
    
    style Save fill:#FFD700
    style Memory fill:#87CEEB
    style Format fill:#90EE90
```

## 🎯 Tipos de Análises Suportadas

### A) Descrição dos Dados
- Tipos de dados (numéricos, categóricos)
- Distribuições (histogramas, boxplots)
- Intervalos (mínimo, máximo, quartis)
- Medidas de tendência central (média, mediana, moda)
- Variabilidade (desvio padrão, variância, IQR)

### B) Identificação de Padrões e Tendências
- Padrões temporais
- Valores mais/menos frequentes
- Agrupamentos ou clusters visuais

### C) Detecção de Anomalias (Outliers)
- Identificação usando IQR, Z-score
- Análise de impacto
- Sugestões de tratamento

### D) Relações entre Variáveis
- Gráficos de dispersão
- Matriz de correlação
- Tabelas cruzadas
- Identificação de correlações

### E) Conclusões e Insights
- Resumo das descobertas
- Insights baseados nas análises
- Recomendações

## 🔄 Loop de Interação Completo

```mermaid
flowchart TD
    Start([Início do programa]) --> LoadCSV[Usuário informa CSV]
    LoadCSV --> AgentLoad[Agente carrega CSV]
    AgentLoad --> Ready[Dataset pronto]
    
    Ready --> LoopStart[Loop de perguntas]
    
    LoopStart --> UserQ[Usuário faz pergunta]
    UserQ --> Check[Agente verifica dataset]
    Check --> Analyze[Agente analisa pergunta]
    Analyze --> ChooseTool[Escolhe ferramenta]
    
    ChooseTool --> Tool1[load_csv]
    ChooseTool --> Tool2[check_dataset_loaded]
    ChooseTool --> Tool3[get_dataset_info]
    ChooseTool --> Tool4[execute_analysis]
    ChooseTool --> Tool5[save_conclusion]
    ChooseTool --> Tool6[get_conclusions]
    
    Tool1 --> Process
    Tool2 --> Process
    Tool3 --> Process
    Tool4 --> Process
    Tool5 --> Process
    Tool6 --> Process
    
    Process --> Response[Gerar resposta]
    Response --> Display[Exibir ao usuário]
    Display --> MoreQ{Mais<br/>perguntas?}
    
    MoreQ -->|Sim| LoopStart
    MoreQ -->|Não| End([Fim])
    
    style Start fill:#90EE90
    style Ready fill:#87CEEB
    style Analyze fill:#FFD700
    style Response fill:#FFB6C1
    style End fill:#90EE90
```

## 📝 Descrição dos Componentes

### 1. Inicialização
- **Carregamento de ambiente**: Lê `OPENAI_API_KEY` do arquivo `.env`
- **Configuração de gráficos**: Define estilo seaborn e parâmetros matplotlib
- **Variáveis globais**: 
  - `datasets`: Dicionário para armazenar DataFrames
  - `current_dataset_name`: Nome do dataset atual
  - `conclusions_memory`: Lista de conclusões salvas

### 2. Criação do Agente
- **Modelo**: OpenAI GPT-4o
- **Ferramentas**: 6 ferramentas especializadas
- **Instruções**: Processo de trabalho detalhado e diretrizes específicas

### 3. Processamento de Perguntas
- **Verificação**: Sempre verifica se dataset está carregado
- **Análise**: O agente decide qual ferramenta usar
- **Execução**: Executa código Python quando necessário
- **Geração de gráficos**: Salva automaticamente em `graficos/`
- **Memória**: Salva conclusões importantes

### 4. Sistema de Memória
- **Conclusões**: Armazenadas em memória e arquivo JSON
- **Persistência**: Conclusões sobrevivem entre sessões
- **Recuperação**: Pode recuperar todas as conclusões a qualquer momento

## 🔧 Estrutura de Dados

### datasets (dict)
```python
{
    "creditcard": DataFrame,  # Dataset carregado
    "outro_dataset": DataFrame # Outro dataset (se carregado)
}
```

### conclusions_memory (list)
```python
[
    {
        "timestamp": "2025-01-XX...",
        "conclusion": "Texto da conclusão"
    },
    ...
]
```

## 📂 Estrutura de Arquivos Gerados

```
graficos/
├── grafico1.png
├── grafico2.png
├── ...
└── conclusions.json
```

## 🔄 Fluxo de Execução Típico

1. **Inicialização**: Carrega variáveis de ambiente
2. **Carregamento**: Usuário informa CSV → agente carrega
3. **Análise**: Usuário faz pergunta → agente:
   - Verifica dataset carregado
   - Escolhe ferramenta apropriada
   - Executa análise
   - Gera gráficos (se necessário)
   - Salva conclusões (se relevante)
   - Retorna resposta
4. **Loop**: Repete passo 3 até usuário sair
5. **Finalização**: Conclusões permanecem salvas em JSON
