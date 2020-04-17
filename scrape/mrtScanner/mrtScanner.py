
from time import sleep
from datetime import datetime

from boto_session import get_new_boto3_session
from scanner import scanWifiTshark, scanWifiIwlist, scanWifiIwparse
from database import pushToDynamoDB
from logger import Logger

logger = Logger('main', boto3_session=get_new_boto3_session())


############# Device config #############

#Choose if scan by "tshark" or "iwlist"
scans = {
	1: scanWifiTshark,
	2: scanWifiIwlist,
	3: scanWifiIwparse,
}

scan_type = 3

################  End ###################

send_list = []

logger.log("Setting up scanner, scanning on type: " + str(scan_type))
while True:
	try:
		start_time = datetime.now()
		logger.log("Initiate scanning")
		if (scan_type is 2):
			try:
				send_list.append(scans[scan_type]('ra0'))
			except:
				try:
					send_list.append(scans[scan_type]('wlan0'))
				except Exception as error:
					print "error"
					print error
					logger.log("iwlist scan died")
					continue
				finally:
					sleep(0)
		else:
			try:
				send_list.append(scans[scan_type]())
			except Exception as error:
				print "crashed!"
				logger.log("Scanning crashed")
				logger.log(error)


		logger.log("scan completed, pushing to db")
		# logger.logToCsv(count, wifi_list)

		while len(send_list) > 0:
			payload = send_list.pop()
			try:
				if isinstance(payload, dict) and len(payload) > 0:
					pushToDynamoDB(payload)
			except Exception as error:
				print error
				logger.log(error)

		logger.log("Scan Completed: time taken to complete one scan is %s" % str(datetime.now() - start_time))

	except Exception as error:
		logger.log(error)
		print error
	sleep(1)
