import  pygit2 
from getpass import getpass
from tqdm import tqdm

def transfer_progress(stats, progress):
   if progress.total_objects > 0:
      porcentage = int((progress.indexed_objects / progress.total_objects) * 100)
      stats.n = porcentage
      stats.refresh()

def download_repository(owner, repo): 
    clone_url = f'https://bitbucket.bvnet.bv/scm/sapt-base/vb-sapt-base-apoio-processamento-tesouraria.git'
    local_path = f'./{repo}'

    username = input('Informe seu usuario do BitBucket: ')
    password = getpass('Informe sua senha do BitBucket: ')

    credentials = pygit2.UserPass(username,password)

    try:
      callbacks = pygit2.RemoteCallbacks(credentials=credentials, transfer_progress=transfer_progress)

      with tqdm(total=100, desc='Clonando repositorio', unit='%') as progress: 
        repository = pygit2.clone_repository(clone_url, local_path, callbacks=callbacks) 
        remote = repository.remotes['origin']
        remote.fetch(callbacks=callbacks)
        progress.update(100)

      print(f'Repositório {owner}/{repo} clonado com sucesso.')
    except Exception as e: 
      print(f'Erro ao clonar o repositório {owner}/{repo}: {e}')


# Exemplo de uso 
owner = 'sapt-base'
repo = 'vb-sapt-base-apoio-processamento-tesouraria'

print(owner)
print(repo)
download_repository(owner, repo)
