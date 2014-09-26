#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: pca.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月26日 星期五 18时50分32秒
#########################################################################
from numpy import *

def loadDataSet(filename, delim = '\t'):
    fr = open(filename)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    dataArr = [map(float, line) for line in stringArr]
    return mat(dataArr)

# about cov matrix http://www.cnblogs.com/chaosimple/p/3182157.html
def pca(dataMat, topNfeat = 9999999):
    meanVals = mean(dataMat, axis = 0)
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar = 0)
    eigVals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]    # just use the topN features
    redEigVects = eigVects[:, eigValInd]
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return (lowDDataMat, reconMat)
