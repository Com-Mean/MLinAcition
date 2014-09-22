#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: fpGrowth.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月19日 星期五 07时35分22秒
#########################################################################
from numpy import *

def loadSimpDat():
    simpleDat = [['r', 'z', 'h', 'j', 'p'],
                 ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                 ['z'],
                 ['r', 'x', 'n', 'o', 's'],
                 ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                 ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
                 ]
    return simpleDat

# as loadSimpDat()
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def dispTree(self, ind=1):
        print('  '*ind, self.name, '  ', self.count)
        for child in self.children.values():
            child.dispTree(ind + 1)

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children.keys():
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
                headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], \
                headerTable, count)

def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink

    nodeToTest.nodeLink = targetNode

# dataSet: {frozenset({'a', 'b'}):1, frozenset({'c'}):1} created from createInitSet()
def createTree(dataSet, minSupp = 1):
    headerTable = {}
    for trans in dataSet.keys():
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans] # 0 or headerTable[item] + dataSet[trans]

    for k in list(headerTable.keys()):     #clean low supp items
        if headerTable[k] < minSupp:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None

    for k in freqItemSet:                         # init the headerTable
        headerTable[k] = [headerTable[k], None]   # count and the headerPtr is the table value
    retTree = treeNode('rootNode_NullSet', 1, None)

    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), \
                    key=lambda p: p[1], reverse= True)]
            updateTree(orderedItems, retTree, \
                    headerTable, count)

    return retTree, headerTable

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSupp, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),
                                 key=lambda p : p[1][0])]
    print(preFix)

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSupp)

        if myHead != None:
            print("conditional tree for:", newFreqSet, '\n', myCondTree.dispTree())
            mineTree(myCondTree, myHead, minSupp, newFreqSet, freqItemList)

if __name__ == '__main__':
    simpleDat = loadSimpDat()
    initSet = createInitSet(simpleDat)
    print(simpleDat,'\n',initSet)
    myFPTree, myHeaderTable = createTree(initSet, 3)
    myFPTree.dispTree()
    mineTree(myFPTree, myHeaderTable, minSupp = 3, preFix=set([]), freqItemList=[])
