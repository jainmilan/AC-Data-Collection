
from ww_APPKEY import APPKEY
CITY = "New Delhi"
FORMAT = "json"
BASE_URL = "http://api.worldweatheronline.com/free/v1/weather.ashx"
REQUEST_URL = BASE_URL + "?q=%s&format=%s&key=%s" %(CITY,FORMAT,APPKEY)
Weather_Data_BasePath = "/home/milan/Projects/Summer_Project/Weather_Data/"

import requests
import datetime
import time
import os
from pytz import timezone

while True:
	
	# Current Time to Create CSV File
	now = datetime.datetime.now(timezone('Asia/Kolkata'))
	
	# TimeStamp and Datetime when Request was Made
	Observation_TimeStamp = time.time()
	Observation_DateTime = datetime.datetime.fromtimestamp(Observation_TimeStamp).strftime('%Y-%m-%d %H:%M:%S')
	
	# JSON Packet Received
	try:
		JSON_Data=requests.get(REQUEST_URL).json()
	except requests.exceptions.ConnectionError:
		print "Network is Down"
		time.sleep(60)
		continue
	except requests.exceptions.URLRequired:
		print "Please provide Correct URL"
	except Exception as E:
		print "Error Encountered: " + E
		
	# Current Condition in the Area
	Current_Condition = JSON_Data['data']['current_condition'][0]
	
	# Weather for the Day
	Weather = JSON_Data['data']['weather'][0]
	
	# Request Made
	Request = JSON_Data['data']['request'][0]
	
	# Date on which weather was Recorded
	Weather_Date = str(Weather['date'])
	
	# Observation Time Returned by WorldWeather
	CC_Time = str(Current_Condition['observation_time'])
	
	# Current Temperature(in degreeC) and Humidity(Percentage)
	Temperature = Current_Condition['temp_C']
	Humidity = Current_Condition['humidity']
	
	# Write to CSV File
	try:
		Data_file = Weather_Data_BasePath + str(now.day) + "_" + str(now.month) + "/"
		if not os.path.isdir(Data_file):
			# If Directory not Available Create Directory
			os.makedirs(Data_file)
		
		Data_file = open(Data_file + str(now.hour)+"_"+str(now.minute)+".csv","a")
		Data_file.write(str(Observation_TimeStamp)+", "+str(Observation_DateTime)+", "+Weather_Date+" "+CC_Time+"(GMT), "+str(Temperature)+", "+str(Humidity)+"\n")
	except IOErro:
		print "Cannot Open the file"
	except Exception as exception_raised:
		print "Error Encountered: " + exception_raised 
		
	
	# Sleep for 10 Minutes. Collecting at a resolution of 10 Minutes
	time.sleep(600)
	
	
