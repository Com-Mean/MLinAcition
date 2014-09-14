#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: adaboost.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月14日 星期日 17时33分05秒
#########################################################################
from numpy import *

def loadSimpleData():
    dataMat = matrix([[1. , 2.1],
                      [2. , 1.1],
                      [1.3, 1. ],
                      [1. , 1. ],
                      [2. , 1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataMat, classLabels

def stumpclassify(dataMatrix, dimen, threshold, thresholdIneq): # dimen 列号
    retArray = ones((shape(dataMatrix)[0], 1))                     # 行号个元素
    if thresholdIneq == 'lt':
        retArray[dataMatrix[:, dimen] <= threshold] = -1.0       # 某一列数据与阈值比较，得到bool向量
    else:
        retArray[dataMatrix[:, dimen] > threshold] = -1.0
    return retArray

def buildStump(dataArr, classLabels, D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClassEst = mat(zeros((m,1)))
    minError = inf

    for i in range(n):
        rangeMin = dataMatrix[:, i].min(); rangeMax = dataMatrix[:, i].max()
        stepSize = (rangeMax - rangeMin)/numSteps
        for j in range(-1, int(numSteps) + 1):
            for inequal in ['lt','gt']:
                threshold = (rangeMin + float(j) * stepSize)
                predictedVals = \
                        stumpclassify(dataMatrix, i, threshold, inequal)
                errArr = mat(ones((m, 1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T * errArr                    # calc weightedError
                print("Split: dim %d, threshold %.2f, thredsh inequal:%s, the weightedError is %.3f" % \
                        (i, threshold, inequal, weightedError))
                if weightedError < minError:
                    minError = weightedError
                    bestClassEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['threshold'] = threshold
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClassEst

def adaBoostTrainDS(dataArr, classLabels, numIt=40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m, 1))/m)
    aggClassEst = mat(zeros((m, 1)))
    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataArr, classLabels, D)
        print('D:', D.T)
        alpha = float(0.5 * log((1.0 - error)/max(error, 1e-16)))
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print('ClassEst:', classEst.T)

        # calc new D
        expon = multiply(-1 * alpha*mat(classLabels).T, classEst)
        D = multiply(D, exp(expon))
        D = D/D.sum()

        # aggregate estimate result
        aggClassEst += alpha * classEst
        print('aggClassEst:',aggClassEst.T)
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m, 1)))
        print('aggErrors:', aggErrors)
        errorRate = aggErrors.sum()/m
        print('Total error:', errorRate)
        if errorRate == 0.0:                   # 训练错误率为0时，adaboost训练停止
            break
    return weakClassArr, aggErrors

def adaClassify(data2Class, classifierArr):
    dataMat = mat(data2Class)
    m = dataMat.shape[0]
    aggClassEst = mat(zeros((m, 1)))
    for i in range(len(classifierArr)):
        classEst = stumpclassify(dataMat, classifierArr[i]['dim'], \
                classifierArr[i]['threshold'],\
                classifierArr[i]['ineq'],)
        aggClassEst += classifierArr[i]['alpha']* classEst
        print(aggClassEst)

    return sign(aggClassEst)

def plotROC(predStrengths, classLabels):
    import matplotlib.pyplot as plt
    print(dir(plt))
    cur = (1.0, 1.0)
    ySum = 0.0
    numPosClass = sum(array(classLabels) == 1.0)
    yStep = 1/float(numPosClass)
    xStep = 1/float(len(classLabels) - numPosClass)
    sortedIndicies = predStrengths.argsort()
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delX = 0; delY = yStep
        else:
            delX = xStep; delY = 0
            ySum += cur[1]
        ax.plot([0, 1], [0, 1], 'b--')
        plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
        plt.title('ROC curve for adaBoost Horse Colic Detection System')
        ax.axis([0, 1, 0, 1])
        plt.show()
        print('The Area Under the Curve is: ', ySum * xStep)

if __name__ == '__main__':
    dataMat, classLabels = loadSimpleData()
    D = mat(ones((5, 1))/5)
    #print(buildStump(dataMat, classLabels, D))
    classifierArr, aggErrors = adaBoostTrainDS(dataMat, classLabels)
    adaClassify([0, 0], classifierArr)
    plotROC(aggErrors, classLabels)
