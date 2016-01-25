import chatroom

class ChatroomManager:

    # Lists for storing active rooms and clients
    active_chatrooms = []
    active_clients = []

    # Last assigned IDs for Clients and rooms
    next_chatroom_id = 0
    next_client_id = 0

    # Global Variable for specifyting chatroom join IDs
    next_chatroom_join_id = 0

    """ Initialize a new ChatroomManager """
    def __init__(self, port_number):
        self.port_number = port_number

    #
    # Functions for Interacting with Id tracking variables
    #

    def get_next_chatroom_id(self):
        return_chatroom_id = self.next_chatroom_id
        self.next_chatroom_id = self.next_chatroom_id + 1
        return return_chatroom_id

    def get_next_chatroom_join_id(self):
        return_chatroom_join_id = self.next_chatroom_join_id
        self.next_chatroom_join_id = self.next_chatroom_join_id + 1
        return return_chatroom_join_id

    def gen_client_id(self):
        return_client_id = self.next_client_id
        self.next_client_id = self.next_client_id + 1
        return return_client_id

    #
    # Functions for interacting with chatrooms
    #

    # Adds a chatroom to the program
    #   Return 0 : Chatroom successfully added
    #   Return 1 : Unsuccessful, chatroom with same name already exists
    def add_chatroom(self, chatroom_name):
        # current_chatroom is used to check if a current chatroom exists with the same name
        current_chatroom = self.get_active_chatroom(chatroom_name)

        if current_chatroom:
            return 1
        else:
            chatroom_id = self.get_next_chatroom_id()
            new_chatroom = chatroom.Chatroom(chatroom_id, self.port_number, chatroom_name)
            self.active_chatrooms.append(new_chatroom)
            return 0

    def remove_chatroom(self, chatroom_id):
        for chatroom in self.active_chatrooms:
            # Remove chatroom from the list of current chatrooms matching
            if chatroom.id == chatroom_id:
                self.active_chatrooms.remove(chatroom)

    def get_active_chatroom(self, chatroom_name):
        for x in self.active_chatrooms:
            if x.name == chatroom_name:
                return x
    #
    # Functions for interacting with clients
    #

    def add_client(self, client_id, client_ip_address, client_port_number, client_name, client_socket):
        if ( self.client_exists(client_id) == False ):
            new_client = chatroom.Client(client_id, client_port_number, client_ip_address, client_name, client_socket)
            self.active_clients.append(new_client)

    # Adds client to chat room
    #   Returns: Chatroom join ID for client
    def add_client_to_chatroom(self, chatroom_name, client):
        room = self.get_active_chatroom(chatroom_name)
        # if room exists we ad the client to it
        if room:
            #if client doesn't exist in chatroom add client to the room
            if ( room.get_join_id(client.id) == -1):
                client_chatroom_join_id = self.get_next_chatroom_join_id()
                room.add_client(client, client_chatroom_join_id)
                return 0
        # if room doesnt exist we add a new room of the specified name
        # on our server and add the client to it
        else:
            self.add_chatroom(chatroom_name)
            self.add_client_to_chatroom(chatroom_name, client)
            return 0

    def remove_client(self, client_id):
        for chatroom in self.active_chatrooms:
            # remove client_from the chatroom it exists
            current_client = self.get_active_client(client_id)
            if current_client:
                self.remove_client_from_chatroom(chatroom.name, current_client)

        for client in self.active_clients:
            # Remove client from list of current clients
            if client.id == client_id:
                self.active_clients.remove(client)

    def remove_client_from_chatroom(self, chatroom_name, client):
        room = self.get_active_chatroom(chatroom_name)
        # if room exists we remove the client from it
        if room:
            room.remove_client(client)
        else:
            return 2

    def get_active_client(self, client_id):
        for client in self.active_clients:
            if client.id == client_id:
                return client

    # checks if a client exists which has the same id as the one passed in
    def client_exists(self, id_in):
        for client in self.active_clients:
            if ( client.id == id_in ):
                return True
        return False

    # Testing methods
    def log_member_data(self):
        print ""
        print "active_chatrooms: "+ (self.active_chatrooms).__repr__()
        print "active_clients: "+ (self.active_clients).__repr__()
        print "next_client_id: %d" % self.next_client_id
        print "next_chatroom_id: %d" % self.next_chatroom_id
        print "next_chatroom_join_id: %d" % self.next_chatroom_join_id
        print ""
