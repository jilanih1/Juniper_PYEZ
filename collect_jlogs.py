#!/usr/bin/env python

from __future__ import print_function
import getpass
import sys
import json
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell

if sys.version_info[:2] <= (2, 7):
	input = raw_input

#hostname = input('Device hostname: ')
#username = input('Device username: ')
password = getpass.getpass('Device password: ')
hostname = '192.168.1.48'
username = 'admin'

dev = Device(host=hostname, user=username, passwd=password)

try:
	dev.open()
except ConnectError as err:
	print('Cannot connect to device: {0}'.format(err))
	sys.exit(1)
except Exception as err:
	print(err)
	sys.exit(1)

jshell = StartShell(dev)
jshell.open()
jshell.run('cli -c "request support information | save /var/tmp/PYEZ_RSI.txt"')
jshell.run('tar -zcvf /var/tmp/PYEZ_varlog.tar.gz /var/log/*')
#flist = json.dumps(jshell.run('cli -c "file list /var/tmp | grep PYEZ"'))

flist = jshell.run('cli -c "file list /var/tmp | grep PYEZ" ')
for line in flist:
	print(line)
jshell.close()
dev.close()
sys.exit(1)

