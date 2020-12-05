#!/usr/bin/env/ python3
import yaml
import jinja2
import time
import logging
from netmiko import Netmiko
import threading
import os

# Update the yaml file name for the specific router you wish to connect to.
yaml_file = 'R4-SANDBOX.yaml'
jinja_template = 'template-205.j2'

# Global date/time/day variable. Used throughout the program for file naming. 
global d8
# YEAR MONTH DAY MINUTE
d8 = time.strftime("%Y-%m-%d-%M")
# ----------------------
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
# ----------------------
# Logging for all Netmiko commands (SSH) Creates a new file. If file exists, it appends new content.
# Sets up Folder | ignores if already present.
createFolder('Logging')

logging.basicConfig(filename=f"Logging/NetmikoLog-{d8}.txt", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

# ----------------------
# Generate the configurations and send it to the devices
def confgen(vars):
    # Generate configuration lines with Jinja2
    with open(jinja_template) as f:
        tfile = f.read()
        template = jinja2.Template(tfile)
        global cfg_list
        cfg_list = template.render(vars)

        # Connect directly to host via SSH on the specified port
        conn = Netmiko(host=vars['hostip'], device_type='alcatel_sros', username="admin", password="admin", response_return=None)

        # Send generated commands to host
        output = conn.send_config_set(cfg_list,cmd_verify=False)

        # Display results
        print('-' * 80)
        print('\nConfiguration applied on ' + vars['host'] + ': \n\n' + output)
        print('-' * 80)

        # Probably a good idea
        conn.disconnect()
# ----------------------
# Parse the YAML file
with open(yaml_file) as f:
    read_yaml = yaml.load(f, Loader=yaml.FullLoader)  # Converts YAML file to dictionary
# ----------------------
# Take imported YAML dictionary and start multi-threaded configuration generation.
# You could condense all yaml files into one if you wanted.
for hosts, vars in read_yaml.items():
    # Add host to vars dictionary
    host = {'host': hosts}
    vars.update(host)

    # Send vars to confgen function using multi-threading, one thread per-host
    threads = threading.Thread(target=confgen, args=(vars,))
    threads.start()

    # Capture PWD -This should be the base of where the program lives.
    PWD = os.getcwd()

    # Setup ConfigZ -
    createFolder('Configurations')

    # Change to the correct folder by hostname. -
    os.chdir('Configurations')

    # Organize the new configuration files. -
    createFolder(vars['host'])

    # Change to the correct folder by hostname. -
    os.chdir(vars['host'])

    # Open a new text file and save the configuration.
    # 'host' is extracted from the yaml file. 
    # This should be the system name.

    y = open(vars['host']+'-cfg-change-'+ (d8) +'.txt','w')
    y.write(cfg_list)

    # Return to the correct directory and re-run code for each NODE.
    os.chdir(PWD)
# ----------------------

