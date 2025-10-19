
// ====================================================================================
// tokenize
// ====================================================================================
void tokenize(std::string const &str, const char delim, std::vector<std::string> &out){
  size_t start;
  size_t end = 0;
  while ((start = str.find_first_not_of(delim, end)) != std::string::npos){
    end = str.find(delim, start);
    out.push_back(str.substr(start, end - start));
  }
}

// ====================================================================================
// Acomp_tuple_ld_ON_l (Comparison to be called in std::sort)
// ====================================================================================
bool Acomp_tuple_ld_ON_l(tuple_ld a, tuple_ld b){ // For Ascending order
  return (std::get<0>(a)<std::get<0>(b));
}

// ====================================================================================
// Acomp_tuple_ldd_ON_l (Comparison to be called in std::sort)
// ====================================================================================
bool Acomp_tuple_ldd_ON_l(tuple_ldd a, tuple_ldd b){ // For Ascending order
  return (std::get<0>(a)<std::get<0>(b));
}

// ====================================================================================
// AAcomp_tuple_lld_ON_ll (Comparison to be called in std::sort)
// ====================================================================================
bool AAcomp_tuple_lld_ON_ll(tuple_lld a, tuple_lld b){ // For Ascending Ascending order
  if (std::get<0>(a) == std::get<0>(b)){
    return (std::get<1>(a)<std::get<1>(b));
  }
  else{
    return (std::get<0>(a)<std::get<0>(b));
  }
}

// ====================================================================================
// Dcomp_tuple_lld_ON_d (Comparison to be called in std::sort)
// ====================================================================================
bool Dcomp_tuple_lld_ON_d(tuple_lld a, tuple_lld b) { // For Descending order 
  double xa = std::get<2>(a);
  double xb = std::get<2>(b);
  return (xa>xb);
  }

// ====================================================================================
// PRF
// ====================================================================================
tuple_ddd PRF(double TP, double FP, double FN, double Beta) {
  // See: Two antagonistic objectives for one multi-scale graph clustering framework,
  //      Bruno Gaume, Ixandra Achitouv, David Chavalarias,
  //      Nature Scientific Reports (2025).
  //      https://www.nature.com/articles/s41598-025-90454-w
  
  double Prec = ((TP + FP) > 0)?TP/(TP + FP):0;
  double Rec = ((TP + FN) > 0)?TP/(TP+ FN):0;
  double FSCORE = ((Prec + Rec) > 0)?(1 + (Beta*Beta)) * ((Prec * Rec) / (((Beta*Beta) * Prec) + Rec)):0;
  return std::make_tuple(Prec, Rec, FSCORE);
}

// ====================================================================================
// graph_from_string
// ====================================================================================
void graph_from_string(char* input, graph  * g, long long RandNodeInt) {
  /*
    // graph g; // g is a weighted graph:
    typedef struct {
        long long nbv; // g.nbv is the number of vertices of g
        long long nbe; // g.nbe is the number of edges of g
        double sumWeight; // g.sumWeight is the sum of the weights of all the edges of g
        double meanWeight; // g.meanWeight is the average weights of the edges of g
        vect_l I; // The vertices of g

        vect_vect_l neighbors; // g.neighbors[x] is a vector<long long> of the neighbors of the vertex x (g.neighbors[x] is sorted in ascending order)
        vect_vect_d weight; // g.weight[x] is a vector<double> of the weights of the edges {x,y} (where the y are the neighbors of x)
            A NOTE, g.neighbors[x] is sorted in ascending order and is aligned with g.weight[x]:
            for(long long i = 0; i < g.neighbors[30].size(); i++) {
                long long y=g.neighbors[30][i]; // y is the ith neighbor of the node 30
                double w=g.weight[30].at(i); // w is the weight of the edge {30,y}
            }
      } graph;
  */
  const char d1 = '!';
  const char d2 = ',';
  std::vector<std::string> LINES;
  tokenize(input, d1, LINES);

  (*g).nbv=stoi(LINES[0]); // initializes nbv (the number of vertices)

  long long nbe = 0;
  for(long long i = 1; i < LINES.size(); i++) {
    std::istringstream sline(LINES[i]);
    std::string tok1; std::getline(sline,tok1,d2); nodeid tok1int = stoi(tok1);
    std::string tok2; std::getline(sline,tok2,d2); nodeid tok2int = stoi(tok2);
    nbe = nbe + 1;
  }

  (*g).nbe=nbe; // initializes nbe (the number of edges)

  (*g).I.resize((*g).nbv);
  for (long long k=0; k<(*g).nbv; ++k) {
    (*g).I[k]=k;
  }
  if (RandNodeInt == 1) { 
    std::random_shuffle((*g).I.begin(), (*g).I.end());
  }

  vect_vect_tuple_ld graphweight;
  graphweight.resize((*g).nbv);

  (*g).sumWeight=0; // initializes sumWeight (the sum of the weights of all edges)
  for(long long i = 1; i < LINES.size(); i++) {
    std::istringstream sline(LINES[i]);
    std::string tok1; std::getline(sline,tok1,d2); nodeid tok1int = stoi(tok1);
    std::string tok2; std::getline(sline,tok2,d2); nodeid tok2int = stoi(tok2);
    std::string tok3; std::getline(sline,tok3,d2); double tok3double = stod(tok3);
    if (tok1int != tok2int){
      graphweight[tok1int].push_back (std::make_tuple(tok2int,tok3double));
      graphweight[tok2int].push_back (std::make_tuple(tok1int,tok3double));
      (*g).sumWeight=(*g).sumWeight+tok3double;
    }
  }

  if (nbe > 0){// initializes meanWeight (the average of the weights of all edges)
    (*g).meanWeight=(*g).sumWeight/nbe;
  }
  else{
    (*g).meanWeight=1;
  }

  (*g).neighbors.resize((*g).nbv);
  (*g).weight.resize((*g).nbv);
  for (long long k=0; k<(*g).nbv; ++k) {
    std::sort(graphweight[k].begin(), graphweight[k].end(), Acomp_tuple_ld_ON_l);
    for(auto it = graphweight[k].begin(); it != graphweight[k].end(); it++){
      (*g).neighbors[k].push_back (std::get<0>(*it)); // initializes the edge {k,*it}
      (*g).weight[k].push_back (std::get<1>(*it)); // initializes the weight of the edge {k,*it}
    }
  }
}

// ====================================================================================
// nodeposition: The position of a neighboring node      
// ====================================================================================
long long nodeposition(vect_l * vi, nodeid j) {
  // vi is a vector<long long> containing the OUTneighbors of a node i (the elements of vi shall already be sorted)
  // IF j is in vi THEN Return the position of j in vi ELSE Return -1
  //    COMPLEXITY: On average, logarithmic in N=vi.size() (the number of OUTneighbors of the node i) 
  //    Performs approximately log2(N)+1 element comparisons.
  std::vector<nodeid>::iterator low;
  long long poslow;
  low = std::lower_bound((*vi).begin(), (*vi).end(), j); // COMPLEXITY: On average, logarithmic in vi.size() (see https://cplusplus.com/reference/algorithm/lower_bound/)
  if (!(low == (*vi).end())){
    poslow = low - (*vi).begin();
    if ((*vi).at(poslow)==j){ 
      return poslow;
    }
    else{
      return -1;
    }
  }
  else{
    return -1;
  }
}

// ====================================================================================
// print_graph    
// ====================================================================================
void print_graph(graph * g) {
  std::cerr << "================================================================" << std::endl;
  std::cerr << "nPnB-QUICK-BEC, GRAPH:" << std::endl;
  std::cerr << "================================================================" << std::endl;
  std::cerr << "g.nbv="<< (*g).nbv << std::endl;
  std::cerr << "g.nbe="<< (*g).nbe << std::endl;
  std::cerr << "g.sumWeight="<< (*g).sumWeight << std::endl;
  std::cerr << "g.meanWeight="<< (*g).meanWeight << std::endl;
  for (long long k=0; k<(*g).nbv; ++k) {
    std::cerr << k << ": ";
    for (long long i=0; i<(*g).neighbors[k].size(); i++){
      std::cerr << "(" << k << ", " << (*g).neighbors[k][i] << ", [" << (*g).weight[k][i] << "]), ";
    }
    std::cerr << std::endl;
  }
  std::cerr << "================================================================" << std::endl;
}

// ====================================================================================
// ClustP_from_string (for clusterings without overlaps)
// ====================================================================================
void ClustP_from_string(std::string input, clusteringP * clust, long long nbv) {
  /*
    typedef struct {
        long long nbvP; // clust.nbvP is the number of vertices of the support graph (g.nbv)
        long long nbmP; // clust.nbmP is the number of living modules
        vect_set_l cP; // clust.cP[3] is the module number 3
        vect_b aliveP; // bool x=clust.aliveP[3]: IF x==true THEN module number 3 is alive ELSE it is dead
        vect_l membP; // long long x=clust.membP[30]: The vertex number 3O is a member of the module number x
    } clusteringP;
  */
  (*clust).nbvP = nbv;
  vect_set_l c; c.resize(nbv); (*clust).cP=c;
  vect_l memb; memb.resize(nbv); (*clust).membP=memb;
  vect_b alive; alive.resize(nbv); (*clust).aliveP=alive;

  for(nodeid i = 0; i < nbv; i++) {
    (*clust).aliveP[i] = false;
  }
  const char d1 = '!';
  const char d2 = ',';
  std::vector<std::string> LINES1;
  tokenize(input, d1, LINES1);
 
  long long nbmP=0;
  for (auto line1 : LINES1){
    set_l mod_i;
    std::vector<std::string> LINES2;
    tokenize(line1, d2, LINES2);

    for (auto line2 : LINES2){
      nodeid nid = std::stoi(line2);
      mod_i.insert(nid);
      (*clust).membP[nid] = nbmP;
    }
    (*clust).cP[nbmP] = mod_i;
    (*clust).aliveP[nbmP] = true;
    nbmP=nbmP+1;
  }
  (*clust).nbmP = nbmP;
}

// ====================================================================================
// emptyClustP
// ====================================================================================
void emptyClustP(clusteringP * clust){
  (*clust).nbvP=0;
  (*clust).nbmP=0;
  (*clust).aliveP.clear();
  (*clust).membP.clear();
  (*clust).cP.clear();
}

// ====================================================================================
// print_clustP
// ====================================================================================
void print_clustP(clusteringP * clust){
  std::cerr << "================================================================" << std::endl;
  std::cerr << "nPnB-QUICK-BEC, CLUSTP:" << std::endl;
  std::cerr << "================================================================" << std::endl;
  std::cerr << "clust.nbvP="<< (*clust).nbvP << std::endl;
  std::cerr << "clust.nbmP="<< (*clust).nbmP << std::endl;
  
  std::cerr << "\nMODULES;" << std::endl;
  for(long long i = 0; i < (*clust).cP.size(); i++) {
    long long length_x = (*clust).cP[i].size();
    long long itit = 0;
    std::cerr << "mod "  << i << ": {";
    for(auto it = (*clust).cP[i].begin(); it != (*clust).cP[i].end(); it++) {
      itit = itit +1;
      std::cerr <<  *it;
      if(itit != length_x){std::cerr << ",";}
    }
    std::cerr << "}" << " aliveP=" << (*clust).aliveP[i] << std::endl;
  }
  std::cerr << "\nMEMBER NODES:" << std::endl;
  for(long long i = 0; i < (*clust).membP.size(); i++) {
    std::cerr << i << ":" << (*clust).membP[i];
    if (i==(*clust).nbvP-1){
      std::cerr << std::endl;
    }
    else{
      std::cerr << ", ";
    }
  }
  std::cerr << "================================================================" << std::endl;
}

// ====================================================================================
// emptySupergraph
// ====================================================================================
void emptySupergraph(Supergraph * G){
  (*G).Super_nbv=0;
  (*G).Super_nodes.clear();
  (*G).Super_nbe=0; 
  (*G).Super_neighbors.clear(); 
  (*G).Super_weight.clear();
}

// ====================================================================================
// initSupergraph
// ====================================================================================
void initSupergraph(graph * g, clusteringP * clust, Supergraph * G){
  /*
    // Supergraph G; // G is a weighted graph, a vertex represents a module of a clusteringP clust on a graph g
    typedef struct {
        long long Super_nbv; // G.Super_nbv is the number of vertices of G (The number of living modules of clust)
        long long Super_nbe; // G.Super_nbe is the number of edges of G
        vect_l Super_nodes;  // clust.cP[G.Super_nodes[x]] is the module of clust that the vertex x represents
        vect_vect_l Super_neighbors; // G.Super_neighbors[x] is a vector<long long> of the neighbors of the vertex x (G.Super_neighbors[x] is sorted in ascending order)
        vect_vect_tuple_dd Super_weight; // G.Super_weight[x] is a vector<tuple<double, double>> of the Superweight of the edges {x,y} (where the y are the neighbors of x)
        
            G.Super_neighbors[x] is sorted in ascending order and is aligned with G.Super_weight[x]:
            for(long long i = 0; i < G.Super_neighbors[30].size(); i++) {
                long long y=G.Super_neighbors[30][i]; // y is the ith neighbor of the node 30
                tuple<double, double> W=G.Super_weight[30].at(i); // W is the Superweight of the edge {30,y}
                // IF
                //      W is equal to: <a,b>
                //      modx is equal to:  clust.cP[G.Super_nodes[30]] (modx is the module of clust that the vertex x represents)
                //      mody is equal to: clust.cP[G.Super_nodes[y]] (mody is the module of clust that the vertex y represents)
                // THEN
                //      a is equal to: the total of the weights of the edges between modx and mody in the graph g
                //      b is equal to: g.meanWeight * (the number of non-edges between the nodes of modx and the nodes of mody in the graph g)
            }
      } Supergraph;
  */
  emptySupergraph(G);
  (*G).Super_nbv=(*clust).nbmP;
  (*G).Super_nodes.resize((*clust).nbmP);
  //
  std::map<long long, long long> D;
  long long ii=0;
  for(long long i = 0; i < (*clust).cP.size(); i++) {
    if ((*clust).aliveP[i]) {
      (*G).Super_nodes[ii]=i;
      D[i]=ii;
      ii = ii+1;
    }
  }
  //
  vect_tuple_lld V;
  for (long long k=0; k<(*g).nbv; ++k) {
    for (long long i=0; i<(*g).neighbors[k].size(); i++){
      if (k<(*g).neighbors[k][i]){
        if (!(D[(*clust).membP[k]] == D[(*clust).membP[(*g).neighbors[k][i]]])){
          V.push_back(std::make_tuple(D[(*clust).membP[k]], D[(*clust).membP[(*g).neighbors[k][i]]], (*g).weight[k][i]));
          V.push_back(std::make_tuple(D[(*clust).membP[(*g).neighbors[k][i]]], D[(*clust).membP[k]], (*g).weight[k][i]));
        }
      }
    }
  }
  std::sort(V.begin(), V.end(), AAcomp_tuple_lld_ON_ll);
  //
  (*G).Super_neighbors.resize((*clust).nbmP);
  (*G).Super_weight.resize((*clust).nbmP);
  (*G).Super_nbe = 0;

  long long x, y, nbe_x_y=0, Super_nbe=0;
  double w;
  if (V.size()>0){
    std::tie (x, y, w) = V[0];
    w=0;
    for (long long i=0; i<V.size(); i++){
      long long xi, yi; double wi;
      std::tie (xi, yi, wi) = V[i];
      if ((x==xi) && (y==yi)){
        w=w+wi;
        nbe_x_y=nbe_x_y+1;
      }
      else{
        Super_nbe=Super_nbe+1;
        double w_no_edge = (((*clust).cP[(*G).Super_nodes[x]].size() * (*clust).cP[(*G).Super_nodes[y]].size())-nbe_x_y) * (*g).meanWeight;
        
        (*G).Super_neighbors[x].push_back(y);
        (*G).Super_weight[x].push_back (std::make_tuple(w, w_no_edge));

        x=xi; y=yi; w=wi; nbe_x_y=1;
      }
    }
    Super_nbe=Super_nbe+1;
    double w_no_edge = (((*clust).cP[(*G).Super_nodes[x]].size() * (*clust).cP[(*G).Super_nodes[y]].size())-nbe_x_y) * (*g).meanWeight;
        
    (*G).Super_neighbors[x].push_back(y);
    (*G).Super_weight[x].push_back (std::make_tuple(w, w_no_edge));
  
    (*G).Super_nbe = Super_nbe;
  }
}

// ====================================================================================
// print_Supergraph
// ====================================================================================
void print_Supergraph(graph *g, clusteringP * clust, Supergraph * G) {
  std::cerr << "================================================================" << std::endl;
  std::cerr << "nPnB-QUICK-BEC, SUPERGRAPH:" << std::endl;
  std::cerr << "================================================================" << std::endl;
  std::cerr << "G.Super_nbv="<< (*G).Super_nbv << std::endl;
  std::cerr << "G.Super_nbe="<< (*G).Super_nbe << std::endl;

  for (long long k=0; k<(*G).Super_nbv; ++k) {
    std::cerr << k ;
    long long length_x = (*clust).cP[(*G).Super_nodes[k]].size();
    long long itit = 0;
    std::cerr << "=mod "  << (*G).Super_nodes[k] << ": [";
    for(auto it = (*clust).cP[(*G).Super_nodes[k]].begin(); it != (*clust).cP[(*G).Super_nodes[k]].end(); it++) {
      itit = itit +1;
      std::cerr <<  *it;
      if(itit != length_x){std::cerr << ",";}
    }
    std::cerr << "] ";
    for (long long i=0; i<(*G).Super_neighbors[k].size(); i++){
        double a, b;
        std::tie (a,b) = (*G).Super_weight[k][i];
        std::cerr << "(" << k << ", " << (*G).Super_neighbors[k][i] << ", [" << a << ", " << b << "]), ";
    }
    std::cerr << std::endl;
  }
  std::cerr << "================================================================" << std::endl;
}

// ====================================================================================
// initSuperClust
// ====================================================================================
void initSuperClust(Supergraph * G, clusteringP * SuperClust){
  emptyClustP(SuperClust);
  (*SuperClust).nbvP = (*G).Super_nbv;
  (*SuperClust).nbmP = (*G).Super_nbv;
  (*SuperClust).cP.resize((*G).Super_nbv);
  (*SuperClust).membP.resize((*G).Super_nbv);
  (*SuperClust).aliveP.resize((*G).Super_nbv);
  for (long long k=0; k<(*G).Super_nbv; ++k) {
    (*SuperClust).aliveP[k]=true;
    (*SuperClust).membP[k]=k;
    set_l mod_k;
    mod_k.insert(k);
    (*SuperClust).cP[k]=mod_k;
  }
}

// ====================================================================================
// Superclust_2_clust 
// ====================================================================================
void Superclust_2_clust(graph *g, clusteringP * clust, Supergraph * G, clusteringP * SuperClust){
  clusteringP newclust;
  newclust.nbvP = (*g).nbv;
  newclust.nbmP = 0;
  newclust.cP.resize((*g).nbv);
  newclust.membP.resize((*g).nbv);
  newclust.aliveP.resize((*g).nbv);
  for(nodeid i = 0; i < (*g).nbv; i++) {
    newclust.aliveP[i] = false;
  }
  long long ii=0;
  for(long long i = 0; i < (*SuperClust).nbvP; i++) {
    if ((*SuperClust).aliveP[i]) {
      set_l mod;
      for(auto it = (*SuperClust).cP[i].begin(); it != (*SuperClust).cP[i].end(); it++){
        for(auto itit = (*clust).cP[(*G).Super_nodes[*it]].begin(); itit != (*clust).cP[(*G).Super_nodes[*it]].end(); itit++){
          mod.insert(*itit);
          newclust.membP[*itit]=ii;
        }
      }
      newclust.nbmP=newclust.nbmP + 1;
      newclust.aliveP[ii]=true;
      newclust.cP[ii]=mod;
      ii=ii+1;
    }
  }
  emptyClustP(clust);
  (*clust).nbvP=newclust.nbvP;
  (*clust).nbmP=newclust.nbmP;
  (*clust).cP.resize((*g).nbv);
  (*clust).membP.resize((*g).nbv);
  (*clust).aliveP.resize((*g).nbv);
  for(long long i = 0; i < newclust.nbvP; i++) {
    (*clust).membP[i]=newclust.membP[i];
    (*clust).aliveP[i]=newclust.aliveP[i];
    (*clust).cP[i]=newclust.cP[i];
  }
}

// ====================================================================================
// Localpartcon
// ====================================================================================
set_set_l Localpartcon(graph * graph, clusteringP * clust, long long m){
  set_set_l componentS;
  vect_l MOD;
  vect_b visited;
  for(auto it = (*clust).cP[m].begin(); it != (*clust).cP[m].end(); it++){
    MOD.push_back(*it);
    visited.push_back(false);
  }
  long long SIZEMOD=(*clust).cP[m].size();
  long long k=0;
  long long nbvisited=0;
  bool CONT=true;
  while (CONT){
    if (not visited[k]){
      set_l component;
      std::queue<nodeid> q;
      q.push(MOD[k]);
      visited[k] = true;
      while (!q.empty()) {
        nodeid node = q.front();
        q.pop();
        component.insert(node);
        nbvisited=nbvisited+1;
        for (long long i=0; i<SIZEMOD; ++i) {
          if (((std::binary_search((*graph).neighbors[node].begin(), (*graph).neighbors[node].end(), MOD[i]))) && !visited[i]){ // one edge {node, MOD[i]} in *graph
            visited[i] = true;
            q.push(MOD[i]);
          }
        }
      }
      if (!component.empty()){componentS.insert(component);}
    }
    k=k+1;
    if ((k==SIZEMOD) or (nbvisited==SIZEMOD)){CONT=false;}
  }
  return componentS;
}


// ====================================================================================
// clust_with_connex_modules
// ====================================================================================
tuple_dddd clust_with_connex_modules(graph * graph, clusteringP * clust){
  double TP=0, FP=0, FN=(*graph).sumWeight;
  double TN=(((*graph).nbv * ((*graph).nbv-1) * 0.5) - (*graph).nbe) * (*graph).meanWeight;

  clusteringP newclust;
  newclust.nbvP = (*graph).nbv;
  newclust.nbmP = 0;
  newclust.cP.resize((*graph).nbv);
  newclust.membP.resize((*graph).nbv);
  newclust.aliveP.resize((*graph).nbv);

  for(nodeid i = 0; i < (*graph).nbv; i++) {
    newclust.aliveP[i] = false;
  }

  for(long long ii = 0; ii < (*clust).cP.size(); ii++) {
    if ((*clust).aliveP[ii]){
      set_set_l componentS=Localpartcon(graph, clust, ii);
      for(auto it = componentS.begin(); it != componentS.end(); it++) {
        set_l mod_it;
        for (auto i : *it){
          mod_it.insert(i);
          newclust.membP[i] = newclust.nbmP;
          for (auto j : *it){
            if (i < j){
              long long pos_node=nodeposition(&((*graph).neighbors[i]), j);
              if (!(pos_node==-1)) { // one edge {i,j} in graph
                TP=TP+(*graph).weight[i].at(pos_node);
                FN=FN-(*graph).weight[i].at(pos_node);
              }
              else{ // no edge {i,j} in graph
                FP=FP+(*graph).meanWeight;
                TN=TN-(*graph).meanWeight;
              }
            }
          }
        }
        newclust.cP[newclust.nbmP] = mod_it;
        newclust.aliveP[newclust.nbmP] = true;
        newclust.nbmP = newclust.nbmP+1;
      }
    }
  }

  emptyClustP(clust);
  (*clust).nbvP=newclust.nbvP;
  (*clust).nbmP=newclust.nbmP;
  (*clust).cP.resize((*graph).nbv);
  (*clust).membP.resize((*graph).nbv);
  (*clust).aliveP.resize((*graph).nbv);
  //
  for(long long i = 0; i < newclust.nbvP; i++) {
    (*clust).membP[i]=newclust.membP[i];
    (*clust).aliveP[i]=newclust.aliveP[i];
    (*clust).cP[i]=newclust.cP[i];
  }

  return std::make_tuple(TP, TN, FP, FN);
}

// ====================================================================================
// GainLeaving (when a node leaves a module, how TruePositives,  FalsePositives, and  FalseNegatives, vary)
// ====================================================================================
tuple_ddd GainLeaving(graph * g, clusteringP * clust, nodeid x, long long mod_x) {
  long long pos;
  double ACC=0;
  long long nbe=0;
  for(auto it = (*clust).cP[mod_x].begin(); it != (*clust).cP[mod_x].end(); it++) {
    if (x != *it){
      pos=nodeposition(&((*g).neighbors[x]), *it);
      if (!(pos==-1)) { // one edge {x,*it} in g
        nbe++;
        ACC=ACC+(*g).weight[x].at(pos);
      }
    }
  }
  // varyingTP, varyingFP, varyingFN
  return std::make_tuple(-ACC, -(((*clust).cP[mod_x].size()-1-nbe)*(*g).meanWeight), ACC);
}

// ====================================================================================
// GainJoining (when a node joins a module, how TruePositives,  FalsePositives, and  FalseNegatives, vary)
// ====================================================================================
tuple_ddd GainJoining(graph * g, clusteringP * clust, nodeid x, long long mod_y) {
  long long pos;
  double ACC=0;
  long long nbe=0;
  for(auto it = (*clust).cP[mod_y].begin(); it != (*clust).cP[mod_y].end(); it++) {
    pos=nodeposition(&((*g).neighbors[x]), *it);
    if (!(pos==-1)) { // one edge {x,*it} in graph
      nbe++;
      ACC=ACC+(*g).weight[x].at(pos);
    }
  }
  // varyingTP, varyingFP, varyingFN
  return std::make_tuple(ACC, ((*clust).cP[mod_y].size()-nbe)*(*g).meanWeight, -ACC);
}

// ====================================================================================
// Partition
// ====================================================================================
tuple_dddd MakePartition(graph * g, clusteringP * clust, tuple_dddd TP_TN_FP_FN, double Beta, double Epsilon){
  double TP, TN, FP, FN; std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
  double Prec, Rec, FSCORE; std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);


  double newTP, newFP, newFN, newTN;
  double newPrec, newRec, newFSCORE;

  double varyingTPiciL, varyingFPiciL, varyingFNiciL, varyingTNiciL;
  double varyingTPici, varyingFPici, varyingFNici, varyingTNici;

  double newTPici, newFPici, newFNici, newTNici;
  double newPrecici, newRecici, newFSCOREici;
  nodeid move_node, with_node;
  bool do_it;

  bool CONT=true;
  while (CONT){
    double CONTFSCORE = FSCORE;
    // ============================================================================
    // // loop on nodes x=(*g).I[k];
    // ============================================================================
    for (long long k=0; k<(*g).nbv; ++k) { // loop on nodes x=(*g).I[k];
      newFSCORE=FSCORE;
      long long x=(*g).I[k];
      long long mod_x = (*clust).membP[x];
      // *****************************************
      // IF x Leaving its module
      // *****************************************
      std::tie (varyingTPiciL, varyingFPiciL, varyingFNiciL) = GainLeaving(g, clust, x, mod_x);
      // *****************************************
      // IF x can Leave its module
      // *****************************************
      if ((*clust).cP[mod_x].size() > 1){
        newTPici=TP+varyingTPiciL; newFPici=FP+varyingFPiciL; newFNici=FN+varyingFNiciL;  newTNici=TN-varyingFPiciL;
        std::tie (newPrecici, newRecici, newFSCOREici) = PRF(newTPici, newFPici, newFNici, Beta); 
        if (newFSCOREici > newFSCORE){
          move_node = x; with_node=-1;
          newFSCORE = newFSCOREici; newPrec = newPrecici; newRec = newRecici;
          newTP = newTPici; newFP = newFPici; newFN = newFNici; newTN = newTNici;
        }
      }
      // ============================================================================
      // loop on neighbors y of x
      // ============================================================================
      set_l AlreadySeen;
      for (long long IT=0; IT<(*g).neighbors[x].size(); ++IT) { // loop on neighbors y of x
        long long y = (*g).neighbors[x][IT];
        long long mod_y = (*clust).membP[y];
        do_it = (AlreadySeen.end() == std::find(AlreadySeen.begin(), AlreadySeen.end(), mod_y));
        if((x != y) && (mod_x != mod_y) && (do_it)){
          AlreadySeen.insert(mod_y);
          // *****************************************
          // IF x Leave its module && x MOve into y's module
          // *****************************************
          std::tie (varyingTPici, varyingFPici, varyingFNici) = GainJoining(g, clust, x, mod_y);
          newTPici=TP+varyingTPiciL; newFPici=FP+varyingFPiciL; newFNici=FN+varyingFNiciL; newTNici=TN-varyingFPiciL;
          newTPici=newTPici+varyingTPici; newFPici=newFPici+varyingFPici; newFNici=newFNici+varyingFNici;
          newTNici=newTNici-varyingFPici;
          std::tie (newPrecici, newRecici, newFSCOREici) = PRF(newTPici, newFPici, newFNici, Beta);
          if (newFSCOREici > newFSCORE){
            if ((*clust).cP[mod_x].size() == 1){
            }
            move_node=x; with_node=y;
            newFSCORE=newFSCOREici; newPrec=newPrecici; newRec=newRecici;
            newTP=newTPici; newFP=newFPici; newFN=newFNici; newTN=newTNici; 
          }
        } 
      }
      // ============================================================================
      // EDIT
      // ============================================================================
      if ((newFSCORE > FSCORE)) {
        FSCORE=newFSCORE; Prec=newPrec; Rec=newRec;
        TP=newTP; FP=newFP; FN=newFN; TN=newTN;
        long long Oldmemb = (*clust).membP[move_node];
        if(with_node == -1){ // move_node ISOLATES itself in its own module
          (*clust).cP[Oldmemb].erase(move_node);
          long long i_freeClust = std::distance( (*clust).aliveP.begin(), std::find((*clust).aliveP.begin(), (*clust).aliveP.end(), false));
          (*clust).cP[i_freeClust].insert(move_node);
          (*clust).membP[move_node]=i_freeClust;
          //
          (*clust).aliveP[i_freeClust]=true;
          (*clust).nbmP=(*clust).nbmP+1;
        }
        else{ // move_node MOVES to go with with_node
          (*clust).cP[Oldmemb].erase(move_node);
          (*clust).cP[(*clust).membP[with_node]].insert(move_node);
          (*clust).membP[move_node]=(*clust).membP[with_node];
          if ((*clust).cP[Oldmemb].empty()){
            (*clust).aliveP[Oldmemb] = false;
            (*clust).nbmP=(*clust).nbmP-1;
          }
        }
        // print_clustP(&clust); // to track each edit
      }
    }
    CONT=((FSCORE-CONTFSCORE)>Epsilon);
  }
  return std::make_tuple(TP, TN, FP, FN);
}


// ====================================================================================
// SuperGainLeaving (when a node leaves a module, how TruePositives,  FalsePositives, and  FalseNegatives, vary)
// ====================================================================================
tuple_ddd SuperGainLeaving(Supergraph * G, clusteringP * CLUST, nodeid x, long long mod_x, clusteringP * clust, double meanWeight) {
  long long pos;
  double varyingTP=0, varyingFP=0, varyingFN=0;
  double a, b;
  for(auto it = (*CLUST).cP[mod_x].begin(); it != (*CLUST).cP[mod_x].end(); it++) {
    if (x != *it){
      pos=nodeposition(&((*G).Super_neighbors[x]), *it);
      if (!(pos==-1)) { // {x,*it} connected in G
        std::tie (a,b) = (*G).Super_weight[x][pos];
        varyingTP = varyingTP-a;
        varyingFP = varyingFP-b;
        varyingFN = varyingFN+a;
      }
      else{ // {x,*it} not connected in G
        varyingFP = varyingFP - (((*clust).cP[(*G).Super_nodes[x]].size() * (*clust).cP[(*G).Super_nodes[*it]].size()) * meanWeight);
      }
    }
  }
  // varyingTP, varyingFP, varyingFN
  return std::make_tuple(varyingTP, varyingFP, varyingFN);
}

// ====================================================================================
// SuperGainJoining (when a node joins a module, how TruePositives,  FalsePositives, and  FalseNegatives, vary)
// ====================================================================================
tuple_ddd SuperGainJoining(Supergraph * G, clusteringP * CLUST, nodeid x, long long mod_y, clusteringP * clust, double meanWeight) {
  long long pos;
  double varyingTP=0, varyingFP=0, varyingFN=0;
  double a, b;
  for(auto it = (*CLUST).cP[mod_y].begin(); it != (*CLUST).cP[mod_y].end(); it++) {
    pos=nodeposition(&((*G).Super_neighbors[x]), *it);
    if (!(pos==-1)) { // {x,*it} connected in G
      std::tie (a,b) = (*G).Super_weight[x][pos];
      varyingTP = varyingTP+a;
      varyingFP = varyingFP+b;
      varyingFN = varyingFN-a;
    }
    else{ // {x,*it} not connected in G
      varyingFP = varyingFP + (((*clust).cP[(*G).Super_nodes[x]].size() * (*clust).cP[(*G).Super_nodes[*it]].size()) * meanWeight);
    }
  }
  // varyingTP, varyingFP, varyingFN
  return std::make_tuple(varyingTP, varyingFP, varyingFN);
}

// ====================================================================================
// MakeSuperPartition
// ====================================================================================
tuple_dddd MakeSuperPartition(Supergraph * G, clusteringP * CLUST, tuple_dddd TP_TN_FP_FN, double Beta, clusteringP * clust, double meanWeight){

  double TP, TN, FP, FN; std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
  double Prec, Rec, FSCORE; std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);

  double newTP, newFP, newFN, newTN;
  double newPrec, newRec, newFSCORE;

  double varyingTPiciL, varyingFPiciL, varyingFNiciL, varyingTNiciL;
  double varyingTPici, varyingFPici, varyingFNici, varyingTNici;

  double newTPici, newFPici, newFNici, newTNici;
  double newPrecici, newRecici, newFSCOREici;
  nodeid move_node, with_node;
  bool do_it;

  bool CONT=true;
  while (CONT){
    CONT=false;
    // ============================================================================
    // // loop on nodes of G
    // ============================================================================
    for (long long k=0; k<(*G).Super_nbv; ++k) { // loop on nodes of G;
      newFSCORE=FSCORE;
      long long x=k;
      long long mod_x = (*CLUST).membP[x];
      // *****************************************
      // IF x Leaving its module
      // *****************************************
      std::tie (varyingTPiciL, varyingFPiciL, varyingFNiciL) = SuperGainLeaving(G, CLUST, x, mod_x, clust, meanWeight);
      // *****************************************
      // IF x can Leave its module
      // *****************************************
        if ((*CLUST).cP[mod_x].size() > 1){
          newTPici=TP+varyingTPiciL; newFPici=FP+varyingFPiciL; newFNici=FN+varyingFNiciL, newTNici=TN-varyingFPiciL;
          std::tie (newPrecici, newRecici, newFSCOREici) = PRF(newTPici, newFPici, newFNici, Beta); 
          if (newFSCOREici > newFSCORE){
            move_node = x; with_node=-1;
            newFSCORE = newFSCOREici; newPrec = newPrecici; newRec = newRecici;
            newTP = newTPici; newFP = newFPici; newFN = newFNici; newTN = newTNici;
          }
        }
      // ============================================================================
      // loop on neighbors y of x
      // ============================================================================
      set_l AlreadySeen;
      for (long long IT=0; IT<(*G).Super_neighbors[x].size(); ++IT) { // loop on neighbors y of x
        long long y = (*G).Super_neighbors[x][IT];
        long long mod_y = (*CLUST).membP[y];
        do_it = (AlreadySeen.end() == std::find(AlreadySeen.begin(), AlreadySeen.end(), mod_y));
        if((x != y) && (mod_x != mod_y) && (do_it)){
          AlreadySeen.insert(mod_y);
          // *****************************************
          // IF x Leave its module && x Move into y's module
          // *****************************************
          std::tie (varyingTPici, varyingFPici, varyingFNici) = SuperGainJoining(G, CLUST, x, mod_y, clust, meanWeight);
          newTPici=TP+varyingTPiciL; newFPici=FP+varyingFPiciL; newFNici=FN+varyingFNiciL; newTNici=TN-varyingFPiciL;
          newTPici=newTPici+varyingTPici; newFPici=newFPici+varyingFPici; newFNici=newFNici+varyingFNici;
          newTNici=newTNici-varyingFPici;
          std::tie (newPrecici, newRecici, newFSCOREici) = PRF(newTPici, newFPici, newFNici, Beta);
          if (newFSCOREici > newFSCORE){
            if ((*CLUST).cP[mod_x].size() == 1){
            }
            move_node=x; with_node=y;
            newFSCORE=newFSCOREici; newPrec=newPrecici; newRec=newRecici;
            newTP=newTPici; newFP=newFPici; newFN=newFNici; newTN=newTNici;
          }
        } 
      }
      // ============================================================================
      // EDIT
      // ============================================================================
      if ((newFSCORE > FSCORE)) {
        CONT=true;
        FSCORE=newFSCORE; Prec=newPrec; Rec=newRec;
        TP=newTP; FP=newFP; FN=newFN; TN=newTN;
        long long Oldmemb = (*CLUST).membP[move_node];
        if(with_node == -1){ // move_node ISOLATES itself in its own module
          (*CLUST).cP[Oldmemb].erase(move_node);
          long long i_freeClust = std::distance( (*CLUST).aliveP.begin(), std::find((*CLUST).aliveP.begin(), (*CLUST).aliveP.end(), false));
          (*CLUST).cP[i_freeClust].insert(move_node);
          (*CLUST).membP[move_node]=i_freeClust;
          //
          (*CLUST).aliveP[i_freeClust]=true;
          (*CLUST).nbmP=(*CLUST).nbmP+1;
        }
        else{ // move_node MOVES to go with with_node
          (*CLUST).cP[Oldmemb].erase(move_node);
          (*CLUST).cP[(*CLUST).membP[with_node]].insert(move_node);
          (*CLUST).membP[move_node]=(*CLUST).membP[with_node];
          if ((*CLUST).cP[Oldmemb].empty()){
            (*CLUST).aliveP[Oldmemb] = false;
            (*CLUST).nbmP=(*CLUST).nbmP-1;
          }
        }
      }
    }
  }
  return std::make_tuple(TP, TN, FP, FN);
}

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// OVERLAPS
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

// ====================================================================================
// ClustO_from_string (for clusterings with overlaps)
// ====================================================================================
void ClustO_from_string(std::string input, clusteringO * clust, long long nbv) {
  /*
    // clusteringO clust; // clust is an overlaping clustering on a graph g which has nbv vertices:
    typedef struct {
        long long nbvO; // clust.nbvO is the number of vertices of the support graph (g.nbv)
        long long nbmO; // clust.nbmO is the number of living modules

        vect_set_l cO;  // clust.cO[3] is the module number 3

        vect_b aliveO;  // bool x=clust.aliveO[3]: // IF x==true THEN module number 3 is alive ELSE it is dead

        vect_set_l membO;   // set_l s=clust.membO[3]; // s is a set<long long>: IF i ∈ s THEN node 3 belongs to the ith module ELSE node 3 does not belong to the ith module
        // Here is the difference with struct clusteringP where membP is a vector<long long>,
        // while here membO is a vector<set<long long>> because clust is an overlaping clustering (a node can belong to several modules)
    } clusteringO;
  */
  (*clust).nbvO = nbv;
  vect_set_l c; c.resize(nbv); (*clust).cO=c;
  vect_set_l membO; membO.resize(nbv); (*clust).membO=membO;
  vect_b alive; alive.resize(nbv); (*clust).aliveO=alive;

  for(nodeid i = 0; i < nbv; i++) {
    (*clust).aliveO[i] = false;
  }
  const char d1 = '!';
  const char d2 = ',';
  std::vector<std::string> LINES1;
  tokenize(input, d1, LINES1);
 
  long long nbmO=0;
  for (auto line1 : LINES1){
    set_l mod_i;
    std::vector<std::string> LINES2;
    tokenize(line1, d2, LINES2);
    for (auto line2 : LINES2){
      nodeid nid = std::stoi(line2);
      mod_i.insert(nid);
      (*clust).membO[nid].insert(nbmO);
    }
    (*clust).cO[nbmO] = mod_i;
    (*clust).aliveO[nbmO] = true;
    nbmO=nbmO+1;
  }
  (*clust).nbmO = nbmO;
}

// ====================================================================================
// print_clustO
// ====================================================================================
void print_clustO(clusteringO * clust){
  std::cerr << "================================================================" << std::endl;
  std::cerr << "nPnB-QUICK-BEC, CLUSTO:" << std::endl;
  std::cerr << "================================================================" << std::endl;
  std::cerr << "clust.nbvO="<< (*clust).nbvO << std::endl;
  std::cerr << "clust.nbmO="<< (*clust).nbmO << std::endl;
  
  std::cerr << "\nMODULES;" << std::endl;
  for(long long i = 0; i < (*clust).cO.size(); i++) {
    long long length_x = (*clust).cO[i].size();
    long long itit = 0;
    std::cerr << "mod "  << i << ": {";
    for(auto it = (*clust).cO[i].begin(); it != (*clust).cO[i].end(); it++) {
      itit = itit +1;
      std::cerr <<  *it;
      if(itit != length_x){std::cerr << ",";}
    }
    std::cerr << "}" << " aliveO=" << (*clust).aliveO[i] << std::endl;
  }

  std::cerr << "\nMEMBER NODES:" << std::endl;
  for(long long i = 0; i < (*clust).membO.size(); i++) {
    std::cerr << i << ": ";
    for(auto it = (*clust).membO[i].begin(); it != (*clust).membO[i].end(); it++){
      std::cerr << *it << ", ";
    }
    std::cerr << std::endl;
  }
  std::cerr << "================================================================" << std::endl;
}

// ====================================================================================
// CardIntersec
// ====================================================================================
long long CardIntersec(set_l *a, set_l *b) { // return |*a ∩ *b|
  long long acc=0;
  if((*a).size() < (*b).size()){
    for (auto i : (*a)){
      if ((*b).end() != (*b).find(i)){   
        acc=acc+1;
      }
    }
  }
  else{
    for (auto i : (*b)){
      if ((*a).end() != (*a).find(i)){   
        acc=acc+1;
      }
    }
  }
  return acc;
}

// ====================================================================================
// GainOverlaps
// ====================================================================================
tuple_ddd GainOverlaps(graph * g, clusteringO * clustO, long long x, long long mody) {
  long long pos;
  double XTP=0, XFP=0;
  for(auto it = (*clustO).cO[mody].begin(); it != (*clustO).cO[mody].end(); it++) { 
    long long CI = CardIntersec(&((*clustO).membO)[x], &((*clustO).membO)[*it]);
    // CI = number of times x and *it are together in a same module
    if (CI == 0){ // x and *it are not together in any modules
      pos=nodeposition(&(*g).neighbors[x], *it);
      if (!(pos==-1)) { // one edge {x,*it} in graph
          XTP=XTP+((*g).weight)[x].at(pos);
      }
      else{
        XFP=XFP+(*g).meanWeight;
      }
    }
  }
  return std::make_tuple(XTP, XFP, -XTP);
}

// ====================================================================================
// ModContribution
// ====================================================================================
tuple_ddd ModContribution(graph *g, clusteringO * clustO, long long mody){
  double TP=0, FP=0;
  long long pos_node;
  for (auto i : (*clustO).cO[mody]){
    for (auto j : (*clustO).cO[mody]){
      if (i < j){
        pos_node=nodeposition(&(*g).neighbors[i], j);
        if (!(pos_node==-1)) { // one edge {i,j} in graph
          TP=TP+(*g).weight[i].at(pos_node);
        }
        else{ // no edge {i,j} in graph
          FP=FP+(*g).meanWeight; 
        }
      }
    }
  }
  return std::make_tuple(TP, FP, -TP);
}

// ====================================================================================
// Acomp_mod_ON_size (Comparison to be called in std::sort)
// ====================================================================================
bool Acomp_mod_ON_size(set_l a, set_l b) { // For Ascending order
  return (a.size()<b.size());
}

// ====================================================================================
// eliminate_duplicates // j'en suis là
// ====================================================================================
  void eliminate_duplicates(clusteringO * clustO){
  for(long long ii = 0; ii < (*clustO).cO.size(); ii++) {
    (*clustO).membO[ii].erase((*clustO).membO[ii].begin(), (*clustO).membO[ii].end());
    
    if (!(*clustO).aliveO[ii]){
      (*clustO).cO[ii].erase((*clustO).cO[ii].begin(), (*clustO).cO[ii].end());
    }
    (*clustO).aliveO[ii]=false;
  }

  std::sort((*clustO).cO.begin(), (*clustO).cO.end(), Acomp_mod_ON_size); 

  for(long long ii = 0; ii < (*clustO).cO.size(); ii++) {
    if ((*clustO).cO[ii].size() > 0){
      (*clustO).aliveO[ii]=true;
      for(long long jj = ii+1; jj < (*clustO).cO.size(); jj++) {
        if ((*clustO).cO[jj].size() > 0){
          (*clustO).aliveO[jj]=true;
          long long CI=CardIntersec(&(*clustO).cO[ii], &(*clustO).cO[jj]); // CI = |(*clust)[ii] \cap (*clust)[jj]|
          if(CI==(*clustO).cO[ii].size()){
            (*clustO).aliveO[ii]=false;
            (*clustO).cO[ii].erase((*clustO).cO[ii].begin(), (*clustO).cO[ii].end());
          }
          else{
            if(CI==(*clustO).cO[jj].size()){
              (*clustO).aliveO[jj]=false;
              (*clustO).cO[jj].erase((*clustO).cO[jj].begin(), (*clustO).cO[jj].end());
            }
          }
        }
      }
    }
  }
  (*clustO).nbmO=0;
  for(long long ii = 0; ii < (*clustO).cO.size(); ii++) {
    if ((*clustO).aliveO[ii]){
      (*clustO).nbmO=(*clustO).nbmO+1;
      for(auto it = (*clustO).cO[ii].begin(); it != (*clustO).cO[ii].end(); it++) {
        (*clustO).membO[*it].insert(ii);
      }
    }
  }
}

// ====================================================================================
// MakeOverlaps
// ====================================================================================
tuple_dddd MakeOverlaps(graph * g, clusteringP * clust, clusteringO * clustO, tuple_dddd TP_TN_FP_FN, double Beta){
  double TP, TN, FP, FN; std::tie (TP, TN, FP, FN) = TP_TN_FP_FN;
  double Prec, Rec, FSCORE; std::tie (Prec, Rec, FSCORE) = PRF(TP, FP, FN, Beta);


  double newTP, newFP, newFN, newTN;
  double newPrec, newRec, newFSCORE;

  double varyingTPiciL, varyingFPiciL, varyingFNiciL, varyingTNiciL;
  double varyingTPici, varyingFPici, varyingFNici, varyingTNici;

  double newTPici, newFPici, newFNici, newTNici;
  double newPrecici, newRecici, newFSCOREici;
  nodeid move_node, with_node;
  bool do_it;
  double TOT_FN_VIRGIN = (((((*g).nbv)*((*g).nbv-1)*0.5)-((*g).nbe))*(*g).meanWeight)+(*g).sumWeight;

  double varyingTP, varyingFP, varyingFN;
  double xxxTP, xxxFP, xxxFN;
  long long itint = 0;
  vect_tuple_lld vectXMF;

  time_t timerintermed = time(NULL);
  for (long long k=0; k<(*g).nbv; ++k) { // loop on nodes x=(*g).I[k];
    time_t timerbegin = time(NULL);
    itint = itint + 1;
    long long x=(*g).I[k];
    tuple_ddd varying = std::make_tuple(0, 0, 0);
    tuple_ddd xyz =std::make_tuple(0.0, 0.0, 0.0);
    bool do_it=false, absent=false;
    long long mod_x = (*clust).membP[x];
    set_l AlreadySeen;
    AlreadySeen.insert(mod_x);
    for (long long IT=0; IT<(*g).neighbors[x].size(); ++IT) { // loop on neighbors y of x
      long long y = (*g).neighbors[x][IT];
      long long mod_y = (*clust).membP[y];
      do_it = (AlreadySeen.end() == AlreadySeen.find(mod_y));
      if(do_it){
        AlreadySeen.insert(mod_y);
        varying = GainJoining(g, clust, x, mod_y);
        std::tie (varyingTP, varyingFP, varyingFN) = varying;
        //
        newTP=TP+varyingTP; newFP=FP+varyingFP; newFN=FN+varyingFN;   
        xyz = PRF(newTP, newFP, newFN, Beta);
        std::tie (newPrec, newRec, newFSCORE) = xyz;
        // =================================================
        if (newFSCORE > FSCORE) {
          tuple_lld nid=std::make_tuple(x, mod_y, newFSCORE);
          vectXMF.push_back(nid);
        } 
        // =================================================
      } 
    } 
  }

  std::sort(vectXMF.begin(), vectXMF.end(), Dcomp_tuple_lld_ON_d);

  for (long long IT=0; IT<vectXMF.size(); ++IT) {
    long long x = std::get<0>(vectXMF[IT]);
    long long mod_y = std::get<1>(vectXMF[IT]);
    bool absent = ((*clustO).membO[mod_y].end() == (*clustO).membO[mod_y].find(x));
    if (absent) {
      tuple_ddd varying = GainOverlaps(g, clustO, x, mod_y);
      std::tie (varyingTP, varyingFP, varyingFN) = varying;
      //
      newTP=TP+varyingTP; newFP=FP+varyingFP; newFN=FN+varyingFN;   
      tuple_ddd xyz = PRF(newTP, newFP, newFN, Beta);
      std::tie (newPrec, newRec, newFSCORE) = xyz;
      // =================================================
      if (newFSCORE > FSCORE) {
        std::tie (xxxTP, xxxFP, xxxFN) = ModContribution(g, clustO, mod_y);
        tuple_ddd yyy = PRF(xxxTP, xxxFP, (TOT_FN_VIRGIN + xxxFN), Beta); 
        double yyyFSCORE=std::get<2>(yyy);
        //
        double xxxTPnew=xxxTP+varyingTP;
        double xxxFPnew=xxxFP+varyingFP;
        double xxxFNnew=xxxFN+varyingFN;
        tuple_ddd yyynew = PRF(xxxTPnew, xxxFPnew, (TOT_FN_VIRGIN + xxxFNnew), Beta);
        //double yyyPrecnew=std::get<0>(yyynew);
        //double yyyRecnew=std::get<1>(yyynew);
        double yyyFSCOREnew=std::get<2>(yyynew);
        //
        if (!(yyyFSCOREnew < yyyFSCORE)){
          FSCORE = newFSCORE; Prec = newPrec; Rec = newRec;
          TP = newTP; FP = newFP; FN = newFN;
          (*clustO).cO[mod_y].insert(x);
          (*clustO).membO[x].insert(mod_y);
        }
      }
    }
  }
  return std::make_tuple(TP, TN, FP, FN);
}



