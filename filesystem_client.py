import socket
import threadpool

# this is a multithreaded client program that was used to test
# the server code

client_thread_pool = threadpool.ThreadPool(3)

ip_address = socket.gethostbyname(socket.gethostname())

port_num = 8080

def connect_to_server_userin():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', port_num)
    print "connecting to %s on port %s\n" % server_address
    sock.connect(server_address)

    client_thread_pool.add_task(
        get_server_response,
        sock
    )

    while True:
        user_in = raw_input()
        message = generate_message(user_in)
        sock.send( message )

    sock.close()

def get_server_response(socket):
    while True:
        data = socket.recv( 1024 )
        if (data != None):
            print data

def generate_message(input):
    split_input = input.split(" ")
    if split_input[0] == "write":
        if len(split_input) != 2:
            print "unrecognised command"
            return ""
        try:
            file = open(split_input[1])
            file_contents = file.read()
            return "%s////%s////%s" % (split_input[0], split_input[1], file_contents)
        except IOError:
            print "no such file in source directory"
            return ""
    else:
        return '////'.join(split_input)

if __name__ == '__main__':
    # Main line for program
    # Create 20 tasks that send messages to the server
    connect_to_server_userin()
    # wait for threads to complete before finishing program
    client_thread_pool.wait_completion()
