import csv
import random
import math
import operator

mydict = {'Winter Storm': 6, 'Lake-Effect Snow': 4, 'Extreme Cold/Wind Chill': 2,'Winter Weather': 1, 'Blizzard': 7, 'Heavy Snow': 3,'High Wind': 8, 'Hail': 5, 'Flood': 12, 'Tornado': 11, 'Flash Flood': 15, 'Coastal Flood': 13, 'Funnel Cloud': 14, 'Heavy Rain': 10, 'Excessive Heat': 16, 'Thunderstorm Wind': 9}
def scrambled(orig):
	dest = orig[:]
	random.shuffle(dest)
	return dest

def loadDataset(f, split, trnSet=[], tstSet=[]):
	print("Loading Dataset")
	with open(f, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		dataset = scrambled(dataset)
		for x in range(len(dataset)-1):
			for y in range(4):
				if y == 0:
					dataset[x][y] = float(mydict[dataset[x][y]])
				elif y== 2:
					dataset[x][y] = float(dataset[x][y][:-1])
				else:
					dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				trnSet.append(dataset[x])
			else:
				tstSet.append(dataset[x])

def eucDist(inst1, inst2, length):
	dist = 0
	for x in range(length):
		if x == 3:
			dist += pow((inst1[x]*3) - (inst2[x]*3), 2)
		elif x == 1:
			dist += pow((inst1[x]/180) - (inst2[x]/180), 2)
		else:
			dist += pow((inst1[x] - inst2[x]), 2)
	return math.sqrt(dist)

def getNeighbors(trnSet, tstInst, k):
	distances = []
	length = len(tstInst)-1
	for x in range(len(trnSet)):
		dist = eucDist(tstInst, trnSet[x], length)
		distances.append((trnSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(tstSet, predictions):
	print("Calculating Accuracy")
	correct = 0
	for x in range(len(tstSet)):
		if tstSet[x][-1] == predictions[x]:
			correct += 1
		if x%50==0:
			print("Correct: {0}/{1}".format(correct, x))
	return (correct/float(len(tstSet))) * 100.0


if __name__ == '__main__':
	trnSet = []
	tstSet = []
	split = 0.70
	loadDataset('please.csv', split, trnSet, tstSet)
	predictions = []
	k = 200
	print("Calculating euc dist and finding neighbors")
	for x in range(len(tstSet)):
		neighbors = getNeighbors(trnSet, tstSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
	accuracy = getAccuracy(tstSet, predictions)
	print('Accuracy: {0}%'.format(accuracy))