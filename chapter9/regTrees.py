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
            if(shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
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
