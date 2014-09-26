#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: svdRec.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月26日 星期五 22时07分47秒
#########################################################################
from numpy import *
from numpy import linalg as la

def loadExData():
    exData = [[1, 1, 1, 0, 0],
              [2, 2, 2, 0, 0],
              [1, 1, 1, 0, 0],
              [5, 5, 5, 0, 0],
              [1, 1, 0, 2, 2],
              [0, 0, 0, 3, 3],
              [0, 0, 0, 1, 1],]
    return exData

# similar measure method
def ecludSim(inA, inB):
    return 1.0/(1.0 + la.norm(inA - inB))

def pearsonSim(inA, inB):
    if len(inA) < 3: return 1.0
    else: return 0.5 + 0.5 * corrcoef(inA, inB, rowvar = 0)[0][1]

def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5*(num/denom)

def standEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0

    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item: continue
        # find the users who estimate the two things (j and item)
        overLap = nonzero(logical_and(dataMat[:, item].A > 0, \
                                      dataMat[:, j].A > 0))[0]
        if len(overLap) == 0: similarity = 0
        else: similarity = simMeas(dataMat[overLap, item], \
                                   dataMat[overLap, j])
        simTotal += similarity
        ratSimTotal += similarity * userRating
        if simTotal == 0: return 0
        else: return ratSimTotal/simTotal

def recommend(dataMat, user, N=3, simMeas = cosSim, estMethod = standEst):
    unratedItems = nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0: return 'You rated everything!'

    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key = lambda it: it[1], reverse = True)[:N]

def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[0]
    simTotal = 0.0; ratSimTotal = 0.0
    U,sigma,VT= la.svd(dataMat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformedItems = dataMat.T * U[:, :4] * Sig4.I
    for j in range(n):
        userRating  = dataMat[user, j]
        if userRating == 0 or j == item: continue
        similarity = simMeas(xformedItems[item, :].T,\
                             xformedItems[j, :].T)
        simTotal += similarity
        ratSimTotal += similarity * userRating

    if simTotal == 0: return 0
    else: return ratSimTotal / simTotal

def getPowSigVals(inSigArr, powerRate = 0.9):
    poweredSig = power(inSigArr, 2)
    powerSum = sum(poweredSig) * powerRate
    powInd = 0; tmpSum = 0
    for i in range(inMat.shape[0]):
        tmpSum += inMat[i]
        if tmpSum >= powerSum:
            powInd = i
            break
    return inSigArr[: powInd + 1]

def printMat(inMat, threshold = 0.8):
    for i in range(32):
        for j in range(32):
            if float(inMat[i, j]) > threshold:
                print(1, end = '')
            else:
                print(0, end = '')
        print('')

def imgCompress(numSV=3, threshold=0.8):
    myl = []
    for line in open('0_5.txt').readlines():
        newRow = []
        for i in range(32):
            newRow.append(int(line[i]))
        myl.append(newRow)
    myMat = mat(myl)
    print('****original matrix******')
    printMat(myMat, threshold)
    U,Sigma,VT = la.svd(myMat)
    SigRecon = mat(zeros((numSV, numSV)))
    for k in range(numSV):
        SigRecon[k, k] = Sigma[k]
    reconMat = U[:,:numSV] * SigRecon * VT[:numSV, :]
    print('****reconstructed matrix using %d sigular values******' % numSV)
    print(reconMat, threshold)



