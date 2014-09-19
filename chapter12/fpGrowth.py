#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: fpGrowth.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月19日 星期五 07时35分22秒
#########################################################################
from numpy import *

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def dispNode(self, ind=1):
        print('  '*ind, self.name, '  ', self.count)
        for child in self.children.values():
            child.dispNode(ind + 1)

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

def createTree(dataSet, minSupp = 1):
    headerTable = {}
    for trans in dataSet.keys():
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans] # 0 or headerTable[item] + dataSet[trans]

    for k in headerTable.keys():     #clean low supp items
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

