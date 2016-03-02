#region - - - - - - - - I M P O R T S - - - - - - - - - -

from socket import socket
from select import select
from o_ini import *

import hashlib

#endregion
#region - - - - - - - - C O N S T A N T S - - - - - - - -

BUFF_SIZE = 1024
PORT = 1356
CODES = {'USER_CREATED': 0, 'SUCCESSFUL': 1, 'ALREADY_EXISTS': 2, 'INVALID_USER': 3, 'INVALID_PASSWORD': 4}
HANDLE_CODES = {v: k for k, v in CODES.items()}

#endregion

#region - - - - - - - - V A R I A B L E S - - - - - - - -

Logged_Clients = []

#endregion

#region - - - - - - - - M E T H O D S - - - - - - - - - -


def create_server():
    server_socket = socket()
    server_socket.bind(('', PORT))
    server_socket.listen(3)
    print 'Server Created.'
    return server_socket


def initialize():
    if not Utilities.path_exists('Users\\'):
        Utilities.create_dir('Users\\')
        print 'Created Directory \'Users\''

def hash(text):
    return hashlib.sha256(text).hexdigest()


def sign_up(username, password, path):
    if not Utilities.path_exists(path):
        Utilities.create_dir(path)
        config = Utilities.create_o_file(path + '\\Config.ini')
        config.set('Password', hash(password))
        return CODES['USER_CREATED']
    else:
        return CODES['ALREADY_EXISTS']


def login(username, password, path):
    if Utilities.path_exists(path):
        user = Utilities.open_o_file(path + '\\Config.ini')
        if hash(password) == user.read('Password'):
            return CODES['SUCCESSFUL']
        else:
            return CODES['INVALID_PASSWORD']
    else:
        return CODES['INVALID_USER']


def isLogged(sock):
    return sock in Logged_Clients

def handle_disconnection(sock):
    if isLogged(sock):
        Logged_Clients.remove(sock)
    sock.close()

#endregion
#region - - - - - - - - M A I N - - - - - - - - - - - - -
def main():
    initialize()
    server_socket = create_server()
    open_client_sockets = []
    while True:
        rlist, wlist, xlist = select([server_socket] + open_client_sockets, [], [])
        for sock in rlist:
            if sock is server_socket:
                (client_socket, client_address) = server_socket.accept()
                open_client_sockets.append(client_socket)
                print 'Client Connected. "%s"' % client_address[0]
            else:
                data = sock.recv(BUFF_SIZE)
                if not data:
                    open_client_sockets.remove(sock)
                    handle_disconnection(sock)
                if isLogged(sock):
                    print data
                else:
                    try:
                        action, username, password = data.split('|')
                        path = 'Users\\' + username
                        if action == 'CREATE':
                            code = sign_up(username, password, path)
                        elif action == 'LOGIN':
                            code = login(username, password, path)
                            if code == CODES['SUCCESSFUL']:
                                Logged_Clients.append(sock)
                        print username, HANDLE_CODES[code]
                        sock.send(HANDLE_CODES[code])
                    except:
                        handle_disconnection(sock)
#endregion

if __name__ == '__main__':
    main()