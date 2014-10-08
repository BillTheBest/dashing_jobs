#!/usr/bin/env python
# Isilon status to Dashing

import subprocess
import httplib
import re
import json

# config variables
# dashing host
host = "127.0.0.1"
port = 3030
widget_id = "/widgets/isi_throughput"
authtoken = "TOKEN"

p = subprocess.Popen(["isi","status","-q"], stdout=subprocess.PIPE).communicate()[0]
pattern = 'Cluster Totals:[^\d]*[\d\.]+[KMG]{0,1}[^\d]*[\d\.]+[KMG]{0,1}[^\d]*([\d\.]+)([KMG]{0,1})[^\d]*([\d\.]+)([KMGT]{0,1})'
m = re.search(pattern, p)

###
# MBps Usage
bytes = float(m.group(1))
if m.group(2) == '':
  mbytes = bytes / 1024 /1024
elif m.group(2) == 'K':
  mbytes = bytes / 1024
elif m.group(2) == 'G':
  mbytes = bytes * 1024
else:
  # group(2) is M
  mbytes = bytes

# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'value': mbytes })
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)

###
# TBs Usage
widget_id = "/widgets/isi_space"
bytes = float(m.group(3))
if m.group(4) == '':
  tbytes = bytes / 1024 / 1024 / 1024 / 1024
elif m.group(4) == 'K':
  tbytes = bytes / 1024 / 1024 /1024
elif m.group(4) == 'M':
  tbytes = bytes / 1024 / 1024
elif m.group(4) == 'G':
  tbytes = bytes / 1024
else:
  # group(4) is T
  tbytes = bytes
  
# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'value': tbytes })
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)