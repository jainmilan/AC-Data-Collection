import os
import glob
import shutil

# Folder containing Room Temperature and Weather File
filedir = "/home/milan/Data/Temperature/1102/1/9/2/"

### To Work on Files in Multiple Folders ###
#folders = os.listdir(filedir)
#print folders
#for folder in folders:
#	list_of_files = glob.glob(str(filedir)+str(folder)+str("/*.csv"))

# Save Weather Data files to this directory
output_dir = "/home/milan/Data/Weather_Data/1102/1/9/2/"

# All files in Input Directory
list_of_files = glob.glob(str(filedir) + str("/*.csv"))

# Iterate through each File
for f in list_of_files:
	reader = open(f)
	for line in reader:
		data = line.split(",")
		if len(data)==3:
			try:
				# Move file to Output Directory
				shutil.move(f,output_dir)
			except:
				continue
			print str(f) + ": " + str(len(data))
			

