def loadDataSet(filepath):
	dataMat = []
	labelMat = []
	fr = open(filepath)
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0,float(lineArr[0]) , float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat,labelMat

def sigmoid(inX):
	return 1.0/(1+exp(-inX))

def gradAscent(dataMeatIn, classLabels):
	dataMatrix = mat(dataMeatIn)
	labelMat = mat(classLabels).transpose()
	m,n = shape(dataMatrix)
	maxCycle = 500
	weights = ones((n,1))
	for k in range(maxCycle):
		h = sigmoid(dataMatrix * weights)
		error = (labelMat -h)
		weights = weights + alpha*dataMatrix.transpose()*error
	return weights

def stocGradAscent0(dataMatrix , classLabels , numIter = 150):
	m,n = shape(dataMatrix)
	alpha = 0.01
	weights = ones(n)
	for i in range(m):
		h= sigmoid(sum(dataMatrix[i]*weights))
		error = classLabels[i] - h
		weights = weights + alpha * error * dataMatrix[i]
	return weights 

def stocGradAscent1(dataMatrix , classLabels):
	m,n = shape(dataMatrix)
	weights = ones(n)
	for j in range(numIter):
		dataIndex = range(m)
		for i in range(m):
			alpha = a/ (1.0 + j + i) + 0.01
			randIndex = int(random.uniform(0, len(dataIndex)))
			h = sigmoid(sum(dataMatrixp[randIndex]*weights))
			error = classLabels[randIndex] -  h
			weights = weights + alpha * error * dataMatrix[randIndex]
			del(dataIndex[randIndex])
	return weights
