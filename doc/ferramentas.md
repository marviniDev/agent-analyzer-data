# 🛠️ Documentação das Ferramentas do Agente EDA

Este documento descreve detalhadamente cada ferramenta disponível no agente genérico de EDA.

## 📋 Índice

1. [load_csv](#1-load_csv)
2. [check_dataset_loaded](#2-check_dataset_loaded)
3. [get_dataset_info](#3-get_dataset_info)
4. [execute_analysis](#4-execute_analysis)
5. [save_conclusion](#5-save_conclusion)
6. [get_conclusions](#6-get_conclusions)

---

## 1. `load_csv`

### Descrição
Carrega um arquivo CSV e o armazena na memória global para análise.

### Parâmetros
- `file_path` (str): Caminho para o arquivo CSV
  - Exemplo: `"./archive/creditcard.csv"`

### Retorno
JSON string contendo:
- `dataset`: Nome do dataset (sem extensão)
- `linhas`: Número de linhas
- `colunas`: Número de colunas
- `nomes_colunas`: Lista de nomes das colunas
- `tipos`: Dicionário com tipos de dados de cada coluna
- `valores_ausentes`: Dicionário com contagem de valores ausentes
- `amostra`: Primeiras 3 linhas do dataset

### Exemplo de Uso
```python
load_csv("./archive/creditcard.csv")
```

### Exemplo de Retorno
```json
{
  "dataset": "creditcard",
  "linhas": 284807,
  "colunas": 31,
  "nomes_colunas": ["Time", "V1", "V2", ..., "Amount", "Class"],
  "tipos": {
    "Time": "float64",
    "V1": "float64",
    ...
  },
  "valores_ausentes": {
    "Time": 0,
    "V1": 0,
    ...
  },
  "amostra": [...]
}
```

### Comportamento
- Armazena o DataFrame em `datasets[dataset_name]`
- Define `current_dataset_name` globalmente
- Retorna erro se o arquivo não existir ou não for válido

---

## 2. `check_dataset_loaded`

### Descrição
Verifica se há um dataset carregado na memória. Use esta ferramenta PRIMEIRO antes de fazer qualquer análise.

### Parâmetros
Nenhum

### Retorno
- Se dataset carregado: String informando nome, dimensões e primeiras colunas
- Se não carregado: Mensagem indicando que é necessário carregar um CSV

### Exemplo de Uso
```python
check_dataset_loaded()
```

### Exemplo de Retorno (Dataset carregado)
```
Dataset 'creditcard' já está carregado na memória. Dimensões: 284807 linhas x 31 colunas. Colunas: Time, V1, V2, V3, V4, V5, V6, V7, V8, V9...
```

### Exemplo de Retorno (Sem dataset)
```
Nenhum dataset carregado. É necessário carregar um CSV primeiro usando load_csv.
```

### Comportamento
- Verifica `current_dataset_name` e `datasets` dict
- Não modifica estado, apenas verifica

---

## 3. `get_dataset_info`

### Descrição
Retorna informações completas e detalhadas sobre o dataset atualmente carregado.

### Parâmetros
Nenhum

### Retorno
JSON string contendo:
- `dataset`: Nome do dataset
- `dimensoes`: String formatada (ex: "284807 linhas x 31 colunas")
- `colunas`: Lista completa de colunas
- `tipos_dados`: Dicionário com tipos de cada coluna
- `valores_ausentes`: Dicionário com contagem de nulos
- `estatisticas_descritivas`: Estatísticas descritivas (count, mean, std, min, 25%, 50%, 75%, max)
- `amostra_5_linhas`: Primeiras 5 linhas do dataset

### Exemplo de Uso
```python
get_dataset_info()
```

### Exemplo de Retorno
```json
{
  "dataset": "creditcard",
  "dimensoes": "284807 linhas x 31 colunas",
  "colunas": ["Time", "V1", "V2", ...],
  "tipos_dados": {
    "Time": "float64",
    ...
  },
  "valores_ausentes": {...},
  "estatisticas_descritivas": {
    "Time": {
      "count": 284807.0,
      "mean": 94813.86,
      ...
    },
    ...
  },
  "amostra_5_linhas": [...]
}
```

### Comportamento
- Retorna erro se nenhum dataset estiver carregado
- Calcula estatísticas descritivas automaticamente
- Inclui amostra para visualização rápida

---

## 4. `execute_analysis`

### Descrição
Executa código Python para análise de dados. Permite cálculos, filtros, agregações e geração de gráficos.

### Parâmetros
- `code` (str): Código Python a ser executado

### Variáveis Disponíveis no Código
- `df`: DataFrame pandas com o dataset carregado
- `pd`: Biblioteca pandas
- `np`: Biblioteca numpy
- `plt`: Biblioteca matplotlib.pyplot
- `sns`: Biblioteca seaborn
- `output_dir`: Path do diretório graficos/

### Retorno
- Se código define `result`: Retorna o valor de `result`
- Se código imprime algo: Retorna o output capturado
- Se houver erro: Retorna mensagem de erro detalhada

### Exemplo de Uso
```python
code = """
import matplotlib.pyplot as plt
import seaborn as sns

# Criar histograma
plt.figure(figsize=(10, 6))
sns.histplot(df['Amount'], bins=50)
plt.title('Distribuição de Amount')
plt.xlabel('Amount')
plt.ylabel('Frequência')
plt.savefig('graficos/distribuicao_amount.png')
plt.close()

result = f"Gráfico salvo! Estatísticas: Média={df['Amount'].mean():.2f}, Mediana={df['Amount'].median():.2f}"
"""
execute_analysis(code)
```

### Diretrizes Importantes
1. **Gráficos**: Sempre use `plt.savefig('graficos/nome.png')` antes de `plt.close()`
2. **Memória**: Use `plt.close()` após cada gráfico
3. **Resultado**: Defina `result` se quiser retornar um valor específico
4. **Erros**: O código é executado em ambiente isolado, erros são capturados

### Comportamento
- Captura stdout durante execução
- Executa código com acesso ao DataFrame
- Retorna output ou erro apropriadamente

---

## 5. `save_conclusion`

### Descrição
Salva uma conclusão importante da análise na memória do agente.

### Parâmetros
- `conclusion` (str): Texto descrevendo a conclusão encontrada

### Retorno
String de confirmação com a conclusão salva

### Exemplo de Uso
```python
save_conclusion("A coluna Amount apresenta muitos outliers, com valores extremos acima de 10.000")
```

### Exemplo de Retorno
```
Conclusão salva: A coluna Amount apresenta muitos outliers, com valores extremos acima de 10.000
```

### Comportamento
- Adiciona entrada em `conclusions_memory` com timestamp
- Salva automaticamente em `graficos/conclusions.json`
- Permite recuperação posterior com `get_conclusions`

### Formato da Conclusão Salva
```json
{
  "timestamp": "2025-01-XXT...",
  "conclusion": "Texto da conclusão"
}
```

---

## 6. `get_conclusions`

### Descrição
Retorna todas as conclusões salvas até o momento.

### Parâmetros
Nenhum

### Retorno
- Se há conclusões: JSON array com todas as conclusões
- Se não há: Mensagem indicando que nenhuma conclusão foi salva

### Exemplo de Uso
```python
get_conclusions()
```

### Exemplo de Retorno (Com conclusões)
```json
[
  {
    "timestamp": "2025-01-XXT10:30:00",
    "conclusion": "A coluna Amount apresenta muitos outliers"
  },
  {
    "timestamp": "2025-01-XXT10:35:00",
    "conclusion": "A correlação entre V1 e V2 é muito alta (0.95)"
  }
]
```

### Exemplo de Retorno (Sem conclusões)
```
Nenhuma conclusão salva ainda.
```

### Comportamento
- Lê de `conclusions_memory` (memória)
- Formata como JSON para fácil leitura
- Não modifica as conclusões, apenas retorna

---

## 🔄 Fluxo de Uso Recomendado

### 1. Carregar Dataset
```
load_csv("./archive/creditcard.csv")
```

### 2. Verificar Dataset (antes de cada análise)
```
check_dataset_loaded()
```

### 3. Obter Informações Gerais (se necessário)
```
get_dataset_info()
```

### 4. Executar Análises Específicas
```
execute_analysis("código python aqui")
```

### 5. Salvar Conclusões Importantes
```
save_conclusion("conclusão importante")
```

### 6. Recuperar Todas as Conclusões
```
get_conclusions()
```

---

## 💡 Dicas de Uso

### Para o Agente
- Sempre use `check_dataset_loaded` primeiro
- Use `get_dataset_info` quando precisar entender a estrutura
- Use `execute_analysis` para qualquer cálculo ou visualização
- Salve conclusões importantes com `save_conclusion`
- Use `get_conclusions` para resumir descobertas

### Para Gráficos
- Sempre salve em `graficos/` com nomes descritivos
- Use `plt.close()` após cada gráfico
- Combine múltiplos gráficos em subplots quando apropriado
- Use seaborn para gráficos mais bonitos

### Para Código
- Defina `result` para retornar valores específicos
- Use `print()` para output de debug
- Trate erros adequadamente (try/except)
- Seja eficiente: não carregue dados desnecessários

---

## ⚠️ Tratamento de Erros

Todas as ferramentas tratam erros adequadamente:

- **load_csv**: Retorna mensagem de erro se arquivo não existir
- **check_dataset_loaded**: Retorna mensagem se dataset não estiver carregado
- **get_dataset_info**: Retorna erro se dataset não estiver carregado
- **execute_analysis**: Captura exceções e retorna mensagem de erro detalhada
- **save_conclusion**: Sempre funciona (apenas adiciona à lista)
- **get_conclusions**: Retorna mensagem se não houver conclusões

---

## 📊 Exemplos Completos

### Exemplo 1: Análise de Distribuição
```python
# 1. Verificar dataset
check_dataset_loaded()

# 2. Gerar histograma
execute_analysis("""
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 6))
sns.histplot(df['Amount'], bins=100, kde=True)
plt.title('Distribuição de Amount')
plt.xlabel('Valor da Transação')
plt.ylabel('Frequência')
plt.savefig('graficos/distribuicao_amount.png')
plt.close()

result = f"Gráfico gerado! Média: {df['Amount'].mean():.2f}, Mediana: {df['Amount'].median():.2f}"
""")

# 3. Salvar conclusão
save_conclusion("A distribuição de Amount é altamente assimétrica, com muitos valores baixos e poucos valores muito altos")
```

### Exemplo 2: Análise de Correlação
```python
# 1. Calcular correlação
execute_analysis("""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Matriz de correlação apenas para variáveis numéricas
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()

# Gráfico de heatmap
plt.figure(figsize=(15, 12))
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
plt.title('Matriz de Correlação')
plt.tight_layout()
plt.savefig('graficos/matriz_correlacao.png')
plt.close()

# Encontrar correlações mais altas
corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
high_corr = corr_pairs[(corr_pairs > 0.7) & (corr_pairs < 1.0)]

result = f"Correlações altas encontradas: {high_corr.head(10).to_dict()}"
""")
```

### Exemplo 3: Detecção de Outliers
```python
# 1. Detectar outliers usando IQR
execute_analysis("""
import matplotlib.pyplot as plt
import seaborn as sns

# Boxplot para visualizar outliers
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['Amount'])
plt.title('Boxplot de Amount - Detecção de Outliers')
plt.ylabel('Amount')
plt.savefig('graficos/boxplot_amount.png')
plt.close()

# Calcular outliers usando IQR
Q1 = df['Amount'].quantile(0.25)
Q3 = df['Amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['Amount'] < lower_bound) | (df['Amount'] > upper_bound)]
outlier_count = len(outliers)
outlier_percentage = (outlier_count / len(df)) * 100

result = f"Outliers detectados: {outlier_count} ({outlier_percentage:.2f}% do total). Limites: [{lower_bound:.2f}, {upper_bound:.2f}]"
""")

# 2. Salvar conclusão
save_conclusion(f"Encontrados {outlier_count} outliers na coluna Amount usando método IQR")
```

