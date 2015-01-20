import csv
import numpy as np 
import scipy
from scipy import signal, misc
import matplotlib.pyplot as plt

def parsetrip(driver,trip):
	s = '../../Data/drivers/' + str(driver) + '/' + str(trip) +'.csv';
	f = open(s,'r');
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


def parsedriver(driver):
	driver_list = [];
	for i in range(200):
		a = parsetrip(driver,i+1);
		driver_list.append(a);
	return driver_list;


# This function computes the element wise difference of each trip
def compute_diff(trip_list):
	num_trips = len(trip_list);
	trip_list_diff = trip_list;
	for i in range(num_trips):
		curr_trip = trip_list[i];
		trip_len = len(curr_trip);
		for j in range(trip_len):
			if ( j > 0):
				trip_list_diff[i][j] = trip_list[i][j] - trip_list[i][j-1];
			else:
				trip_list_diff[i][j] = 0;
	return trip_list_diff;


# This function outputs a list of arrays with all arrays being of the same size
def normalize_trip_list(trip_list):
	norm_trip_list = trip_list;
	num_trips = len(trip_list);
	max_length = 0;
	for i in range(num_trips):
		curr_len = len(trip_list[i]);
		if (curr_len > max_length):
			max_length = curr_len;

	for j in range(num_trips):
		norm_trip_list[j] = scipy.signal.resample(trip_list[j],max_length, scipy.signal.get_window(boxcar,max_length));
	return norm_trip_list;

# This function computes the Fourier Transform of each of the rows.
def compute_transform(trip_list):
	transform_list = trip_list;
	num_trips = len(trip_list);
	for i in range(num_trips):
		transform_list[i] = np.fft.fft(trip_list[i]);
	return transform_list



if __name__ == "__main__":

	drive_1_diff = compute_diff(parsedriver(1));
	drive_1_norm = normalize_trip_list(drive_1_diff);
	drive_1_transform = compute_transform(drive_1_norm);
	for i in range(len(drive_1_transform)):
		print len(drive_1_transform[i]);
	print len(drive_1_transform);








