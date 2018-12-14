import os
import logging
import logging.handlers
import datetime
import shutil
import psutil
import subprocess
import sys
import os
from shutil import copytree, ignore_patterns

##sys.argv[1] == Environment variable set by usbmount UM_MOUNTPOINT

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

log.debug('Python Ingestion Started')

flag = False
isMounting = True

if len(sys.argv) > 1:
	log.debug('The sys arg 1 exists')
	log.debug('The sys arg is %s'%sys.argv[1])
	while(isMounting):
        	if os.listdir(source):
                	isMounting = False
                	flag = True
                	print("Mounted")
        	else:
                	print("Not Mounted Yet")

	if(flag):
        	destination = '/new-pool/network/ingest/%s'%datetime.datetime.now().strftime("%Y-%m-%d %H.%M")
        	try :
                	copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))
                	subprocess.call("sudo umount %s" %source, shell=True)
        	except Exception as e:
                	print(e)

else:
	log.debug('The sys arg DOES NOT exist')
