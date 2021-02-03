# Matthew McCracken
# python knapsack.py -f test1.txt -r
# search for "# debug" and uncomment to store which items are being taken

import sys
import math
import time

# knapsack class to store data about the bag and potential items
class knapsack:
	maxWeight = 0.0
	allItems = []
	exWeights = []
	exValues = []
	exItems = []
	numberOfItems = 0
	# debug
	# pickedItems = []

# function to read from the file and populate a knapsack object
def createKnapsack(filename):

	# open file
	f = open(filename, "r")

	# instantiate new knapsack object
	newKnapsack = knapsack()

	# get max weight and # of items
	line = f.readline()
	line = line.rstrip('\n')
	line = line.rstrip(' ')
	tempList = line.split(',')
	newKnapsack.numberOfItems = tempList[0]
	newKnapsack.maxWeight = tempList[1]

	# get all possible items and put it into a list + manipulate the data
	line = f.readline()
	while (line != ''):
		# remove the endline character
		line = line.rstrip('\n')
		line = line.rstrip(' ')

		# check if exhaustive search is being used because I am going to implement it differently
		if exhaustiveSearchWithPruningMethod or exhaustiveSearchWithoutPruningMethod:
			tempList = line.split(',')
			newKnapsack.exItems.append(tempList[0])
			newKnapsack.exWeights.append(float(tempList[1]))
			newKnapsack.exValues.append(float(tempList[2]))

		# any method except for exhaustive search goes here as they work the same way
		else:
			# split the list into different elements based on the commas locations
			newKnapsack.allItems.append(line.split(','))

			# convert weight and value to floats
			newKnapsack.allItems[-1][1] = float(newKnapsack.allItems[-1][1])
			newKnapsack.allItems[-1][2] = float(newKnapsack.allItems[-1][2])

			# append the value:weight ratio onto the end of each nested list
			newKnapsack.allItems[-1].append(newKnapsack.allItems[-1][2] / newKnapsack.allItems[-1][1])

			# convert the nested list into a nested tuple
			newKnapsack.allItems[-1] = tuple(newKnapsack.allItems[-1])

		# read the next line
		line = f.readline()

	# close file and return knapsack object
	f.close()
	return newKnapsack

# sort the list by its value:weight ratio
def sortByRatio(ks):
	ks.allItems.sort(key=lambda x:x[3], reverse=True)
	return ks

# sort the list by its value
def sortByValue(ks):
	ks.allItems.sort(key=lambda x:x[2], reverse=True)
	return ks

# sort the list by its weight
def sortByWeight(ks):
	ks.allItems.sort(key=lambda x:x[1], reverse=False)
	return ks

# pick which items go in the bag based on how they were sorted
def pickItems(ks):

	# declare function variables
	currentWeight = 0.0
	totalValue = 0.0

	# iterate through all items and take each until the bag is full
	for i in ks.allItems:

		# check to make sure the new item is not too heavy
		if i[1] <= float(ks.maxWeight) - currentWeight:

			# add the item to list and add its weight to the total
			# debug
			# ks.pickedItems.append(i)
			currentWeight += i[1]
			totalValue += i[2]

	# output value
	return totalValue

def exhaustiveSearchWithPruning(maxWeight, weightsList, valuesList, totalItems):

	# base case: if we run out of items to try or run out of bag space return 0
	if maxWeight == 0 or totalItems == 0:
		return 0

	# if last item in list (i.e. item about to be checked) has a weight greater than max
	# remove item from pool, mostly for edge case use
	if (weightsList[totalItems-1] > maxWeight):
		return exhaustiveSearchWithPruning(maxWeight, weightsList, valuesList, totalItems-1)

	# otherwise, continue down tree of possibilities and take the max of each option on the way back up
	else:
		a = valuesList[totalItems-1] + exhaustiveSearchWithPruning(maxWeight - weightsList[totalItems-1], weightsList, valuesList, totalItems-1)
		b = exhaustiveSearchWithPruning(maxWeight, weightsList, valuesList, totalItems-1)
		if a >= b:
			return a
		else:
			return b

def exhaustiveSearchWithoutPruning(ks):

	# get power set
	ks.allItems = getPowerSet(ks.exItems)

	# declare variables to hold max values
	maxValue = 0.0

	# declare variables to hold testing values
	currentWeight = 0.0
	currentValue = 0.0

	# iterate through power set
	for i in ks.allItems:
		for j in i:

			# keep track of testing variables in case they are better than max values
			myIndex = ks.exItems.index(j)
			currentWeight += ks.exWeights[myIndex]
			currentValue += ks.exValues[myIndex]

		# test to see if the new values are better than the older ones and save them if they are
		if currentWeight <= float(ks.maxWeight) and currentValue > maxValue:
			maxValue = currentValue

		# reset values of testing variables for next iteration
		currentValue = 0.0
		currentWeight = 0.0

	# return maximum value found
	return maxValue

# function to get a power set given a list of items
def getPowerSet(myList):

	# gets list length
	size = len(myList)

	# temporary list to copy values into
	tempList = []

	# go through list getting every possible subset
	for i in range(1 << size):
		tempList.append([myList[j] for j in range(size) if (i & (1 << j))])

	# return the templist that now contains all subsets
	return tempList

# user input variables
filename = ""
exhaustiveSearchWithPruningMethod = False
exhaustiveSearchWithoutPruningMethod = False
weightSort = False
valueSort = False
ratioSort = False

# get user input for method of solving and test filename
n = len(sys.argv)
for i in range(1, n):
    if sys.argv[i] == "-f":
    	filename = sys.argv[i+1]
    elif sys.argv[i] == "-e":
    	exhaustiveSearchWithoutPruningMethod = True
    elif sys.argv[i] == "-ep":
    	exhaustiveSearchWithPruningMethod = True
    elif sys.argv[i] == "-w":
    	weightSort = True
    elif sys.argv[i] == "-v":
    	valueSort = True
    elif sys.argv[i] == "-r":
    	ratioSort = True

# make sure user passed in all required data
if filename == "":
	sys.exit("pass in the name of a file (-f <filename>)")
elif not exhaustiveSearchWithPruningMethod and not exhaustiveSearchWithoutPruningMethod and not weightSort and not valueSort and not ratioSort:
	sys.exit("specify a method of solving (-e, -ep, -w, -v, -r)")

# create the knapsack object from the file
ks = createKnapsack(filename)

# start the timer after reading from file and sanitizing input
start_time = time.time()

# pick a solution method and output the resulting value
if weightSort:
	sortByWeight(ks)
	print("Max Value:", pickItems(ks))
elif valueSort:
	sortByValue(ks)
	print("Max Value:", pickItems(ks))
elif ratioSort:
	sortByRatio(ks)
	print("Max Value:", pickItems(ks))
elif exhaustiveSearchWithPruningMethod:
	print("Max Value:", exhaustiveSearchWithPruning(float(ks.maxWeight), ks.exWeights, ks.exValues, int(ks.numberOfItems)))
elif exhaustiveSearchWithoutPruningMethod:
	print("Max Value:", exhaustiveSearchWithoutPruning(ks))

# print final runtime
print("Time(sec):", round(time.time() - start_time, 5))