from agno.agent import Agent
from agno.tools import tool
from agno.models.openai import OpenAIChat
import sys
import io
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# ----------- Pré-processamento -----------

def preprocess_csv(caminho_do_arquivo, sample_size=5):
    """Carrega CSV e gera metadados e estatísticas compactas para não estourar tokens"""
    df = pd.read_csv(caminho_do_arquivo)

    # Metadados gerais
    metadata = {
        "n_linhas": len(df),
        "n_colunas": len(df.columns),
        "colunas": list(df.columns),
        "tipos": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().mean().round(3).to_dict()
    }

    # Estatísticas descritivas resumidas (sem amostra gigante)
    stats = df.describe(include="all").transpose().fillna("").to_dict()

    # Pequena amostra só para referência (5 linhas)
    sample = df.sample(min(sample_size, len(df)), random_state=42).to_dict(orient="records")

    preprocessed_data = {
        "metadata": metadata,
        "stats": stats,
        "sample": sample
    }

    return preprocessed_data

df_global = pd.read_csv("./archive/creditcard.csv")
preprocessed_data = preprocess_csv("./archive/creditcard.csv") # Sua função de pré-processamento

@tool
def dataset_overview():
    """Retorna um resumo pré-processado do dataset (metadados, estatísticas e pequena amostra). Use para perguntas GERAIS sobre a estrutura dos dados."""
    return preprocessed_data

@tool
def code_interpreter(code: str) -> str:
    """
    Executa código Python para responder a perguntas ESPECÍFICAS que exigem CÁLCULOS, FILTROS ou AGREGAÇÕES nos dados.
    O código deve usar um DataFrame pandas chamado 'df'.
    """
    local_vars = {"df": df_global}
    
    try:
        # Executa o código e captura o último valor
        exec_globals = {}
        exec_locals = {"df": df_global}
        exec(code, exec_globals, exec_locals)

        # Se o código definiu uma variável chamada 'result', retornamos isso
        if "result" in exec_locals:
            return str(exec_locals["result"])

        # Caso contrário, retorna o que foi impresso
        output = io.StringIO()
        sys.stdout = output
        exec(code, exec_globals, exec_locals)
        sys.stdout = sys.__stdout__
        return output.getvalue().strip() or "O código foi executado, mas não retornou nada."

    except Exception as e:
        sys.stdout = sys.__stdout__
        return f"Ocorreu um erro ao executar o código: {e}"

# ----------- Criar Agente com Instruções Refinadas -----------
# Substitua apenas a criação do agente. O resto do código está ótimo.

analyst_agent = Agent(
    tools=[dataset_overview, code_interpreter],
    model=OpenAIChat(
        id="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    ),
    num_history_runs=1,
    # executar só duas vezes
    

    # DESCRIÇÃO E INSTRUÇÕES FINAIS
    description="Você é um assistente de IA que tem acesso a DUAS ferramentas e NADA MAIS.",
    instructions=[
        "Sua única tarefa é responder perguntas sobre um dataset usando as ferramentas disponíveis.",
    ],
)



print("\n--- Pergunta 2: Cálculo Específico (Média) ---")
analyst_agent.print_response("Selecione a coluna 'Amount' e 'Class' e crie um gráfico de barras mostrando a média de 'Amount' para cada valor de 'Class'.")

