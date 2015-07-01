import numpy as np 
from numpy import *

def loadData(fileName):
	dataMat = []
	fr = open(fileName)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		#fltLine = map(lambda x:float(x) ,curLine)
		fltLine = map(float,curLine)
		dataMat.append(fltLine)
	return dataMat

def distEclud(vecA,vecB):
	#print type(np.sqrt(sum(np.power(vecA - vecB, 2))))
	#power = np.power(vecA - vecB ,2)
	#sq = np.sqrt(sum(power))
	#print sq
	return sqrt(sum(power(vecA - vecB, 2))) 

def randCent(dataSet , k ):
	n = np.shape(dataSet)[1]
	centroids = np.mat(np.zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j])-minJ)
		centroids[:,j] = minJ + rangeJ *np.random.rand(k,1)
	return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m,2)))#create mat to assign data points 
	                                  #to a centroid, also holds SE of each point
	centroids = createCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):#for each data point assign it to the closest centroid
			minDist = inf; minIndex = -1
			for j in range(k):
 				distJI = distMeas(centroids[j,:],dataSet[i,:])
				if distJI < minDist:
					minDist = distJI; minIndex = j
			if clusterAssment[i,0] != minIndex: clusterChanged = True
			clusterAssment[i,:] = minIndex,minDist**2
		print centroids
		for cent in range(k):#recalculate centroids
			ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
			centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean 
	return centroids, clusterAssment
#'''
def biKmeans(dataSet , k , distMeas = distEclud):
	m = shape(dataSet)[0]
	print type(m)
	clusterAssment = mat(zeros((m,2)))
	centroid0 = mean(dataSet , axis = 0).tolist()[0]
	centList = [centroid0]
	for j in range(m):
		clusterAssment[j,1] = distMeas(mat(centroid0) , dataSet[j,:])**2

	while(len(centList) < k ):
		lowestSSE = float("inf")
		for i in range(len(centList)):
			ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
			centroidMat, splitClustAss = kMeans(ptsInCurrCluster , 2 ,distMeas)
			sseSplit = sum(splitClustAss[:,1])
			sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1])
		print "sseSplit ans sseNotSplit" ,sseSplit,sseNotSplit
		if(sseSplit + sseNotSplit) < lowestSSE:
			bestCentToSplit = i
			bestNewCents = centroidMat
			bestClustAss = splitClustAss.copy()
			lowestSSE = sseSplit + sseNotSplit
		bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0]  = len(centList)
		bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0]  = bestCentToSplit
		print 'the bestCentToSplit is:', bestCentToSplit
		print 'the len of bestClustAss is:',len(bestClustAss)
		centList[bestCentToSplit] = bestNewCents[0,:]
		centList.append(bestNewCents[1,:].tolist()[0])
		clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] =bestClustAss
	return mat(centList) , clusterAssment
