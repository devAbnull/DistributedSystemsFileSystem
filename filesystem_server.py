import socket
import threadpool
import os
import filesystem_servermodel

# global threadpool for server
server_thread_pool = threadpool.ThreadPool(500)

port_number = 8080

ip_address = socket.gethostbyname(socket.gethostname())

file_system_manager = filesystem_servermodel.FileSystemManager('FileSystemDir')

def create_server_socket():
    # create socket  and initialise to localhost:8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', port_number)
    print "starting up on %s port %s" % server_address
    # bind socket to server address and wait for incoming connections4
    sock.bind(server_address)
    sock.listen(1)
    
    while True:
        # sock.accept returns a 2 element tuple
        connection, client_address = sock.accept()
        #print "Connection from %s, %s\n" % connection, client_address
        # Hand the client interaction off to a seperate thread
        server_thread_pool.add_task(
            start_client_interaction,
            connection,
            client_address
        )


def start_client_interaction(connection, client_address):
    try:
        #A client id is generated, that is associated with this client
        curr_client_id = file_system_manager.add_client(connection)
        while True:
            data = connection.recv(1024)
            split_data = seperate_input_data(data)
            # Respond to the appropriate message
            if data == "KILL_SERVICE\n":
                kill_service(connection)
            else:
                error_response(connection, 1)
    except:
        error_response(connection, 0)
        connection.close()

def kill_service(connection):
    # Kill service
    response = "Killing Service"
    connection.sendall("%s" % response)
    connection.close()
    os._exit(0)

def error_response(connection, error_code):
    if error_code == 0:
        response = "server error"
    if error_code == 1:
        response = "unrecognised command"
    connection.sendall(response)

#Function to split reveived data strings into its component elements
def seperate_input_data(input_data):
    seperated_data = []
    input_data_split = input_data.split(' ')
    return seperated_data

if __name__ == '__main__':
    create_server_socket()
    # wait for threads to complete
    server_thread_pool.wait_completion()
