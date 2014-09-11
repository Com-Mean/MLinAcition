#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: numpyIntro.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月06日 星期六 16时33分05秒
#########################################################################

import numpy as np

def triangleWave(x, c, c0, hc=1.0):
    x = x - int(x)
    ret = 0
    if x >= c:
        ret = 0
    elif x < c0:
        ret = (hc/c0)*x
    else:
        ret = (hc/(c0 -c))*(x - c)
    return ret

def triangleFunc(x, c, c0, hc=1.0):
    def trgFun(x):
        x = x - int(x)
        ret = 0
        if x >= c:
            ret = 0
        elif x < c0:
            ret = (hc/c0)*x
        else:
            ret = (hc/(c0 -c))*(x - c)
        return ret
    return np.frompyfunc(trgFun, 1, 1)

if __name__=="__main__":
    x = np.linspace(0, 2, 1000)
    y = np.array([triangleWave(t, 0.6, 0.4, 1.0) for t in x])

    triangleFun = np.frompyfunc(lambda x: triangleWave(0.6, 0.4, 1.0), 1, 1)
    y2 = triangleFun(x)

    y3 = triangleFunc(0.6, 0.4, 1.0)(x)
