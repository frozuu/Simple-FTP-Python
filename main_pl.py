import ftplib
import os


HOST = 'HOST'
USERNAME = 'LOGIN/USERNAME'
PASSWORD = 'PASSWORD'
PORT = 21

try:
    ftp = ftplib.FTP()
    ftp.connect(HOST, PORT)
    ftp.login(USERNAME, PASSWORD)
except:
    print('Nie można połączyć się z serwerem FTP. Sprawdź swoje dane logowania.')
    input()
    exit()


print('Dostępne polecenia:')
print('ls - wyświetla listę plików i folderów w bieżącym katalogu')
print('cd <ścieżka> - zmienia bieżący katalog na podaną ścieżkę')
print('rm <plik> lub del <plik> - usuwa podany plik')
print('touch <plik> lub create <plik> - tworzy nowy plik o podanej nazwie')
print('rmf <plik> - usuwa podany plik bez raportowania błędu, jeśli nie istnieje')
print('exit - zamyka program\n')

current_directory = '/'
while True:
    command = input('Wprowadź polecenie: ')
    if command == 'ls':
        files = ftp.nlst()
        for file in files:
            print(file)
    elif command.startswith('cd '):
        path = command[3:]
        if path == '':
            current_directory = '/'
        elif path == '..' or path == 'back':
            current_directory = os.path.dirname(current_directory.rstrip('/')) + '/'
        else:
            new_directory = os.path.join(current_directory, path)
            try:
                ftp.cwd(new_directory)
                current_directory = new_directory + '/'
            except ftplib.error_perm as e:
                print(f'Nie można zmienić na {new_directory}: {e}')
    elif command.startswith('rm '):
        filename = command[3:]
        ftp.delete(filename)
    elif command.startswith('del '):
        filename = command[4:]
        ftp.delete(filename)
    elif command.startswith('touch ') or command.startswith('create '):
        filename = command.split(' ')[-1]
        try:
            ftp.storlines('STOR ' + filename, open(filename, 'rb'))
        except FileNotFoundError:
            print(f'Nie znaleziono pliku: {filename}')
    elif command.startswith('rmf '):
        filename = command[4:]
        try:
            ftp.delete(filename)
        except:
            pass
    elif command == 'exit':
        break
    else:
        print('Nieznane polecenie')

ftp.quit()
