import os
import logging
import logging.handlers
import datetime
import shutil
import subprocess
import sys
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
	source = sys.argv[1]
	destination = '/new-pool/network/ingest/%s'%datetime.datetime.now().strftime("%Y-%m-%d %H.%M")
	log.debug("Copying to %s"%destination)
	try :
		copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))
		subprocess.call("pumount %s" %source, shell=True)
		subprocess.call("sudo udevadm trigger --action=remove /sys/class/block/sdd1", shell=True)
	except Exception as e:
		log.debug("ERROR")
		log.critical(e)
else:
	log.debug('The sys arg DOES NOT exist')
