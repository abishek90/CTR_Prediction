import csv
import random

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




#main method for testing the code
if __name__ == "__main__":

	valid_list = valid_drivers();
	trip_list = createteset(1,6,20);
	for i  in range(len(trip_list)):
		print trip_list[i][0:10];


