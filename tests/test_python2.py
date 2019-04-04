import sys
import pytest
from titanium_silver.docker_client import Docker_Client
from threading import Thread, Event
import time
import os
import pdb

@pytest.mark.skipif(sys.platform == 'darwin', reason="does not run on osx yet")
def test_basic():
	dcli = Docker_Client()
	# print(os.getcwd())
	thread_list = list()
	for i in range(1):
		print("Spawn container: %d"%i)
		thread_list.append(dcli.spawn_process(name='myapp', num=i, params='%d 5000'%i, path=os.getcwd()+'/tests/SC', lang='Python2Container'))
	
	for i, t in enumerate(thread_list):
		assert('Hello container: %d\n'%i == t.result_queue.get().decode('utf-8'))
