
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// main: mmm (C++ <--RAM--> Python)
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
extern "C" {
  const char* mmm(char* GraphString, char* ClustZero, char* BetaIn, char* RandNode, char* EpsilonIN, char* Verbose){
    double Beta = std::stod(BetaIn);
    double Epsilon = std::stod(EpsilonIN);
    long long VerboseInt = std::stoi(Verbose);
    long long RandNodeInt = std::stoi(RandNode);

    // ===================================================================
    std::cerr << "\n================================================================" << std::endl;
    std::cerr << "nPnB-QUICK-BEC: mmm with: " << "Beta=" << std::to_string(Beta) ;
    std::cerr << ", Epsilon="<< std::to_string(Epsilon) << std::endl;
    // ===================================================================

    // import g the graph
    graph g;
    graph_from_string(GraphString, &g, RandNodeInt);
    // ===================================================================
    std::cerr << "G:" << std::to_string(g.nbv ) << " vertices, " <<  std::to_string(g.nbe) << " edges, ";
    std::cerr << std::to_string(g.meanWeight) << " = mean edges weight" << std::endl;
    // ===================================================================
    
    // import clust the partitional clustering on the graph g (where its modules are sets of nodes of g)
    clusteringP clust;
    ClustP_from_string(ClustZero, &clust, g.nbv);

    time_t timerbegin = time(NULL); double seconds;
    time_t timerintermed = time(NULL);

    // initialize clust, TP, TN, FP, FN (where modules of clust are connex in g)
    tuple_dddd TP_TN_FP_FN;
    TP_TN_FP_FN = clust_with_connex_modules(&g, &clust);
    double TP, TN, FP, FN;
    std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;

    // initialize Prec, Rec, FSCORE (the intrinsec scores of clust with respect to g)
    double Prec, Rec, FSCORE;
    std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);

    // ===================================================================
    std::cerr << "Clust.Input |C0|=" << std::to_string(clust.nbmP) << std::endl;
    std::cerr << "-->Connex modules in G: |C|=" << std::to_string(clust.nbmP) << ":";
    std::cerr << " ("  << difftime(time(NULL), timerintermed) << " seconds)" << std::endl;

    std::cerr << "   P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec);
    std::cerr <<  ", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE) << std::endl;
    std::cerr << "----------------------------------------------------------------\n" << std::endl;
    timerintermed = time(NULL);  
    // ===================================================================
    Supergraph G;
    clusteringP CLUST;
    bool CONT=true;

    while (CONT){
      double CONTFSCORE = FSCORE;
      
      TP_TN_FP_FN = MakePartition(&g, &clust, TP_TN_FP_FN, Beta, Epsilon);
      TP_TN_FP_FN = clust_with_connex_modules(&g, &clust);
      std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
      std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);
      // ===================================================================
      std::cerr << "----------------------------------------------------------------" << std::endl;
      std::cerr << "NODES MOVE-->|C|=" << std::to_string(clust.nbmP) << ": ";
      std::cerr << "P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec);
      std::cerr <<  ", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE);
      std::cerr << " ("  << difftime(time(NULL), timerintermed) << " seconds)" << std::endl;
      std::cerr << "----------------------------------------------------------------" << std::endl;
      timerintermed = time(NULL);  
      // ===================================================================

      if (FSCORE==CONTFSCORE){
        CONT=false;
      }
      else{
        CONTFSCORE=FSCORE;
        initSupergraph(&g, &clust, &G);
        initSuperClust(&G, &CLUST);

        TP_TN_FP_FN = MakeSuperPartition(&G, &CLUST, TP_TN_FP_FN, Beta, &clust, g.meanWeight);
        Superclust_2_clust(&g, &clust, &G, &CLUST);
        TP_TN_FP_FN = clust_with_connex_modules(&g, &clust);
        std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
        std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);
        // ===================================================================
        std::cerr << "MODULES MOVE-->|C|=" << std::to_string(clust.nbmP) << ": ";
        std::cerr << "P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec);
        std::cerr <<  ", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE);
        std::cerr << " ("  << difftime(time(NULL), timerintermed) << " seconds)" << std::endl;
        std::cerr << "----------------------------------------------------------------" << std::endl;
        timerintermed = time(NULL);  
        // ===================================================================

        if (FSCORE==CONTFSCORE){
          CONT=false;
        }
        else{
          CONTFSCORE=FSCORE;
          TP_TN_FP_FN = MakePartition(&g, &clust, TP_TN_FP_FN, Beta, Epsilon);
          TP_TN_FP_FN = clust_with_connex_modules(&g, &clust);
          std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
          std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);
          // ===================================================================
          std::cerr << "NODES MOVE-->|C|=" << std::to_string(clust.nbmP) << ": ";
          std::cerr << "P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec);
          std::cerr <<  ", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE);
          std::cerr << " ("  << difftime(time(NULL), timerintermed) << " seconds)" << std::endl;
          std::cerr << "----------------------------------------------------------------\n" << std::endl;
          timerintermed = time(NULL);  
          // ===================================================================
          if (Epsilon==0.0){ // We want to promote quality
            if (FSCORE==CONTFSCORE){
              CONT=false;
            }
          }
          else{ // We want to promote speed
            CONT=false; // To speed up calculations: A single round in the while loop is sufficient for good quality.
          }
        }
      }
    }
 
    // ============================================================================
    // Return clust as string (communication with Python)
    // ============================================================================
    seconds = difftime(time(NULL), timerbegin);
    std::ostringstream out_stream;
    for(long long i = 0; i < clust.cP.size(); i++) {
      if(clust.aliveP[i]) {
        long long length = clust.cP[i].size();
        long long itit = 0;
        for(auto it = clust.cP[i].begin(); it != clust.cP[i].end(); it++) {
          itit = itit +1;
          out_stream << std::to_string(*it);
          if(itit != length){out_stream << ",";}
        }  
        out_stream << "!";
      }
    }
    double FSCORE1;
    if ((Prec + Rec) > 0){FSCORE1 = (2) * ((Prec * Rec) / (Prec + Rec));} else {FSCORE1=0;}

    out_stream << "#"; out_stream << std::to_string(Prec); // Precision
    out_stream << "#"; out_stream << std::to_string(Rec); // Recall
    out_stream << "#"; out_stream << std::to_string(FSCORE1); // F1 score
    out_stream << "#"; out_stream << std::to_string(FSCORE); // Fbeta score
    out_stream << "#"; out_stream << std::to_string(TP); // True positive 
    out_stream << "#"; out_stream << std::to_string(TN); // True negative 
    out_stream << "#"; out_stream << std::to_string(FP); // False positive 
    out_stream << "#"; out_stream << std::to_string(FN); // False negative 
    out_stream << "#"; out_stream << std::to_string(seconds);

    const std::string tmp = out_stream.str();
    char* char_ret = new char[tmp.length() + 1];
    strcpy(char_ret, tmp.c_str());

    // ============================================================================
    std::cerr << "----------------------------------------------------------------" << std::endl;
    std::cerr << "Clust.Output: |C|=" << std::to_string(clust.nbmP) << ", TP=" << std::to_string(TP) << ", TN=" << std::to_string(TN) << ", FP=" << std::to_string(FP) << ", FN=" << std::to_string(FN) << std::endl;
    std::cerr << "P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec) <<", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE) << std::endl;
    std::cerr << "OVERALL TIME: " << std::to_string(seconds) << " seconds" << std::endl;
    std::cerr << "================================================================\n" << std::endl;
    // ============================================================================

    return char_ret;
  }
}

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// main: overlaps (C++ <--RAM--> Python)
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
extern "C" {
  const char* overlaps(char* GraphString, char* ClustZero, char* BetaIn, char* RandNode, char* Verbose){
    double Beta = std::stod(BetaIn);
    long long VerboseInt = std::stoi(Verbose);
    long long RandNodeInt = std::stoi(RandNode);

    // ===================================================================
    std::cerr << "\n================================================================" << std::endl;
    std::cerr << "nPnB-QUICK-BEC: Overlaps with: " << "Beta=" << std::to_string(Beta) << std::endl;
    // ===================================================================

    // import g the graph
    graph g;
    graph_from_string(GraphString, &g, RandNodeInt);

    // ===================================================================
    std::cerr << "G:" << std::to_string(g.nbv ) << " vertices, " <<  std::to_string(g.nbe) << " edges, ";
    std::cerr << std::to_string(g.meanWeight) << " = mean edges weight" << std::endl;
    // ===================================================================

   // import clust the partitional clustering on the graph g (where its modules are sets of nodes of g)
   clusteringP clust;
   ClustP_from_string(ClustZero, &clust, g.nbv);
   time_t timerbegin = time(NULL); double seconds; 

   // initialize clust, TP, TN, FP, FN (where modules of clust are connex in g)
   time_t timerintermed = time(NULL);
   tuple_dddd TP_TN_FP_FN;
   TP_TN_FP_FN = clust_with_connex_modules(&g, &clust);
   double TP, TN, FP, FN;
   std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;

   // initialize Prec, Rec, FSCORE (the intrinsec scores of clust with respect to g)
   double Prec, Rec, FSCORE;
   std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);

   // ===================================================================
   std::cerr << "Clust.Input |C0|=" << std::to_string(clust.nbmP) << std::endl;
   std::cerr << "-->Connex modules in G: |C|=" << std::to_string(clust.nbmP) << ":";
   std::cerr << " ("  << difftime(time(NULL), timerbegin) << " seconds)" << std::endl;

   std::cerr << "   P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec);
   std::cerr <<  ", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE) << std::endl;
   std::cerr << "----------------------------------------------------------------\n" << std::endl;
   timerintermed = time(NULL);  
   // ===================================================================

   // init clustO
   clusteringO clustO;
   ClustO_from_string(ClustZero, &clustO, g.nbv);

   timerintermed = time(NULL); 
   TP_TN_FP_FN = MakeOverlaps(&g, &clust, &clustO, TP_TN_FP_FN, Beta);
   timerintermed = time(NULL); 

   seconds = difftime(time(NULL), timerbegin);
 
   double FSCORE1;
   if ((Prec + Rec) > 0){FSCORE1 = (2) * ((Prec * Rec) / (Prec + Rec));} else {FSCORE1=0;}
   std::ostringstream out_stream;
   for(long long i = 0; i < clustO.cO.size(); i++) {
     if(clustO.aliveO[i]) {
       long long length_x = clustO.cO[i].size();
       long long itit = 0;
       for(auto it = clustO.cO[i].begin(); it != clustO.cO[i].end(); it++) {
         itit = itit +1;
         out_stream << std::to_string(*it);
         if(itit != length_x){out_stream << ",";}
       }
       out_stream << "!";
     }
   }
 
   TN=((((g.nbv)*(g.nbv-1)*0.5)-(g.nbe))*g.meanWeight)-FP;
 
   out_stream << "#"; out_stream << std::to_string(Prec); // Precision
   out_stream << "#"; out_stream << std::to_string(Rec); // Recall
   out_stream << "#"; out_stream << std::to_string(FSCORE1); // F1 score
   out_stream << "#"; out_stream << std::to_string(FSCORE); // Fbeta score
   out_stream << "#"; out_stream << std::to_string(TP); // True positive 
   out_stream << "#"; out_stream << std::to_string(TN); // True negative 
   out_stream << "#"; out_stream << std::to_string(FP); // False positive 
   out_stream << "#"; out_stream << std::to_string(FN); // False negative 
   out_stream << "#"; out_stream << std::to_string(seconds);
 
   const std::string tmp = out_stream.str();
   char* char_ret = new char[tmp.length() + 1];
   strcpy(char_ret, tmp.c_str());
 
   // ============================================================================
   std::cerr << "----------------------------------------------------------------" << std::endl;
   std::cerr << "Clust.Output:|C|=" << std::to_string(clustO.nbmO) << ", P=" << std::to_string(Prec) << ", R=" << std::to_string(Rec) <<", F(Beta=" << std::to_string(Beta) << ")=" << std::to_string(FSCORE) << std::endl;
   std::cerr << "OVERALL TIME: " << std::to_string(seconds) << " seconds" << std::endl;
   std::cerr << "================================================================\n" << std::endl;
   // ============================================================================

   return char_ret;
  }
}

