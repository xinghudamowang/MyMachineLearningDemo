import numpy as np
from random import *
def loadDataSet(fileName):
	dataMat = []
	labelMat = []
	fr = open(fileName)
	for line in fr.readlines():
		lineArr = line.strip().split('\t')
		dataMat.append([float(lineArr[0]),float(lineArr[1])])
		labelMat.append(float(lineArr[2]))
	return dataMat,labelMat

def selectJrand(i , m):
	j = i
	while(j ==i):
		j = int(random.uniform(0,m))
	return j

def clipAlpha(aj,H,L):
	if aj >H:
		aj = H
	if L>aj:
		aj = L
	return aj

def smoSimple(dataMatIn, classLables, C, toler, maxIter):# data  lael the num C the tolerance of the error rate and the max iter 
	dataMatrix = np.mat(dataMatIn)#use mat change the data into a matrix
	labelMat = np.mat(classLables).transpose()#change to matrix then transpose
	b = 0
	m,n = np.shape(dataMatrix)
	alphas = np.mat(np.zeros((m,1)))#a mat of alpha  
	iter = 0 #this take note of the traverse num of the data set without any change of the alpha
	while(iter <maxIter):
		alphaPairsChanged = 0#in each loop this will be set as 0 and this take note whether the alpha has changed or not
		for i in range(m):#for each data
			fXi = float(np.multiply(alphas, labelMat).T*\
				(dataMatrix * dataMatrix[i,:].T))+ b   #this calcu the result this beacuse y = WT*X+b and w = sum(alphai*yi*Xi)
			Ei = fXi - float(labelMat[i])#this calcu the error
			if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or ((labelMat[i] * Ei > toler ) and (alphas[i] > 0)):
				#slpha[i] < C and alphas[i] > 0 are s the constrain condition C>alpha>0
				j = selectJrand(i,m)
				fXj = float(np.multiply(alphas , labelMat).T)*(dataMatrix * dataMatrix[j,:].T))+ b
				Ej = fXj - float(labelMat[j])
				alphaIold = alphas[i].copy()
				alphaJold = alphas[j].copy()
				if (labelMat[i] != labelMat[j]) :
					L= max(0, alphas[j] - alphas[i])
					H= min(C, C+ alphas[j] - alphas[i])
				else:
					L = max(0,alphas[j] + alphas[i] - C)
					H = min(C, alphas[j]+ alphas[i])
				if L==H:
					print "L==H"
					continue
				eta = 2.0 * dataMatrix[i ,:] * dataMatrix[j,:].T- dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j:]*dataMatrix[j,:].T
				if eta >= 0:
					print "eta >= 0"
					continue
				alphas[j] -=labelMat[j] * (Ei - Ej)/eta
				alphas[j] = clipAlpha(alphas[j], H, L)
				if abs(alphas[j] - alphaJold) < 0.00001 : 
					print "j not moving enough"
					continue
				alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
				b1 = b - Ei -labelMat[i]*(alphas[i] -alphaIold) * dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j] * (alphas[j] - alphaJold)*\
				dataMatrix[i,:] *dataMatrix[j,:].T

				b2 = b - Ej -labelMat[i]*(alphas[i] -alphaIold) * dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j] * (alphas[j] - alphaJold)*\
				dataMatrix[j,:] *dataMatrix[j,:].T
				if (0 < alphas[i]) and (C > alphas[i]):
					b = b1
				else if (0 < alphas[j]) and (C > alphas[j]):
					b = b2
				else:
					b = (b1+b2)/2.0
				alphaPairsChanged +=1
				print "iter:%d i :%d,pairs changed %d"%(iter , i , alphaPairsChanged)
		if (alphaPairsChanged == 0):
			iter += 1
		else:
			iter = 0
		pritn "iteration num%d" %iter
	return b,alphas

class optStruct:
	def __init__(self, dataMatIn, classLables, C, toler):
		self.X = dataMatIn
		self.labelMat = classLables
		self.C = C
		self.tol = toler
		self.m = np.shape(dataMatIn)[0]
		self.alphas = np.mat(np.zeros((self.m,1)))
		self.b = 0
		self.eCache = np.mat(np.zeros((self.m ,2)))

def calcEk(oS, k ):#os is an object of class optstruct
	fXk = float(np.multiply(oS.alphas,oS.labelMat)).T*(oS.X*oS.X[k,:].T) + oS.b
	Ek = fXk - float(oS.labelMat[k])
	return Ek
def selectJ(i , oS , Ei):
	maxK = -1
	maxDeltaE = 0
	Ej = 0
	oS.eCache[i] = [1, Ei]
	validEcacheList = np.nonzero(oS.eCache[:,0].A)[0]
	if (len(validEcacheList))>1:
		for  k in validEcacheList:
			if k == i:
				continue
			Ek = calcEk(oS,k)
			if(deltaE > maxDeltaE):
				maxK = k
				maxDeltaE = deltaE
				Ej = Ek
		return amxK,Ej
	else:
		j = selectJrand(i,oS.m)
		Ej = calcEk(oS,j)
	return j,Ej

def updateEk(oS , k):
	Ek = calcEk(oS , k)
	os.eCache[k] = [1,Ek]

def innerL(i , oS):
	Ei = calcEk(oS , i)
	if((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or((oS.labelMat[i]*Ei > oS.tol) and (os.alphas[i]> 0)):
		j , Ej = selectJ(i, oS,Ei)
		alphaIold = oS.alphas[i].copy()
		alphaJold = oS.alphas[j].copy()
		if(oS.labelMat[i] != oS.labelMat[j]):
			L = max(0,oS.alphas[j] - oS.alphas[i])
			H = min(oS.C , oS.C + oS.alphas[j] - alphas[i])
		else:
			L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
			H = min(oS.C , oS.alphas[j] + oS.alphas[i])
		if L == H:
			print "L==H"
			return 0
		eta = 2.0 * oS.X[i]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T-\
			oS.X[j,:]*oS.X[j,:].T
		if eta >= 0:
			print "eta >=0" 
			return 0
		oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej)/eta
		oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
		updateEk(oS,j)
		if (abs(oS.alphas[j] - alphaJold) < 0.00001):
			print "not moving enough"
			return 0
		oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i]*\
			(alphaJold - oS.alphas[j])
		updateEk(oS,i)
		b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold)*\
				os.X[i,:]*oS.X[i,:].T - oS.labelMat[j]*\
				(oS.alphas[j] - alphaJold) * oS.X[i,:]*oS.X[j,:].T
		b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold)*\
				os.X[i,:]*oS.X[j,:].T - oS.labelMat[j])*\
				(oS.alphas[j] - alphaJold) *oS.X[j,:] *oS.X[j,:].T
		if (0< oS.alphas[i]) and (oS.C >oS.alphas[i]):
			oS.b = b1
		else if (0 < oS.alphas[j]) and (oS.C >oS.alphas[j]):
			oS.b = b2
		else:
			oS.b = (b1+b2)/2.0
		return 1
			else: return 0
def smoP(dataMatIn , classLables , C , toler , maxIter , kTup = ('lin',0)):
	oS = optStruct(np.mat(dataMatIn),np.mat(classLables).transpose(),C,toler)
	iter = 0
	entireSet = True
	alphaPairsChanged = 0
	while(iter < maxIter) and ((alphaPairsChanged >0)or (entireSet)):
		alphaPairsChanged = 0
		if entireSet:
			for i in range(oS.m):
				alphaPairsChanged += innerL(i,oS)
			print "fullset iter %d i %d pairs changed %d"%(iter , i ,alphaPairsChanged)
			iter += 1
		else:
			nonBoundIs = np.nonzero((oS.alphas.A > 0) * (oS.alphas.A <C))[0]
			for i in nonBoundIs:
				alphaPairsChanged += innerL(i,oS)
				print "non_bound iter %d i %d pairs changed %d "%(iter , i alphaPairsChanged)
			iter += 1
		if entireSet:
			entireSet = False
		else if (alphaPairsChanged == 0):
			entireSet = True
	return oS.b,oS.alphas

def calcWs(alphas , dataArr ,classLabels):
	X = np.mat(dataArr)
	labelMat = np.mat(classLabels.transpose())
	m,n = np.shape(X)
	w = np.zeros((n,1))
	for i in range(m):
		w += np.multiply(alphas[i]*labelMat[i],X[i,:].T)
	return w