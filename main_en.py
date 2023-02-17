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
    print('Could not connect to FTP server. Check your login credentials.')
    input()
    exit()


print('Available commands:')
print('ls - display a list of files and folders in the current directory')
print('cd <path> - change the current directory to the specified path')
print('rm <file> or del <file> - delete the specified file')
print('touch <file> or create <file> - create a new file with the specified name')
print('rmf <file> - delete the specified file without reporting an error if it does not exist')
print('exit - exit the program\n')

current_directory = '/'
while True:
    command = input('Enter command: ')
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
                print(f'Could not change to {new_directory}: {e}')
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
            print(f'File not found: {filename}')
    elif command.startswith('rmf '):
        filename = command[4:]
        try:
            ftp.delete(filename)
        except:
            pass
    elif command == 'exit':
        break
    else:
        print('Unknown command')

ftp.quit()
