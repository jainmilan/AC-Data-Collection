import os
import csv
import glob
import time
import math
import time
import glob
import json
import logging
import requests
import datetime
import logging.handlers
from pytz import timezone

from CONFIGURATION import SA_API_KEY
from CONFIGURATION import DEVICE_LOCATION
from CONFIGURATION import DEVICE_NAME
from CONFIGURATION import URL_SENSOR_ACT

from CONFIGURATION import LOG_DIRECTORY
from CONFIGURATION import AC_DATA_DIRECTORY
from CONFIGURATION import WEATHER_DATA_DIRECTORY
from CONFIGURATION import WAIT_BEFORE_NEXT_UPLOAD

log_file = LOG_DIRECTORY + 'Log_Upload.txt'
logging.basicConfig(filename=log_file,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

class SensorActDataUpload:
	
	def sensor_act_upload(self, payload, data_directory):
		
		# Header for the Packet to SensorAct
		headers = { 'Content-Type': 'application/json; charset=UTF-8'}
		timestamp = []
		temperature = []		
		# Current Unix Timestamp and Datetime
		current_timestamp = time.time()
		current_datetime = datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
			
		# List of files to Upload
		list_of_files = glob.glob(data_directory + str("*.csv"))
		
		# For Loop to iterate through every File in the folder
		for f in list_of_files:
	
			# Check if file is in use for data collection
			time_from_last_modification = int(time.time()) - int(os.stat(f).st_mtime)
			if time_from_last_modification > 900:
				with open(f) as filein:
					reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
					logging.info('Starting Upload of File: ' + str(f))
					for row in reader:
						timestamp.append(int(row[0]))
						temperature.append(row[1])
					payload["data"]["timestamp"] = timestamp[0]
					payload["data"]["channels"][0]["readings"] = temperature
					
					try:
						# Upload Data
						r = requests.post(URL_SENSOR_ACT, data=json.dumps(payload), headers=headers)
	
					except requests.exceptions.ConnectionError:
						# If Connection Down
						logging.error('Network Down')
						# Exit from function
						return(1)
					
					except Exception as Error:
						print(Error)
						logging.error(Error)
						return(1)
	
					try:
						# Delete the File
						logging.info('File Uploaded.')
						logging.warning('Deleting File: ' + str(f))
						os.remove(f)
						
					except OSError:
						# File is uploaded but not found
						logging.error('Either file already deleted or not found!') 
						continue
			else:
				logging.warning('Cannot Upload. Data Collection Going On: ' + str(f))
	
if __name__ == "__main__":
	while True:
		upload = SensorActDataUpload()
		payload = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : DEVICE_NAME, "sname" :"", "sid" : "1", "timestamp" : 0, "channels" : [ { "cname" : "channel1", "unit" : "celsius" ,"readings" : [] } ] } }
		payload_1 = payload
		data_directory_1 = AC_DATA_DIRECTORY
		payload_1["data"]["sname"] = "TemperatureSensor"
		upload.sensor_act_upload(payload_1,data_directory_1)
		payload_2 = payload
		payload_2["data"]["sname"] = "WeatherData"
		data_directory_2 = WEATHER_DATA_DIRECTORY
		upload.sensor_act_upload(payload_2,data_directory_2)
		time.sleep(WAIT_BEFORE_NEXT_UPLOAD)

