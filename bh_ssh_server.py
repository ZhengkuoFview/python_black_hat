import socket
import paramiko
import threading
import sys

host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'justin') and (password == 'lovesthepython'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, port))
    sock.listen(100)
    print('[+] Listening for connection ...')
    client, addr = sock.accept()
except Exception as e:
    print('[-] Listen failed: ' + str(e))
    sys.exit(1)

print('[+] Got a connection!')

try:
    bh_session = paramiko.Transport(client)
    bh_session.add_server_key(host_key)
    server = Server()
    try:
        bh_session.start_server(server=server)
    except paramiko.SSHException as x:
        print('[-] SSH negotiation failed.')

    chan = bh_session.accept(20)
    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send(b'Welcome to bh_ssh')
    while True:
        try:
            command = input('Enter command: ').strip('\n')
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024) + b'\n')
            else:
                chan.send(b'exit')
                print('exiting')
                bh_session.close()
                break
        except KeyboardInterrupt as e:
            bh_session.close()
            print('[-] Caught exception: ' + str(e))

except Exception as e:
    print('[-] Caught exception: ' + str(e))
finally:
    bh_session.close()
    sys.exit(1)
