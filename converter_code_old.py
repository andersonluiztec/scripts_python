import os
import shutil
import openai
import base64


# Configurações da API do OpenAI
openai.api_key = base64.b64decode('c2stVk1FMm5oTnJRdmRzTDBDcEZkd1RUM0JsYmtGSncyRFhVb0NzM0J1N3kxQVQ3NWVY').decode('utf-8') # Substitua pelo seu API key da OpenAI

def translate_code(code, target_language):
    translation = openai.Completion.create(
        engine='text-davinci-003',  # Substitua pelo mecanismo desejado
        prompt=code,
        max_tokens=100,  # Substitua pelo número desejado de tokens de saída
        temperature=0.7,  # Substitua pela temperatura desejada (quanto maior, mais aleatório)
        n=1,  # Substitua pelo número desejado de respostas
        stop=None,  # Substitua pela string de parada personalizada, se necessário
    )
    translated_code = translation.choices[0].text.strip()

    return translated_code

def translate_repository(repo_url, target_language, new_branch):
    g = Github('YOUR_GITHUB_ACCESS_TOKEN')  # Substitua pelo seu token de acesso do GitHub

    try:
        repo = g.get_repo(repo_url)
        owner = repo.owner.login
        repo_name = repo.name
        print(f'Repositório {owner}/{repo_name} obtido com sucesso.')

        # Clonar o repositório em um diretório temporário
        local_path = f'./temp/{repo_name}'
        os.makedirs(local_path, exist_ok=True)

        repo_clone_url = repo.clone_url
        os.system(f'git clone {repo_clone_url} {local_path}')
        print(f'Repositório {owner}/{repo_name} clonado com sucesso.')

        # Criar uma nova branch para os códigos traduzidos
        repo.create_git_ref(f'refs/heads/{new_branch}', repo.get_branch('main').commit.sha)
        print(f'Nova branch {new_branch} criada com sucesso.')

        # Obter a lista de arquivos no repositório
        files = []
        for root, _, filenames in os.walk(local_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))

        # Traduzir e salvar os arquivos
        for file_path in files:
            with open(file_path, 'r') as file:
                code = file.read()

            translated_code = translate_code(code, target_language)

            # Salvar o código traduzido no mesmo diretório com a extensão '.java' (ou a extensão apropriada)
            translated_file_path = f'{file_path}.{target_language}'
            with open(translated_file_path, 'w') as file:
                file.write(translated_code)

            print(f'Código traduzido salvo em {translated_file_path}')

            # Criar um novo arquivo no repositório do GitHub com o código traduzido
            rel_file_path = os.path.relpath(translated_file_path, local_path)
            new_file = repo.create_file(rel_file_path, f'Tradução para {target_language}', translated_code, branch=new_branch)
            print(f'Código traduzido enviado para {new_file.html_url}')

    except Exception as e:
        print(f'Erro ao clonar ou traduzir o repositório {repo_url}: {e}')

    # Remover o diretório temporário
    shutil.rmtree(local_path)

# Exemplo de uso
repo_url = 'owner/repo'  # Substitua pelo nome do usuário/organização e nome do repositório target_language = 'java'  # Substitua pela linguagem de destino desejada new_branch = 'translated-code'  # Substitua pelo nome da nova branch

#translate_repository(repo_url, target_language, new_branch)

retorno = translate_code('Translate the following Visual Basic code to Java:\n\nPrivate Sub Command1_Click()\nText1.Text = \"Ate mais tarde !\"\nEnd Sub', 'java')

print(retorno)
