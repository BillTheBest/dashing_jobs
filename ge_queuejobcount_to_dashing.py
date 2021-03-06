#!/usr/bin/env python
# gridengine waiting job count to dashing
# ships count of waiting jobs to dashing for stats display

import subprocess
import re
import httplib
import json

# config variables
# dashing host
host = "127.0.0.1"
port = 3030
widget_id = "/widgets/ge_qwjobcount"
authtoken = "TOKEN"

# get number of jobs in 'qw' state
raw = subprocess.check_output(["qstat","-f","-u","*"])
match = re.findall('\d+ [\d\.]+ [\w\d\.]+\s+\w+\s+qw\s+\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}\s+\d+', raw)
value = len(match)

# post to dashing
params = json.dumps({ 'auth_token': authtoken, 'current': value})
conn = httplib.HTTPConnection(host, port)
conn.request("POST", widget_id, params)