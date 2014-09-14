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

def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    #print(inputSet)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print('The word: %s is not in my Vocabulary!'%word)
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

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)

    trainingSet = range(50); testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet(randIndex))
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    
    errorCount = 0
    for docIndex in testSet:
        wordVec = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVec), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
        print('The error rate is:%f'%(float(errorCount/len(testSet))))

def calcMostFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), \
            reverse = True)
    return sortedFreq[:30]


def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])

    trainingSet = list(range(2*minLen)); testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print('The error rate is:%f' % (float(errorCount / len(testSet))))
    return vocabList, p0V, p1V

def getTopWords(ny, sf):
    import operator
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0: topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0: topNY.append((vocabList[i], p1V[i]))

    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse = True)
    print('SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**')
    for item in sortedSF:
        print(item)

    print(p1V)
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse = True)
    print('NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**')
    for item in sortedNY:
        print(item)

if __name__=='__main__':
    #testingNB()
    import feedparser
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    print('%s\n%s'%(ny, sf))
    #print(localWords(ny, sf))
    print(getTopWords(ny, sf))
