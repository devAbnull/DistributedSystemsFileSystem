import filesystem_servermodel

# initialise file system manager
# test to see if initialization occurred
file_system_manager = filesystem_servermodel.FileSystemManager('FileSystemDir')
assert file_system_manager

# test adding a client
file_system_manager.add_client("dummy_socket_data")
assert len(file_system_manager.active_clients) == 1
assert file_system_manager.active_clients[0].id == 0

file_system_manager.add_client("dummy_socket_data")
assert len(file_system_manager.active_clients) == 2
assert file_system_manager.active_clients[1].id == 1

# test removing a client
client = file_system_manager.get_active_client(0)
file_system_manager.remove_client(client)
assert len(file_system_manager.active_clients) == 1
assert file_system_manager.active_clients[0].id == 1

# test client_exists
assert file_system_manager.client_exists(1) == True
assert file_system_manager.client_exists(0) == False

# test adding events
file_system_manager.add_event("cd directory_1")
assert len(file_system_manager.events) == 1
file_system_manager.add_event("ls")
assert len(file_system_manager.events) == 2
file_system_manager.add_event("cd directory_2")
assert len(file_system_manager.events) == 3
file_system_manager.add_event("up")
assert len(file_system_manager.events) == 4

# test loggin events
file_system_manager.log_events()
