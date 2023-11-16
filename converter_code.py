import argparse
import os
import pygit2
from tqdm import tqdm
import shutil
from getpass import getpass
import openai
import base64

# Configurações da API do OpenAI
openai.api_key = base64.b64decode('c2stVk1FMm5oTnJRdmRzTDBDcEZkd1RUM0JsYmtGSncyRFhVb0NzM0J1N3kxQVQ3NWVY').decode('utf-8') # Substitua pelo seu API key da OpenAI

def translate_code(code, source_language, target_language):
    return code
    #translated_code = code
    #try:
    #    translation = openai.Completion.create(
    #        engine='text-davinci-003',  # Substitua pelo mecanismo desejado
    #        prompt=f'Translate the following {source_language} code to {target_language}:\n\n{code}',
    #        max_tokens=100,  # Substitua pelo número desejado de tokens de saída
    #        temperature=0.7,  # Substitua pela temperatura desejada (quanto maior, mais aleatório)
    #        n=1,  # Substitua pelo número desejado de respostas
    #        stop=None,  # Substitua pela string de parada personalizada, se necessário
    #    )
    #    translated_code = translation.choices[0].text.strip()
    #    return translated_code
    #except Exception as e:
    #    print(f'Erro: {e}')
    #    return code

def clone_repository(clone_url):
    print(f'Iniciando Clone com argumentos {clone_url}') 
    
    local_path = f'./{os.path.splitext(clone_url.rsplit("/",1)[-1])[0]}'

    username = input('Informe seu usuario do BitBucket: ')
    password = getpass('Informe sua senha do BitBucket: ')

    try:
        callbacks = pygit2.RemoteCallbacks()
        progress = tqdm(desc='Clonando repositório', unit=' objects')
      
        def transfer_progress(stats):
            progress.n = stats.indexed_objects
            progress.refresh()

        callbacks.credentials = pygit2.UserPass(username, password)
        callbacks.transfer_progress = transfer_progress

        if os.path.exists(local_path):
          shutil.rmtree(local_path)

        repository = pygit2.clone_repository(clone_url, local_path,callbacks=callbacks)
        progress.close()

        print(f'Repositório {local_path} clonado com sucesso.')
    except Exception as e:
        progress.close()
        print(f'Erro ao clonar o repositório {local_path}: {e}')

def push_repository(repo_path, issue_jira):

    try:

        commit_message = f'[{issue_jira}] tradução de código fonte realizada'

        username = input('Informe seu usuario do BitBucket: ')
        password = getpass('Informe sua senha do BitBucket: ')

        repository = pygit2.Repository(repo_path)

        index = repository.index 
        index.add_all() 
        index.write() 

        author = pygit2.Signature(username, f"{username}@bv.com.br")
        committer = author 

        tree = index.write_tree() 

        commit = repository.create_commit(  
            "HEAD",
            author, 
            committer, 
            commit_message, 
            tree, 
            [repository.head.target], 
        ) 

        credentials = pygit2.UserPass(username, password) 
        remote = repository.remotes["origin"]
        remote.credentials = credentials 
        
        callbacks = pygit2.RemoteCallbacks(credentials=credentials) 
        remote.push(["refs/heads/master"], callbacks=callbacks) 
        
        print("Alterações adicionadas, commitadas e enviadas com sucesso.")
    except Exception as e: 
        print(f"Erro ao adicionar, commitar e enviar alterações: {e}")

def translate_repository(source_path, target_path, source_language, target_language, extension_target_language):
    try:

        for nome_arquivo in os.listdir(source_path):
            caminho_arquivo = os.path.join(source_path, nome_arquivo)

            extensoes_nao_permitidas = ['.bmp', '.jpg', '.idx', '.sql', '.txt', '.exe', '.dll', '.frx', '.xls', '.ico','.gif', '.log','.png', '.properties', '.save', '.gitignore', '.pack','.sample','.bkp', '']
            nome, extensao = os.path.splitext(nome_arquivo)

            if os.path.isfile(caminho_arquivo) and (extensao.lower() not in extensoes_nao_permitidas):
        
                with open(caminho_arquivo, 'r') as file:
                    code = file.read()
                    translated_code = translate_code(code, source_language, target_language)

                    translated_file_path = f'{os.path.join(target_path, nome)}{extension_target_language}'
                    os.makedirs(os.path.dirname(translated_file_path), exist_ok=True)
                    with open(translated_file_path, 'w') as file:
                        file.write(translated_code)

                    print(f'Código traduzido salvo em {translated_file_path}')
            
            elif os.path.isdir(caminho_arquivo):
                translate_repository(caminho_arquivo, os.path.join(target_path, nome), source_language, target_language, extension_target_language)

    except Exception as e:
        print(f'Erro: {e}')


def main():
    parser = argparse.ArgumentParser(description='Traduzir código fonte utilizando a api da OpenAI')
    subparsers = parser.add_subparsers(title='Comandos', dest='command')

    # Subcomando "translate_directory"
    parser_translate = subparsers.add_parser('translate', help='Traduzir o código fonte de todo um diretorio')
    parser_translate.add_argument('source_path', default=None, nargs='?', help='Caminho fisico do repositorio de origem a ser traduzido')
    parser_translate.add_argument('target_path', default=None, nargs='?', help='Caminho fisico do repositorio de destino onde irá repositar o código fonte traduzido')
    parser_translate.add_argument('source_language', default=None, nargs='?', help='Linguagem de programação que está escrita o código fonte de origem')
    parser_translate.add_argument('target_language', default=None, nargs='?', help='Linguagem de programação de destino para tradução')
    parser_translate.add_argument('extension_target_language', default=None, nargs='?', help='Extesão da linguagem de programação de destino para tradução')

    # Subcomando "clone_repository"
    parser_clone = subparsers.add_parser('clone', help='Clonar local um repositorio do BitBucket')
    parser_clone.add_argument('url', default=None, nargs='?', help='Url do repositorio do BitBucket')

    # Subcomando "push_repository"
    parser_clone = subparsers.add_parser('push', help='Enviar alterações para o repositorio remoto do BitBucket')
    parser_clone.add_argument('repo_path', default=None, nargs='?', help='Caminho fisico do repositorio')    
    parser_clone.add_argument('issue_jira', default=None, nargs='?', help='Issue do Jira atrelada ao commit')

    args = parser.parse_args()

    if (args.command == 'translate'):
        #source_path
        if (args.source_path is None):
            args.source_path = input('Informar o caminho fisico do repositorio de origem a ser traduzido (Ex.: C:\\AndersonSilva\\Projetos\\PoC_Codex\\vb-sapt-base-apoio-processamento-tesouraria):')

            if args.source_path == '':
                args.source_path = f'C:\\AndersonSilva\\Projetos\\PoC_Codex\\vb-sapt-base-apoio-processamento-tesouraria'
            
        #target_path
        if (args.target_path is None):
            args.target_path = input('Informar o caminho fisico do repositorio de destino onde irá repositar o código fonte traduzido (Ex.: C:\\AndersonSilva\\Projetos\\PoC_Codex\\arqt-poc-converter-code):')

            if args.target_path == '':
                args.target_path = f'C:\\AndersonSilva\\Projetos\\PoC_Codex\\arqt-poc-converter-code'

        #source_language
        if (args.source_language is None):
            args.source_language = input('Informar a linguagem de programação que está escrita o código fonte de origem (Ex.: Visual Basic 6):')

            if args.source_language == '':
                args.source_language = f'Visual Basic 6'

        #target_language
        if (args.target_language is None):
            args.target_language = input('Informar a linguagem de programação de destino para tradução (Ex.: Java) :')

            if args.target_language == '':
                args.target_language = f'Java'

        #extension_target_language
        if (args.extension_target_language is None):
            args.extension_target_language = input('Informar a extesão da linguagem de programação de destino para tradução (Ex.: .java): ')

            if args.extension_target_language == '':
                args.extension_target_language = f'.java'
        
        translate_repository(args.source_path,
                            args.target_path,
                            args.source_language,
                            args.target_language,
                            args.extension_target_language)
                

    elif (args.command == 'clone'):
        if (args.url is None):
            args.url = input('Informar url do bitbucket (Ex.: https://bitbucket.bvnet.bv/scm/sapt-base/vb-sapt-base-apoio-processamento-tesouraria.git): ')
            
            if args.url == '':
                args.url = 'https://bitbucket.bvnet.bv/scm/sapt-base/vb-sapt-base-apoio-processamento-tesouraria.git'
            
        clone_repository(args.url)

    elif (args.command == 'push'):
        if (args.repo_path is None):
            args.repo_path = input('Informar caminho fisico do repositorio (Ex.: C:\\AndersonSilva\\Projetos\\PoC_Codex\\arqt-poc-converter-code): ')
            
            if args.repo_path == '':
                args.repo_path = f'C:\\AndersonSilva\\Projetos\\PoC_Codex\\arqt-poc-converter-code'
            
        if (args.issue_jira is None):
            args.issue_jira = input('Informar issue do Jira (Ex.: ARC-1451):')
            
            if args.issue_jira == '':
                args.issue_jira = f'ARC-1451'
            

        push_repository(args.repo_path, args.issue_jira)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    
