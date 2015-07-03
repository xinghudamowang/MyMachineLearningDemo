# -*- coding: utf-8 -*-
from numpy import *
class treeNode():
	def __init__(self,nameValue , numOccur , parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None #Lianjie相似的元素项
		self.parent = parentNode#当前节点的父节点
		self.children = {}#节点的子节点
	def inc(self, numOccur):
		self.count += numOccur

	def disp(self,ind = 1):#display tree 
		print ' ' * ind ,self.name,'',self.count
		for child in self.children.values():
			child.disp(ind+1)

def creatTree(retDict , minSup = 1):#retDict 是  createInitSet 的返回结果
	headerTable = {}
	for trans in retDict:
		for item in trans:#trans 是dict的key 是一个frozenset  即每条数据
			headerTable[item] = headerTable.get(item,0) + retDict[trans]#遍历了数据集并统计每个元素出现的频率，得到的headerTable里的key 
			# 以及value	
	for k in headerTable.keys(): #删除小于最小支持度的
		if headerTable[k] < minSup:
			del(headerTable[k])
	freqItemSet = set(headerTable.keys())#建立一个频繁1项集
	if len(freqItemSet) == 0:return None,None#集合为空

	for k in headerTable:#k 是 headerTable 的key
		headerTable[k] = [headerTable[k] , None]#重新初始化headerTable  ，headerTable除了存储每个项目的频次，还存储该项的指针
	retTree = treeNode('Null_Set', 1, None)#初始化树，建立根节点
	for tranSet , count in retDict.items():# retDict的key & value
		print count
		localD = {}
		for item in tranSet:#每个key 中的值  即 每条项目数据的每个项#第一次扫描数据集
			if item in freqItemSet:#如果item是符合大于最小支持度的
				localD[item] = headerTable[item][0]#将item 加入字典，值为该item在headerTable中的值
				# localD 中的item是对源数据集中一条项目剔除项目中非频繁1项集中的项之后形成的新项，并在后面进行排序
				#例如['r', 'z', 'h', 'j', 'p'] 剔除非频繁1项集中的项之后为['r', 'z'] 下次循环进行下一条的处理
				#localD的值为{'r':headerTable[item][0],'z':headerTable[item][0]}
		if len(localD) > 0:#
			orderedItems = [v[0] for v in sorted(localD.items(),key = lambda p: p[1],reverse = True)]#对localID根据value值降序排序

			updateTree(orderedItems , retTree, headerTable, count)#更新树 即利用排序后的localD 生成FP树
	return retTree , headerTable

def updateTree(items , inTree, headerTable, count):
	if items[0] in inTree.children:
		inTree.children[items[0]].inc(count)#如果该频繁1项集的项在子树种，子树值+1
	else:
		inTree.children[items[0]] = treeNode(items[0],count ,inTree)#否则建立新节点值为1
		if headerTable[items[0]][1] == None:#如果headerTable 中对应的频繁1项集的项的指针为空  则指向该节点
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1],inTree.children[items[0]])#更新headerTable，具体见updateHeader
	if len(items) >1:
		updateTree(items[1::],inTree.children[items[0]],headerTable, count)#对剩下的items更新树

def updateHeader(nodeToTest ,targetNode):
	while(nodeToTest.nodeLink != None):#当对应项指向非空对应项指向的节点的nodeLink指针指向新插入节点
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode

def loadSimpDat():#data for test
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):#初始化数据集，将每条数据作为字典的key 字典的值为 数据的出现频次，置为1
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

# 寻找条件模式基
#条件模式基是指以所查找节点为终止节点的路径的集合 每条路径称为前缀路径
def ascendTree(leafNode , prefixPath):#从一个节点开始迭代上溯整棵树直到根节点为止
	if leafNode.parent != None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent , prefixPath)

def findPrefixPath(basePat , treeNode):#寻找所有前缀路径即为指定节点生成条件模式基
	condPats = {}#条件模式基
	while treeNode != None:#当节点不为空
		prefixPath = []
		ascendTree(treeNode , prefixPath)#回溯寻找前缀路径
		if len(prefixPath) >1:#当prefixPath 长度大于1  即路径长>1 路径存在 
			condPats[frozenset(prefixPath[1:])] = treeNode.count  #将路径加入condPats 作为key  value为 节点的值
		treeNode = treeNode.nodeLink  #treeNode更新为另一个同名的节点
	return condPats

def mineTree(inTree, headerTable , minSup , preFix , freqItemList):
	bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p: p[1])]
	# print "bigl+++",v 	
	for basePat in bigL:
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat , headerTable[basePat][1])
		myCondTree , myHead = creatTree(condPattBases , minSup)

		if myHead != None:
			mineTree(myCondTree , myHead , minSup , newFreqSet , freqItemList)


# 获取频繁项集，调用mineTree，inTree FP树，head 为headerTable ， freqItemList 需要在调用前创建空列表以存储频繁向集。preFix为条件模式基
# if:'__name__' == "__mian__":
# 	freqItemList = []
# 	mineTree(inTree, headerTable , minSup , preFix , freqItemList):