from datetime import datetime
from subprocess import check_output

from pythonwifi.iwlibs import Wireless

import iw_parse
from boto_session import get_new_boto3_session
from logger import Logger

logger = Logger('scanner', boto3_session=get_new_boto3_session())
today = datetime.now().strftime("%Y-%m-%d")

def scanWifiTshark():

	def parseDate(t):
		if (t[4] == ' '):
			t = t[:4] + '0' + t[5:27]
		else:
			t = t[:27]
		return datetime.strptime(t, '%b %d, %Y %H:%M:%S.%f')

	logger.log("start scan wifi")
	try:
		time = datetime.now()
		logger.log("started scanning")
		logger.log("Timestamp: " + str(time))
		scan_output = check_output(['sudo','tshark','-f','wlan[0] == 0x80 and broadcast','-i','mon0','-O','wlan','-T','fields','-e','frame.number','-e','frame.time','-e','wlan.bssid','-e','wlan_radio.signal_dbm','-e','wlan_mgt.ssid','-a', 'duration:1'])
		logger.log(str(scan_output))
		clean_output = {}
		for i in scan_output.split('\n'):
			line = i.split('\t')
			if len(line) is 5:
				clean_output[line[2]] = {
					'time': str(parseDate(line[1])),
					'bssid': line[2],
					'rssi': line[3],
					'ssid': line[4]
					}
		output = {}
		output['time'] = str(time)
		output['result'] = clean_output

		return output

	except Exception as error:
		logger.log(error)
		logger.log("something crashed")

def scanWifiIwlist(interface):
	try:
		logger.log("scanning on " + str(interface) + "...")
		time = datetime.now()
		wifi = Wireless(interface)
		results = wifi.scan()
		logger.log("Scan completed: %s access points found" % len(results))
		(num_channels, frequencies) = wifi.getChannelInfo()

		scan_results = {}

		for ap in results:
			ap_dict = {
				'bssid': ap.bssid,
				# This is rss and not rssi
				'rssi': ap.quality.getSignallevel(),
				'ssid': None if not ap.essid else ap.essid,
				'time': str(time),
				'frequency': ap.frequency.getFrequency(),
				#'channel': frequencies.index(wifi._formatFrequency(ap.frequency.getFrequency())),
				'mode': ap.mode,
				'quality': "%s/%s" % (ap.quality.quality, wifi.getQualityMax().quality),
				'noise': ap.quality.getNoiselevel(),
				'extra': ap.custom,
			}
			scan_results[ap.bssid] = ap_dict

		logger.log(scan_results)
		output = {}
		output['time'] = str(time)
		output['result'] = scan_results
		return output

	except Exception as error:
		logger.log(error)
		raise error


def scanWifiIwparse():
	try:
		logger.log("started scanning...")
		time = datetime.now()
		scan_output = iw_parse.get_interfaces('wlan0')
		logger.log("finished iw_parse")
		scan_results = {}
		def extract(cell, prop):
			try:
				return None if (prop not in cell or cell[prop] == '') else cell[prop]
			except Exception as error:
				logger.log("Error in extract1")
				logger.log(error)
				logger.log("Error in extract2")
				return None
		for cell in scan_output:
			if 'Address' in cell:
				try:
					ap_dict = {
						'bssid': extract(cell, 'Address'),
						'rssi': extract(cell, 'Signal Level'),
						'ssid': extract(cell, 'Name'),
						'time': str(time),
						'channel': extract(cell, 'Channel'),
						'quality': extract(cell, 'Quality'),
						'bit_rate': extract(cell, 'Bit Rates'),
						'last_beacon': extract(cell, 'Beacon'),
						'encryption': extract(cell, 'Encryption')
					}
					if ap_dict['last_beacon']:
						ap_dict['last_beacon'] = int(ap_dict['last_beacon'].replace('ms ago', ''))
					scan_results[cell['Address']] = ap_dict
				except Exception as error:
					logger.log(error)
					continue
			else:
				logger.log("Cell has no address")
				logger.log(cell)

		logger.log(scan_results)
		output = {}
		output['time'] = str(time)
		output['result'] = scan_results
		return output

	except Exception as error:
		logger.log(error)
		raise error
