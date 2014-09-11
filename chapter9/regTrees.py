#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: regTrees.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月11日 星期四 21时41分18秒
#########################################################################
from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)     # let line to be mapped to float data
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :][0]  # ndarray二维矩阵取数据
    mat1 = dataMat[nonzero(dataMat[:, feature] <= value)[0], :][0]
    return mat0, mat1

def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat == None: return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feature, value)
    retTree['left'] = createTree(lSet)
    retTree['right'] = createTree(rSet)
    return retTree

# line model Tree
def linearSolve(dataSet):
    m,n = shape(dataSet)
    X = mat(ones((m, n)))
    Y = mat(ones((m, 1)))
    X[:, 1:n] = dataMat[:, 0:n-1]; Y = dataSet[:, -1]
    xTx = X.T*X
    if linalg.det(xTx) ==0.0:
        raise NameError('This matrix is singular, cannot do inverse,\n\
                try increasing the second value of ops')
    ws = xTx.I * (X.T * Y)
    return ws, X, Y

def modelLeaf(dataSet):
    ws, X, Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws, X, Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat, 2))

# classification Tree, input nominal attri value must change to binary attri
def majorityCntclass(classList):
    if len(dataSet) == 0:
        return None
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1

    sortedClassCount = sorted(classCount.iteritems(), \
            key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]
    
def classificationLeaf(dataSet):
    if len(set(dataSet[:, -1])) == 1:
        return dataSet[0, -1]
    else:
        return majorityCntclass(dataSet[:, -1])

def classificationErr(dataSet):
    if len(dataSet) == 0:
        return None

    classList = dataSet[:, -1]
    classCount = {}
    giniGain = 0
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1

    for key in classCount.keys():
        giniGain += classCount[key]/len(classList)

    return 1 - giniGain

# regression Tree
def regLeaf(dataSet):
    return mean(dataSet[:, -1])

def regErr(dataSet):
    return var(dataMat[:, -1]) * shape(dataSet)[0]

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1: # all data have the same class
        return None, leafType(dataSet)

    tolS = ops[0]; tolN = = ops[1]
    m,n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue= 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:, featIndex]):
            mat0,mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if(shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): 
                continue
            
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS

    if (S - bestS) < tolS:                       # err declined less than threshold tolS
        return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if(shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): # data remain in the node is less than threshold tolN
        return None, leafType(dataSet)
    return bestIndex, bestValue

def isTree(obj):
    return (type(obj).__name__ == 'dict')

def getMean(tree):
    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])
    
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])

    return (tree['left'] + tree['right'])/2.0

def prune(tree, testData):
    if shape(testData)[0] == 0:
        return getMean(tree)

    if isTree(tree['right']) or isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])

    if isTree(tree['left']):
        tree['left'] = prune(tree['left'], lSet)
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rSet)
    if not isTree(tree['left']) and not isTree(tree['right']): # arrive the leaf
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        errorNoMerge = sum(power(lSet[: -1] - tree['left'], 2)) +\
                sum(power(rSet[: -1] - tree['right'], 2))
        treeMean = (tree['left'] + tree['right'])/2.0
        errorMerge = sum(power(testData[:, -1] - treeMean, 2))
        if errorMerge < errorNoMerge:
            print("Merging")
            return treeMean
        else:
            return tree
    else:
        return tree

# forcast process
def regTreeEval(model, inDat):
    return float(model)

def modelTreeEval(model, inDat):
    n = shape(inDat)[1]
    X = mat(ones((1, n+1)))
    X[:, 1:n+1] = inDat
    return float(X * model)

def treeForecast(tree, inData, modelEval = regTreeEval):
    if not isTree(tree):
        return modelEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForcast(tree['left'], inData, modelEval)
        else:
            return modelEval(tree['left'], inData)
    else:
        if isTree(tree['right']):
            return treeForcast(tree['right'], inData, modelEval)
        else:
            return modelEval(tree['right'], inData)

def createForecast(tree, testData, modelEval=regTreeEval):
    m = len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i, 0] = treeForecast(tree, testData, modelEval)
    return yHat

