import os
import sys
import csv
import time
import glob
import json
import math
import time
import datetime
import requests

from pytz import timezone
from SENSOR_ACT_CONFIG import SA_API_KEY
from SENSOR_ACT_CONFIG import DEVICE_LOCATION
from SENSOR_ACT_CONFIG import DEVICE_NAME
from SENSOR_ACT_CONFIG import URL_SENSOR_ACT

FLYPORT_DATA_BASEPATH =	[Path_To_CSV_Folder]

# Log File	
log_file = open(FLYPORT_DATA_BASEPATH + "Log_File.txt","a")
	
while(True):
	
	# Current Unix Timestamp and Datetime
	observation_timestamp = time.time()
	observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

	# List of files to Upload
	list_of_files = glob.glob(FLYPORT_DATA_BASEPATH+str("*.csv"))
	log_file.write(str(observation_datetime) + "=> Files To Upload: " + str(list_of_files) + "\n")
	
	# For Loop to iterate through every File in the folder
	for f in list_of_files:
		# Check if file is in use for data collection
		if int(time.time())-int(os.stat(f).st_mtime)>900:
			with open(f) as filein:
				reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
				log_file.write(str(observation_datetime) + "=> Starting Upload of File: " + str(f) + "\n")
				
				for row in reader:
					
					timestamp = math.fabs(row[0])
					temperature = row[1]
					pir = row[2]
					light = row[3]
					
					# Create Packet
					headers = { 'Content-Type': 'application/json; charset=UTF-8'}
					payload1 = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : str(DEVICE_NAME), "sname" :"PIRSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [pir] } ] } }
					payload2 = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : str(DEVICE_NAME), "sname" :"TemperatureSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [temperature] } ] } }
					payload3 = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : str(DEVICE_NAME), "sname" :"LightSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [light] } ] } }

					try:
						# Upload Data
						r1 = requests.post(URL_SENSOR_ACT, data=json.dumps(payload1), headers=headers)
						r2 = requests.post(URL_SENSOR_ACT, data=json.dumps(payload2), headers=headers)
						r3 = requests.post(URL_SENSOR_ACT, data=json.dumps(payload3), headers=headers)
						
					except requests.exceptions.ConnectionError:
						# If Connection Down
						log_file.write(str(observation_datetime) + "=> Network Down: " + str(f) + "\n")
						continue
					
					except Exception as exception_raised:
						# Any Other Exception Raised
						log_file.write(str(observation_datetime) + "=> " + str(exception_raised) + "\n")
						continue
				log_file.write(str(observation_datetime) + "=> File Uploaded. Now Deleting \n")
				os.remove(f)
		else:
			log_file.write(str(observation_datetime) + "=> Data Collection Going On \n")
	time.sleep(900)
