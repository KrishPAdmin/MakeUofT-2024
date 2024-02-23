import socket
import os
import shutil
from datetime import datetime

def receive_file(client_socket, file_path, filesize, archive=False, archive_dir=None):
    with open(file_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < filesize:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            file.write(chunk)
            bytes_received += len(chunk)

    if archive and archive_dir:
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        # Generate timestamped filename for the archive
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{timestamp}{os.path.splitext(file_path)[1]}"
        archive_file_path = os.path.join(archive_dir, archive_file_name)

        shutil.copy(file_path, archive_file_path)
        print(f"File {file_path} received and archived as {archive_file_name}.")
    else:
        print(f"File {file_path} received.")

def send_file(client_socket, file_path):
    filesize = os.path.getsize(file_path)
    client_socket.send(f"{os.path.basename(file_path)};{filesize}".encode())

    with open(file_path, 'rb') as file:
        while True:
            bytes_read = file.read(1024)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    print(f"File {file_path} sent.")

def main():
    host = 'makeuoftserver.krishadmin.com'
    port = 666
    archive_dir = '/home/krishkillr-admin/server/archive'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")

        request = client_socket.recv(1024).decode()
        command, file_info = request.split(' ', 1)

        if command == 'POST':
            file_name, filesize = file_info.split(';')
            file_path = f'/home/krishkillr-admin/server/files/{file_name}'
            receive_file(client_socket, file_path, int(filesize), archive=True, archive_dir=archive_dir)
        elif command == 'GET':
            directory, file_name = file_info.split('/', 1)
            file_path = f'/home/krishkillr-admin/server/{directory}/{file_name}'
            if os.path.exists(file_path) and os.path.isfile(file_path):
                send_file(client_socket, file_path)
            else:
                client_socket.send("File not found".encode())
        else:
            client_socket.send("Invalid command".encode())

        client_socket.close()

if __name__ == "__main__":
    main()
