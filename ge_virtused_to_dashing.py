#!/usr/bin/env python
# GridEngine stats to dashing
# retrieves GB of virtual memory in use from qstat and pushes to Dashing

import subprocess
import re
import httplib
import json

# config variables
# dashing host
host = "127.0.0.1"
port = 3030
widget_id = "/widgets/ge_virtused"
authtoken = "TOKEN"

# get amount of virtual memory in use
raw = subprocess.check_output(["qstat","-F","virtual_used"])
match = re.findall('hl:virtual_used=([\d\.]+)G', raw)

#loop to add values from all nodes
used=0
for m in match:
  used += float(m)

#round to 2 places
used = round(used,2)

# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'value': used})
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)