#region - - - - - - - - I M P O R T S - - - - - - - - - -

from socket import socket
from select import select
from o_ini import *

import hashlib

#endregion
#region - - - - - - - - C O N S T A N T S - - - - - - - -

BUFF_SIZE = 1024
PORT = 1356

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
                try:
                    action, username, password = sock.recv(BUFF_SIZE).split('|')
                    path = 'Users\\' + username
                    if action == 'Create':
                        if not Utilities.path_exists(path):
                            Utilities.create_dir(path)
                            config = Utilities.create_file(path + '\\Config.ini')
                            config.set('Password', hashlib.sha256(password).hexdigest())
                            sock.send('Created')
                            print 'User Created. "%s"' % username
                        else:
                            sock.send('Already_Exists')
                    elif action == 'Login':
                        if Utilities.path_exists(path):
                            user = Utilities.open_file(path + '\\Config.ini')
                            if hashlib.sha256(password).hexdigest() == user.read('Password'):
                                sock.send('Successful')
                                print '%s Logged In.' % username
                            else:
                                sock.send('Invalid_Pass')
                        else:
                            sock.send('Invalid_User')
                except:
                    open_client_sockets.remove(sock)
                    sock.close()
#endregion

if __name__ == '__main__':
    main()