#!/usr/bin/python

import subprocess
from datetime import datetime

print("Pre-Commit Hook")
# update requirements

# change last_change in config
subprocess.run('pipreqs --force', shell=True)
subprocess.run('sort-requirements requirements.txt', shell=True)
with open('config.py', 'r') as file:
    # read a list of lines into data
    data = file.readlines()
    for i, line in enumerate(data):
        if 'last_change' in data[i]:
            data[i] = f"last_change = '{datetime.now().strftime('%d-%b-%Y %H:%M')}'"

with open('config.py', 'w') as file:
    file.writelines(data)
