"""
Exemplo de uso programático do agente EDA
Este arquivo demonstra como usar o agente sem a interface interativa
"""

from eda_agent import eda_agent

def exemplo_basico():
    """Exemplo básico de uso do agente"""
    
    print("=" * 70)
    print("EXEMPLO DE USO DO AGENTE EDA")
    print("=" * 70)
    
    # 1. Carregar o dataset
    print("\n1. Carregando dataset...")
    response = eda_agent.run("Carregue o arquivo CSV: ./archive/creditcard.csv")
    print(f"✅ {response.content[:200]}...")
    
    # 2. Perguntar sobre tipos de dados
    print("\n2. Analisando tipos de dados...")
    response = eda_agent.run("Quais são os tipos de dados de cada coluna?")
    print(f"💡 {response.content[:300]}...")
    
    # 3. Perguntar sobre estatísticas
    print("\n3. Calculando estatísticas descritivas...")
    response = eda_agent.run("Quais são as estatísticas descritivas da coluna 'Amount'?")
    print(f"💡 {response.content[:300]}...")
    
    # 4. Gerar gráfico
    print("\n4. Gerando gráfico...")
    response = eda_agent.run("Crie um histograma da distribuição da coluna 'Amount' e salve como 'distribuicao_amount.png'")
    print(f"💡 {response.content[:300]}...")
    
    # 5. Obter conclusões
    print("\n5. Obtendo conclusões...")
    response = eda_agent.run("Apresente um resumo das conclusões encontradas")
    print(f"💡 {response.content[:400]}...")
    
    print("\n" + "=" * 70)
    print("Exemplo concluído!")
    print("=" * 70)

if __name__ == "__main__":
    exemplo_basico()

