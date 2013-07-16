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

from SENSOR_ACT_CONFIG_AH import SA_API_KEY_AH
from SENSOR_ACT_CONFIG_AH import DEVICE_LOCATION_AH
from SENSOR_ACT_CONFIG_AH import DEVICE_NAME_AH
from SENSOR_ACT_CONFIG_AH import URL_SENSOR_ACT_AH

from SENSOR_ACT_CONFIG_MJ import SA_API_KEY_MJ
from SENSOR_ACT_CONFIG_MJ import DEVICE_LOCATION_MJ
from SENSOR_ACT_CONFIG_MJ import DEVICE_NAME_MJ
from SENSOR_ACT_CONFIG_MJ import URL_SENSOR_ACT_MJ

FLYPORT_DATA_BASEPATH =	[Flyport Data Base Directory]

FLYPORT_DATA_BASEPATH_1 = FLYPORT_DATA_BASEPATH + "flyport1/"
FLYPORT_DATA_BASEPATH_2 = FLYPORT_DATA_BASEPATH + "flyport2/"

# Log File	
log_file_1 = open(FLYPORT_DATA_BASEPATH_1 + "Log_File.txt","a")
log_file_2 = open(FLYPORT_DATA_BASEPATH_2 + "Log_File.txt","a")

# Lock to delete Files
lock_file_1 = 0
lock_file_2 = 0
	
while(True):
	
	# Current Unix Timestamp and Datetime
	observation_timestamp = time.time()
	observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

	# List of files to Upload
	list_of_files = glob.glob(FLYPORT_DATA_BASEPATH_1+str("*.csv"))
	log_file_1.write(str(observation_datetime) + "=> Files To Upload: " + str(list_of_files) + "\n")
	
	# For Loop to iterate through every File in the folder
	for f in list_of_files:
	
		# Check if file is in use for data collection
		if int(time.time())-int(os.stat(f).st_mtime)>900:
			with open(f) as filein:
				reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
				log_file_1.write(str(observation_datetime) + "=> Starting Upload of File: " + str(f) + "\n")
				
				for row in reader:
					
					timestamp = math.fabs(row[0])
					temperature = row[1]
					pir = row[2]
					light = row[3]
					
					# Create Packet
					headers = { 'Content-Type': 'application/json; charset=UTF-8'}
					payload1 = { 'secretkey' : SA_API_KEY_AH, "data" : { "loc" : DEVICE_LOCATION_AH, "dname" : str(DEVICE_NAME_AH), "sname" :"PIRSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [pir] } ] } }
					payload2 = { 'secretkey' : SA_API_KEY_AH, "data" : { "loc" : DEVICE_LOCATION_AH, "dname" : str(DEVICE_NAME_AH), "sname" :"TemperatureSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [temperature] } ] } }
					payload3 = { 'secretkey' : SA_API_KEY_AH, "data" : { "loc" : DEVICE_LOCATION_AH, "dname" : str(DEVICE_NAME_AH), "sname" :"LightSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [light] } ] } }

					try:
						# Upload Data
						r1 = requests.post(URL_SENSOR_ACT_AH, data=json.dumps(payload1), headers=headers)
						r2 = requests.post(URL_SENSOR_ACT_AH, data=json.dumps(payload2), headers=headers)
						r3 = requests.post(URL_SENSOR_ACT_AH, data=json.dumps(payload3), headers=headers)
						
					except requests.exceptions.ConnectionError:
						# If Connection Down
						log_file_1.write(str(observation_datetime) + "=> Network Down: " + str(f) + "\n")
						# Lock the file so that it won't be deleted
						lock_file_1 = 1
						# Exit from file
						break
					
					except Exception as exception_raised:
						# Any Other Exception Raised
						log_file_1.write(str(observation_datetime) + "=> " + str(exception_raised) + "\n")
						continue
				
				if lock_file_1 == 0:
					# If file not locked
					log_file_1.write(str(observation_datetime) + "=> File Uploaded. Now Deleting \n")
					os.remove(f)
				else:
					# Go To Sleep
					break
		else:
			log_file_1.write(str(observation_datetime) + "=> Cannot Upload. Data Collection Going On: " + str(f) + "\n")
	
	# List of files to Upload
	list_of_files = glob.glob(FLYPORT_DATA_BASEPATH_2+str("*.csv"))
	log_file_2.write(str(observation_datetime) + "=> Files To Upload: " + str(list_of_files) + "\n")
	
	# For Loop to iterate through every File in the folder
	for f in list_of_files:
		# Check if file is in use for data collection
		if int(time.time())-int(os.stat(f).st_mtime)>900:
			with open(f) as filein:
				reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
				log_file_2.write(str(observation_datetime) + "=> Starting Upload of File: " + str(f) + "\n")
				
				for row in reader:
					
					timestamp = math.fabs(row[0])
					temperature = row[1]
					pir = row[2]
					light = row[3]
					
					# Create Packet
					headers = { 'Content-Type': 'application/json; charset=UTF-8'}
					payload1 = { 'secretkey' : SA_API_KEY_MJ, "data" : { "loc" : DEVICE_LOCATION_MJ, "dname" : str(DEVICE_NAME_MJ), "sname" :"PIRSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [pir] } ] } }
					payload2 = { 'secretkey' : SA_API_KEY_MJ, "data" : { "loc" : DEVICE_LOCATION_MJ, "dname" : str(DEVICE_NAME_MJ), "sname" :"TemperatureSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [temperature] } ] } }
					payload3 = { 'secretkey' : SA_API_KEY_MJ, "data" : { "loc" : DEVICE_LOCATION_MJ, "dname" : str(DEVICE_NAME_MJ), "sname" :"LightSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [light] } ] } }

					try:
						# Upload Data
						r1 = requests.post(URL_SENSOR_ACT_MJ, data=json.dumps(payload1), headers=headers)
						r2 = requests.post(URL_SENSOR_ACT_MJ, data=json.dumps(payload2), headers=headers)
						r3 = requests.post(URL_SENSOR_ACT_MJ, data=json.dumps(payload3), headers=headers)
						
					except requests.exceptions.ConnectionError:
						# If Connection Down
						log_file_2.write(str(observation_datetime) + "=> Network Down: " + str(f) + "\n")
						# Lock the file so that it won't be deleted
						lock_file_2 = 1
						# Exit from file
						break
					
					except Exception as exception_raised:
						# Any Other Exception Raised
						log_file_2.write(str(observation_datetime) + "=> " + str(exception_raised) + "\n")
						continue
				
				if lock_file_2 == 0:
					# If file not locked
					log_file_2.write(str(observation_datetime) + "=> File Uploaded. Now Deleting \n")
					os.remove(f)
				else:
					# Go To Sleep
					break
		else:
			log_file_2.write(str(observation_datetime) + "=> Cannot Upload. Data Collection Going On: " + str(f) + "\n")
	log_file_1.write(str(observation_datetime) + "=> Sleeping \n")
	log_file_2.write(str(observation_datetime) + "=> Sleeping \n")
	time.sleep(900)
	log_file_1.write(str(observation_datetime) + "=> Back To Work \n")
	log_file_2.write(str(observation_datetime) + "=> Back To Work \n")
