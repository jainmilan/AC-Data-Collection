CITY_ID = 1273294
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
REQUEST_URL = BASE_URL + "?id=%d" %(CITY_ID)
WEATHER_DATA_BASEPATH = "/home/milan/Projects/Summer_Project/AC_Data_Collection/Data/Weather_Data_OW/"
SLEEP_NETWORK_DOWN = 60
TIME_TO_SLEEP = 600

import requests
import datetime
import time
import os
from pytz import timezone

LOG_FILE = open(WEATHER_DATA_BASEPATH + "Log_File.txt","a")

# Current Temperature(in degreeC) and Humidity(Percentage)
humidity = ''
temperature = ''

# Current Time to Create CSV File
now = datetime.datetime.now(timezone('Asia/Kolkata'))

while True:

	# TimeStamp and Datetime when Request was Made
	observation_timestamp = abs(time.time())
	observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
	# JSON Packet Received
	try:
		json_data=requests.get(REQUEST_URL).json()
		
		# Current Condition in the Area
		current_condition = json_data['main']
		
		# Timestamp on which weather was Recorded (Open Weather)
		epoch_time = str(json_data['dt'])
		
		# Current Temperature(in degreeC) and Humidity(Percentage)
		temperature = (current_condition['temp'])-273.15
		humidity = current_condition['humidity']	

		# Write to CSV File
		try:
			data_file = WEATHER_DATA_BASEPATH + str(now.day) + "_" + str(now.month) + "/"
			if not os.path.isdir(data_file):
				# If Directory not Available Create Directory
				os.makedirs(data_file)
			data_file = open(data_file + str(now.hour)+"_"+str(now.minute)+".csv","a")
			data_file.write(str(observation_timestamp)+","+epoch_time+","+str(temperature)+","+str(humidity)+"\n")
		except IOError:
			# Writing To the Log File
			LOG_FILE.write(str(observation_datetime) + "=> Cannot Open the file\n")
		except Exception as exception_raised:
			# Writing To the Log File
			LOG_FILE.write(str(observation_datetime) + "=> Error Encountered1: " + str(exception_raised)+"\n")	
		except requests.exceptions.ConnectionError:
			# Writing To the Log File
			LOG_FILE.write(str(observation_datetime) + "=> Network is Down\n")
			time.sleep(SLEEP_NETWORK_DOWN)
			continue

	except requests.exceptions.URLRequired:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Please provide Correct URL\n")

	except Exception as E:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Error Encountered: " + str(E) + "\n")

	

	# Sleep for TIME_TO_SLEEP Minutes. Collecting at a resolution of TIME_TO_SLEEP Minutes
	time.sleep(TIME_TO_SLEEP)
