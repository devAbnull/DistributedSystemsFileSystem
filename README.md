Repository for Distributed Systems assignment Distributed File System

To run the file_system
  - python file_system_server

To run the Client
  - python filesystem_client

There are a number of commands that can be run on the client that will have suitable responses returned by the server

  - ls - list files and directories in the current directory
  - ls path - list files in specified directory
  - cd path - move to specified directory
  - up - move up one directory

  - read path - read the contents of a file
  - write file_name - writes file from current directory on local machine to the current directory on the remote server

  - mkdir path - make a directory at the following path
  - rmdir path - delete a directory and its contents

  - lock filename - locks the specified file
  - release filename - releases a specified file

  - exit - exit the client

Features the following
  - Distributed transparent file access
  - Directory Service
    - The current position of each client is stored in their object on the server
    - There are functions that resolve paths
  - Caching (in the client)
    - a list of recently viewed items is stored
    - a thread is charged with making sure items are discarded after a set period of time.
  - Locking
    - Items being written to or deleted require a lock
    - Locks are stored in a list on the server
    - A thread has the task of checking that all of the locks have an owner who is active on the server. This process runs every minute.
