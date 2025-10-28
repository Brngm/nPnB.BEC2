
  // See: Two antagonistic objectives for one multi-scale graph clustering framework,
  //      Bruno Gaume, Ixandra Achitouv, David Chavalarias,
  //      Nature Scientific Reports (2025).
  //      https://www.nature.com/articles/s41598-025-90454-w


// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// extern: TPTNFPFN_Intrinsic (C++ <--RAM--> Python)
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
extern "C" {
  const char* TPTNFPFN_Intrinsic(char* GraphString, char* ClustZero){
    time_t timerbegin = time(NULL);
    // we import graph data
    graph g;
    graph_from_string(GraphString, &g, 1);

    // init clust
    clusteringO clust;
    ClustO_from_string(ClustZero, &clust, g.nbv);

    // ============================================================================
    std::cerr << "\n================================================================" << std::endl;
    std::cerr << "TPTNFPFN_Intrinsic(G,C): "  << "G:[" << std::to_string(g.nbv) << " vertices, " <<  std::to_string(g.nbe) << " edges, ";
    std::cerr << std::to_string(g.meanWeight) << " = mean edges weight]" << std::endl;
    std::cerr << "C:[" << std::to_string(clust.nbmO) << " module(s)]" << std::endl;
    // ============================================================================
    // init TP, FP, FN, TN
    double TP=0, TN=0, FP=0, FN=0;
    TN=(((double(g.nbv)*double((g.nbv-1))*0.5)-double(g.nbe))*g.meanWeight);
    FN=g.sumWeight;

    long long pos;
    // ------------------------------------------------------------------------------------
    for(long long ii = 0; ii < clust.cO.size(); ii++) {
      if (clust.aliveO[ii]){
        for (auto i : clust.cO[ii]){
          for (auto j : clust.cO[ii]){
            if (i < j){
              double xxx=0;
              for (auto k : clust.membO[i]){
                if (clust.membO[j].end() != clust.membO[j].find(k)){
                  xxx=xxx+1;
                }
              }
              pos=nodeposition(&(g.neighbors[i]), j);
              if (!(pos==-1)) { // one edge {i,j} in graph
                TP=TP+(g.weight[i].at(pos)/xxx);
                FN=FN-(g.weight[i].at(pos)/xxx);
              }
              else{
                FP=FP+(g.meanWeight/xxx);
                TN=TN-(g.meanWeight/xxx);
              }
            }
          }
        }
      }
    }

    // ============================================================================
    // Return TP, TN, FP, FN as string (communication with Python)
    // ============================================================================
    std::ostringstream out_stream;
    out_stream << std::to_string(TP); // True positive 
    out_stream << "!"; out_stream << std::to_string(TN); // True negative 
    out_stream << "!"; out_stream << std::to_string(FP); // False positive 
    out_stream << "!"; out_stream << std::to_string(FN); // False negative 

    const std::string tmp = out_stream.str();
    char* char_ret = new char[tmp.length() + 1];
    strcpy(char_ret, tmp.c_str());
    
    double seconds= difftime(time(NULL), timerbegin);
    // ============================================================================
    std::cerr << "----------------------------------------------------------------" << std::endl;
    std::cerr << "TP=" << std::to_string(TP) << ", TN=" << std::to_string(TN) << ", FP=" << std::to_string(FP) << ", FN=" << std::to_string(FN) << std::endl;
    std::cerr << "OVERALL TIME: " << std::to_string(seconds) << " seconds" << std::endl;
    std::cerr << "================================================================\n" << std::endl;
    // ============================================================================

    return char_ret;
  }
}

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// extern: TPTNFPFN_GOLD_C (C++ <--RAM--> Python)
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
extern "C" {
  const char* TPTNFPFN_GOLD_C(char* GOLD, char* C, char* n_vertices){
    time_t timerbegin = time(NULL);
    long long n_verticesInt = std::stoi(n_vertices);

    // init clustGOLD
    clusteringO clustGOLD;
    ClustO_from_string(GOLD, &clustGOLD, n_verticesInt);

    // init clust
    clusteringO clust;
    ClustO_from_string(C, &clust, n_verticesInt);

    double n_edges=0;
    for(long long ii = 0; ii < clustGOLD.cO.size(); ii++) {
      if (clustGOLD.aliveO[ii]){
        for (auto i : clustGOLD.cO[ii]){
          for (auto j : clustGOLD.cO[ii]){
            if (i < j){
              double xxx=0;
              for (auto k : clustGOLD.membO[i]){
                if (clustGOLD.membO[j].end() != clustGOLD.membO[j].find(k)){
                  xxx=xxx+1;
                }
              }
              n_edges=n_edges+(1/xxx);
            }
          }
        }
      }
    }

    // ============================================================================
    std::cerr << "\n================================================================" << std::endl;
    std::cerr << "TPTNFPFN_GOLD_C(Gold,C): " << "Gold:[" << std::to_string(clustGOLD.nbmO) << " module(s)], ";
    std::cerr << "C:[" << std::to_string(clust.nbmO) << " module(s)]" << std::endl;
    // ============================================================================
    // init TP, FP, FN
    double TP=0, TN=0, FP=0, FN=0;
    TN=(((double(n_verticesInt)*double((n_verticesInt-1))*0.5)-n_edges));
    FN=n_edges;
    bool Eclust, Egold;
    // ------------------------------------------------------------------------------------
    for(long long ii = 0; ii < clust.cO.size(); ii++) {
      if (clust.aliveO[ii]){
        for (auto i : clust.cO[ii]){
          for (auto j : clust.cO[ii]){
            if (i < j){
              double xxx=0;
              for (auto k : clust.membO[i]){
                if (clust.membO[j].end() != clust.membO[j].find(k)){
                  xxx=xxx+1;
                }
              }
              Egold=false;
              for (auto k : clustGOLD.membO[i]){
                if (clustGOLD.membO[j].end() != clustGOLD.membO[j].find(k)){
                  Egold=true;
                  break;
                }
              }
              //
              if (Egold){
                TP=TP+(1.0/xxx);
                FN=FN-(1.0/xxx);
              }
              else{
                FP=FP+(1.0/xxx);
                TN=TN-(1.0/xxx);
              }
            }
          }
        }
      }
    }

  // ============================================================================
  // Return TP, TN, FP, FN as string (communication with Python)
  // ============================================================================
    std::ostringstream out_stream;
    out_stream << std::to_string(TP); // True positive 
    out_stream << "!"; out_stream << std::to_string(TN); // True negative 
    out_stream << "!"; out_stream << std::to_string(FP); // False positive 
    out_stream << "!"; out_stream << std::to_string(FN); // False negative 

    const std::string tmp = out_stream.str();
    char* char_ret = new char[tmp.length() + 1];
    strcpy(char_ret, tmp.c_str());
    
    double seconds= difftime(time(NULL), timerbegin);
    // ============================================================================
    std::cerr << "----------------------------------------------------------------" << std::endl;
    std::cerr << "TP=" << std::to_string(TP) << ", TN=" << std::to_string(TN) << ", FP=" << std::to_string(FP) << ", FN=" << std::to_string(FN) << std::endl;
    std::cerr << "OVERALL TIME: " << std::to_string(seconds) << " seconds" << std::endl;
    std::cerr << "================================================================\n" << std::endl;

    return char_ret;
  }
}

