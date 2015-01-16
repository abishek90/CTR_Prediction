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