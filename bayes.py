import numpy as np
import math
def loadDataSet():
	postingList = [['my','dog','has','flea','problems','help','please'],
					['maybe','not','take','him','to','dog','park','stupid'],
					['my','dalmation','is','so','cute','I','love','him'],
					['stop','posting','stupid','worthless','garbage'],
					['mr','licks','ate','my','steak','how'],
					['quit','buying','worthless','dog','food','stupid']]
	classVec = [0,1,0,1,0,1]
def creatVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
		return lis(vocabSet)
def setOfWordsVec(vocabList , inputSet):
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word %s is not in my Vocab"%word
	return returnVec

def  trainNB0(trainMatrix , trainCategory):#trainCategory is the class list of the document
	numTrainDocs = len(trainMatrix)# the num of the document
	numWords = len(trainMatrix[0])#num of the word in every document
	pAbusive = sum(trainCategory)/float(numTrainDocs)#calcu the prob of the P(Ci) in this statement calcu the P(C1)
	p0Num = ones(numWords)#generate  an array of zero
	p1Num = ones(numWords)#the same as above
	p0Denom = 2.0
	p1Denom = 2.0
	for i in range(numTrainDocs):#in each document
		if trainCategory[i] = 1: #if the document i is class 1
			p1Num += trainMatrix[i]#this calcu the num of each word in the vovablist in each document
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]#class 0
			p0Denom += sum(trainMatrix[i])
	p1Vec = log(p1Num/p1Denom)#this is the prob of P(W|C1) Which means the prob of the appearance of the word wj(wj is the word in cocablist) 
	#in document i when the document belongs to Class1
	p0Vec = log(p0Num/p0Denom) #to avoid underflow use log
	return p0Vec,p1Vec,pAbusive  #this return the P(W|C0) P(W|C1) and the P(C1)

def classifyNB(vec2Classfy , p0Vec , p1Vec , pClass1):
	p1 = sum(vec2Classfy * p1Vec) +log(pClass1)#this calcu the prob that a document belongs to class1
	p0 = sum(vec2Classfy * p0Vec) +log(1.0 - plcass1)
	if p1> p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts , listClasses = loadDataSet()#
	myVocabList = creatVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWordsVec(myVocabList , postinDoc))
	p0V , p1V , pAb = trainNB0(array(trainMat),array(listClasses))
	testEntry = ['love','my','dalmation']
	thisDoc = array(setOfWordsVec(myVocabList, testEntry))
	print testEntry , 'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)
	testEntry = ['stupid' , 'garbage']
	thisDoc = array(setOfWordsVec(myVocabList , testEntry))
	print testEntry, 'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)()

def bagWord2VecMN(vocabList , inputSet):
	returnVec = [0] *len(vocabList,inputSet)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
	return returnVec