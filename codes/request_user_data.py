import requests
import os
from dotenv import load_dotenv
import json

# Carregando chaves em segredo
load_dotenv()

# Definindo toke de acesso
access_token_ = os.getenv("GIT_HUB_API_TOKEN")

# Definindo headers
headers = {'Authorization': f"token {access_token_}"}

# Parâmetros de interesse
params = {
}

# Lendo json com informacoes dos usuarios
users_data_file = open('jsons/users_data.json')
users_request_data = json.load(users_data_file)

users_data = []

# URL de interesse do api
for user in users_request_data:
    USER_LOGIN = user['user_login']
    user_end_point =  f"https://api.github.com/users/{USER_LOGIN}"
    
    # Fazendo requisição
    response = requests.get(user_end_point, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        users_data.append(
            {
                'name' : data['name'], 
                'company' : data['company'], 
                'blog' : data['blog'], 
                'email' : data['email'], 
                'bio' : data['bio'], 
                'public_repos' : data['public_repos'], 
                'followers' : data['followers'],  
                'following' : data['following'], 
                'created_at' : data['created_at']
            }
        )
                
    else:
        print(f"Falha na requisição do usuário: {USER_LOGIN}")


# Formatando json     
json_users_data = json.dumps(users_data, indent=4)

# Salvando json de usuário
with open('jsons/users_microdata.json', 'w') as f:
    f.write(json_users_data)
    
print(f"Arquivo 'users_microdata.json' criado com sucesso!")