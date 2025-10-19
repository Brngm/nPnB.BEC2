

// TODO ajuster les commentaire

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// nPnB_QUICK_BEC.cpp:
//      C++ code for fast clustering methods in nPnB framework
//
// Author:
//      Bruno Gaume <bruno.gaume@iscpif.fr>
//      March 2025
//
// nPnB framework Reference:
//      Two antagonistic objectives for one multi-scale graph clustering framework,
//      Bruno Gaume, Ixandra Achitouv, David Chavalarias Nature Scientific Reports (2025)
//      https://www.nature.com/articles/s41598-025-90454-w
//
// BEC2 Algorithm Reference:
//      BEC.2: A fast and relevant Multi-Scale Graph Clustering algorithm in nPnB framework,
//      Bruno Gaume (2025)
//
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Four functions can be called from Python:
//      CLUSTERING WITHOUT OVERLAPS:
//        (1) const char* mmm(char* GraphString, char* ClustZero, char* BetaIn, char* RandNode, char* EpsilonIN, char* Verbose)
//      CLUSTERING ALLOWING OVERLAPS:
//        (2) const char* overlaps(char* GraphString, char* ClustZero, char* BetaIn, char* RandNode, char* Verbose)
//      METRICS:
//        (3) const char* TPTNFPFN_Intrinsic(char* GraphString, char* ClustZero)
//        (4) const char* TPTNFPFN_GOLD_C(char* GOLD, char* C, char* n_vertices)
//
// Input integrity checking must be done in the calling Python program:
// (nPnB_QUICK_BEC_Interface.py<--->nPnB_QUICK_BEC_Wrapper.py<--->nPnB_QUICK_BEC_C++/result/bin/libnPnB-QUICK-BEC.so)
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Terms of use:
//      The project nPnB_QUICK_BEC is released under a dual licence.
//      To give everyone maximum freedom to make use of nPnB_QUICK_BEC and derivative works, we make the code open source under the
//      GNU General Public License version 3 or any later version (see LICENSE_GPLv3.txt https://www.gnu.org/licenses/gpl-3.0.en.html).
//      For a non-copyleft license, please contact us.
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <set>
#include <time.h>
#include <math.h>
#include <random>
#include <filesystem>
#include <map>
#include <queue>
#include <stdio.h>
#include <string.h>
#include <algorithm>
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#include "nPnB-QUICK-BEC_handy_types.h"
#include "nPnB-QUICK-BEC_struct.h"
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#include "nPnB-QUICK-BEC_tools.cpp"
#include "nPnB-QUICK-BEC_extern_metrics.cpp"
#include "nPnB-QUICK-BEC_extern_clustering_methods.cpp"
