import nmap
import json
import traceback
import sys

ip = '10.100.2.203'

try:
    nm = nmap.PortScanner()
    scan = nm.scan(hosts=ip, arguments='-sS -O')
    scan = json.dumps(scan)
    print ("Hostname = " + nm[ip].hostname())
    print ("Scan information : " + str(scan))
#except Exception as e:
#    print (e)
except Exception as e:
    print (traceback.format_exception(None, e, e.__traceback__),  file=sys.stderr, flush=True)
