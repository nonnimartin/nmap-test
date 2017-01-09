import nmap
import json
import traceback
import sys, getopt
import sqlite3

#Set IP address
ip   = '127.0.0.1'
args = '-sS -O' 
#Create database connection object
db   = './data.db'
conn = sqlite3.connect(db)
c = conn.cursor()

#get CLI args
cmd_args = sys.argv

#Go through CLI options, where argument value = cmd_args[opt + 1]
for opt in range(len(cmd_args)):
    if cmd_args[opt] == '-i':
        ip = cmd_args[opt + 1]
    if cmd_args[opt] == '-j':
        json_print = True
    else:
        json_print = False
try:
    nm = nmap.PortScanner()
    scan = nm.scan(hosts=ip, arguments=args)
    scan_json = json.dumps(scan)
    #print ("Hostname = " + nm[ip].hostname())
    #print ("Scan information : " + str(scan))
except Exception as e:
    print (traceback.format_exception(None, e, e.__traceback__),  file=sys.stderr, flush=True)

try:
    os = scan['scan'][ip]['osmatch'][0]['name']
except:
    os = "No OS detected"

try:
    device_type = scan['scan'][ip]['osmatch'][0]['osclass'][0]['type']
except:
	device_type = "No device type detected"

try:
    mac = scan['scan'][ip]['addresses']['mac']
except:
    mac = "No MAC detected"

try:
    vendor = scan['scan'][ip]['osmatch'][0]['osclass'][0]['vendor']
except:
    vendor = "No vendor detected"

scan_time   = scan['nmap']['scanstats']['timestr']
command     = scan['nmap']['command_line']


try:
        c.execute('INSERT INTO scan_data(ip, os, device_type, mac, scan_time, vendor, command) VALUES (?, ?, ?, ?, ?, ?, ?)', [ip, os, device_type, mac, scan_time, vendor, command])
except sqlite3.IntegrityError:
        print('Error inserting new data')

if json_print:
    print (scan_json)

# Committing changes/close
conn.commit()
conn.close()
