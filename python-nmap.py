import nmap
import json
import traceback
import sys
import sqlite3

#Set IP address
ip   = '192.168.1.72'
args = '-sS -O' 
#Create database connection object
db   = './data.db'
conn = sqlite3.connect(db)
c = conn.cursor()

try:
    nm = nmap.PortScanner()
    scan = nm.scan(hosts=ip, arguments=args)
    scan_json = json.dumps(scan)
    #print ("Hostname = " + nm[ip].hostname())
    #print ("Scan information : " + str(scan))
except Exception as e:
    print (traceback.format_exception(None, e, e.__traceback__),  file=sys.stderr, flush=True)

os          = "fixThisSoItCanBeEmpty"
device_type = 'test'
mac         = scan['scan'][ip]['addresses']['mac']
scan_time   = scan['nmap']['scanstats']['timestr']
vendor      = scan['scan'][ip]['vendor'][mac]
command     = scan['nmap']['command_line']


try:
        c.execute('INSERT INTO scan_data(ip, os, device_type, mac, scan_time, vendor, command) VALUES (?, ?, ?, ?, ?, ?, ?)', [ip, os, device_type, mac, scan_time, vendor, command])
except sqlite3.IntegrityError:
        print('Error inserting new data')

# Committing changes/close
conn.commit()
conn.close()
