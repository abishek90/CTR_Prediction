import csv
import random
import cmath
import numpy as np
import matplotlib.pyplot as plt
import math

valid_list = [];

#Function to parse a particular trip of a driver
def parsetrip(driver,trip):
	s = '../../Data/drivers/' + str(driver) + '/' + str(trip) +'.csv';
	try:
		f = open(s,'r');
	except:
		return 0;
	csv_f = csv.reader(f);
	trip_list = [];
	count = 0;
	for row in csv_f:
		count = count + 1;
		if count == 1:
			continue;
		else:
			a = float(row[0]) + float(row[1])*1j;
			trip_list.append(a);
	f.close();
	return trip_list;

#Function to parse a driver 
def parsedriver(driver):
	driver_list = [];
	for i in range(200):
		a = parsetrip(driver,i+1);
		driver_list.append(a);
	return driver_list;


#function to update the global variable with a valid_list of drivers
def valid_drivers():
	for i in range(3700):
		s = '../../Data/drivers/' + str(i+1) + '/' + str(1) +'.csv';
		try:
			f = open(s,'r');
		except:
			continue;
		valid_list.append(i+1);
	return valid_list;

#function to smoothen large acceleration in the position vectors
def smooth_trip(trip):
	speed = np.diff(trip);
	for i in range(len(speed)-1):
		temp = cmath.polar(speed[i+1] - speed[i]);
		if temp[0] > 20:
			t2 = speed[i+1];
			speed[i+1] = speed[i];
			for j in range(i+2,len(trip)):
				trip[j] = trip[j-1] + speed[j-1];


#function to calculate the number of turns in a trip and the average speed in each turn as a 3-tuple
def num_turns(trip):
	length = len(trip);
	i = 0;
	c_l = 0;
	c_r = 0;
	avg_speed = 0;
	while i < length - 5:
		c1 = trip[i+4] - trip[i+2];
		c2 = trip[i+2] - trip[i];
		a1 = cmath.polar(c1)[1];
		a2 = cmath.polar(c2)[1];
		if abs(a1 - a2) > (math.pi)/4:
			if a1 > a2:
				c_l = c_l +1;
			else:
				c_r = c_r + 1;
			temp = trip[i:i+4];
			avg_speed = avg_speed + cmath.polar(np.mean(np.diff(temp)))[0];
			i = i + 5;
		else:
			i = i+1;
	turn_par = [];
	turn_par.append(float(c_l) );
	turn_par.append(float(c_r) );
	if c_l + c_r > 0:
		turn_par.append(float(avg_speed/(c_l+c_r)) );
	else:
		turn_par.append(0);
	return turn_par;






#function to create a test set, where num trips from driver 'driver' is present and (total - num) trips of random drivers are added at the end.
def createteset(driver, num,total):
	main_list =  parsedriver(driver);
	trip_list = [];
	my_sample = random.sample(range(200), num);
	for i in range(num):
		trip_list.append(main_list[my_sample[i]]);
	for i in range(total - num):
		a = random.randrange(0, len(valid_list));
		b = random.randrange(1,201);
		trip = parsetrip(valid_list[a],b);
		trip_list.append(trip);
	return trip_list;

#function to find average acceleration before and after a stop and the number of stops
def stopping_param(trip):
	length = len(trip);
	stop_par = [];
	speed = np.diff(trip);
	acc = np.diff(speed);
	avg_acc = 0;
	avg_dcc = 0;
	count = 0;
	for i in range(length - 6):
		if cmath.polar(speed[i])[0] == 0 and i>=4:
			s = (cmath.polar(acc[i-1])[0]  +  cmath.polar(acc[i-2])[0]  +  cmath.polar(acc[i-3])[0]  +  cmath.polar(acc[i-4])[0] )/4;
			d = (cmath.polar(acc[i])[0]  +  cmath.polar(acc[i+1])[0]  +  cmath.polar(acc[i+2])[0]  +  cmath.polar(acc[i+3])[0] )/4;
			avg_acc = avg_acc + d;
			avg_dcc = avg_dcc + s;
			count = count + 1;
	stop_par.append(float(count) );
	if count > 0:
		stop_par.append(float(avg_acc/count) );
		stop_par.append(float(avg_dcc/count) );
	else:
		stop_par.append(0 );
		stop_par.append(0);
	return stop_par;

#function to return normalised parameters for regression for a given trip-list
def regression_parameters(trip_list):
	num = len(trip_list);
	features_list = [];
	for i in range(num):
		curr_trip = trip_list[i];
		smooth_trip(curr_trip);
		feature = [];
		length = len(curr_trip);
		feature.append(float(length) );
		speed = np.diff(curr_trip);
		acc = np.diff(speed);
		speed = np.absolute(speed);
		acc = np.absolute(acc);
		feature.append(float(np.mean(speed) ));
		feature.append(float(np.mean(acc) ));
		feature.append(float(np.std(speed)) );
		feature.append(float( np.std(acc)));
		turnpar = num_turns(curr_trip);
		stoppar = stopping_param(curr_trip);
		feature.append(turnpar[0]/length);
		feature.append(turnpar[1]/length);
		feature.append(turnpar[2]);
		feature.append(stoppar[0]/length);
		feature.append(stoppar[1]);
		feature.append(stoppar[2]);
		features_list.append(feature);
	features_list = np.array(features_list);
	for i in range(len(features_list[0])):
		avg = np.mean(features_list[:,i]);
		stdev = np.std(features_list[:,i]);
		if stdev != 0:
			features_list[:,i] = (features_list[:,i] - avg)/stdev;

	return features_list;










#main method for testing the code
if __name__ == "__main__":

	valid_list = valid_drivers();
	trip = parsetrip(1,120);
	smooth_trip(trip);
	acc = np.diff(np.diff(trip));
	for i in range(len(acc)):
		t = cmath.polar(acc[i]);
		acc[i] = t[0];
	turn_par = num_turns(trip);
	print turn_par;
	stop_par = stopping_param(trip);
	print stop_par,len(trip);
	features_list = regression_parameters(parsedriver(1));
	print features_list[1:10,:];


