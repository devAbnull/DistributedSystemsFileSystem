class Chatroom:

    """initialise a new chatroom object"""
    def __init__(self, id, port_number, name):
        self.active_clients = []
        self.id = id
        self.port_number = port_number
        self.name = name

    # Add tuple of values representing a client
    # return 0 - Successfully added to the room
    # return 1 - Unsucessful ( Same client id exists in chat)
    # return 2 - Unsuccessful (Same join id exists in chat)
    def add_client(self, client, chatroom_join_id):
        for x in self.active_clients:
            # If same id exists in chat
            if x[0].id == client.id:
                return 1
            #If same handle exists in chat
            elif x[1] == chatroom_join_id:
                return 2

        self.active_clients.append([client, chatroom_join_id])
        return 0

    # Removes the passed client object from the chatroom should one be an active member
    def remove_client(self, client):
        for x in self.active_clients:
            # if the the passed client objects id matches the one found in the active_clients
            # that entry is removed from thye active clients array
            if x[0].id == client.id:
                self.active_clients.remove(x)

    # Gets the join id for a corresponding client id
    # return -1 -  no value found
    # return positive integer - value found
    def get_join_id(self, client_id_in):
        for client_tuple in self.active_clients:
            if (client_tuple[0].id == client_id_in):
                return client_tuple[1]
        return -1


class Client:
    """Initialize a new ChatClient"""
    def __init__(self, id, port_number, ip_address, name, socket):
        self.id = id
        self.port_number = port_number
        self.ip_address = ip_address
        self.name = name
        self.socket = socket
