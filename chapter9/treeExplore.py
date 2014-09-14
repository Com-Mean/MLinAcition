#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: treeExplore.py
# Author: lpqiu
# mail: qlp_1018@126.com
# Created Time: 2014年09月13日 星期六 21时42分58秒
#########################################################################

from numpy import *
from tkinter import *
import regTrees

def reDraw(tolS, tolN):
    pass

def drawNewTree():
    pass

def treeExplore():
    root = Tk()
    label(root, text="Plot Place Holder").grid(row=0, columnspan=3)

    label(root, text="tolN").grid(row=1, column=0)
    tolNEntry = Entry(root)
    tolNEntry.grid(row=1, column=1)
    tolNEntry.insert(0, '10')
    
    label(root, text='tolS').grid(row=2, column=0)
    tolSEntry = Entry(root)
    tolSEntry.grid(row=2, column=1)
    tolSEntry.insert(0, '1.0')

    Button(root, text='ReDraw', command=drawNewTree).grid(row=1, column=2,\
            rowspan=3)
    chkBtnVar = IntVar()
    chkBtn = Checkbutton(root, text='Model Tree', variable=chkBtnVar)
    chkBtn.grid(row=3, column=0, columnspan=2)

    reDraw.drawDat= mat(regTrees.loadDataSet('sine.txt'))
    reDraw.testDat = arange(min(reDraw.rawDat[:,0]), \
            max(reDraw.rawDat[:,0]), 0.01)
    reDraw(1.0, 10)
    root.mainloop()

if __name__=="__main__":
    treeExplore()
