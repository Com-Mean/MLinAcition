#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: mrMeanMapper.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月28日 星期日 15时36分30秒
#########################################################################
import sys
from numpy import mat, mean, power

def read_input(file):
    for line in file:
        yield line.rstrip()

input = read_input(sys.stdin)
input = [float(line) for line in input]
numInputs = len(input)
sqInput = power(input, 2)
print('%d\t%f\t%f' % (numInputs, mean(input), mean(sqInput)))
print('Report: still alive', file=sys.stderr)
