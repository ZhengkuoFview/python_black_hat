import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on {ip}:{port}".format(ip=bind_ip, port=bind_port))

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("[*] Received: {request}".format(request=request))
    client_socket.send(b'ACK!')
    client_socket.close()

while True:
    client, addr = server.accept()
    print(
        "[*] Accepted connection from: {ip}:{port}".format(
            ip=addr[0],
            port=addr[1]
        )
    )
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
