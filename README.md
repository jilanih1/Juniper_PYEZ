# collect_jlogs.py
Simple script to collect RSI and full /var/log directory from a Juniper device using Juniper's PyEZ module for Python.

### Modules
- Juniper PyEZ module (created by Juniper)
- Paramiko module

Both can be installed on Linux using pip:
```
  $ pip install junos-eznc
  $ pip install paramiko
```
### Python 2/3 Compatibility
Print function behaves like Python3 in Python2 with the following:
```
  from __future__ import print_function
```
**Note:** *This must be the first line in the code.*

The following code checks the version of Python and if it's Python 2.7 or lower it uses raw_input instead of input:
```
  if sys.version_info[:2] <= (2, 7):
	  input = raw_input
```
**Note:** *Need to import sys module.*
### Juniper device configurations.
The script connects to the Juniper device via a NETCONF session over SSH (Port 830).

The following configurations are necessary:
```
admin@Juniper_Lab_Router> show configuration system services
ssh {
    root-login allow;
    protocol-version v2;
}
netconf {
    ssh {
        port 830;
    }
}
```
