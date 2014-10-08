#!/usr/bin/env python
# gridengine user jobs to dashing
# ships count of user jobs to dashing for stats display

import subprocess
import re
import httplib
import json

# config variables
# dashing host
host = "127.0.0.1"
port = 3030
widget_id = "/widgets/ge_userjobcount"
authtoken = "TOKEN"

# number of days to count
days = "7"
homedir = "/home"

# initialize output
output = []

#get user list
raw = subprocess.check_output(["ls",homedir])
unames = raw.split()
for uname in unames:
  # get real name
  raw = subprocess.check_output(["getent", "passwd", uname])
  n = raw.split(":")
  label = n[4]
  if label == '':
    label = uname
  
  # get count of jobs from GE
  raw = subprocess.check_output(["qacct","-o",uname,"-j","-d",days])
  value = raw.count('jobnumber')
  
  # add name and job count to output
  output.append({"label": label, "value": value})

# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'items': output})
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)