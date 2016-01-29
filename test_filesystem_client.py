import filesystem_client

filesystem_client.add_to_cache("/helo/there1/", "someconteasdfasdf")
filesystem_client.add_to_cache("/helo/there2/", "someconteasdfasdf")
filesystem_client.add_to_cache("/helo/there3/", "someconteasdfasdf")
filesystem_client.add_to_cache("/helo/there4/", "somecontedfsasdfasdf")
filesystem_client.add_to_cache("/helo/there5/", "someconteasdfasdf")
assert len(filesystem_client.cache_queue) == 5
filesystem_client.add_to_cache("/helo/there6/", "someconteasdfasdf")
assert len(filesystem_client.cache_queue) == 5
filesystem_client.add_to_cache("/helo/there7/", "someconteasdfasdf")
assert len(filesystem_client.cache_queue) == 5
assert filesystem_client.search_cache("/helo/there4/") == "somecontedfsasdfasdf"
assert filesystem_client.search_cache("/helo/there41/") == None
#filesystem_client.auto_update_cache()
#filesystem_client.add_to_cache("/helo/there8/", "someconteasdfasdf")
#filesystem_client.auto_update_cache()
#filesystem_client.auto_update_cache()
#filesystem_client.auto_update_cache()
#filesystem_client.log_cache()
#filesystem_client.add_to_cache("/helo/there9/", "someconteasdfasdf")
#filesystem_client.log_cache()
#filesystem_client.auto_update_cache()
#filesystem_client.auto_update_cache()
#filesystem_client.log_cache()
