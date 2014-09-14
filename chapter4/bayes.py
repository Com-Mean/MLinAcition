#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: bayes.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月13日 星期六 23时24分31秒
#########################################################################
# two classes

from numpy import *

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', \
                    'problem', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', \
                    'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', \
                    'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how',\
                    'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]

    classVec = [0, 1, 0, 1, 0, 1]              # 1 stand for abusive, 0 stand for normal
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)    # A∪B
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    #print(inputSet)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print('The word: %s is not in my Vocabulary!'%d)
    return returnVec

def trainNB0(trainMat, trainCatgry):
    numTrainDocs = len(trainMat)
    numWords = len(trainMat[0])
    pAbusive = sum(trainCatgry)/float(numTrainDocs)
    #p0Num = zeros(numWords); p1Num = zeros(numWords)
    #p0Denom = 0.0; p1Denom = 0.0
    p0Num = ones(numWords); p1Num = ones(numWords) # m-estimate m =2, p=0.5
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCatgry[i] == 1:
            p1Num += trainMat[i]
            p1Denom += sum(trainMat[i])
        else:
            p0Num += trainMat[i]
            p0Denom += sum(trainMat[i])

    #p1Vect = p1Num/p1Denom
    #p0Vect = p0Num/p0Denom
    p1Vect = log(p1Num/p1Denom)  # avoid underflow
    p0Vect = log(p0Num/p0Denom)

    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    # logA+ logB = log(A+B)
    p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
    print('p0: {0}, p1: {1}'.format(p0, p1))
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    #print(listOPosts, listClasses)
    myVocabList = createVocabList(listOPosts)
    print(myVocabList)

    trainMat = []
    for postDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postDoc))

    for i in range(len(trainMat)):
        print(trainMat[i],listClasses[i])
    p0V, p1V, pAb = trainNB0(trainMat, listClasses)
    print("{0}\n{1}\n{2}".format(pAb, p0V, p1V))

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print('{0} classified as: {1}'.format(testEntry, classifyNB(thisDoc, p0V, p1V, pAb)))

    testEntry = ['stupid', 'garbage',]
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print('{0} classified as: {1}'.format(testEntry, classifyNB(thisDoc, p0V, p1V, pAb)))

if __name__=='__main__':
    testingNB()
