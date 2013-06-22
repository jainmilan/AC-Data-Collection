from WW_APPKEY import APPKEY
CITY = "New Delhi"
FORMAT = "json"
BASE_URL = "http://api.worldweatheronline.com/free/v1/weather.ashx"
REQUEST_URL = BASE_URL + "?q=%s&format=%s&key=%s" %(CITY,FORMAT,APPKEY)
WEATHER_DATA_BASEPATH = "/home/milan/Projects/Summer_Project/Weather_Data/"
SLEEP_NETWORK_DOWN = 60
TIME_TO_SLEEP = 600

import requests
import datetime
import time
import os
from pytz import timezone

LOG_FILE = open(WEATHER_DATA_BASEPATH + "Log_File.txt","a")

while True:
	
	# Current Time to Create CSV File
	now = datetime.datetime.now(timezone('Asia/Kolkata'))
	
	# TimeStamp and Datetime when Request was Made
	observation_timestamp = time.time()
	observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
	# JSON Packet Received
	try:
		json_data=requests.get(REQUEST_URL).json()
	except requests.exceptions.ConnectionError:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Network is Down\n")
		time.sleep(SLEEP_NETWORK_DOWN)
		continue
	except requests.exceptions.URLRequired:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Please provide Correct URL")
	except Exception as E:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Error Encountered: " + E)
		
	# Current Condition in the Area
	current_condition = json_data['data']['current_condition'][0]
	
	# Weather for the Day
	weather = json_data['data']['weather'][0]
	
	# Request Made
	request = json_data['data']['request'][0]
	
	# Date on which weather was Recorded
	weather_date = str(weather['date'])
	
	# Observation Time Returned by WorldWeather
	cc_time = str(current_condition['observation_time'])
	
	# Current Temperature(in degreeC) and Humidity(Percentage)
	temperature = current_condition['temp_C']
	humidity = current_condition['humidity']
	
	# Write to CSV File
	try:
		data_file = WEATHER_DATA_BASEPATH + str(now.day) + "_" + str(now.month) + "/"
		if not os.path.isdir(data_file):
			# If Directory not Available Create Directory
			os.makedirs(data_file)
		
		data_file = open(data_file + str(now.hour)+"_"+str(now.minute)+".csv","a")
		data_file.write(str(observation_timestamp)+","+str(observation_datetime)+","+weather_date+" "+cc_time+"(GMT),"+str(temperature)+","+str(humidity)+"\n")
	except IOError:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Cannot Open the file")
	except Exception as exception_raised:
		# Writing To the Log File
		LOG_FILE.write(str(observation_datetime) + "=> Error Encountered: " + exception_raised)
	
	# Sleep for TIME_TO_SLEEP Minutes. Collecting at a resolution of TIME_TO_SLEEP Minutes
	time.sleep(TIME_TO_SLEEP)
	
	
