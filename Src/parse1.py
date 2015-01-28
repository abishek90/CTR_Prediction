import csv
import random
import cmath
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn import svm
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.ensemble import RandomForestClassifier


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
	avg_acc = 0;
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
			avg_acc = avg_acc + np.absolute(np.mean(np.diff(np.diff(temp))));
			i = i + 5;
		else:
			i = i+1;
	turn_par = [];
	turn_par.append(float(c_l) );
	turn_par.append(float(c_r) );
	if c_l + c_r > 0:
		turn_par.append(float(avg_speed/(c_l+c_r)) );
		turn_par.append(float(avg_acc/(c_l+c_r)) );
	else:
		turn_par.append(0);
		turn_par.append(0);
	return turn_par;






#function to create a test set, where num trips from driver 'driver' is present and (total - num) trips of random drivers are added at the end.
def createteset(driver, num,total):
	main_list =  parsedriver(driver);
	trip_list = [];
	if num <= 200:
		my_sample = random.sample(range(200), num);
	else:
		my_sample =  np.random.randint(0,200, num);
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
		feature.append(turnpar[3]);
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
		else:
			features_list[:,i] = (features_list[:,i] - avg);

	return features_list;

#does logistic regression on the chosen paramters
def logit_predict(driver):
	num = 1000;
	total = 1200;
	train_list = createteset(driver,num,total);
	train_X = regression_parameters(train_list);
	train_Y = [];
	for i in range(total):
		if(i < num):
			train_Y.append(float(1) );
		else:
			train_Y.append(float(0) );
	logreg = linear_model.LogisticRegression(C=1e4);
	logreg.fit(train_X,train_Y);
	main_list = parsedriver(driver);
	test_X = regression_parameters(main_list);
	test_Y = logreg.predict_proba(test_X);
	return test_Y;

#does svr on the chosen parameters
def svm_predict(driver):
	num = 1000;
	total = 1200;
	train_list = createteset(driver,num,total);
	train_X = regression_parameters(train_list);
	train_Y = [];
	for i in range(total):
		if(i < num):
			train_Y.append(float(1) );
		else:
			train_Y.append(float(0) );
	clf = svm.SVC(C=100, gamma=100, kernel='rbf', probability=True);
	clf.fit(train_X,train_Y);
	main_list = parsedriver(driver);
	test_X = regression_parameters(main_list);
	test_Y = clf.predict_proba(test_X);
	return test_Y;


#does svr on the chosen parameters
def GBRT_predict(driver):
	num = 1000;
	total = 1200;
	train_list = createteset(driver,num,total);
	train_X = regression_parameters(train_list);
	train_Y = [];
	for i in range(total):
		if(i < num):
			train_Y.append(float(1));
		else:
			train_Y.append(float(0));
	clf = GradientBoostingClassifier(n_estimators = 200 , learning_rate = 0.5 , max_depth = 3);
	clf.fit(train_X,train_Y);
	main_list = parsedriver(driver);
	test_X = regression_parameters(main_list);
	test_Y = clf.predict_proba(test_X);
	print clf.classes_;
	print clf.predict(test_X);
	print test_Y;
	return test_Y;

# this turned out best for n_estimator = 50 (not much change in performance)
def cross_validation_RF(driver):
	num = 1000;
	total = 1200;
	number = [10 , 25 , 50 , 100 , 200 , 300 , 500];
	points = [];
	for i in range(len(number)):
		clf = RandomForestClassifier(n_estimators = number[i]);
		avg = 0;
		for j in range(10):
			train_list = createteset(driver,num,total);
			train_X = regression_parameters(train_list);
			train_Y = [];
			for i in range(total):
				if(i < num):
					train_Y.append(float(1));
				else:
					train_Y.append(float(0));
			scores = cross_validation.cross_val_score(clf,train_X,train_Y,scoring='accuracy',cv = 5);
			avg = avg + scores.mean();
		points.append(avg/10);

	return points; 
#gives the best results for C =  and gamma = 1500 , does not work at all
def cross_validation_svm(driver):
	num = 1000;
	total = 1200;
	number = [0.01, 0.1 , 1 , 10 , 100 , 1000, 10000];
	gnumber = [0.1, 1 , 10, 20, 100 , 500, 1000, 1500];
	points = [];
	for i in range(len(gnumber)):
		clf = svm.SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3,gamma=gnumber[i], kernel='rbf', max_iter=-1, probability=False, random_state=None,shrinking=True, tol=0.001, verbose=False);
		avg = 0;
		for j in range(10):
			train_list = createteset(driver,num,total);
			train_X = regression_parameters(train_list);
			train_Y = [];
			for i in range(total):
				if(i < num):
					train_Y.append(float(1));
				else:
					train_Y.append(float(0));
			scores = cross_validation.cross_val_score(clf,train_X,train_Y,cv = 5);
			avg = avg + scores.mean();
		points.append(avg/10);

	return points; 
#works best for c = 1e4
def cross_validation_logistic(driver):
	num = 1000;
	total = 1200;
	number = [0.01, 0.1 , 1, 10, 100, 1000, 10000];
	points = [];
	for i in range(len(number)):
		logreg = linear_model.LogisticRegression(C=number[i]);
		avg = 0;
		for j in range(10):
			train_list = createteset(driver,num,total);
			train_X = regression_parameters(train_list);
			train_Y = [];
			for i in range(total):
				if(i < num):
					train_Y.append(float(1));
				else:
					train_Y.append(float(0));
			scores = cross_validation.cross_val_score(logreg,train_X,train_Y,cv = 5);
			avg = avg + scores.mean();
		points.append(avg/10);

	return points; 

def RF_predict(driver):
	num = 1000;
	total = 1200;
	train_list = createteset(driver,num,total);
	train_X = regression_parameters(train_list);
	train_Y = [];
	for i in range(total):
		if(i < num):
			train_Y.append(float(1) );
		else:
			train_Y.append(float(0) );
	clf = RandomForestClassifier(n_estimators = 50);
	clf.fit(train_X,train_Y);
	main_list = parsedriver(driver);
	test_X = regression_parameters(main_list);
	test_Y = clf.predict_proba(test_X);
	return test_Y;

def combination_RFlogit(driver):
	num = 1000;
	total = 1200;
	train_list = createteset(driver,num,total);
	train_X = regression_parameters(train_list);
	train_Y = [];
	for i in range(total):
		if(i < num):
			train_Y.append(float(1) );
		else:
			train_Y.append(float(0) );
	clf1 = linear_model.LogisticRegression(C=1e4);
	clf11 = linear_model.LogisticRegression(C=1e4);
	clf2 = RandomForestClassifier(n_estimators = 50);
	clf1.fit(train_X, train_Y);
	clf2.fit(train_X, train_Y);
	train_list2 = createteset(driver,num,total);
	train_X2 = regression_parameters(train_list2);
	train_Y2 = [];
	for i in range(total):
		if(i < num):
			train_Y2.append(float(1) );
		else:
			train_Y2.append(float(0) );
	test_Y1 = clf1.predict_proba(train_X2)[:,1];
	test_Y2 = clf2.predict_proba(train_X2)[:,1];
	trainf = np.column_stack( (test_Y1.transpose(), test_Y2.transpose() ) );
	clf11.fit(trainf, train_Y2);
	main_list = parsedriver(driver);
	test_X = regression_parameters(main_list);
	l1 = clf1.predict_proba(test_X)[:,1] 
	l2 = clf2.predict_proba(test_X)[:,1]
	testf = np.column_stack((l1.transpose(), l2.transpose() ) );
	out = clf11.predict_proba(testf);
	return out;




def print_to_file(filename):
	fo = open(filename,'w');
	s = 'driver_trip,prob\n';
	fo.write(s);
	length = 1;
	for i in range(length):
	 	test = combination_RFlogit(valid_list[i]);
	 	for j in range(200):
	 		s = str(valid_list[i])+'_'+str(j+1)+','+str(test[j,1])+'\n';
	 		fo.write(s);
	 	if i%10 == 0:
	 		print i+1;
	fo.close();
















#main method for testing the code
if __name__ == "__main__":
	valid_list = valid_drivers();
	print_to_file('foo_cv.csv')
	#print cross_validation_RF(valid_list[11]);
	
	

	


