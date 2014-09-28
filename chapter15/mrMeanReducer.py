#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: mrMeanReducer.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月28日 星期日 15时47分03秒
#########################################################################
import sys
from numpy import mat, mean, power

def read_input(file):
    for line in file:
        yield line.rstrip()

input = read_input(sys.stdin)
mapperOut = [line.split('\t') for line in input]
cumVal = 0.0
cumSumSq = 0.0
cumN = 0.0
for instance in mapperOut:
    nj = float(instance[0])
    cumN += nj
    cumVal += nj*float(instance[1])
    cumSumSq += nj*float(instance[2])
mean = cumVal / cumN
varSum = (cumSumSq - 2*mean*cumVal + cumN * mean * mean) / cumN
print('%d\t%f\t%f' % (cumN, mean, varSum))
print('Report: still alive', file=sys.stderr)
