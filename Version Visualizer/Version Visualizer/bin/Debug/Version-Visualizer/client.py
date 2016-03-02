#region - - - - - - - - I M P O R T S - - - - - - - - - -

from socket import socket
from o_ini import *
import os
from Project import *

#endregion
#region - - - - - - - - C O N S T A N T S - - - - - - - -
GUI_IP = '127.0.0.1'
GUI_PORT = 1356
BUFF_SIZE = 1024
VERSION_PATH = os.getenv('APPDATA') + r'\\.VersionVisualizer'
#endregion
#region - - - - - - - - M E T H O D S - - - - - - - - - -
def connect_to_server(IP, PORT):
    s = socket()
    s.connect((IP, PORT))
    return s

def create_server():
    s = socket()
    s.bind((GUI_IP, GUI_PORT))
    s.listen(1)
    return s

def isInit():
    return Utilities.path_exists(VERSION_PATH)

def initialize():
    Utilities.create_dir(VERSION_PATH)
    #Utilities.create_dir(os.getenv('APPDATA') + r'\\.VersionVisualizer\Users')

def handle_data(data):
    data = data.split('|')
    command = data[0]
    arguments = data[1:]
    if command == 'GetProjectList':
        return '?'.join(get_project_list())
    elif command == 'CreateProject':
        name = arguments[0]
        files_path = arguments[1].split('?')
        try:
            create_project(VERSION_PATH, name, files_path)
            return 'SUCCESS'
        except:
            return 'FAILED'

def get_project_list():
    return [f for f in os.listdir(VERSION_PATH) if os.path.isdir(os.path.join(VERSION_PATH, f))]

#endregion
#region - - - - - - - - M A I N - - - - - - - - - - - - -
def main():
    if not isInit():
        initialize()
        print 'Initialization complete.'
    server_socket = create_server()
    print 'Server Established.'
    client, client_address = server_socket.accept()
    print 'Client Connected!'
    while True:
        data = client.recv(BUFF_SIZE)
        output = handle_data(data)
        client.send(output + '<EOF>')

#endregion
if __name__ == '__main__':
    main()
