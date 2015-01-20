import csv
f = open("train","r")

csvreader1 = csv.reader(f)
for i in range(3):
	print 
# A baseline is just to compute the fraction of times a particular ad was clicked
numlines = 0;
for lines in f:
	numlines +=1
print numlines

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

#this is a comment