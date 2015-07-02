# -*- coding: utf-8 -*-
from numpy import *


def loadData():
	return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]] # test data

def createCl(dataSet):
	Cl = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in Cl:
				Cl.append([item])
	Cl.sort()
	return map(frozenset , Cl)#map c1 to the frozenset so that the element could be used as the key  in dict  in ssCnt

def scanD(D, Ck, minSupport):
	#D = map(set,D)
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not ssCnt.has_key(can):
					ssCnt[can] = 1
				else:
					ssCnt[can] +=1
	numItems = float(len(D))
	retLis = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >= minSupport:
			retLis.insert(0,key)
		supportData[key] = support
	return retLis , supportData

def aprioriGen(Lk, k):#create Ck use Lk k 表示又Lk 产生的频繁项集的每个集合的频繁项个数 例如  L1  产生C1  由一个 产生两个频繁向的集合，则k= 2
	retLis = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			if L1 == L2:
				retLis.append(Lk[i] | Lk[j])
	return retLis

def apriori(dataSet , minSupport = 0.5):#apriori  调用apriorigen 产生频繁项集
	C1 = createCl(dataSet)
	D = map(set , dataSet)
	L1 , supportData = scanD(D , C1 , minSupport)
	L = [L1]
	k = 2
	while(len(L[k-2])>0):
		Ck = aprioriGen(L[k-2],k)
		Lk , supK = scanD(D,Ck,minSupport) #产生Lk  以及计算支持度  如L1-->L2  计算L2中集合的支持度
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L,supportData
#'''
def generateRules(L,supportData, minConf = 0.7):
	bigRuleList =[]
	for i in range(1,len(L)):#从频繁项集 的第二个开始（集合中项数为2）创建规则
		for freqSet in L[i]:
			H1 = [frozenset([item]) for  item in freqSet] 
			#print "H",H1
			if(i>1):
				rulesFromConseq(freqSet , H1 , supportData , bigRuleList , minConf)#当i>1 继续生成规则 
			else:
				calcConf(freqSet , H1 , supportData , bigRuleList , minConf) #i = 1 时候  集合中只有两个元素，计算规则的置信度
	return bigRuleList #返回规则

def calcConf(freqSet , H , supportData , br1, minConf = 0.7):
	prunedH = []#存放生成的规则
	for conseq in H:
		conf = supportData[freqSet]/supportData[freqSet - conseq]
		if conf >= minConf:
			print freqSet-conseq, '--->' ,conseq , 'conf:' ,conf
			br1.append((freqSet-conseq,conseq , conf))
			prunedH.append(conseq)
			#print "prunedH",prunedH
	#print "total",prunedH
	return prunedH

def rulesFromConseq(freqSet , H , supportData , br1 , minConf = 0.7):
	m = len(H[0])
	if(len(freqSet) > (m+1)):
		Hmp1 = aprioriGen(H ,m+1)
		Hmp1 = calcConf(freqSet ,Hmp1, supportData , br1, minConf)
		if (len(Hmp1) > 1):
			rulesFromConseq(freqSet , Hmp1, supportData, br1, minConf)

