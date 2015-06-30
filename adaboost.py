import numpy as np
def loadSimpData():
	dataMat = np.mat([[1. , 2.1],[2. , 1.1],[1.3 , 1.],[1. , 1.],[2. , 1.]])
	classLabels =[1.0 , 1.0 , -1.0 , -1.0 , 1.0]
	return dataMat , classLabels #this is test data and the input data nust be organized in this shape

def stumpClassify(dataMatrix , dimen , threshVal , threshIneq):
	retArray = np.ones((np.shape(dataMatrix)[0],1))
	if threshIneq ==  'lt':
		retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
	else:
		retArray[dataMatrix[:,dimen] > threshVal] = -1.0
	return retArray

def buildStump(dataArr , classLabels , D):
	dataMatrix = np.mat(dataArr)
	labelMat = np.mat(classLabels).T
	m,n = np.shape(dataMatrix)
	numSteps = 10.0 
	bestStump = {}
	bestClassEst = np.mat(np.zeros((m,1)))
	minError = float("inf")
	for i in range(n):
		rangeMin = dataMatrix[:,i].min()
		rangeMax = dataMatrix[:,i].max()
		stepSize = (rangeMax - rangeMin) / numSteps
		for j in range(-1 , int(numSteps)+1):
			for inequal in ['lt' , 'gt']:
				threshVal = (rangeMin + float(j) * stepSize)
				predictedVals  =stumpClassify(dataMatrix , i , threshVal , inequal)
				errArr = np.mat(np.ones((m,1)))
				errArr[predictedVals == labelMat] = 0
				weightedError = D.T*errArr
				if weightedError < minError:
					minError = weightedError
					bestClassEst = predictedVals.copy()
					bestStump['dim'] = i
					bestStump['thresh'] = threshVal
					bestStump['ineq'] = inequal
	return bestStump , minError , bestClassEst

def adaBoostTrainsDS(dataArr , classLabels , numIt = 40): #the numIt means the num of iterate
	weakClassArr = []
	m = np.shape(dataArr)[0]
	D = np.mat(np.ones((m,1))/m)
	aggClassEst = np.mat(np.zeros((m,1)))
	for i in range(numIt):
		bestStump, error ,classEst = buildStump(dataArr , classLabels , D)
		print "D",D.T
		alpha = float(0.5 * np.log((1.0-error)/max(error , np.e - 16 )))
		bestStump['alpha'] = alpha
		weakClassArr.append(bestStump)
		print "classEst" ,classEst.T
		labelMat = np.mat(classLabels)
		expon = np.multiply(-1*alpha * labelMat.T,classEst)
		D = np.multiply(D,np.exp(expon))
		D = D/D.sum()
		aggClassEst += alpha*classEst
		print "aggClassEst",aggClassEst.T
		aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T,np.ones((m,1)))
		errorRate = aggErrors.sum()/m
		print "total error ", errorRate,"\n"
		if errorRate == 0.0:
			break
	return weakClassArr

def adaClassify(datToClass , classfierArr):
	dataMatrix = np.mat(datToClass)
	m = np.shape(dataMatrix)[0]
	aggClassEst = np.mat(np.zeros((m,1)))
	for i  in rnage(len(classfierArr)):
		classEst = stumpClassify(dataMatrix , classfierArr[i]['dim'] , classfierArr[i]['thresh'], classfierArr[i]['ineq'])
		aggClassEst += classfierArr[i]['alpha']*classEst
		print aggClassEst
	return np.sign(aggClassEst)
