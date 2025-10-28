#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    nPnB_QUICK_BEC_Wrapper.py:
        Wrapper for fast clustering methods in nPnB framework
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
        _TPTNFPFN_Intrinsic(GraphString, ClustString)

        _TPTNFPFN_GOLD_C(GOLDString, ClustString, n_verticesString)

    CLUSTERING WITHOUT OVERLAPS:
        _mmm(GraphString, ClustZero, Beta, RandNode, Epsilon, Verbose)

    CLUSTERING ALLOWING OVERLAPS:
        _overlaps(GraphString, ClustZero, Beta, RandNode, Verbose)
"""
import ctypes
from pathlib import Path

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def _mmm(GraphString, ClustZero, Beta, RandNode, Epsilon, Verbose):
    """
    _mmm(GraphString, ClustZero, Beta, RandNode, Epsilon, Verbose)
    """
    # =====================================================================
    here=str(Path(__file__).resolve().parent)
    lib_path = here+"/nPnB-QUICK-BEC_C++/result/bin/libnPnB-QUICK-BEC.so" # Path to the compiled shared library
    lib_Move = ctypes.CDLL(lib_path)
    lib_Move.mmm.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib_Move.mmm.restype = ctypes.c_char_p
    # Call the C++ function
    output = lib_Move.mmm(GraphString, ClustZero, Beta, RandNode, Epsilon, Verbose)
    return output
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def _overlaps(GraphString, ClustZero, Beta, RandNode, Verbose):
    """
    _Overlaps(GraphString, ClustZero, Beta, RandNode, Verbose)
    """
    # =====================================================================
    here=str(Path(__file__).resolve().parent)
    lib_path = here+"/nPnB-QUICK-BEC_C++/result/bin/libnPnB-QUICK-BEC.so" # Path to the compiled shared library
    lib_Overlaps = ctypes.CDLL(lib_path)
    lib_Overlaps.overlaps.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib_Overlaps.overlaps.restype = ctypes.c_char_p
    # Call the C++ function
    output = lib_Overlaps.overlaps(GraphString, ClustZero, Beta, RandNode, Verbose)
    return output
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def _TPTNFPFN_Intrinsic(GraphString, ClustString):
    """
    _TPTNFPFN_Intrinsic(GraphString, ClustString)
    """
    # =====================================================================
    here=str(Path(__file__).resolve().parent)
    lib_path = here+"/nPnB-QUICK-BEC_C++/result/bin/libnPnB-QUICK-BEC.so" # Path to the compiled shared library
    lib_TPTNFPFN_Intrinsic = ctypes.CDLL(lib_path)
    lib_TPTNFPFN_Intrinsic.TPTNFPFN_Intrinsic.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib_TPTNFPFN_Intrinsic.TPTNFPFN_Intrinsic.restype = ctypes.c_char_p
    # Call the C++ function
    output = lib_TPTNFPFN_Intrinsic.TPTNFPFN_Intrinsic(GraphString, ClustString)
    return output
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def _TPTNFPFN_GOLD_C(GOLDString, ClustString, n_verticesString):
    """
    _TPTNFPFN_GOLD_C(GOLDString, ClustString, n_verticesString)
    """
    # =====================================================================
    here=str(Path(__file__).resolve().parent)
    lib_path = here+"/nPnB-QUICK-BEC_C++/result/bin/libnPnB-QUICK-BEC.so" # Path to the compiled shared library
    lib_TPTNFPFN_GOLD_C = ctypes.CDLL(lib_path)
    lib_TPTNFPFN_GOLD_C.TPTNFPFN_GOLD_C.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib_TPTNFPFN_GOLD_C.TPTNFPFN_GOLD_C.restype = ctypes.c_char_p
    # Call the C++ function
    output = lib_TPTNFPFN_GOLD_C.TPTNFPFN_GOLD_C(GOLDString, ClustString, n_verticesString)
    return output
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

