import os
import csv
import glob
import time
import math
import json
import logging
import requests
import datetime
from pytz import timezone

from CONFIGURATION import SA_API_KEY
from CONFIGURATION import DEVICE_LOCATION
from CONFIGURATION import DEVICE_NAME
from CONFIGURATION import URL_SENSOR_ACT

from CONFIGURATION import AC_DATA
from CONFIGURATION import SLEEP_TIME
from CONFIGURATION import WEATHER_DATA
from CONFIGURATION import LOG_DIRECTORY
from CONFIGURATION import UPLOAD_SLEEP_TIME

log_file = LOG_DIRECTORY + 'Log_Upload.txt'
logging.basicConfig(filename=log_file,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

while(True):

        # Lock to delete Files
        lock_file_1 = 0
        lock_file_2 = 0

        # Current Unix Timestamp and Datetime
        observation_timestamp = time.time()
        observation_datetime = datetime.datetime.fromtimestamp(observation_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # List of files to Upload
        list_of_files_ac = glob.glob(AC_DATA + str("*.csv"))
        logging.info('Files To Upload: ' + str(list_of_files_ac))

        # For Loop to iterate through every File in the folder
        for f in list_of_files_ac:

		# Unlock the File
		lock_file_1 = 0
		
                # Check if file is in use for data collection
                if int(time.time())-int(os.stat(f).st_mtime)>900:
                        with open(f) as filein:
                                reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
                                logging.info('Starting Upload of File: ' + str(f))
                                for row in reader:

                                        timestamp = math.fabs(row[0])
                                        temperature = row[1]

                                        # Create Packet
                                        headers = { 'Content-Type': 'application/json; charset=UTF-8'}
                                        payload = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : str(DEVICE_NAME), "sname" :"TemperatureSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "celsius" ,"readings" : [temperature] } ] } }

                                        try:
                                                # Upload Data
                                                r = requests.post(URL_SENSOR_ACT, data=json.dumps(payload), headers=headers)

                                        except requests.exceptions.ConnectionError:
                                                # If Connection Down
                                                logging.error('Network Down')
                                                # Lock the file so that it won't be deleted
                                                lock_file_1 = 1
                                                # Exit from file
                                                break

                                if lock_file_1 == 0:
                                        # If file not locked
                                        logging.info('File Uploaded.')
                                        logging.warning('Deleting File: ' + str(f))
                                        os.remove(f)
                                else:
                                        # Go To Sleep
                                        break
                else:
					logging.warning('Cannot Upload. Data Collection Going On: ' + str(f))
        
        # List of files to Upload
        list_of_files_weather = glob.glob(WEATHER_DATA+str("*.csv"))
        logging.info('Files To Upload: ' + str(list_of_files_weather))
        
        # For Loop to iterate through every File in the folder
        for f in list_of_files_weather:
	
		# Unlock Weather Files
		lock_file_2 = 0

                # Check if file is in use for data collection
                if int(time.time())-int(os.stat(f).st_mtime)>900:
                        with open(f) as filein:
                                reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
                                logging.info('Starting Upload of File: ' + str(f))
                                for row in reader:

                                        w_timestamp = math.fabs(row[0])
                                        w_temperature = row[1]

                                        # Create Packet
                                        headers = { 'Content-Type': 'application/json; charset=UTF-8'}
                                        payload = { 'secretkey' : SA_API_KEY, "data" : { "loc" : DEVICE_LOCATION, "dname" : str(DEVICE_NAME), "sname" :"WeatherData", "sid" : "1", "timestamp" : w_timestamp, "channels" : [ { "cname" : "channel1", "unit" : "celsius" ,"readings" : [w_temperature] } ] } }

                                        try:
                                                # Upload Data
                                                r = requests.post(URL_SENSOR_ACT, data=json.dumps(payload), headers=headers)

                                        except requests.exceptions.ConnectionError:
                                                # If Connection Down
                                                logging.error('Network Down')
                                                # Lock the file so that it won't be deleted
                                                lock_file_2 = 1
                                                # Exit from file
                                                break

                                if lock_file_2 == 0:
                                        # If file not locked
                                        logging.info('File Uploaded.')
                                        logging.warning('Deleting File: ' + str(f))
                                        os.remove(f)
                                else:
                                        # Go To Sleep
                                        break
                else:
                        logging.warning('Cannot Upload. Data Collection Going On: ' + str(f))
        logging.info('Sleeping')
        time.sleep(UPLOAD_SLEEP_TIME)
        logging.info('Back To Work')

