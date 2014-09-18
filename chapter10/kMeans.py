#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: kMeans.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月18日 星期四 03时20分49秒
#########################################################################
from numpy import * 
import urllib
import json

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

def geoGrab(stAddress, city):
    apiStem = 'http://where.yahooapis.com/geocode?'
    param = {}
    params['flags'] = 'J'              # json datastruct
    params['appid'] = 'ppp68N8t'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = urllib.urlencode(params)
    yahooApi = apiStem + url_params
    print(yahooApi)
    c = urllib.urlopen(yahooApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(filename):
    fw = open('places.txt', 'w')
    fp = open(filename)
    for line in fp.readlines():
        curLine = line.strip().split('\t')
        retDict = geoGrab(curLine[1], curLine[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print('%s\t%f\t%f' % (curLine[0], lat, lng))
            fw.write('%s\t%f\t%f\n' % (curLine[0], lat, lng))
        else:
            print('Error fetching!')
        sleep(1)
    fw.close()

# calc spherical distance  
def distSLC(vecA, vecB):
    a = sin(vecA[0,1] * pi/180) * sin(vecB[0,1] * pi/180)
    b = cos(vecA[0,1] * pi/180) * cos(vecB[0,1] * pi/180) * \
            cos(pi * (vecB[0, 0] - vecA[0,0])/180)
    return arccos(a + b) * 6371.0 

import matplotlib
import matplotlib.pyplot as plt

def clusterClubs(numClust=5):
    datList = []
    for line in open('place.txt').readlines():
        curLine = line.split('\t')
        datList.append(float(curLine[4]), float(curLine[3]))

    datMat = mat(datList)
    myCentroids, clustAssing = binkMeans(dataMat, numClust, \
            distMeas = distEclud)
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    scatterMarkers = ['s', 'o', '^', '8', 'p', \
                      'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0 = fig.add_axes(rect, label='ax0', **axprops)
    imgP = plt.imread('Portland.png')
    ax0.imshow(imgP)
    ax1 = fig.add_axes(rect, label='ax1', frameon=False)
    for i in range(numClust):
        ptsInCurClust = datMat[nonzero(clustAssing[:, 0].A == i)[0], :]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        ax1.scatter(ptsInCurClust[:,0].flatten().A[0], \
                ptsInCurClust[:,1].flatten().A[0],\
                marker=markerStyle, s = 90)
        ax1.scatter(myCentroids[:,0].flatten().A[0],\
                myCentroids[:, 1].flatten().A[0], marker='+', s = 300)
    plt.show()

    return 0

if __name__ == '__main__':
    print(randCentroids(array([1, 2, 3, 4]).reshape(2, 2), 2))
