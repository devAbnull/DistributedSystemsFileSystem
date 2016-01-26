import sys
import socket
import threadpool
import os
import re
import chatroom_manager

# global threadpool for server
server_thread_pool = threadpool.ThreadPool(500)

port_number = 8080

ip_address = socket.gethostbyname(socket.gethostname())

current_chatroom_manager = chatroom_manager.ChatroomManager(port_number)

def create_server_socket():
    # create socket  and initialise to localhost:8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', port_number)

    print "starting up on %s port %s\n" % server_address

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
        #It is to be used to check that one thread does not spawn multiple
        #clients.
        curr_client_id = current_chatroom_manager.gen_client_id()

        while True:

            data = connection.recv(1024)
            if (data != None):
                print "received message:\n%s" % data

            # Respond to the appropriate message
            if data == "KILL_SERVICE\n":
                kill_service(connection)
            elif data[0:4] == "HELO" and data[-1] == '\n':
                helo_response(connection, data)
            else:
                split_data = seperate_input_data(data)
                #Check for Disconnect Command
                if split_data[0] == "JOIN_CHATROOM":
                    join_chatroom(connection, client_address, curr_client_id, split_data)
                elif split_data[0] == "LEAVE_CHATROOM":
                    leave_chatroom(connection, curr_client_id, split_data)
                elif split_data[0] == "DISCONNECT":
                    disconnect(connection, curr_client_id, split_data)
                elif split_data[0] == "CHAT":
                    send_message(connection, curr_client_id, split_data)
    except:
        error_response(connection, 0)
        connection.close()

def kill_service(connection):
    # Kill service
    response = "Killing Service\n"
    connection.sendall("%s" % response)
    connection.close()
    os._exit(0)

def helo_response(connection, data):
    # Respond to HELO message
    # Construct the appropriate response
    response = data
    response += "IP:[" + ip_address + "]\n"
    response += "Port:[" + str(port_number) +"]\n"
    response += "StudentID:[a09577ec2fe97c36c854f4010526ed2f81b4747edea7d4247ded8c32f76e93f2]\n"
    connection.sendall("%s" % response)

def join_chatroom(connection, client_address, client_id, split_data):
    #Create client and add to chatroom
    current_chatroom_manager.add_client( client_id, client_address, 0, split_data[7], connection )
    err_val = current_chatroom_manager.add_client_to_chatroom( split_data[1], current_chatroom_manager.get_active_client( client_id ) )

    # user already exists in the room successfully added
    if ( err_val == 1 ):
        error_response(connection, err_val)

    # Successfully added
    else:
        #Create and send response
        chatroom_name = split_data[1]
        room_ref = current_chatroom_manager.get_active_chatroom(chatroom_name).id
        join_id = current_chatroom_manager.get_active_chatroom(chatroom_name).get_join_id(client_id)
        response = "JOINED_CHATROOM: %s\n" % str(chatroom_name)
        response += "SERVER_IP: %s\n" % str(ip_address)
        response += "PORT: %s\n" % str(port_number)
        response += "ROOM_REF: %s\n" % str(room_ref)
        response += "JOIN_ID: %s\n" % str(join_id)
        connection.sendall("%s" % response)

def leave_chatroom(connection, client_id, split_data):
    # Remove client from chatroom
    join_id = current_chatroom_manager.get_active_chatroom(split_data[1]).get_join_id(client_id)
    err_val = current_chatroom_manager.remove_client_from_chatroom(split_data[1], current_chatroom_manager.get_active_client( client_id ))

    # if chatroom doesn't exist throw error
    if ( err_val == 2 ):
        error_response(connection, err_val)

    # Successfully added
    else:
        #Create and send response
        chatroom_name = split_data[1]
        response = "LEFT_CHATROOM: %s\n" % str(chatroom_name)
        response += "JOIN_ID: %s\n" % str(join_id)
        connection.sendall("%s" % response)

# Disconnects a user from the chatroom
def disconnect(connection, client_id, split_data):
    current_chatroom_manager.remove_client(client_id)
    print "\nClient %s Disconnected\n" % str(client_id)
    connection.close()

# Sends a message to a chat which a client is a member of
def send_message(connection, curr_client_id, split_data):
    # Get room sing room_ref
    current_room = current_chatroom_manager.get_active_chatroom(split_data[1]);
    #Generate message string
    #message = generate_message(split_data[1], current_chatroom_manager.get_active_client(curr_client_id).name, split_data[7] )
    message = "CHAT: %s\n" % str(split_data[1])
    message += "CLIENT_NAME: %s\n" % str( current_chatroom_manager.get_active_client(curr_client_id).name )
    message += "MESSAGE: %s\n" % str(split_data[7])

    # Get socket for each client and send the message
    for client in current_room.active_clients:
        client[0].socket.sendall("%s" % message)
        #connection = client[0].socket
        #connection.sendall("%s", message)

# Function for providing error responses for various error cases
def error_response(connection, err_val):
    response = "ERROR_CODE: %s\n" % str(err_val)

    if( err_val == 0 ):
        response += "ERROR_DESCRPTION: %s\n" % "Server error"
    elif ( err_val == 1 ):
        response += "ERROR_DESCRPTION: %s\n" % "You are already in that chat room"
    elif ( err_val == 2 ):
        response += "ERROR_DESCRPTION: %s\n" % "That room doesn't exist"

    connection.sendall("%s" % response)

#Function to split reveived data strings into its component elements
def seperate_input_data(input_data):
    seperated_data = []

    input_data_split = input_data.split('\n')

    for i in input_data_split:
        i = i.split(": ")
        #seperated_data.append(i)
        for j in i:
            j = j.split(':')
            for k in j:
                seperated_data.append(k)

    return seperated_data

if __name__ == '__main__':
    create_server_socket()
    # wait for threads to complete
    server_thread_pool.wait_completion()
