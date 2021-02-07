# Matthew McCracken
# python knapsack.py -f tests/test1.txt -r

import sys
import math
import time
import random

# knapsack class to store data about the bag and potential items
class knapsack:
	maxWeight = 0.0
	allItems = []
	exWeights = []
	exValues = []
	exItems = []
	numberOfItems = 0
	pickedItems = []

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
			newKnapsack.exWeights.append(int(tempList[1]))
			newKnapsack.exValues.append(int(tempList[2]))

		# any method except for exhaustive search goes here as they work the same way
		else:
			# split the list into different elements based on the commas locations
			newKnapsack.allItems.append(line.split(','))

			# convert weight and value to ints
			newKnapsack.allItems[-1][1] = int(newKnapsack.allItems[-1][1])
			newKnapsack.allItems[-1][2] = int(newKnapsack.allItems[-1][2])

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
	totalItems = 0

	# iterate through all items and take each until the bag is full
	for i in ks.allItems:

		# check to make sure the new item is not too heavy
		if i[1] <= int(ks.maxWeight) - currentWeight:

			# add the item to list and add its weight to the total
			ks.pickedItems.append(i)
			currentWeight += i[1]
			totalValue += i[2]
			totalItems += 1

	# output value
	return totalValue, currentWeight, totalItems

def greedyHillClimbing(ks):

	# hold max value for comparing
	maxValue = 0

	# temporary lists to decide which greedy approach is best
	weightItems = []
	valueItems = []
	ratioItems = []

	# greedy by weight approach
	sortByWeight(ks)
	weightMax = pickItems(ks)[0]
	weightItems = ks.pickedItems
	ks.pickedItems = []

	# greedy by value approach
	sortByValue(ks)
	valueMax = pickItems(ks)[0]
	valueItems = ks.pickedItems
	ks.pickedItems = []

	# greedy by ratio approach
	sortByRatio(ks)
	ratioMax = pickItems(ks)[0]
	ratioItems = ks.pickedItems
	ks.pickedItems = []

	# if ratio max is the highest value save value and items picked
	if ratioMax >= weightMax and ratioMax >= valueMax:
		maxValue = ratioMax
		ks.pickedItems = ratioItems

	# if value max is the highest value save value and items picked
	elif valueMax >= ratioMax and valueMax >= weightMax:
		maxValue = valueMax
		ks.pickedItems = valueItems

	# weight max must be the highest value so save value and items picked
	else:
		maxValue = weightMax
		ks.pickedItems = ratioItems

	# begin hill climbing

	# go through some amount of the list testing values
	iterations = math.ceil(int(ks.numberOfItems)*5)

	# iterate through items in list
	for i in range(len(ks.pickedItems)):

		# repeat random testing until reaching iterations
		for j in range(iterations):

			# cap time if needed
			if time.time() > hcTimeout:
				sys.exit(filename + " Reached max time")

			# get random index of all items to test in place of i
			testIndex = random.randint(0,int(ks.numberOfItems)-1)

			# if the random value selected is already in the list it cannot be added
			if ks.allItems[testIndex] in ks.pickedItems:
				continue

			# if the weight becomes greater than the max possible weight it cannot be used
			if int(ks.maxWeight) - int(ks.pickedItems[i][1]) + int(ks.allItems[testIndex][1]) <= int(ks.maxWeight):

				# if new max value is greater than old and it made it through previous checks, switch old values with new ones
				if maxValue - int(ks.pickedItems[i][2]) + int(ks.allItems[testIndex][2]) > maxValue:
					maxValue = maxValue - int(ks.pickedItems[i][2]) + int(ks.allItems[testIndex][2])
					ks.pickedItems[i] = ks.allItems[testIndex]
					break

			# if the weight is too much, check a combination of 2 random new items

			# generate 2nd random index to try
			testIndex2 = random.randint(0,int(ks.numberOfItems)-1)

			# check to make sure we are not at the end of i, test indeices are different, and the new value does not already exist
			if i < len(ks.pickedItems)-1 and testIndex != testIndex2 and ks.allItems[testIndex2] not in ks.pickedItems:

				# make sure it not above the max weight
				if int(ks.maxWeight) - int(ks.pickedItems[i][1]) - int(ks.pickedItems[i+1][1]) + int(ks.allItems[testIndex][1]) + int(ks.allItems[testIndex2][1]) <= int(ks.maxWeight):
					
					# see if we found a better value between the 2 random values and update variables if so
					if maxValue - int(ks.pickedItems[i][2]) - int(ks.pickedItems[i+1][2]) + int(ks.allItems[testIndex][2]) + int(ks.allItems[testIndex2][2]) > maxValue:
						maxValue = maxValue - int(ks.pickedItems[i][2]) - int(ks.pickedItems[i+1][2]) + int(ks.allItems[testIndex][2]) + int(ks.allItems[testIndex2][2])
						ks.pickedItems[i] = ks.allItems[testIndex]
						ks.pickedItems[i+1] = ks.allItems[testIndex2]

	# get current weight and total items
	currentWeight = 0
	totalItems = 0
	for i in ks.pickedItems:
		currentWeight += int(i[1])
		totalItems += 1

	# return the max value found
	return maxValue, currentWeight, totalItems

def getExhaustiveBagStats(ks):

	# convert values in lists to ints
	for i in range(int(ks.numberOfItems)):
		ks.exWeights[i] = int(ks.exWeights[i])
		ks.exValues[i] = int(ks.exValues[i])

	# initialize table
	tempList = [[0 for i in range(int(ks.maxWeight)+1)] for j in range(int(ks.numberOfItems)+1)]
			
	# Create Table
	for i in range(int(ks.numberOfItems)+1):
		for j in range(int(ks.maxWeight)+1):

			# initialize table
			if i == 0 or j == 0:
				tempList[i][j] = 0

			# check if weight is possible
			elif ks.exWeights[i-1] <= j:

				# get values for 2 different possibilities
				a = ks.exValues[i-1] + tempList[i-1][j-ks.exWeights[i-1]]
				b = tempList[i-1][j]

				# compare them and save the greater one
				if a >= b:
					tempList[i][j] = a
				else:
					tempList[i][j] = b

			# otherwise, keep old value
			else:
				tempList[i][j] = tempList[i-1][j]

	# save answer
	totalValue = tempList[int(ks.numberOfItems)][int(ks.maxWeight)]
	totalValueCopy = totalValue
	totalWeight = 0
	totalItems = 0
	
	# loop through bag
	for i in range(int(ks.numberOfItems), 0, -1):

		# if we reach the end
		if totalValue <= 0:
			break

		# rejected item
		if tempList[i-1][int(ks.maxWeight)] == totalValue:
			continue

		# otherwise it was accepted
		else:

			# This item is included.
			totalItems += 1
			totalWeight += ks.exWeights[i-1]
			
			# subtract value from total
			ks.maxWeight = int(ks.maxWeight) - ks.exWeights[i-1]
			totalValue = totalValue - ks.exValues[i-1]

	# return resulting bag stats
	return totalValueCopy, totalWeight, totalItems

def exhaustiveSearchWithPruning(maxWeight, weightsList, valuesList, totalItems):

	if time.time() > timeout:
		with open("ep.csv", "a") as myfile:
			myfile.write(filename[filename.index('\\')+1:])
			myfile.write(",")
			myfile.write("Exhaustive With Pruning")
			myfile.write(",undef,undef,undef,MAX\n")
		sys.exit(filename + " Reached max time")

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

			if time.time() > timeout:
				sys.exit(filename + " Reached max time")

			# keep track of testing variables in case they are better than max values
			myIndex = ks.exItems.index(j)
			currentWeight += ks.exWeights[myIndex]
			currentValue += ks.exValues[myIndex]

		# test to see if the new values are better than the older ones and save them if they are
		if currentWeight <= int(ks.maxWeight) and currentValue > maxValue:
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
		if time.time() > timeout:
			sys.exit(filename + " Reached max time")

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
hillClimbing = False

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
    elif sys.argv[i] == "-h":
    	hillClimbing = True

# make sure user passed in all required data
if filename == "":
	sys.exit("pass in the name of a file (-f <filename>)")
elif not exhaustiveSearchWithPruningMethod and not exhaustiveSearchWithoutPruningMethod and not weightSort and not valueSort and not ratioSort and not hillClimbing:
	sys.exit("specify a method of solving (-e, -ep, -w, -v, -r, -h)")

# create the knapsack object from the file
ks = createKnapsack(filename)

# start the timer after reading from file and sanitizing input
start_time = time.time()

timeout = time.time() + 60*20
hcTimeout = time.time() + 60*5

# pick a solution method and output the resulting value
if weightSort:
	sortByWeight(ks)
	res = pickItems(ks)
	timeCopy = round((time.time()-start_time) * 1000)
	print(filename, int(res[1]), int(res[0]), int(res[2]), timeCopy, sep=',')

elif valueSort:
	sortByValue(ks)
	res = pickItems(ks)
	timeCopy = round((time.time()-start_time) * 1000)
	print(filename, int(res[1]), int(res[0]), int(res[2]), timeCopy, sep=',')

elif ratioSort:
	sortByRatio(ks)
	res = pickItems(ks)
	timeCopy = round((time.time()-start_time) * 1000)
	print(filename, int(res[1]), int(res[0]), int(res[2]), timeCopy, sep=',')

elif exhaustiveSearchWithPruningMethod:
	tv = exhaustiveSearchWithPruning(int(ks.maxWeight), ks.exWeights, ks.exValues, int(ks.numberOfItems))
	timeCopy = round((time.time()-start_time) * 1000)
	res = getExhaustiveBagStats(ks)
	print(filename, int(res[1]), int(tv), int(res[2]), timeCopy, sep=',')

elif exhaustiveSearchWithoutPruningMethod:
	tv = exhaustiveSearchWithoutPruning(ks)
	timeCopy = round((time.time()-start_time) * 1000)
	res = getExhaustiveBagStats(ks)
	print(filename, int(res[1]), int(tv), int(res[2]), timeCopy, sep=',')

elif hillClimbing:
	res = greedyHillClimbing(ks)
	timeCopy = round((time.time()-start_time) * 1000)
	print(filename, int(res[1]), int(res[0]), int(res[2]), timeCopy, sep=',')