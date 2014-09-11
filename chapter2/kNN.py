#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: kNN.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月06日 星期六 13时25分51秒
#########################################################################

from numpy import *
import operator

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0,0], [0, 0.1]])
    labels = ['A','A','B','B',]
    return group, labels

def kNNClassify(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
