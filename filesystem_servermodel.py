import datetime
import threadpool
import time

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
    def change_directory(self, dir_name ):
        self.dir_level = self.dir_level + 1
        self.dir_path.append( dir_name )

    # Move up a directory level
    # Return 0 : Success
    # Return 1 : At top directory level
    def move_up_directory(self):
        if self.dir_level > 0:
            self.dir_path.pop()
            self.dir_level = self.dir_level - 1
            return 0
        else:
            return 1

    #
    # Testing functions
    #
    def log_member_data(self):
        print ""
        print "dir_path: " + (self.dir_path).__repr__()
        print "socket: " + (self.socket).__repr__()
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
    # ( client_id, time, path )
    locked_files = []

    # ThreadPool will contain threads managing the autorelease
    # of locks
    file_system_manager_threadpool = threadpool.ThreadPool(1)

    # Create new File System Manager and initialise the root
    def __init__(self, root_path):
        self.root_path = root_path
        #Add autorelease function to a new thread
        self.file_system_manager_threadpool.add_task(
            self.auto_release
        )

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
            i = i + 1

    def get_active_client(self, client_id):
        for client in self.active_clients:
            if client.id == client_id:
                return client

    def update_client(self, client_in):
        i = 0
        for client in self.active_clients:
            if client.id == client_in.id:
                self.active_clients[i] = client_in
            i = i + 1

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

    def log_events(self):
        print "EID\tTIME\t\t\t\tCOMMAND"
        for event in self.events:
            print "%d\t%s\t%s" % (event[0], event[2], event[1])

    #
    # Functions for moving directories
    #

    def change_directory(self, dir_name, client_id):
        client = self.get_active_client(client_id)
        client.change_directory(dir_name)
        self.update_client(client)
        self.add_event("cd " + dir_name)

    def move_up_directory(self, client_id):
        client = self.get_active_client(client_id)
        client.move_up_directory()
        self.update_client(client)
        self.add_event("up")

    # Passed the name of an item this function returns the path
    # to that item
    def resolve_path(self, client_id, item_name):
        client = self.get_active_client(client_id)
        file_path = ""
        for path_element in client.dir_path:
            file_path = file_path + "%s/" % path_element
        file_path = file_path + item_name
        return file_path

    #
    # Functions for interacting with locking
    #

    # Locks an item if it is not locked
    # Return 0 : Item was locked
    # Return 1 : Item was not locked
    def lock_item(self, client, item_name):
        file_path = self.resolve_path(client.id, item_name)
        if self.check_lock(client, file_path) ==  True:
            return 1
        else:
            lock_timestamp = datetime.datetime.now()
            lock_record = (client.id, lock_timestamp, file_path)
            self.locked_files.append(lock_record)
            self.add_event("lock " + file_path)
            return 0

    # Unlocks an item if it was locked
    def release_item(self, client, item_name):
        file_path = self.resolve_path(client.id, item_name)
        i = 0
        for locked_file in self.locked_files:
            if file_path == locked_file[2]:
                if client.id == locked_file[0]:
                    self.locked_files.pop(i)
                    self.add_event("release " + file_path)
            i = i + 1

    # Checks if an item is locked
    # Return True : Item is locked
    # Returns False : Item is not locked
    def check_lock(self, client, item_name):
        file_path = self.resolve_path(client.id, item_name)
        for locked_file in self.locked_files:
            if locked_file[2] == file_path:
                return True
        return False

    # Traverses the list of locked items and releases locked item if
    # client does not exist
    # Run in a thread initialized in the __init__ function
    def auto_release(self):
        while True:
            # auto release occurs every minute
            time.sleep(60)
            new_locked_file_list = []
            for locked_file in self.locked_files:
                for client in self.active_clients:
                    if locked_file[0] == client.id:
                        new_locked_file_list.append(locked_file)
            self.locked_files = new_locked_file_list

    def log_locks(self):
        print "LID\tTIME\t\t\t\tPATH"
        for locked_file in self.locked_files:
            print "%d\t%s\t%s" % locked_file

    #
    # Functions for interacting with items
    #

    # Returns whether or not a passed file path has a corresponding file
    def item_exists(self, client_id, item_name):
        file_path = self.resolve_path(client_id, item_name)
        try:
            open(file_path)
        except IOError:
            return False
        return True

    # returns the contents of a file as a string#
    # Return 0 : Item read successfully
    # Return 1 : Item doesn't exist
    def read_item(self, client_id, item_name):
        # check if item exists
        item_exists = self.item_exists(client_id, item_name)
        if item_exists == False:
            return "%s doesn't exist"
        else:
            # read item
            file_path = self.resolve_path(client_id, item_name)
            file = open(file_path, 'r')
            file_contents = file.read()
            # add event
            self.add_event("read " + file_path)
            return file_contents

    # Writes a passed string to a file with a passed name
    # Return 0 : Write successfull
    # Return 1 : Write unsuccessfull, File locked
    def write_item(self, client_id, item_name, file_contents):
        # lock_item
        client = self.get_active_client(client_id)
        lock_res = self.lock_item(client, item_name)
        if lock_res == 1:
            return 1
        # write to it
        file_path = self.resolve_path(client_id, item_name)
        file = open(file_path, 'w+')
        file.truncate()
        file.write(file_contents)
        # add write event
        self.add_event("write " + file_path)
        # release it
        self.release_item(client, item_name)
        return 0

    # disconnect client from server
    def exit(connection, client_id):
        # get client
        # remove client from active clients
        # disconnect socket
        # add event
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
