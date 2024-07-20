import requests
import os
from dotenv import load_dotenv
import json

# Carregando chaves em segredo
load_dotenv()

# Definindo toke de acesso
### SUBSTITUIR PELA SUA PRÓPRIA API KEY CASO NECESSÁRIO
access_token_ = os.getenv("GIT_HUB_API_TOKEN")

# Definindo headers
headers = {'Authorization': f"token {access_token_}"}
page_ = 1
itens_per_page_ = 20

# Parâmetros de interesse
params = {
    'q': 'followers:31..100',  # Procurando usuários com pelo menos 1 seguidor
    'per_page': itens_per_page_,       # Quantidade de resultados por página 
    'page': page_,
}

# URL de interesse do api
url_search = 'https://api.github.com/search/users'


# Fazendo requisição
response = requests.get(url_search, params=params, headers=headers)

# Criando json parametrizado para informações de interese
json_users = []

# Checando se resposta foi positiva 200 = OK
if response.status_code == 200:
    data = response.json()    
    
    # Como prova de conceito, vou utilizar apenas as 5 primeiras páginas
    total_page_ = int(data['total_count']/itens_per_page_) # Usar isso para tudo
    total_page_ = 5 # Substituindo o valor para evitar um processo demorado para a POC
    
    while params['page'] < total_page_:
        # Garante que a resposta existe antes de tentar popular os dados
        if response.status_code == 200:
            data = response.json()  
            for user in data['items']:
                json_users.append({'user_login': user['login'], 'user_id': user['id'], 'user_repo_url':user['repos_url']})
        
        # Mudando paginacao da resposta
        params['page'] += 1
        response = requests.get(url_search, params=params, headers=headers)
      

# Formatando json     
json_users_data = json.dumps(json_users, indent=4)

# Salvando json de usuário
with open('jsons/users_data.json', 'w') as f:
    f.write(json_users_data)
    
print(f"Arquivo 'users_data.json' criado com sucesso!")