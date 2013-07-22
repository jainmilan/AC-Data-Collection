import os
import json
import time
import logging
import requests
import datetime

from pytz import timezone

from FORECAST_FOR_DEVELOPER_CONFIG import APIKEY
from FORECAST_FOR_DEVELOPER_CONFIG import BASEURL
from FORECAST_FOR_DEVELOPER_CONFIG import LATITUDE
from FORECAST_FOR_DEVELOPER_CONFIG import LONGITUDE

from FORECAST_FOR_DEVELOPER_CONFIG import TIME_TO_SLEEP
from FORECAST_FOR_DEVELOPER_CONFIG import SLEEP_NETWORK_DOWN
from FORECAST_FOR_DEVELOPER_CONFIG import WEATHER_DATA_BASEPATH

LOCATION = str(LATITUDE) + "," + str(LONGITUDE)
URL = "http://api.forecast.io/forecast/66faf14caaa7ec35985a52b1785f678f/29.0167,77.3833" #BASEURL + APIKEY + "/" + LOCATION
print URL

log_file = WEATHER_DATA_BASEPATH + "Log_File.txt"
logging.basicConfig(filename=log_file,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

# Current Temperature(in degreeC) and Humidity(Percentage)
humidity = 0.0
temperature = 0.0

# Current Time to Create CSV File
now = datetime.datetime.now(timezone('Asia/Kolkata'))

while True:

	# TimeStamp and Datetime when Request was Made
	observation_timestamp = time.time()
	observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
	# JSON Packet Received
	try:
		weather_data = requests.get(str(URL)).json()
		
		# Current Condition in the Area
		current_condition = weather_data["currently"]
	
		# Timestamp Returned by Forecast for Developer
		cc_timestamp = current_condition['time']
		
		# Current Temperature(in degreeC) and Humidity(Percentage)
		temperature = current_condition['temperature']
		humidity = current_condition['humidity']	
		
		# Write to CSV File
		try:
			data_file = WEATHER_DATA_BASEPATH + str(now.day) + "_" + str(now.month) + "/"
			if not os.path.isdir(data_file):
				# If Directory not Available Create Directory
				os.makedirs(data_file)
			data_file = open(data_file + str(now.hour)+"_"+str(now.minute)+".csv","a")
			data_file.write(str(cc_timestamp) + "," + str(temperature) + "," + str(humidity) + "\n")
		except IOError:
			# Writing To the Log File
			logging.error('Cannot Open the file')
		except Exception as exception_raised:
			# Writing To the Log File
			logging.error('Error Encountered' + str(exception_raised))
		except requests.exceptions.ConnectionError:
			# Writing To the Log File
			logging.error('Network is Down')
			time.sleep(SLEEP_NETWORK_DOWN)
			continue
		
	except requests.exceptions.URLRequired:
		# Writing To the Log File
		logging.error('Please provide Correct URL')
	except Exception as exception_raised:
		# Writing To the Log File
		logging.error('Error Encountered' + str(exception_raised))
		
	# Sleep for TIME_TO_SLEEP Minutes. Collecting at a resolution of TIME_TO_SLEEP Minutes
	time.sleep(TIME_TO_SLEEP)
