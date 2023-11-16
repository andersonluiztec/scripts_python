import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git
from getpass import getpass
from tqdm import tqdm

def download_repository(owner, repo): 
    clone_url = f'https://bitbucket.bvnet.bv/scm/sapt-base/vb-sapt-base-apoio-processamento-tesouraria.git'
    local_path = f'./{repo}'

    username = input('Informe seu usuario do BitBucket: ')
    password = getpass('Informe sua senha do BitBucket: ')

    try:
      git.Repo.clone_from(clone_url, local_path, progress=tqdm, username=username, password=password) 

      print(f'Repositório {owner}/{repo} clonado com sucesso.')
    except Exception as e: 
      print(f'Erro ao clonar o repositório {owner}/{repo}: {e}')


# Exemplo de uso 
owner = 'sapt-base'
repo = 'vb-sapt-base-apoio-processamento-tesouraria'

print(owner)
print(repo)
download_repository(owner, repo)
