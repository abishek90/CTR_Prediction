import numpy as np 
import scipy
from scipy import signal, misc
import matplotlib.pyplot as plt

# This function computes the element wise difference of each trip
def compute_diff(trip_list):
	num_trips = len(trip_list);
	trip_list_diff = [];
    for i in range(len(trip_list)):
    	curr_trip = trip_list[i];
    	curr_trip = np.diff(curr_trip);
    	curr_trip = np.diff(curr_trip);
    	trip_list_diff.append(curr_trip);
    return trip_list_diff;


# This function outputs a list of arrays with all arrays being of the same size
def normalize_trip_list(trip_list):
	norm_trip_list = [];
	num_trips = len(trip_list);
	max_length = 0;
	for i in range(num_trips):
		curr_len = len(trip_list[i]);
		if (curr_len > max_length):
			max_length = curr_len;

	for j in range(num_trips):
		norm_trip_list[j] = scipy.signal.resample(trip_list[j],max_length);
	return norm_trip_list;

# This function computes the Fourier Transform of each of the rows.
def compute_transform(trip_list):
	transform_list = [];
	num_trips = len(trip_list);
	for i in range(num_trips):
		transform_list[i] = numpy.fft.fft(trip_list[i]);
	return transform_list









