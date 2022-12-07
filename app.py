import pandas as pd 
import datetime
from datetime import datetime


def calcular_retorno_cdi(data_inicio: str, data_fim: str, valor: str):
    
    valor = float(valor)
    
    # consumindo api da taxa cdi 
    
    #dados = pd.read_json('https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json')  
    dados = pd.read_csv('dados.csv', sep=',') 
    
    # converter data 27
    start = datetime.strptime(data_inicio, '%d/%m/%Y')
    end = datetime.strptime(data_fim, '%d/%m/%Y')
    
    # alterando formato para data e assim poder fazer as operações necessárias
    dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y')

    # pegar valores de variação do fator cdi 
    dados_retorno = dados['valor'].pct_change()
    
    # criando campo no dataframe
    dados['retorno'] = dados_retorno
    
    
    # slice do intervalo solicitado pelo usuário 
    dados = dados.loc[(dados['data'] >= start) & (dados['data'] <= end)]
    
    
    # converter de % para real
    dados['retorno'] = dados['retorno'].apply(lambda x: x / 100)
    dados['valor'] = dados['valor'].apply(lambda x: x / 100)
    
    
    # novo campo para colocar o valor atual para acompanhamento
    dados['valor_atual'] = 0
    
    
    # atribuir o valor inicial 
    dados['valor_atual'].iloc[0] = valor
    # dados.loc[0, 'valor_atual'] = valor
    # dados['valor_atual'][0] = valor
    
    for item in range (dados.shape[0]):
        if item > 0:
            result = dados.iloc[item - 1]['valor_atual'] * (dados.iloc[item]['valor'] + 1)
            #dados.iloc[item]['valor_atual'] = result
            #print(dados.iloc[item]['valor_atual'])
            #print(f' dados {dados.iat[item, 2]}')
            dados.iat[item, 4] = result
    
    valor = dados.iloc[dados.shape[0]-1]['valor_atual'] - dados.iloc[1]['valor_atual']
    juros_percentual = round(((dados.iloc[dados.shape[0]-1]['valor_atual'] - dados.iloc[1]['valor_atual']) / dados.iloc[1]['valor_atual']) * 100, 2)
    print(f'valor inicial {round(dados.iloc[dados.shape[0]-1]["valor_atual"], 2)}')
    print(f'Juros gerados dinheiro: {round(valor, 2)} R$')
    print(f'Juros gerados percentual: {juros_percentual} %')
    print(f'Juros gerados percentual: {juros_percentual} %')
    
    dados.to_csv('restulado2.csv', sep=',', index=False)

def menu() -> int : 
    print('1. Calcular juros: ')
    print('2. Encerrar: ')
    opcao_usuario = input('Digite a opção desejada: ')
    
    return opcao_usuario


rodar = True

while(rodar):
    opttion = int(menu())
    
    if opttion == 1: 
        
        data_inicio = input('Data Inicio: ')
        data_fim = input('Data Fim: ')
        valor = input('Valor: ')
        calcular_retorno_cdi(data_inicio, data_fim, valor)   
        
    elif opttion == 2:
        break 
    
    else: 
        print('opção inválida')
    
    




