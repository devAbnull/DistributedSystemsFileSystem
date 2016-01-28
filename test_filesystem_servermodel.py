import os
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
client = file_system_manager.get_active_client(1)
file_system_manager.remove_client(client)
assert len(file_system_manager.active_clients) == 1
assert file_system_manager.active_clients[0].id == 0

# test client_exists
assert file_system_manager.client_exists(0) == True
assert file_system_manager.client_exists(1) == False

# test updating clients
client = filesystem_servermodel.Client(0, "other_dummy_socket_data", "FileSystemDir")
assert file_system_manager.get_active_client(0).socket == "dummy_socket_data"
file_system_manager.update_client(client)
assert file_system_manager.get_active_client(0).socket == "other_dummy_socket_data"

file_system_manager.add_client("dummy_socket_data")
client = filesystem_servermodel.Client(2, "other_dummy_socket_data", "FileSystemDir")
assert file_system_manager.get_active_client(2).socket == "dummy_socket_data"
file_system_manager.update_client(client)
assert file_system_manager.get_active_client(2).socket == "other_dummy_socket_data"

# test adding events
file_system_manager.add_event("cd directory_1")
assert len(file_system_manager.events) == 1
file_system_manager.add_event("ls")
assert len(file_system_manager.events) == 2
file_system_manager.add_event("cd directory_2")
assert len(file_system_manager.events) == 3
file_system_manager.add_event("up")
assert len(file_system_manager.events) == 4

# test moving directories
# client id will be 3
file_system_manager.add_client("dummy_socket_data")
client = file_system_manager.get_active_client(3)
assert client.dir_level == 0
assert len(client.dir_path) == 1
assert client.dir_path[0] == "FileSystemDir"
file_system_manager.change_directory("directory_1", 3)
client = file_system_manager.get_active_client(3)
assert client.dir_level == 1
assert len(client.dir_path) == 2
assert client.dir_path[1] == "directory_1"
file_system_manager.change_directory("directory_2", 3)
client = file_system_manager.get_active_client(3)
assert client.dir_level == 2
assert len(client.dir_path) == 3
assert client.dir_path[2] == "directory_2"

# Tesing moving up directory levels
file_system_manager.move_up_directory(3)
client = file_system_manager.get_active_client(3)
assert client.dir_level == 1
assert len(client.dir_path) == 2
assert client.dir_path[1] == "directory_1"
file_system_manager.move_up_directory(3)
client = file_system_manager.get_active_client(3)
assert client.dir_level == 0
assert len(client.dir_path) == 1
assert client.dir_path[0] == "FileSystemDir"
file_system_manager.move_up_directory(3)
client = file_system_manager.get_active_client(3)
assert client.dir_level == 0
assert len(client.dir_path) == 1
assert client.dir_path[0] == "FileSystemDir"

# test locking
client = file_system_manager.get_active_client(3)
client1 = file_system_manager.get_active_client(4)
assert file_system_manager.check_lock(client, "item1") == False
client = file_system_manager.get_active_client(3)
file_system_manager.add_client("dummy_socket_data")
client1 = file_system_manager.get_active_client(4)
file_system_manager.lock_item(client, "item1")
file_system_manager.lock_item(client, "item2")
file_system_manager.lock_item(client1, "item3")
file_system_manager.lock_item(client1, "item4")
assert file_system_manager.check_lock(client, "item1") == True
#file_system_manager.log_locks()
file_system_manager.release_item(client, "item1")
assert file_system_manager.check_lock(client, "item1") == False
#file_system_manager.log_locks()
#file_system_manager.remove_client(client1)
#file_system_manager.auto_release()
#file_system_manager.log_locks()

# Test path resolution
file_system_manager.change_directory("directory_1", 3)
file_system_manager.change_directory("directory_2", 3)
file_system_manager.change_directory("directory_3", 3)
assert file_system_manager.resolve_path(3, "test_item") == "FileSystemDir/directory_1/directory_2/test_item"
file_system_manager.move_up_directory(3)
file_system_manager.move_up_directory(3)
assert file_system_manager.resolve_path(3, "test_item") == "FileSystemDir/test_item"

# Test item_exists function
file_system_manager.write_item(3, "test_file1", "hello this is a test file\n")
assert file_system_manager.item_exists(3, "test_file1") == 0
assert file_system_manager.item_exists(3, "no_file") == -1

# Test reading file
assert file_system_manager.read_item(3, "test_file1") == "hello this is a test file\n"
assert file_system_manager.read_item(3, "directory_1") == "directory_1 is a directory"
assert file_system_manager.read_item(3, "no_file") == "no_file doesn't exist"

# write_item
file_system_manager.write_item(3, "test_file2", "I smell")
assert file_system_manager.read_item(3, "test_file2") == "I smell"
file_system_manager.write_item(3, "directory_1", "I smell")
assert file_system_manager.read_item(3, "directory_1") == "directory_1 is a directory"

#delete file
client = file_system_manager.get_active_client(3)
file_system_manager.lock_item(client, "test_file1")
file_system_manager.delete_file(3, "test_file1") == 1
file_system_manager.delete_file(3, "directory_1") == 2
file_system_manager.delete_file(3, "no_file") == 3
file_system_manager.release_item(client, "test_file1")
file_system_manager.delete_file(3, "test_file1") == 0
assert file_system_manager.read_item(3, "test_file1") == "test_file1 doesn't exist"

# mkdir
assert file_system_manager.make_directory(3, "new_test_directory") == 0
os.rmdir("FileSystemDir/new_test_directory")
assert file_system_manager.make_directory(3, "item1") == 1
assert file_system_manager.make_directory(3, "directory_1") == 2


# test logging events
file_system_manager.log_events()
