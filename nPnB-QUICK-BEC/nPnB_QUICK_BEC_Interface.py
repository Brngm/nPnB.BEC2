#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    nPnB_QUICK_BEC_Interface.py:
        Python interface for fast clustering in nPnB framework
        Python3: (nPnB_QUICK_BEC_Interface.py<--->nPnB_QUICK_BEC_Wrapper.py<--->nPnB_BEC2_WU_C++/result/bin/libnPnB-QUICK-BEC.so)

    Author:
        Bruno Gaume <bruno.gaume@iscpif.fr>
        March 2025
    
    nPnB framework Reference:
        Two antagonistic objectives for one multi-scale graph clustering framework,
        Bruno Gaume, Ixandra Achitouv, David Chavalarias Nature Scientific Reports (2025)
        https://www.nature.com/articles/s41598-025-90454-w

    BEC2 Algorithm Reference:
        BEC.2: A fast and relevant Multi-Scale Graph Clustering algorithm in nPnB framework,
        Bruno Gaume (2025)
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    METRICS:
        PRF(s, TruePositive, TrueNegative, FalsePositive, FalseNegative)
        return (P, R, F);

        TPTNFPFN_Intrinsic(g, Clust)
        return TP, TN, FP, FN

        TPTNFPFN_GOLD_C(GOLD, Clust, n_vertices)
        return TP, TN, FP, FN;

    CLUSTERING WITHOUT OVERLAPS:
        nPnB_mmm(g, sp=0.5,  C0string=False, RandNode=False, Epsilon=0.01, Verbose=False)
        return ClustP, Prec, Rec, FSCORE1, FSCOREs, TP, TN, FP, FN, Time;

    CLUSTERING ALLOWING OVERLAPS:
        nPnB_overlaps(g, so=0.15,  C0string=False, RandNode=False, Verbose=False)
        return ClustO, Prec, Rec, FSCORE1, FSCOREs, TP, TN, FP, FN, Time;
"""


import igraph as ig
import os
import numpy as np
import random as rd
import copy
import codecs
import time
import math

# =====================================================
import nPnB_QUICK_BEC_Wrapper as WRAPP
# =====================================================

def PRF(s, TruePositive, TrueNegative, FalsePositive, FalseNegative):
    """
    PRF(s, TruePositive, TrueNegative, FalsePositive, FalseNegative)
    return (P, R, Fs)
    """
    beta=s2beta(s)
    P=0.0; R=0.0; F=0.0
    if (TruePositive + FalsePositive) > 0:
        P = TruePositive/(TruePositive + FalsePositive)
    if (TruePositive + FalseNegative) > 0:
        R = TruePositive/(TruePositive + FalseNegative)
    if (P + R) > 0:
        F = (1 + beta**2) * ((P * R) / (((beta**2) * P) + R))  
    return (P, R, F)

def TPTNFPFN_Intrinsic(g, Clust):
    """
    TPTNFPFN_Intrinsic(g, Clust)
    return TP, TN, FP, FN
    """
    GraphString = graph2string(g)
    ClustString = clust2string(Clust)
    stringByte = WRAPP._TPTNFPFN_Intrinsic(GraphString, ClustString)
    string=stringByte.decode("utf-8")
    d1 = '!'
    LINES=string.split(d1)
    TP=float(LINES[0]); TN=float(LINES[1]); FP=float(LINES[2]); FN=float(LINES[3]); 
    return TP, TN, FP, FN

def TPTNFPFN_GOLD_C(GOLD, Clust, n_vertices):
    """
    TPTNFPFN_GOLD_C(GOLD, Clust, n_vertices)
    return TP, TN, FP, FN;
    """
    GOLDString = clust2string(GOLD)
    ClustString = clust2string(Clust)
    n_verticesString = "%i"%(n_vertices); n_verticesString = n_verticesString.encode('utf-8')

    stringByte = WRAPP._TPTNFPFN_GOLD_C(GOLDString, ClustString, n_verticesString)
    string=stringByte.decode("utf-8")
    d1 = '!'
    LINES=string.split(d1)
    TP=float(LINES[0]); TN=float(LINES[1]); FP=float(LINES[2]); FN=float(LINES[3]); 
    return TP, TN, FP, FN

def nPnB_mmm(g, sp=0.5,  C0string=False, RandNode=False, Epsilon=0.01, Verbose=False):
    """
    nPnB_mmm(g, sp=0.5,  C0string=False, RandNode=False, Epsilon=0.01, Verbose=False)
    return ClustP, Prec, Rec, FSCORE1, FSCOREsp, TP, TN, FP, FN, Time
    """
    TIMEstart = time.time()
    assert ((sp >= 0) and (sp <=1)), ("sp Must be in [0,1]")
    assert ((Epsilon >= 0) and (Epsilon < 1) ), ("Epsilon Must be in [0,1[")
    # =====================================================================
    if RandNode:
        RandNode = "1"; RandNode = RandNode.encode('utf-8')
    else:
        RandNode = "0"; RandNode = RandNode.encode('utf-8')

    if Verbose:
        Verbose = "1"; Verbose = Verbose.encode('utf-8')
    else:
        Verbose = "0"; Verbose = Verbose.encode('utf-8')
    
    betap=s2beta(sp)
    if (betap<0.0000001):
        betap=0.0000001
    strBetaP = "%.10f"%(betap); strBetaP = strBetaP.encode('utf-8')

    strEpsilon = "%.10f"%(Epsilon); strEpsilon = strEpsilon.encode('utf-8')
    #
    if (C0string==False):
        C0string = clust2string([[i] for i in range(len(g["nodes"]))])
    #
    GraphString = graph2string(g)
    CstringP = WRAPP._mmm(GraphString, C0string, strBetaP, RandNode=RandNode, Epsilon=strEpsilon, Verbose=Verbose)
    ClustP, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time = string2clust(CstringP)
    #
    return ClustP, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time

def nPnB_overlaps(g, so=0.15,  C0string=False, RandNode=False, Verbose=False):
    """
    nPnB_overlaps(g, so=0.15,  C0string=False, RandNode=False, Verbose=False)
    return ClustO, Prec, Rec, FSCORE1, FSCOREso, TP, TN, FP, FN, Time
    """
    TIMEstart = time.time()
    assert (so >= 0) and (so <=1), ("so Must be in [0,1]")
    # =====================================================================
    if RandNode:
        RandNode = "1"; RandNode = RandNode.encode('utf-8')
    else:
        RandNode = "0"; RandNode = RandNode.encode('utf-8')

    if Verbose:
        Verbose = "1"; Verbose = Verbose.encode('utf-8')
    else:
        Verbose = "0"; Verbose = Verbose.encode('utf-8')
        
    betao=s2beta(so)
    if (betao<0.0000001):
        betao=0.0000001
    strBetaO = "%.10f"%(betao); strBetaO = strBetaO.encode('utf-8')
    #
    if (C0string==False):
        C0string = clust2string([[i] for i in range(g.vcount())])
    #
    GraphString = graph2string(g)
    CstringO = WRAPP._overlaps(GraphString, C0string, strBetaO, RandNode=RandNode, Verbose=Verbose)
    ClustP, with_nodes, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time = string2clust_with_nodes(CstringO)
    #
    return ClustP, with_nodes, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Tools
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def beta2s(beta):
    """
    beta2s(beta): return (2*(math.atan(beta)))/math.pi
    """
    return (2*(math.atan(beta)))/math.pi

def s2beta(s):
    """
    s2beta(s): return (math.tan((math.pi*s)/2))
    """
    return (math.tan((math.pi*s)/2))
    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# stringByte <----> object
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def graph2string(g):
    """
    """
    d1 = '!'; d2 = ','
    #
    DIC={}
    nbv=len(g["nodes"])
    for x in g["links"]:
        i=x["source"]; j=x["target"]; w=x["weight"]; 
        assert ((i < nbv) and (j < nbv)), ("Only %i nodes, but in links: %s"%(nbv,x))
        assert (not (i==j)), ("No reflexive edge, but in links:"%(x))
        assert (w > 0), ("Wwights must be >0, but in links:"%(x))

        ii=min([i,j]); jj=max([i,j])
        DIC[(ii,jj)]=0

    nb_e = 0
    sum_w = 0
    for x in g["links"]:
        i=x["source"]; j=x["target"]; w=x["weight"];
        ii=min([i,j]); jj=max([i,j])
        DIC[(ii,jj)]=DIC[(ii,jj)] + w
        nb_e = nb_e + 1
        sum_w = sum_w + w

    if (nb_e == 0):
        mean_w = 1
    else:
        mean_w = sum_w/nb_e

    CH="%s%s%s"%(d1,str(nbv),d1)
    for key in DIC:
        ii=key[0]; jj=key[1]
        CH=CH+"%s%s%s%s%s%s"%(str(ii), d2, str(jj), d2, str(DIC[(ii,jj)]/mean_w), d1)
    return CH.encode('utf-8')

def clust2string(clust):
    """
    clust2string(clust)
    """
    d1 = '!';  d2 = ','
    string = ""
    for mod in clust:
        line = ""
        for i in range(len(mod)):
            if i == (len(mod)-1):
                line = line + str(mod[i])
            else:
                line = line + str(mod[i]) + d2
        line = line + d1
        string = string + line  
    return string.encode('utf-8')

def string2clust(stringByte):
    """
    string2clust(stringByte)
    """
    string=stringByte.decode("utf-8")
    d0="#"; PRELINE=string.split(d0);
    string=PRELINE[0];
    Prec=float(PRELINE[1]); Rec=float(PRELINE[2]); FSCORE1=float(PRELINE[3]); FSCOREbeta=float(PRELINE[4]);
    TP=float(PRELINE[5]); TN=float(PRELINE[6]); FP=float(PRELINE[7]); FN=float(PRELINE[8]); 
    Time=float(PRELINE[9])
    
    d1 = '!'; d2 = ','
    clust=[]
    LINES=string.split(d1)
    for i in range(len(LINES)-1):
        line=LINES[i]
        mod=[]
        lineSplit=line.split(d2)
        for x in lineSplit:
            mod.append(int(x))
        clust.append(mod)
    return clust, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time

def string2clustO(stringByte):
    """
    string2clust_with_nodes(stringByte)
    """
    string=stringByte.decode("utf-8")
    d0="#"; PRELINE=string.split(d0);
    string=PRELINE[0];
    Prec=float(PRELINE[1]); Rec=float(PRELINE[2]); FSCORE1=float(PRELINE[3]); FSCOREbeta=float(PRELINE[4]);
    TP=float(PRELINE[5]); TN=float(PRELINE[6]); FP=float(PRELINE[7]); FN=float(PRELINE[8]); 
    Time=float(PRELINE[9])
    
    d1 = '!'; d2 = ','; d3=";"
    clustP=[]
    with_nodes=[]
    LINES=string.split(d1)
    for i in range(len(LINES)-1):
        line=LINES[i]
        mod=[]
        lineSplit=line.split(d2)
        for x in lineSplit:
            mod.append(int(x))
        clust.append(mod)
    return clustP, with_nodes, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time

def string2clust_with_nodes(stringByte):
    """
    string2clust_with_nodes(stringByte)
    """
    string=stringByte.decode("utf-8")
    d0="#"; PRELINE=string.split(d0);
    string=PRELINE[0];
    Prec=float(PRELINE[1]); Rec=float(PRELINE[2]); FSCORE1=float(PRELINE[3]); FSCOREbeta=float(PRELINE[4]);
    TP=float(PRELINE[5]); TN=float(PRELINE[6]); FP=float(PRELINE[7]); FN=float(PRELINE[8]); 
    Time=float(PRELINE[9])
    
    d1 = '!'; d2 = ';'; d3=","
    clustP=[]
    with_nodes=[]
    LINES=string.split(d1)
    for i in range(len(LINES)-1):
        line=LINES[i]
        lineSplit=line.split(d2)
        line0=lineSplit[0]
        line1=lineSplit[1]

        mod=[]
        lineSplit=line0.split(d3)
        for x in lineSplit:
            mod.append(int(x))
        clustP.append(mod)

        wn=[]
        lineSplit=line1.split(d3)
        for x in lineSplit:
            if not x=='':
                wn.append(int(x))
        with_nodes.append(wn)

    return clustP, with_nodes, Prec, Rec, FSCORE1, FSCOREbeta, TP, TN, FP, FN, Time

