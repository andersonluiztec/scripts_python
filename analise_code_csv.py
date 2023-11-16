import os
import requests

total_arquivos = 0
total_linhas = 0
total_palavras = 0
total_caracteres = 0
total_custo_dolar = 0
quantidade_custo_token = 1000
preco_token = 0 

def analisar_arquivo(arquivo):
    global total_arquivos
    num_linhas = 0
    num_palavras = 0
    num_caracteres = 0
    
    with open(arquivo, 'r') as f:
        total_arquivos += 1
        for linha in f:
            num_linhas += 1
            palavras = linha.split()
            num_palavras += len(palavras)
            num_caracteres += len(linha)

    return num_linhas, num_palavras, num_caracteres

def obter_preco_token():
    try:
        # Faça a chamada real à API da OpenAI para obter o preço do token
        url = "https://api.openai.com/v1/pricing"
        headers = {
            "Authorization": "Bearer KEY" 
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        preco_token = data["data"][0]["cost"]["amount"]
    except:
        # Retorna um valor mockado caso ocorra algum erro na chamada à API
        preco_token = 0.02  

    return preco_token

def calcular_custo_aproximado(palavras):
    global quantidade_custo_token, preco_token
    custo_dolar = ((palavras * 2) / quantidade_custo_token) * (preco_token)
    return custo_dolar

def varrer_diretorio_arquivos(diretorio):
    global total_linhas, total_palavras, total_caracteres, total_custo_dolar



    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)

        extensoes_nao_permitidas = ['.bmp', '.jpg', '.idx', '.sql', '.txt', '.exe', '.dll', '.frx', '.xls', '.ico','.gif', '.log','.png', '.properties', '.save', '.gitignore', '.pack','.sample','.bkp', '']
        nome, extensao = os.path.splitext(nome_arquivo)

        if os.path.isfile(caminho_arquivo) and (extensao.lower() not in extensoes_nao_permitidas):
    
            try:
                linhas, palavras, caracteres = analisar_arquivo(caminho_arquivo)

                # Calcular custo Aproximado
                custo_dolar = calcular_custo_aproximado(palavras)

                print(f"{caminho_arquivo};{linhas};{palavras};{caracteres};${custo_dolar:.2f}")

            except Exception as e:
                print(f"ERRO: {caminho_arquivo};{linhas};{palavras};{caracteres};${custo_dolar:.2f};{e}")

            total_linhas += linhas
            total_palavras += palavras
            total_caracteres += caracteres
            total_custo_dolar += custo_dolar
    
        elif os.path.isdir(caminho_arquivo):
            varrer_diretorio_arquivos(caminho_arquivo)


# Diretório contendo os arquivos VB
diretorio = 'C:\\AndersonSilva\\Projetos\\PoC_Codex\\vb-sapt-base-apoio-processamento-tesouraria'

#cabeçalho do csv
print(f"Arquivo;Quantidade de linhas de código;Quantidade de palavras;Quantidade de caracteres;Estimativa de custo aproximado (dólar)")

preco_token = obter_preco_token()

varrer_diretorio_arquivos(diretorio)

print("\n")
print("------ Resultado Total ------")
print(f"Quantidade total de arquivos;{total_arquivos}")
print(f"Quantidade total de linhas de código;{total_linhas}")
print(f"Quantidade total de palavras;{total_palavras}")
print(f"Quantidade total de caracteres;{total_caracteres}")
print(f"Quantidade de Token para estimativa de custo;{quantidade_custo_token}")
print(f"Valor Custo pela quantidade de Token (dólar);${preco_token:.2f}")
print(f"Estimativa de custo total aproximado (dólar);${total_custo_dolar:.2f}")