import os
import shutil
import datetime

# Diretório de origem e destino
origem = '/home/valcann/backupsFrom'
destino = '/home/valcann/backupsTo'

# Diretório de logs
log_dir = '/home/valcann/'

# Data limite para exclusão de arquivos (3 dias atrás)
limite = datetime.datetime.now() - datetime.timedelta(days=3)

# Listar todos os arquivos no diretório de origem e seus detalhes
with open(os.path.join(log_dir, 'backupsFrom.log'), 'w') as log_file:
    for root, _, files in os.walk(origem):
        for file in files:
            file_path = os.path.join(root, file)
            file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            file_modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            file_size = os.path.getsize(file_path)

            # Escrever os detalhes no arquivo de log
            log_file.write(f'Nome: {file}\n')
            log_file.write(f'Tamanho: {file_size} bytes\n')
            log_file.write(f'Data de Criação: {file_creation_time}\n')
            log_file.write(f'Data da Última Modificação: {file_modification_time}\n')
            log_file.write('\n')

            # Copiar arquivos mais recentes para o diretório de destino
            if file_creation_time >= limite:
                shutil.copy2(file_path, os.path.join(destino, file))

# Remover arquivos com data de criação superior a 3 dias
for root, _, files in os.walk(origem):
    for file in files:
        file_path = os.path.join(root, file)
        file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

        if file_creation_time < limite:
            os.remove(file_path)

# Registrar as ações no arquivo de log do diretório de destino
with open(os.path.join(log_dir, 'backupsTo.log'), 'w') as log_file:
    log_file.write(f'Arquivos copiados para {destino} em {datetime.datetime.now()}\n')

print('Script concluído!')
