import os
import web
import datetime
import time,glob
import MySQLdb,sys

# Downloaded from NMS Server
input_filedir = "/home/milan/Data/Power_Orignal/203/Phase-3_2/September/"

# List of Files to be Converted
list_of_files = glob.glob(str(input_filedir) + str("/*.csv"))

# Save to this directory
output_filedir = "/home/milan/Data/Power_Converted/203/Phase-3_2/September/"

for f in list_of_files:
	reader = open(f)
	filename = os.path.basename(f)
	for line in reader:
		
		# Remove Metadata
		if str(line).startswith('#'):
			continue
		
		# Separate out Datetime and Power
		data = line.split(",")
		
		# Change to Epoch Timestamp
		datetime = data[0].split("+")
		# Format of Time in the file
		format_time = '%Y-%m-%dT%H:%M:%S'					
		split_datetime = datetime.datetime.strptime(datetime[0],format_time)
		timestamp = int(time.mktime(split_datetime.timetuple()))
		
		# Get Power Reading
		power = float(data[1])
		
		# Write to new CSV
		output = open(output_filedir + filename,'a')
		output.write(str(timestamp) + "," + str(power) + "\n")
		output.close()
	
		
