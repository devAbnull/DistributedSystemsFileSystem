import datetime

class Client:
    # Initialise a new File System client
    def __init__(self, id, socket, path_to_root):
        self.id = id
        self.socket = socket
        self.dir_level = 0
        # Path to root is the path to the root of the file_system
        self.dir_path = [path_to_root]


        #
        # Functions for working with directories
        #

        # Move into the passed directory
        def move_into_dir( dir_name ):
            self.dir_level = self.dir_level + 1
            self.dir_path.push( dir_name )

        # Move up a directory level
        # Return 0 : Success
        # Return 1 : At top directory level
        def move_up_dir():
            if dir_level > 0:
                self.dir_path.pop()
                return 0
            else:
                return 1

        #
        # Testing functions
        #
        def log_member_data(self):
            print ""
            print "dir_path: "+ (self.dir_path).__repr__()
            print "id: %d" % self.id
            print "dir_level: %d" % self.dir_level
            print ""


class FileSystemManager:

    # List for storing active clients
    active_clients = []

    # Next ID to be assigned to new client and events
    next_client_id = 0
    next_event_id = 0

    # List of events and IDs
    # ( event_id , command, time )
    events = []

    # List of the paths of currently locked files
    # ( path, client_id, time )
    locked_files = []

    # Create new File System Manager and initialise the root
    def __init__(self, root_path):
        self.root_path = root_path

    # Generate a client ID and update next_client_id
    def gen_client_id(self):
        return_client_id = self.next_client_id
        self.next_client_id = self.next_client_id + 1
        return return_client_id

    # Generate a client ID and update next_event_id
    def gen_event_id(self):
        return_event_id = self.next_event_id
        self.next_event_id = self.next_event_id + 1
        return return_event_id

    #
    # Functions for interacting with clients
    #

    def add_client(self, connection):
        new_client_id = self.gen_client_id();
        new_client = Client(new_client_id, connection, self.root_path)
        self.active_clients.append(new_client)

    def remove_client(self, client_in):
        i = 0
        for client in self.active_clients:
            if client.id == client_in.id:
                self.active_clients.pop(i)

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

    #
    # Functions for interacting with events
    #

    def add_event(self, command):
        new_event_id = self.gen_event_id()
        event_timestamp = datetime.datetime.now()
        new_event_record = (new_event_id, command, event_timestamp)
        self.events.append(new_event_record)
        return 0

    def log_events(self):
        print "EID\tTIME\t\t\t\tCOMMAND"
        for event in self.events:
            print "%d\t%s\t%s" % (event[0], event[2], event[1])
        return 0

    #
    # Functions for interacting with locking
    #

    def lock_item(client, item_name):
        return 0

    def release_item(item_name):
        return 0

    def check_lock(item_name):
        return 0

    # Traverses the list of locked items and releases locked item if
    # client does not exist
    def auto_release(self):
        return 0

    def log_locks(self):
        return 0

    #
    # Testing functions
    #
    def log_member_data(self):
        print ""
        print "active_clients: "+ (self.active_clients).__repr__()
        print "events: "+ (self.events).__repr__()
        print "locked_files: "+ (self.locked_files).__repr__()
        print "next_client_id: %d" % self.next_client_id
        print "next_event_id: %d" % self.next_event_id
        print ""
