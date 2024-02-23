import socket
import os

def send_request(host, port, command, file_name, directory=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    if command == 'GET':
        request = f'{command} {directory}/{file_name}'
    else:  # POST
        file_path = os.path.join(os.getcwd(), file_name)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print("File not found.")
            return
        filesize = os.path.getsize(file_path)
        request = f'{command} {os.path.basename(file_path)};{filesize}'

    client_socket.send(request.encode())

    if command == 'POST':
        with open(file_path, 'rb') as file:
            while True:
                bytes_read = file.read(1024)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        print(f"{file_name} has been sent successfully.")
    elif command == 'GET':
        response = client_socket.recv(1024).decode()
        if response == "File not found":
            print("File not found on the server.")
            return

        filename, filesize = response.split(';')
        filesize = int(filesize)

        with open(filename, 'wb') as file:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                file.write(chunk)
                bytes_received += len(chunk)
        print(f"{filename} has been received successfully.")

    client_socket.close()

def main(type, file_name, directory=None):
    host = 'makeuoftserver.krishadmin.com'  # Replace with the server's IP address
    port = 666                              # The same port as used by the server

    send_request(host, port, type, file_name, directory)