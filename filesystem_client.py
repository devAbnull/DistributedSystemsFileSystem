import socket
import sys
import threadpool

from random import randint

# this is a multithreaded client program that was used to test
# the server code

client_thread_pool = threadpool.ThreadPool(20)

ip_address = socket.gethostbyname(socket.gethostname())

port_num = 8080

# A list containing a series of potential server messages for testing
messages = [
    "HELO\n",
    "HELO tesasdfasdft \n",
    "KILL_SERVICE\n",
    "A message for testing\n",
    "Another message for testing\n",
]

def connect_to_server_userin():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_address = ('46.101.47.238', port_num)
    server_address = ('127.0.0.1', port_num)
    print "connecting to %s on port %s\n" % server_address
    sock.connect(server_address)

    client_thread_pool.add_task(
        get_server_response,
        sock
    )

    while True:
        user_in = raw_input()
        message = generate_message( user_in )
        print message
        sock.send( message )

    sock.close()

def get_server_response(socket):
    while True:
        data = socket.recv( 1024 )
        if (data != None):
            print data

def generate_message(input):
    split_input = input.split(' ')
    if (split_input[0] == "join"):
        response = "JOIN_CHATROOM: %s\n" % str(split_input[1])
        response += "CLIENT_IP: %s\n" % str(ip_address)
        response += "PORT: %s\n" % str(0)
        response += "CLIENT_NAME: %s\n" % str(split_input[2])
    if (split_input[0] == "leave"):
        response = "LEAVE_CHATROOM: %s\n" % str(split_input[1])
        response += "JOIN_ID: %s\n" % str(split_input[2])
        response += "CLIENT_NAME: %s\n" % str(split_input[3])
    if (split_input[0] == "disconnect"):
        response = "DISCONNECT: %s\n" % str(ip_address)
        response += "PORT: %s\n" % str(0)
        response += "CLIENT_NAME: %s\n" % str(split_input[1])
    if (split_input[0] == "chat"):
        response = "CHAT: %s\n" % str(split_input[1])
        response += "JOIN_ID: %s\n" % str(split_input[2])
        response += "CLIENT_NAME: %s\n" % str(split_input[3])
        response += "MESSAGE: %s\n" % str(split_input[4])
    return response

if __name__ == '__main__':
    # Main line for program
    # Create 20 tasks that send messages to the server
    connect_to_server_userin()
    # wait for threads to complete before finishing program
    client_thread_pool.wait_completion()
