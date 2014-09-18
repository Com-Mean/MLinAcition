#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: kMeans.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月18日 星期四 03时20分49秒
#########################################################################
from numpy import * 


def loadDataSet(filename):
    dataMat = []
    fp = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def randCentroids(dataSet, k):
    n = shape(dataSet)[1]
    print(n)
    centroids = mat(zeros((k,n)))
    for j in range(n):
        print(j)
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k,1) # random is the numpy_lib's random
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCentroids): # need an itertor more
    m = dataSet.shape[0]
    clusterMem = mat(zeros((m, 2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        print(centroids)
        for i in range(k):
            minDist = inf; minIndex = -1
            for j in range(k):
                distIJ = distMeas(dataSet[i], centroids[j])
                if minDist > distIJ:
                    minDist = distIJ, minIndex = j
            if clusterMem[i, 0] != minIndex: clusterChanged = True
            clusterMem[i,:] = minIndex, minDist 

        for cent in range(k):
            ptsInClust = dataSet[(clusterMem[:,0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterMem

def binkMeans(dataSet, k, distMeas=distEclud, binK=2):
    m = dataSet.shape[0]
    clusterMem = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centroids = [centroid0]
    for i in range(m):
        clusterMem[i,:] = 0,distMeas(dataSet[i,:], centroid0)


    while(len(centroids) < k):
        lowerSSE = inf; 
        bestIndexToSplit = -1; bestSplitCents = None
        bestSplitClustMem = None
        for j in range(len(centroids)):
            ptsInCurClust = dataSet[nonzero(clusterMem[:, 0].A==i)[0], :]    # crate a new set with selected data
            tmpCentroids, tmpClusterMem = kMeans(ptsInCurClust, binK, distMeas)
            sseSplit = sum(tmpClusterMem[:,1])
            sseNotSplit = sum(clusterMem[nonzero(clusterMem[:,0] != i), 1])
            print('sseSplit: %f, sseNotSplit: %f'%(sseSplit, sseNotSplit))

            if(sseSplit + sseNotSplit) < lowerSSE:
                lowerSSE = sseSplit + sseNotSplit
                bestIndexToSplit = j
                bestSplitCents = tmpCentroids

        del(centroids[bestIndexToSplit])
        centroids.extend(bestSplitCents)
        bestSplitCents[:, 0] += len(centroids) - 1 - (len(bestSplitCents) - 1)# 0,1 + bestSplitCents[0]'s index in centroids
        clusterMem[nonzero(clusterMem[:, 0].A==bestSplitCents), :] = bestSplitClustMem[:,:]

    return centroids, clusterMem

if __name__ == '__main__':
    print(randCentroids(array([1, 2, 3, 4]).reshape(2, 2), 2))
