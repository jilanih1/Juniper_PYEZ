#!/usr/bin/env python
#MODULES#################################################################################
from __future__ import print_function
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell
import json
import getpass
import sys
import subprocess
import paramiko
import datetime
#########################################################################################
if __name__ == '__main__':

	if sys.version_info[:2] <= (2, 7):
		input = raw_input
#VARIABLES###############################################################################
	date = str(datetime.datetime.today().strftime('%Y_%m_%d'))
	proc = subprocess.Popen('pwd', stdout=subprocess.PIPE)
	pwd = proc.stdout.read()
	pwd = pwd.strip('\n') + '/'
	save1 = pwd + date + '_PYEZ_RSI.txt'
	save2 = pwd + date + '_PYEZ_varlog.tar.gz'
	vartmp = '/var/tmp/'
	file1 = vartmp + date + '_PYEZ_RSI.txt'
	file2 = vartmp + date + '_PYEZ_varlog.tar.gz'
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#hostname = input('Device hostname: ')
	#username = input('Device username: ')
	password = getpass.getpass('Device password: ')
	hostname = '192.168.1.48'
	username = 'admin'
	dev = Device(host=hostname, user=username, passwd=password)
#########################################################################################
#GENERATING LOGS ON JUNOS################################################################
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
	jshell.run('cli -c "request support information | save ' + file1 + '"')
	jshell.run('tar -zcvf ' + file2 + ' /var/log/*')
	#flist = json.dumps(jshell.run('cli -c "file list /var/tmp | grep PYEZ"'))

	flist = jshell.run('cli -c "file list /var/tmp | grep PYEZ" ')
	for line in flist:
		print(line)
	jshell.close()
	dev.close()
#########################################################################################
#PULLING LOGS FROM DEVICE################################################################
	ssh.connect(hostname='192.168.1.48',username='admin',password=password)
	sftp = ssh.open_sftp()
	sftp.get('' + file1 + '','' + save1 + '')
	sftp.get('' + file2 + '','' + save2 + '')
	sftp.close()
	ssh.close()
#########################################################################################
sys.exit(1)
#########################################################################################
