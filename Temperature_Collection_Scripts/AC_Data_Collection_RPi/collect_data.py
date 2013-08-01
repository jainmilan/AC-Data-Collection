import os
import time
import logging
import datetime

from pytz import timezone
from CONFIGURATION import LOG_DIRECTORY
from CONFIGURATION import DATA_DIRECTORY
from CONFIGURATION import SLEEP_TIME

# Starting execution of the program
start_time = time.time()

#global init_time
init_time = time.time()

#global init_time_t
init_time_t = datetime.datetime.now(timezone('Asia/Kolkata'))

log_file = LOG_DIRECTORY + 'Log_Pi.txt'

# Current Time to Create CSV File
now = datetime.datetime.now(timezone('Asia/Kolkata'))

logging.basicConfig(filename=log_file,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

while(1):

	# *Code Snippet from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/*
	# Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before.
	tfile = open("/sys/bus/w1/devices/28-000004a5a601/w1_slave")
	# Read all of the text in the file.
	text = tfile.read()
	# Close the file now that the text has been read.
	tfile.close()
	# Split the text with new lines (\n) and select the second line.
	secondline = text.split("\n")[1]
	# Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
	temperaturedata = secondline.split(" ")[9]
	# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
	temperature = float(temperaturedata[2:])
	# Put the decimal point in the right place and display it.
	temperature = temperature / 1000
	# * *
	
	# Current Time
	current_time = time.time()
	#global init_time
	#global init_time_t

	# Collect 15 Minutes of Data
	end_time = init_time + 900
	if current_time > end_time:
		init_time = current_time
		init_time_t = datetime.datetime.now(timezone('Asia/Kolkata'))
	
	timestamp = time.time()
	
	# Write to CSV File
	try:
		data_file = DATA_DIRECTORY + str(init_time_t.day) + "_" + str(init_time_t.month) + "_" + str(init_time_t.hour) + "_" + str(init_time_t.minute) + ".csv"
		DATA_FILE = open(data_file,"a")
		DATA_FILE.write(str(timestamp) + "," + str(temperature) + "\n")
	except IOError:
		# Writing To the Log File
		logging.error('Cannot open the file.')
	except Exception as exception_raised:
		# Writing To the Log File
		logging.error('Error Encountered: ' + str(exception_raised))
	
	# Time just before the sleep
	end_time = time.time()
	
	# Time taken to execute the program
	execution_time = end_time - start_time
	
	# Time remaining for which program should sleep
	SLEEP_TIME_REAL = SLEEP_TIME - execution_time
	
	# Program going to sleep
	time.sleep(SLEEP_TIME_REAL)
	
	# Starting execution of program
	start_time = time.time()
