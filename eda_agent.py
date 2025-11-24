from agno.agent import Agent
from agno.tools import tool
from agno.models.openai import OpenAIChat
import sys
import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para salvar arquivos
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuração global
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Dicionário global para armazenar dados carregados
datasets = {}
current_dataset_name = None
conclusions_memory = []

def ensure_output_dir():
    """Garante que o diretório de saída existe"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

@tool
def load_csv(file_path: str) -> str:
    """
    Carrega um arquivo CSV e o armazena na memória.
    Use esta ferramenta primeiro para carregar o dataset que você vai analisar.
    
    Args:
        file_path: Caminho para o arquivo CSV (ex: './archive/creditcard.csv')
    
    Returns:
        Resumo do dataset carregado
    """
    global current_dataset_name
    
    try:
        df = pd.read_csv(file_path)
        dataset_name = Path(file_path).stem
        
        # Armazena o dataset
        datasets[dataset_name] = df
        current_dataset_name = dataset_name
        
        # Gera resumo
        summary = {
            "dataset": dataset_name,
            "linhas": len(df),
            "colunas": len(df.columns),
            "nomes_colunas": list(df.columns),
            "tipos": df.dtypes.astype(str).to_dict(),
            "valores_ausentes": df.isnull().sum().to_dict(),
            "amostra": df.head(3).to_dict(orient="records")
        }
        
        return json.dumps(summary, indent=2, default=str)
    except Exception as e:
        return f"Erro ao carregar CSV: {str(e)}"

@tool
def check_dataset_loaded() -> str:
    """
    Verifica se há um dataset carregado na memória.
    Use esta ferramenta PRIMEIRO antes de fazer qualquer análise para verificar se o dataset já está disponível.
    
    Returns:
        Informação sobre o dataset carregado ou mensagem indicando que nenhum dataset está carregado
    """
    global current_dataset_name, datasets
    
    if not current_dataset_name or current_dataset_name not in datasets:
        return "Nenhum dataset carregado. É necessário carregar um CSV primeiro usando load_csv."
    
    df = datasets[current_dataset_name]
    return f"Dataset '{current_dataset_name}' já está carregado na memória. Dimensões: {len(df)} linhas x {len(df.columns)} colunas. Colunas: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}"

@tool
def get_dataset_info() -> str:
    """
    Retorna informações gerais sobre o dataset atualmente carregado.
    Use para entender a estrutura dos dados antes de fazer análises específicas.
    IMPORTANTE: Use check_dataset_loaded primeiro para verificar se há um dataset carregado.
    """
    global current_dataset_name, datasets
    
    if not current_dataset_name or current_dataset_name not in datasets:
        return "Nenhum dataset carregado. Use load_csv primeiro."
    
    df = datasets[current_dataset_name]
    
    info = {
        "dataset": current_dataset_name,
        "dimensoes": f"{len(df)} linhas x {len(df.columns)} colunas",
        "colunas": list(df.columns),
        "tipos_dados": df.dtypes.astype(str).to_dict(),
        "valores_ausentes": df.isnull().sum().to_dict(),
        "estatisticas_descritivas": df.describe().to_dict(),
        "amostra_5_linhas": df.head(5).to_dict(orient="records")
    }
    
    return json.dumps(info, indent=2, default=str)

@tool
def execute_analysis(code: str) -> str:
    """
    Executa código Python para análise de dados.
    O DataFrame está disponível como 'df' e você pode usar pandas, numpy, matplotlib, seaborn.
    
    IMPORTANTE: 
    - Para gerar gráficos, use plt.savefig('output/grafico.png') antes de plt.close()
    - Defina uma variável 'result' com o resultado da análise se quiser retornar algo
    - Use plt.close() após salvar cada gráfico para liberar memória
    
    Args:
        code: Código Python a ser executado
    
    Returns:
        Resultado da execução ou mensagem de erro
    """
    global current_dataset_name, datasets
    
    if not current_dataset_name or current_dataset_name not in datasets:
        return "Erro: Nenhum dataset carregado. Use load_csv primeiro."
    
    df = datasets[current_dataset_name]
    output_dir = ensure_output_dir()
    
    # Captura stdout
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    try:
        # Executa o código
        exec_globals = {
            'df': df.copy(),
            'pd': pd,
            'np': np,
            'plt': plt,
            'sns': sns,
            'output_dir': output_dir
        }
        exec_locals = {}
        
        exec(code, exec_globals, exec_locals)
        
        # Captura output
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Se há uma variável 'result', retorna ela
        if 'result' in exec_locals:
            result = exec_locals['result']
            if isinstance(result, (pd.DataFrame, pd.Series)):
                return f"{output}\n\n{result.to_string()}"
            return f"{output}\n\n{str(result)}"
        
        return output.strip() if output.strip() else "Código executado com sucesso."
        
    except Exception as e:
        sys.stdout = old_stdout
        return f"Erro ao executar código: {str(e)}\nTipo: {type(e).__name__}"

@tool
def save_conclusion(conclusion: str) -> str:
    """
    Salva uma conclusão importante da análise na memória do agente.
    Use esta ferramenta sempre que descobrir algo relevante sobre os dados.
    
    Args:
        conclusion: Texto descrevendo a conclusão encontrada
    
    Returns:
        Confirmação de que a conclusão foi salva
    """
    global conclusions_memory
    
    conclusion_entry = {
        "timestamp": datetime.now().isoformat(),
        "conclusion": conclusion
    }
    
    conclusions_memory.append(conclusion_entry)
    
    # Salva em arquivo também
    output_dir = ensure_output_dir()
    memory_file = output_dir / "conclusions.json"
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        json.dump(conclusions_memory, f, indent=2, ensure_ascii=False)
    
    return f"Conclusão salva: {conclusion}"

@tool
def get_conclusions() -> str:
    """
    Retorna todas as conclusões salvas até o momento.
    Use para resumir as descobertas da análise.
    """
    global conclusions_memory
    
    if not conclusions_memory:
        return "Nenhuma conclusão salva ainda."
    
    return json.dumps(conclusions_memory, indent=2, ensure_ascii=False)

# Criar o agente
eda_agent = Agent(
    tools=[load_csv, check_dataset_loaded, get_dataset_info, execute_analysis, save_conclusion, get_conclusions],
    model=OpenAIChat(
        id="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    ),
    description="Você é um assistente especializado em Análise Exploratória de Dados (EDA).",
    instructions=[
        "Você é um analista de dados experiente capaz de realizar análises exploratórias completas em datasets CSV.",
        "",
        "SEU PROCESSO DE TRABALHO (SEMPRE SEGUIR ESTA ORDEM):",
        "1. PRIMEIRO: Use check_dataset_loaded para verificar se já há um dataset carregado na memória",
        "2. Se não houver dataset carregado, use load_csv para carregar o arquivo CSV",
        "3. Use get_dataset_info para entender a estrutura dos dados (se necessário)",
        "4. Execute análises específicas usando execute_analysis para responder à pergunta do usuário",
        "5. Salve conclusões importantes com save_conclusion",
        "",
        "REGRA CRÍTICA:",
        "- NUNCA peça ao usuário o caminho do arquivo CSV. O dataset já foi carregado no início da sessão.",
        "- SEMPRE use check_dataset_loaded primeiro para verificar se o dataset está disponível.",
        "- Se check_dataset_loaded retornar que há um dataset carregado, use-o diretamente. NÃO tente carregar novamente.",
        "- Responda diretamente às perguntas do usuário usando execute_analysis, não pergunte sobre o que fazer.",
        "",
        "TIPOS DE ANÁLISES QUE VOCÊ DEVE REALIZAR:",
        "",
        "A) DESCRIÇÃO DOS DADOS:",
        "   - Identificar tipos de dados (numéricos, categóricos)",
        "   - Calcular distribuições (histogramas, boxplots)",
        "   - Encontrar intervalos (mínimo, máximo, quartis)",
        "   - Calcular medidas de tendência central (média, mediana, moda)",
        "   - Calcular variabilidade (desvio padrão, variância, IQR)",
        "",
        "B) IDENTIFICAÇÃO DE PADRÕES E TENDÊNCIAS:",
        "   - Analisar padrões temporais (se houver coluna de tempo/data)",
        "   - Identificar valores mais/menos frequentes",
        "   - Detectar agrupamentos ou clusters visuais",
        "",
        "C) DETECÇÃO DE ANOMALIAS (OUTLIERS):",
        "   - Identificar valores atípicos usando IQR, Z-score ou visualizações",
        "   - Analisar impacto dos outliers",
        "   - Sugerir tratamento (remoção, transformação, investigação)",
        "",
        "D) RELAÇÕES ENTRE VARIÁVEIS:",
        "   - Criar gráficos de dispersão para variáveis numéricas",
        "   - Calcular matriz de correlação",
        "   - Criar tabelas cruzadas para variáveis categóricas",
        "   - Identificar variáveis mais/menos correlacionadas",
        "",
        "E) CONCLUSÕES:",
        "   - Sempre salve conclusões importantes com save_conclusion",
        "   - Ao final, use get_conclusions para apresentar um resumo",
        "",
        "DIRETRIZES PARA GRÁFICOS:",
        "   - Sempre salve gráficos em 'output/' com nomes descritivos",
        "   - Use plt.savefig('output/nome_do_grafico.png') antes de plt.close()",
        "   - Use plt.close() após cada gráfico para liberar memória",
        "   - Use seaborn para gráficos mais bonitos quando apropriado",
        "   - Adicione títulos e labels descritivos",
        "",
        "DIRETRIZES PARA CÓDIGO:",
        "   - O DataFrame está disponível como 'df'",
        "   - Use pandas para manipulação de dados",
        "   - Use matplotlib/seaborn para visualizações",
        "   - Defina 'result' se quiser retornar um valor específico",
        "   - Seja eficiente: não carregue dados desnecessários",
        "   - Para perguntas sobre distribuições: crie histogramas para cada variável numérica",
        "   - Para perguntas sobre intervalos: calcule min, max, quartis usando df.describe() ou código específico",
        "   - Para perguntas sobre variabilidade: calcule desvio padrão e variância usando df.std() e df.var()",
        "",
        "RESPOSTAS:",
        "   - Seja claro e didático nas explicações",
        "   - SEMPRE execute o código necessário para responder a pergunta, não apenas sugira o que fazer",
        "   - Sempre mencione quando gráficos foram salvos e onde",
        "   - Apresente números e estatísticas de forma organizada",
        "   - Relacione descobertas com o contexto do problema",
        "   - NÃO pergunte ao usuário o que fazer - execute a análise diretamente",
    ],
)

def main():
    """Interface interativa para o agente EDA"""
    global current_dataset_name
    
    print("=" * 70)
    print("🤖 AGENTE DE ANÁLISE EXPLORATÓRIA DE DADOS (EDA)")
    print("=" * 70)
    print("\nEste agente pode analisar qualquer arquivo CSV e responder perguntas sobre:")
    print("  • Descrição dos dados (tipos, distribuições, estatísticas)")
    print("  • Padrões e tendências")
    print("  • Detecção de anomalias")
    print("  • Relações entre variáveis")
    print("  • Conclusões e insights")
    print("\n" + "=" * 70)
    
    # Pergunta inicial sobre o arquivo CSV
    csv_path = input("\n📁 Digite o caminho do arquivo CSV (ou Enter para usar './archive/creditcard.csv'): ").strip()
    if not csv_path:
        csv_path = "./archive/creditcard.csv"
    
    print(f"\n⏳ Carregando dataset: {csv_path}")
    response = eda_agent.run(f"Carregue o arquivo CSV: {csv_path}")
    print(f"\n✅ {response.content}\n")
    
    # Informa ao agente que o dataset está carregado e pronto para análise
    eda_agent.run("O dataset já foi carregado e está disponível na memória. Você pode começar a responder perguntas sobre os dados.")
    
    print("=" * 70)
    print("💬 Agora você pode fazer perguntas sobre os dados!")
    print("   Digite 'sair' para encerrar")
    print("   Digite 'conclusoes' para ver um resumo das análises")
    print("=" * 70)
    
    # Loop de perguntas
    while True:
        print("\n" + "-" * 70)
        pergunta = input("\n❓ Sua pergunta: ").strip()
        
        if not pergunta:
            continue
        
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("\n👋 Encerrando...")
            break
        
        if pergunta.lower() == 'conclusoes':
            print("\n📊 Buscando conclusões salvas...")
            response = eda_agent.run("O dataset já está carregado. Apresente um resumo completo de todas as conclusões encontradas nas análises realizadas.")
        else:
            print(f"\n🔍 Analisando...")
            # Adiciona contexto de que o dataset já está carregado
            pergunta_com_contexto = f"O dataset já está carregado na memória. {pergunta}"
            response = eda_agent.run(pergunta_com_contexto)
        
        print(f"\n💡 Resposta:\n{response.content}")
        
        # Verifica se há gráficos gerados
        output_dir = Path("output")
        if output_dir.exists():
            recent_files = sorted(output_dir.glob("*.png"), key=os.path.getmtime, reverse=True)[:3]
            if recent_files:
                print(f"\n📈 Gráficos recentes salvos em: {', '.join([str(f) for f in recent_files])}")

if __name__ == "__main__":
    main()

