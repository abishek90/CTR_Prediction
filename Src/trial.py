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

# This is an additional comment

#this is a comment