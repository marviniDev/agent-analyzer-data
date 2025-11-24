# Agentes Autônomos – Relatório da Atividade Extra

**Projeto**: Agente Genérico de Análise Exploratória de Dados (EDA)  
**Data**: Janeiro 2025  
**Equipe**: Marcos Vinícius

---

## 1. Framework Escolhida

### Agno Framework

A framework escolhida para o desenvolvimento do agente foi **Agno**, uma biblioteca Python moderna e poderosa para criação de agentes autônomos de IA.

#### Motivos da Escolha:

1. **Simplicidade de Uso**: Interface intuitiva e fácil de implementar
2. **Integração com OpenAI**: Suporte nativo para modelos GPT (GPT-4o)
3. **Sistema de Ferramentas**: Permite criar ferramentas customizadas facilmente com o decorador `@tool`
4. **Gerenciamento de Histórico**: Controle automático do histórico de conversas
5. **Flexibilidade**: Permite criar agentes especializados com instruções detalhadas

#### Tecnologias Utilizadas:

- **Agno**: Framework principal para criação do agente
- **OpenAI GPT-4o**: Modelo de linguagem para processamento de perguntas e geração de código
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib/Seaborn**: Geração de gráficos e visualizações
- **Python-dotenv**: Gerenciamento seguro de variáveis de ambiente

---

## 2. Estrutura da Solução

### 2.1 Arquitetura Geral

A solução foi estruturada em camadas bem definidas:

```
┌─────────────────────────────────────┐
│     Interface Interativa (CLI)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Agente Agno (GPT-4o)           │
│   - Processamento de perguntas      │
│   - Decisão de ferramentas          │
│   - Geração de respostas            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Camada de Ferramentas          │
│  ┌──────────────────────────────┐ │
│  │ 1. load_csv                   │ │
│  │ 2. check_dataset_loaded       │ │
│  │ 3. get_dataset_info           │ │
│  │ 4. execute_analysis          │ │
│  │ 5. save_conclusion            │ │
│  │ 6. get_conclusions            │ │
│  └──────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Camada de Estado               │
│  - datasets (dict)                  │
│  - current_dataset_name             │
│  - conclusions_memory               │
└─────────────────────────────────────┘
```

### 2.2 Componentes Principais

#### 2.2.1 Ferramentas (Tools)

O agente possui **6 ferramentas especializadas**:

1. **`load_csv`**: Carrega qualquer arquivo CSV dinamicamente
2. **`check_dataset_loaded`**: Verifica se há dataset carregado na memória
3. **`get_dataset_info`**: Retorna informações completas sobre o dataset
4. **`execute_analysis`**: Executa código Python para análises específicas e geração de gráficos
5. **`save_conclusion`**: Salva conclusões importantes na memória
6. **`get_conclusions`**: Recupera todas as conclusões salvas

#### 2.2.2 Sistema de Memória

- **Memória de Curto Prazo**: Histórico de conversa mantido pelo Agno
- **Memória de Longo Prazo**: 
  - Conclusões salvas em `output/conclusions.json`
  - Gráficos salvos em `output/*.png`

#### 2.2.3 Execução de Código

A ferramenta `execute_analysis` cria um ambiente Python isolado com acesso a:
- `df`: DataFrame pandas com o dataset
- `pd`, `np`, `plt`, `sns`: Bibliotecas de análise e visualização
- `output_dir`: Diretório para salvar gráficos

### 2.3 Fluxo de Funcionamento

1. **Inicialização**: Carrega variáveis de ambiente e configura o agente
2. **Carregamento de Dataset**: Usuário informa CSV → agente carrega na memória
3. **Processamento de Perguntas**: 
   - Agente verifica se dataset está carregado
   - Escolhe ferramenta apropriada
   - Executa análise ou consulta
   - Gera gráficos quando necessário
   - Salva conclusões importantes
4. **Resposta**: Formata e retorna resultado ao usuário
5. **Loop**: Repete até usuário sair

### 2.4 Estrutura de Arquivos

```
agent-ia-EDA/
├── eda_agent.py              # Agente principal
├── main_agent.py             # Versão anterior (referência)
├── requirements.txt           # Dependências
├── .env                      # Variáveis de ambiente (NÃO commitado)
├── .gitignore                # Arquivos ignorados
│
├── archive/
│   └── creditcard.csv        # Dataset de exemplo
│
├── output/                   # Gerado automaticamente
│   ├── *.png                # Gráficos gerados
│   └── conclusions.json      # Conclusões salvas
│
└── doc/                      # Documentação
    ├── fluxograma.md
    ├── ferramentas.md
    ├── arquitetura.md
    └── README.md
```

---

## 3. Perguntas e Respostas

### Pergunta 1: Quais são os tipos de dados de cada coluna do dataset?

**Pergunta**: "Quais são os tipos de dados (numéricos, categóricos) de cada coluna?"

**Resposta do Agente**:

O dataset possui 31 colunas com os seguintes tipos:

**Colunas Numéricas (float64)**:
- `Time`: Representa o número de segundos desde a primeira transação
- `V1` a `V28`: Variáveis transformadas por PCA (30 colunas numéricas)
- `Amount`: Valor da transação (float64)

**Colunas Categóricas/Inteiras (int64)**:
- `Class`: Variável categórica binária
  - 0 = transação normal
  - 1 = transação fraudulenta

**Resumo**:
- Total de colunas: 31
- Colunas numéricas: 30 (Time, V1-V28, Amount)
- Colunas categóricas: 1 (Class)
- Valores ausentes: Nenhum (dataset completo)

**Conclusão**: O dataset é composto majoritariamente por variáveis numéricas contínuas, com uma única variável categórica binária (Class) que representa a variável target.

---

### Pergunta 2: Qual a distribuição da coluna Amount? (COM GRÁFICO)

**Pergunta**: "Crie um histograma mostrando a distribuição da coluna Amount"

**Resposta do Agente**:

Analisando a distribuição da coluna `Amount`:

**Estatísticas Descritivas**:
- Média: 88.35
- Mediana: 22.00
- Desvio Padrão: 250.12
- Mínimo: 0.00
- Máximo: 25,691.16
- Quartil 25% (Q1): 5.65
- Quartil 75% (Q3): 77.05

**Análise da Distribuição**:
A distribuição de `Amount` é altamente assimétrica (positiva), com:
- A maioria das transações concentrada em valores baixos
- Poucas transações com valores muito altos (outliers)
- Mediana muito menor que a média, indicando assimetria

**Gráfico Gerado**: `output/distribuicao_amount.png`

![Distribuição de Amount](output/distribuicao_amount.png)

**Conclusão**: A distribuição mostra que a maioria das transações tem valores relativamente baixos, com uma cauda longa à direita indicando a presença de transações com valores muito altos.

---

### Pergunta 3: Qual o intervalo (mínimo, máximo) de cada variável numérica?

**Pergunta**: "Qual o intervalo de cada variável (mínimo, máximo)?"

**Resposta do Agente**:

Aqui estão os intervalos (mínimo e máximo) das principais variáveis numéricas:

**Variáveis Principais**:
- **Time**: 
  - Mínimo: 0.00 segundos
  - Máximo: 172,792.00 segundos (~48 horas)
  
- **Amount**: 
  - Mínimo: 0.00
  - Máximo: 25,691.16

**Variáveis PCA (V1 a V28)**:
As variáveis V1 a V28 foram transformadas por PCA e apresentam intervalos variados:

- **V1**: [-56.41, 2.45]
- **V2**: [-72.72, 22.06]
- **V3**: [-48.33, 9.38]
- **V4**: [-5.68, 16.88]
- **V5**: [-113.74, 34.80]
- **V6**: [-26.16, 73.30]
- **V7**: [-43.56, 120.59]
- **V8**: [-73.22, 20.01]
- **V9**: [-13.41, 15.59]
- **V10**: [-24.59, 23.75]
- **V11**: [-4.80, 12.02]
- **V12**: [-18.68, 7.85]
- **V13**: [-5.79, 7.13]
- **V14**: [-19.21, 10.53]
- **V15**: [-4.50, 8.88]
- **V16**: [-14.13, 17.32]
- **V17**: [-25.16, 9.25]
- **V18**: [-9.50, 5.04]
- **V19**: [-7.21, 5.59]
- **V20**: [-54.50, 39.42]
- **V21**: [-34.83, 27.20]
- **V22**: [-10.93, 10.50]
- **V23**: [-44.81, 22.53]
- **V24**: [-2.84, 4.58]
- **V25**: [-10.30, 7.52]
- **V26**: [-2.60, 3.52]
- **V27**: [-22.57, 31.61]
- **V28**: [-15.43, 33.85]

**Variável Target**:
- **Class**: 
  - Mínimo: 0 (normal)
  - Máximo: 1 (fraude)

**Observação**: As variáveis V1-V28 foram normalizadas pelo PCA, por isso apresentam valores centrados em torno de zero com diferentes escalas.

---

### Pergunta 4: Qual a variabilidade dos dados (desvio padrão, variância)?

**Pergunta**: "Qual a variabilidade dos dados (desvio padrão, variância)?"

**Resposta do Agente**:

Aqui está a análise de variabilidade (desvio padrão e variância) das principais variáveis:

**Variáveis Principais**:

1. **Time**:
   - Desvio Padrão: 47,483.15
   - Variância: 2,252,647,000.00
   - Coeficiente de Variação: 50.07%
   - **Interpretação**: Alta variabilidade temporal, refletindo transações ao longo de ~48 horas

2. **Amount**:
   - Desvio Padrão: 250.12
   - Variância: 62,560.00
   - Coeficiente de Variação: 283.20%
   - **Interpretação**: Variabilidade muito alta, indicando grande dispersão dos valores (presença de outliers)

**Variáveis PCA (V1 a V28)**:

As variáveis transformadas por PCA apresentam variabilidades diferentes:

**Maior Variabilidade**:
- **V2**: Desvio Padrão = 1.65, Variância = 2.72
- **V1**: Desvio Padrão = 1.96, Variância = 3.84
- **V3**: Desvio Padrão = 1.65, Variância = 2.72

**Menor Variabilidade**:
- **V24**: Desvio Padrão = 0.61, Variância = 0.37
- **V25**: Desvio Padrão = 0.60, Variância = 0.36
- **V26**: Desvio Padrão = 0.52, Variância = 0.27

**Variável Target**:
- **Class**: 
  - Desvio Padrão: 0.29
  - Variância: 0.08
  - **Interpretação**: Baixa variabilidade (variável binária), com distribuição desbalanceada (mais transações normais que fraudulentas)

**Resumo**:
- A variável `Amount` apresenta a maior variabilidade absoluta
- As variáveis PCA têm variabilidades relativamente baixas (normalizadas)
- O desbalanceamento do dataset é refletido na baixa variabilidade de `Class`

**Conclusão**: A alta variabilidade de `Amount` sugere a necessidade de tratamento de outliers ou transformações para análises mais robustas.

---

### Pergunta 5: Existem valores atípicos (outliers) nos dados? Como eles afetam a análise?

**Pergunta**: "Existem valores atípicos nos dados? Como esses outliers afetam a análise?"

**Resposta do Agente**:

Sim, existem valores atípicos significativos, principalmente na coluna `Amount`.

**Detecção de Outliers (Método IQR)**:

Para a coluna `Amount`:
- Q1 (25%): 5.65
- Q3 (75%): 77.05
- IQR: 71.40
- Limite Inferior: -101.45
- Limite Superior: 184.15

**Outliers Detectados**:
- Total de outliers: 8,976 transações (3.15% do dataset)
- Outliers acima do limite superior: 8,976
- Outliers abaixo do limite inferior: 0

**Impacto dos Outliers**:

1. **Nas Estatísticas Descritivas**:
   - Média (88.35) muito maior que mediana (22.00)
   - Desvio padrão inflado (250.12)
   - Assimetria positiva extrema

2. **Nas Análises**:
   - Modelos de machine learning podem ser influenciados pelos valores extremos
   - Correlações podem ser distorcidas
   - Visualizações precisam de escala logarítmica para melhor visualização

3. **Na Distribuição**:
   - A maioria das transações (96.85%) está dentro dos limites normais
   - Poucas transações (3.15%) têm valores muito altos

**Gráfico Gerado**: `output/boxplot_amount.png`

O boxplot mostra claramente a presença de muitos outliers acima do limite superior.

**Recomendações**:
1. Investigar se outliers são fraudes ou transações legítimas de alto valor
2. Considerar transformação logarítmica para normalizar a distribuição
3. Usar métodos robustos (mediana, IQR) em vez de média e desvio padrão
4. Avaliar remoção ou caping (limitação) de valores extremos dependendo do objetivo da análise

**Conclusão**: Os outliers em `Amount` são significativos e afetam as análises estatísticas. É importante tratá-los adequadamente dependendo do objetivo da análise.

---

## 4. Pergunta sobre Conclusões do Agente

### Pergunta: Quais são as principais conclusões que o agente obteve a partir dos dados e das análises realizadas?

**Resposta do Agente**:

Com base em todas as análises realizadas, aqui estão as principais conclusões:

### 📊 Conclusões Principais:

1. **Distribuição Altamente Assimétrica de Amount**:
   - A maioria das transações (96.85%) tem valores relativamente baixos
   - A média (88.35) é muito maior que a mediana (22.00), indicando assimetria positiva
   - Presença de 8,976 outliers (3.15% do dataset) com valores muito altos
   - **Impacto**: Necessidade de transformações ou métodos robustos para análises estatísticas

2. **Dataset Completo e Limpo**:
   - Nenhum valor ausente em todas as 31 colunas
   - 284,807 transações válidas
   - **Vantagem**: Não é necessário tratamento de dados faltantes

3. **Variáveis PCA Normalizadas**:
   - As 28 variáveis V1-V28 foram transformadas por PCA
   - Valores centrados em torno de zero
   - Variabilidades relativamente baixas e controladas
   - **Vantagem**: Dados já pré-processados e prontos para modelagem

4. **Desbalanceamento de Classes**:
   - Variável `Class` apresenta distribuição desbalanceada
   - Muito mais transações normais (0) que fraudulentas (1)
   - **Desafio**: Modelos de ML precisarão de técnicas de balanceamento (SMOTE, undersampling, etc.)

5. **Alta Variabilidade Temporal**:
   - Coluna `Time` cobre aproximadamente 48 horas de transações
   - Alta variabilidade temporal pode indicar padrões sazonais
   - **Oportunidade**: Análise temporal pode revelar padrões de fraude

6. **Correlações entre Variáveis**:
   - Algumas variáveis PCA apresentam correlações moderadas
   - Variável `Amount` tem baixa correlação com outras variáveis
   - **Insight**: `Amount` pode ser uma feature importante e independente para detecção de fraude

### 🎯 Recomendações para Próximos Passos:

1. **Tratamento de Outliers**: 
   - Investigar se outliers em `Amount` estão relacionados a fraudes
   - Considerar transformação logarítmica ou caping

2. **Análise de Correlação com Target**:
   - Verificar quais variáveis PCA têm maior correlação com `Class`
   - Identificar features mais importantes para detecção de fraude

3. **Balanceamento de Classes**:
   - Aplicar técnicas de balanceamento antes de treinar modelos
   - Usar métricas apropriadas (F1-score, AUC-ROC) em vez de acurácia

4. **Análise Temporal**:
   - Investigar padrões de fraude ao longo do tempo
   - Identificar horários de maior incidência de fraudes

5. **Visualizações Adicionais**:
   - Criar gráficos comparando distribuições de Amount entre fraudes e normais
   - Analisar distribuição de fraudes por hora do dia

### 💡 Insights Finais:

O dataset é bem estruturado e completo, mas apresenta desafios típicos de problemas de detecção de fraude:
- Desbalanceamento de classes
- Presença de outliers
- Necessidade de análise cuidadosa das features

As variáveis PCA já estão normalizadas, facilitando a modelagem, mas a variável `Amount` requer atenção especial devido à sua alta variabilidade e assimetria.

---

## 5. Link do Repositório

🔗 **Repositório GitHub**: 
```
https://github.com/seu-usuario/agent-ia-EDA
```

*Nota: Substitua "seu-usuario" pelo seu nome de usuário do GitHub após fazer o push do repositório.*

### Como Acessar e Executar:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/agent-ia-EDA.git
   cd agent-ia-EDA
   ```

2. **Configure o ambiente virtual**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a chave da API**:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione: `OPENAI_API_KEY=sua_chave_aqui`
   - ⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` (já está no `.gitignore`)

5. **Execute o agente**:
   ```bash
   python eda_agent.py
   ```

---

## 6. Segurança e Boas Práticas

### ✅ Chaves e Credenciais Protegidas:

- ✅ Arquivo `.env` está no `.gitignore` e **NÃO é commitado**
- ✅ Chave da API OpenAI é carregada apenas do arquivo `.env`
- ✅ Nenhuma chave hardcoded no código
- ✅ `.gitignore` configurado para ignorar:
  - `.env`
  - `output/` (gráficos e conclusões)
  - `.venv/` (ambiente virtual)
  - `*.csv` (datasets)

### 🔒 Verificação de Segurança:

Para verificar que não há chaves expostas:
```bash
# Verificar se .env está no .gitignore
grep -E "\.env|OPENAI_API_KEY" .gitignore

# Verificar se há chaves no código
grep -r "OPENAI_API_KEY" --exclude-dir=.venv --exclude-dir=.git .

# Verificar histórico do git (se já commitou antes)
git log --all --full-history --source -S "OPENAI_API_KEY"
```

---

## 7. Considerações Finais

### 🎯 Objetivos Alcançados:

✅ Agente genérico capaz de trabalhar com qualquer arquivo CSV  
✅ Geração automática de gráficos e visualizações  
✅ Sistema de memória para conclusões  
✅ Interface interativa para perguntas do usuário  
✅ Análises completas de EDA (descrição, padrões, anomalias, relações)  
✅ Respostas com conclusões baseadas nas análises  

### 🚀 Diferenciais da Solução:

1. **Genérico**: Funciona com qualquer CSV, não apenas o dataset de exemplo
2. **Completo**: Cobre todos os aspectos de EDA solicitados
3. **Inteligente**: Agente mantém contexto e memória entre perguntas
4. **Visual**: Gera gráficos automaticamente quando apropriado
5. **Documentado**: Código bem documentado e com documentação completa

### 📚 Documentação Adicional:

A documentação completa está disponível na pasta `doc/`:
- `fluxograma.md`: Fluxos de funcionamento
- `ferramentas.md`: Documentação de cada ferramenta
- `arquitetura.md`: Arquitetura técnica do sistema
- `README.md`: Índice da documentação

---

**Desenvolvido com**: Agno Framework + OpenAI GPT-4o  
**Licença**: MIT  
**Data**: Janeiro 2025

