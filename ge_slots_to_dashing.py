#!/usr/bin/env python
# counts number of slots in use and pushes to dashing

import subprocess
import re
import httplib
import json

# config variables
# dashing host
host = "127.0.0.1"
port = 3030
widget_id = "/widgets/ge_slotsused"
authtoken = "TOKEN"

# get number of slots in use
raw = subprocess.check_output(["qstat","-f"])
match = re.findall('\d+\/(\d+)\/(\d+)', raw)

used=0
total=0
for m,t in match:
  used += int(m)
  total += int(t)
  
# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'value': used})
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)