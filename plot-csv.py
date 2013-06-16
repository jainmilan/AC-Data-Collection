import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

data = np.genfromtxt('/home/milan/Projects/Summer_Project/Data/Combine/Final/06June0200-0215-Temp.csv',delimiter=',',names=['time1','channel','temperature'])
data2 = np.genfromtxt('/home/milan/Projects/Summer_Project/Data/Combine/Final/06June0200-0215-Meter.csv',delimiter=',',names=['time2','power'])
time = data['time1']
channel = data['channel']
temp = data['temperature']
time2 = data2['time2']
scaled_power = data2['power']
dates = [dt.datetime.fromtimestamp(ts) for ts in time]
dates2 = [dt.datetime.fromtimestamp(ts2) for ts2 in time2]
datenums = md.date2num(dates)
datenums2 = md.date2num(dates2)
fig = plt.figure()													
ax1 = fig.add_subplot(111)											
ax1.plot(datenums,temp,'b')	
ax1.set_xlabel('Date_Time')										
ax1.set_ylabel('Temperature(C)', color='b')
plt.xticks( rotation=25 )
plt.yticks(np.arange(29.5, 31.5	, 0.5))
ax2 = ax1.twinx()
ax2.plot(datenums2,scaled_power,'r')
ax2.set_xlabel('Date_Time')										
ax2.set_ylabel('Power(Watts)', color='r')
ax = plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.xticks( rotation=25 )
plt.yticks(np.arange(0, 4000,500))
plt.show()
