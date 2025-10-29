
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Library for managing graph visualization by assigning vertex colorings
    according to a clustering constructed with nPnB
    according to a description scale (module granularity).
"""
import codecs
import math
import random as rd
import builtins
import json

# =============================================================================
#import igraph as ig
# If you don't need to use graphs in igraph format you can comment out this line,
# and remove the two functions: json2ig et ig2json
# =============================================================================

# =============================================================================
def PrintClust(c):
    """
        PrintClust(g,c)
        Prints the clustering c on the graph g
    """
    nbv = len(set([i for m in c for i in m]))
    c.sort(key = lambda z : len(z), reverse=True)
    for m in c:
        m.sort(reverse=False)
        
    member=[[] for _ in range(nbv)]
    for i in range(len(c)):
        m=c[i]
        for j in range(len(m)):
            x = m[j]
            member[x].append(i)

    # modules
    CH="Modules:\n"
    for i in range(len(c)):
        m=c[i]
        CH=CH+"  %i (|m.%i|=%i): {"%(i, i, len(m))
        for j in range(len(m)):
            x = m[j]
            CH=CH+str(x)
            if j<len(m)-1:
                CH=CH+", "
        CH=CH+"}"
        if i<len(c)-1:
            CH=CH+"\n"
    print(CH)

    # nodes in overlaps
    CH=""
    for i in range(nbv):
        x=member[i]
        if len(x) > 1:
            CH=CH+"  node %i in: "%(i)
            for j in range(len(x)):
                CH=CH+"m.%i"%(x[j])
                if j<len(x)-1:
                    CH=CH+", "
            if i<nbv-1:
                CH=CH+"\n"
    if not (CH == ""):
        CH="Nodes in overlaps:\n"+CH
        print(CH)
    print("")

# =============================================================================
def add_degrees(g):
    """
    add_degrees(g)
    adds the 'deg' field to the json
    """
    nbv=len(g["nodes"]); nbe=len(g["links"])
    deg=[0 for _ in range(nbv)]
    for i in range(nbe):
        deg[g["links"][i]["source"]]=deg[g["links"][i]["source"]]+g["links"][i]["weight"]
        deg[g["links"][i]["target"]]=deg[g["links"][i]["target"]]+g["links"][i]["weight"]
    for i in range(nbv):
        g["nodes"][i]["deg"]=deg[g["nodes"][i]["id"]]

# =============================================================================
def makeJsonGraphGroups(g, member,score, label=False):
    """
        makeJsonGraphGroups(g, member,score, label=False)
        Builds the JSON file of the clustered graph g by the clusterings builded with member
    """
    nbv=len(g["nodes"]); nbe=len(g["links"]); nbscore=len(score)
    # ======================= 
    # scales
    CH='        {\n         "scales": [\n'
    for i in range(nbscore):
        lastc=("," if i<(nbscore-1) else "")
        CH=CH+'            {"s":%s, "score": %s}%s\n'%(str(score[i][0]), score[i][1],lastc)
    
    # nodes =================
    CH=CH+'        ],\n          "nodes": [\n'
    for i in range(nbv):
        lastc=("," if i<(nbv-1) else "")
        if label:
            name=g["nodes"][i]["label"]; name=name.encode('UTF-8'); name=name.decode('UTF-8')
        else:
            name=""; name=name.encode('UTF-8'); name=name.decode('UTF-8')
        CH=CH+'            {"id": %i, "name": "%s", "deg": %s, "group": %s}%s\n'%(g["nodes"][i]["id"], name, g["nodes"][i]["deg"], member[i],lastc)

    # links =================
    CH=CH+'        ],\n         "links": [\n'
    for i in range(nbe):
        lastc=("," if i<(nbe-1) else "")
        CH=CH+'            {"source": %i, "target": %i, "value": %.2f}%s\n'%(g["links"][i]["source"],
                                                                            g["links"][i]["target"],g["links"][i]["weight"],lastc)
    CH=CH+'          ]\n        }\n'
    return CH

# =============================================================================
def makeHTML(g, member, score, V2D3D="3D", title="GRAPH", label=False):
    """
        makeHTML(g, member, score, V2D3D="3D", title="GRAPH", label=False)
        Builds the HTML page to 2D-3D-display the clustered graph g by the clusterings builded with member
    """
    if V2D3D=="2D":
        return make2DHTML(g, member, score, title, label)
    else:
        return make3DHTML(g, member, score, title, label)

# =============================================================================
def make2DHTML(graph, member, score, title="GRAPH", label=False):
    """
        make2DHTML(graph, c, pagetitle="GRAPH", title="GRAPH", subtitle="GROUPE", label=False)
        Builds the HTML page to 2D-display the clustered graph graph by the clusterings builded with member
    """
    nl="\n"
    
    CH="""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        """+nl
    
    CH=CH+"      <title>%s 2D</title>"%(graph["name"])+nl

    CH=CH+"""
            <style>
            body {
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                color: #333;
            }
            #2d-graph {
                width: 100%;
                height: 800px;
                border: 1px solid #ccc;
            }
            #loading {
                text-align: center;
                font-style: italic;
                color: #777;
            }
            #controls {
                margin-bottom: 15px;
            }
            .group-button {
                padding: 8px 16px;
                margin-right: 10px;
                background-color: #757575;
                border: none;
                color: white;
                border-radius: 6px;
                cursor: pointer;
            }
            .group-button:hover {
                background-color: #4F4F4F;
            }
            .group-button.active {
                background-color: #050505;
            }
        
            /* === SCORE DISPLAY avec animation === */
            #score-display {
                display: inline-block;
                margin-top: 10px;
                margin-left: 10px;
                font-weight: bold;
                font-size: 20px;          
                color: #FFFFFF;
                background-color: #050505;
                padding: 5px 10px;        /* épaisseur autour du texte */
                border-radius: 5px;
                transition: transform 0.0s ease, #757575 0.0s ease;
            }
        
            /* Animation lors de la mise à jour */
            #score-display.updated {
                transform: scale(1.0);
                background-color: #757575;
            }
        
            /* effet de lueur douce */
            @keyframes glow {
                0% { box-shadow: 0 0 0px #757575; }
                50% { box-shadow: 0 0 20px #757575; }
                100% { box-shadow: 0 0 0px #757575; }
            }
        
            #score-display.glow {
                animation: glow 0.0s ease;
            }
            </style>
        </head>
        
        <body>
            <div class="container">
                """+nl
    
    CH=CH+"      <h1>%s: |V|=%i, |E|=%i</h1>"%(graph["name"],len(graph["nodes"]), len(graph["links"]))+nl

    CH=CH+"""
        <div id="controls">
            <span>Description scales :</span>
            <div id="group-buttons" style="display:inline-block; margin-left:10px;"></div>
            <span id="score-display"></span>
        </div>
    
        <div id="loading">Chargement du graphe...</div>
        <div id="2d-graph"></div>
        </div>
    
        <!-- Librairie locale -->
        <script src="../VascoAsturiano-libs/2d-force-graph.min.js"></script>
    
        <!-- Données intégrées -->
        <script type="application/json" id="graph-data">
            """+nl

    CH=CH+"           "+makeJsonGraphGroups(graph, member,score, label)+nl

    CH=CH+"""
        </script>
    
        <script>
        window.addEventListener("load", () => {
            const rawData = document.getElementById("graph-data").textContent;
            const data = JSON.parse(rawData);
    
            const NODE_R = 8;
            data.nodes.forEach(n => n.val = n.deg*NODE_R);
    
            const Graph = ForceGraph()(document.getElementById("2d-graph"))
            .graphData(data)
            .nodeAutoColorBy(node => node.group[0])
            .nodeRelSize(1)
            .backgroundColor("#fff")
            .linkWidth(0.5)
            .enableNodeDrag(true)
            .nodeCanvasObject((node, ctx, globalScale) => {
                const label = node.name;
                const fontSize = 12 / globalScale;
                ctx.fillStyle = node.color;
                ctx.beginPath();
                ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
                ctx.fill();
    
                ctx.font = `${fontSize}px Sans-Serif`;
                ctx.textAlign = "left";
                ctx.textBaseline = "top";
                ctx.fillStyle = "black";
                ctx.fillText(label, node.x, node.y + 6);
            })
            .nodePointerAreaPaint((node, color, ctx) => {
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI, false);
                ctx.fill();
            })
            function hexToRgb(hex) {
            const res = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return res ? [
            parseInt(res[1], 16),
            parseInt(res[2], 16),
            parseInt(res[3], 16)
            ] : [0, 0, 0];
        }
    
        function rgbToHex(r, g, b) {
            const toHex = x => x.toString(16).padStart(2, "0");
            return "#" + toHex(r) + toHex(g) + toHex(b);
        }
    
        function averageColor(c1, c2) {
            const [r1, g1, b1] = hexToRgb(c1);
            const [r2, g2, b2] = hexToRgb(c2);
            const r = Math.round((r1 + r2) / 2);
            const g = Math.round((g1 + g2) / 2);
            const b = Math.round((b1 + b2) / 2);
            return rgbToHex(r, g, b);
        }
    
        function updateLinkColors() {
            data.links.forEach(link => {
            const srcNode = typeof link.source === "object" ? link.source : data.nodes.find(n => n.id === link.source);
            const tgtNode = typeof link.target === "object" ? link.target : data.nodes.find(n => n.id === link.target);
            const c1 = srcNode.color || "#000000";
            const c2 = tgtNode.color || "#000000";
            link.color = averageColor(c1, c2);
            });
        }
    
            setTimeout(() => {
            updateLinkColors();
            Graph.graphData(data);
            document.getElementById("loading").style.display = "none";
            }, 500);
    
            // --- Création des boutons ---
            const groupButtonsContainer = document.getElementById("group-buttons");
            const scoreDisplay = document.getElementById("score-display");
            const scales = data.scales || [];
            const maxGroupLength = Math.max(...data.nodes.map(n => n.group.length));
            const numButtons = Math.min(scales.length, maxGroupLength);
            const initButtons = ~~(numButtons / 2);
            Graph.nodeAutoColorBy(node => node.group[initButtons]);
    
            function setScoreText(index) {
            if (scales[index]) {
                scoreDisplay.textContent = scales[index]["score"];
    
                // --- Animation du score ---
                scoreDisplay.classList.add("updated", "glow");
                setTimeout(() => {
                scoreDisplay.classList.remove("updated", "glow");
                }, 600);
            } else {
                scoreDisplay.textContent = "";
            }
            }
    
            for (let i = 0; i < numButtons; i++) {
            const btn = document.createElement("button");
            btn.textContent = scales[i]["s"];
            btn.classList.add("group-button");
            if (i === initButtons) {
                btn.classList.add("active");
                setScoreText(i);
            }
    
            btn.addEventListener("click", () => {
                document.querySelectorAll(".group-button").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
    
                data.nodes.forEach(n => delete n.color);
    
                Graph.nodeAutoColorBy(node => node.group[i]);
                Graph.graphData(data);
    
                setTimeout(() => {
                updateLinkColors();
                Graph.graphData(data);
                }, 300);
    
                setScoreText(i);
            });
    
            groupButtonsContainer.appendChild(btn);
            }
        });
        </script>
    </body>
    </html>
            """+nl
    return CH

# =============================================================================
def make3DHTML(graph, member, score, title="GRAPH", label=False):
    """
        make3DHTML(graph, c, pagetitle="GRAPH", title="GRAPH", subtitle="GROUPE", label=False)
        Builds the HTML page to 3D-display the clustered graph graph by the clusterings builded with member
    """
    nl="\n"
    
    CH="""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
        """+nl
    
    CH=CH+"      <title>%s 3D</title>"%(graph["name"])+nl

    CH=CH+"""
          <style>
            body {
          margin: 0;
          padding: 20px;
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
        }
        .container {
          max-width: 1200px;
          margin: 0 auto;
        }
        h1 {
          color: #333;
        }
        #3d-graph {
          width: 100%;
          height: 800px;
          border: 1px solid #ccc;
        }
        #loading {
          text-align: center;
          font-style: italic;
          color: #777;
        }
        #controls {
          margin-bottom: 15px;
        }
        .group-button {
          padding: 8px 16px;
          margin-right: 10px;
          background-color: #757575;
          border: none;
          color: white;
          border-radius: 6px;
          cursor: pointer;
        }
        .group-button:hover {
          background-color: #4F4F4F;
        }
        .group-button.active {
          background-color: #050505;
        }
    
        /* === SCORE DISPLAY avec animation === */
        #score-display {
          display: inline-block;
          margin-top: 10px;
          margin-left: 10px;
          font-weight: bold;
          font-size: 20px;          
          color: #FFFFFF;
          background-color: #050505;
          padding: 5px 10px;        /* épaisseur autour du texte */
          border-radius: 5px;
          transition: transform 0.0s ease, #757575 0.0s ease;
        }
    
        /* Animation lors de la mise à jour */
        #score-display.updated {
          transform: scale(1.0);
          background-color: #757575;
        }
    
        /* effet de lueur douce */
        @keyframes glow {
          0% { box-shadow: 0 0 0px #757575; }
          50% { box-shadow: 0 0 20px #757575; }
          100% { box-shadow: 0 0 0px #757575; }
        }
    
        #score-display.glow {
          animation: glow 0.0s ease;
        }
      </style>
    </head>
    
    <body>
      <div class="container">
        """+nl
    
    CH=CH+"      <h1>%s: |V|=%i, |E|=%i</h1>"%(graph["name"],len(graph["nodes"]), len(graph["links"]))+nl

    CH=CH+"""
        <div id="controls">
          <span>Description scales :</span>
          <div id="group-buttons" style="display:inline-block; margin-left:10px;"></div>
          <span id="score-display"></span>
        </div>
    
        <div id="loading">Chargement du graphe...</div>
        <div id="3d-graph"></div>
      </div>
    
      <!-- Librairie locale -->
      <script src="../VascoAsturiano-libs/3d-force-graph.js"></script>
    
      <!-- Données intégrées -->
      <script type="application/json" id="graph-data">
        """+nl

    CH=CH+"           "+makeJsonGraphGroups(graph, member,score, label)+nl

    CH=CH+"""
      </script>
    
      <script>
        window.addEventListener("load", () => {
          const rawData = document.getElementById("graph-data").textContent;
          const data = JSON.parse(rawData);
    
          const NODE_R = 8;
          data.nodes.forEach(n => n.val = n.deg*NODE_R);
    
          const Graph = ForceGraph3D()(document.getElementById("3d-graph"))
            .graphData(data)
            .nodeLabel(node => `${node.name}`)
            .nodeAutoColorBy(node => node.group[0])
            .nodeResolution(8)
            .nodeRelSize(1)
            .nodeOpacity(0.9)
            .linkOpacity(0.8)
            .linkWidth(0.8)
            .backgroundColor("#ffffff")
            .showNavInfo(true);
    
          function hexToRgb(hex) {
            const res = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return res ? [
              parseInt(res[1], 16),
              parseInt(res[2], 16),
              parseInt(res[3], 16)
            ] : [0, 0, 0];
          }
    
          function rgbToHex(r, g, b) {
            const toHex = x => x.toString(16).padStart(2, "0");
            return "#" + toHex(r) + toHex(g) + toHex(b);
          }
    
          function averageColor(c1, c2) {
            const [r1, g1, b1] = hexToRgb(c1);
            const [r2, g2, b2] = hexToRgb(c2);
            const r = Math.round((r1 + r2) / 2);
            const g = Math.round((g1 + g2) / 2);
            const b = Math.round((b1 + b2) / 2);
            return rgbToHex(r, g, b);
          }
    
          function updateLinkColors() {
            data.links.forEach(link => {
              const srcNode = typeof link.source === "object" ? link.source : data.nodes.find(n => n.id === link.source);
              const tgtNode = typeof link.target === "object" ? link.target : data.nodes.find(n => n.id === link.target);
              const c1 = srcNode.color || "#000000";
              const c2 = tgtNode.color || "#000000";
              link.color = averageColor(c1, c2);
            });
          }
    
          setTimeout(() => {
            updateLinkColors();
            Graph.graphData(data);
            document.getElementById("loading").style.display = "none";
          }, 500);
    
          // --- Création des boutons ---
          const groupButtonsContainer = document.getElementById("group-buttons");
          const scoreDisplay = document.getElementById("score-display");
          const scales = data.scales || [];
          const maxGroupLength = Math.max(...data.nodes.map(n => n.group.length));
          const numButtons = Math.min(scales.length, maxGroupLength);
          const initButtons = ~~(numButtons / 2);
          Graph.nodeAutoColorBy(node => node.group[initButtons]);
    
          function setScoreText(index) {
            if (scales[index]) {
              scoreDisplay.textContent = scales[index]["score"];
    
              // --- Animation du score ---
              scoreDisplay.classList.add("updated", "glow");
              setTimeout(() => {
                scoreDisplay.classList.remove("updated", "glow");
              }, 600);
            } else {
              scoreDisplay.textContent = "";
            }
          }
    
          for (let i = 0; i < numButtons; i++) {
            const btn = document.createElement("button");
            btn.textContent = scales[i]["s"];
            btn.classList.add("group-button");
            if (i === initButtons) {
              btn.classList.add("active");
              setScoreText(i);
            }
    
            btn.addEventListener("click", () => {
              document.querySelectorAll(".group-button").forEach(b => b.classList.remove("active"));
              btn.classList.add("active");
    
              data.nodes.forEach(n => delete n.color);
    
              Graph.nodeAutoColorBy(node => node.group[i]);
              Graph.graphData(data);
    
              setTimeout(() => {
                updateLinkColors();
                Graph.graphData(data);
              }, 300);
    
              setScoreText(i);
            });
    
            groupButtonsContainer.appendChild(btn);
          }
        });
      </script>
    </body>
    </html>
        """+nl
    return CH

# =============================================================================
def saveChemCH(chem, CH):
    """
        saveChemCH(chem, CH)
        Save the string CH at chem
    """
    f=codecs.open(chem, "w",  encoding='utf8')
    f.write(CH)
    f.close()

# =============================================================================
def write_json_compact_readable(
        data,
        filename="",
        indent=2,
        max_line_length=100,
        sort_keys=False,
        return_str=False
    ):
    """
        def write_json_compact_readable(
            data,
            filename="",
            indent=2,
            max_line_length=100,
            sort_keys=False,
            return_str=False
        )
        Writes readable, compact, robust, and configurable JSON.
        - Supports all JSON depths.
        - Sort_keys option to sort keys.
        - Return_str option to return JSON as a string.
        - Resists overriding list or dict.
    """

    list_type = builtins.list
    dict_type = builtins.dict

    def format_value(value, level):
        space = ' ' * (indent * level)

        # --- dictionary ---
        if isinstance(value, dict_type):
            items = value.items()
            if sort_keys:
                items = sorted(items)
            items = [f'"{k}": {format_value(v, level+1)}' for k, v in items]
            inline = '{' + ', '.join(items) + '}'
            if len(space) + len(inline) > max_line_length:
                multiline = ',\n'.join(
                    ' ' * (indent*(level+1)) + f'"{k}": {format_value(v, level+1)}'
                    for k, v in (sorted(value.items()) if sort_keys else value.items())
                )
                return '{\n' + multiline + f'\n{space}' + '}'
            return inline

        # --- list ---
        elif isinstance(value, list_type):
            if all(isinstance(el, dict_type) for el in value):
                items = [json.dumps(el, separators=(", ", ": ")) for el in value]
                inline = '[ ' + ', '.join(items) + ' ]'
                if len(space) + len(inline) > max_line_length:
                    return '[\n' + ',\n'.join(
                        ' ' * (indent*(level+1)) + json.dumps(el, separators=(", ", ": "))
                        for el in value
                    ) + f'\n{space}]'
                else:
                    return inline
            else:
                items = [format_value(el, level+1) for el in value]
                inline = '[ ' + ', '.join(items) + ' ]'
                if len(space) + len(inline) > max_line_length:
                    return '[\n' + ',\n'.join(
                        ' ' * (indent*(level+1)) + format_value(el, level+1)
                        for el in value
                    ) + f'\n{space}]'
                else:
                    return inline

        # --- simple values ​​---
        else:
            return json.dumps(value, separators=(", ", ": "))

    formatted_json = format_value(data, 0)

    # Returns the string if requested
    if return_str:
        return formatted_json

    # Write to a file if filename specified
    if filename:
        with open(filename, "w") as f:
            f.write(formatted_json + '\n')
            
# =============================================================================
def build_fractalGraph(depth=3, n=20, k=5, p_intra=0.5, p_inter=0.02):
    """
        build_fractalGraph(depth=3, n=20, k=3, p_intra=0.5, p_inter=0.02)
        Constructs a fractal graph
    """
    def OKedge(depth, r, i, j, n, k, mbase):
        OK = False
        for x in range(2,depth+1):
            nbsici = n * (k**(x))
            mici = (n * (k**(x))**2)
            pici = mbase / mici
            if (i//nbsici) == (j//nbsici): # i and j are in the same SuperCluster of level x
                if r <= pici:
                    OK=True; break;
        return OK
    
    nbs = n * (k**depth)
    mbase = n*n*p_inter
    edges=[]
    for i in range(nbs) :
        for j in range(i+1, nbs) :
            r=rd.random()
            if (i//n) == (j//n) : # i and j are in the same SubCluster
                if r <= p_intra :
                   edges.append((i,j))
            elif (i//(n*k)) == (j//(n*k)) : # i and j are in the same Cluster
                if r <= p_inter :
                   edges.append((i,j))
            elif  OKedge(depth, r, i, j, n, k, mbase):
                edges.append((i,j))

    ##igraph format
    #import igraph as ig
    #g=ig.Graph(n=nbs,
    #    edges=edges,
    #    directed=False)
    # return g

    ## json format
    graph={ 
        "information": ["fractalGraph(depth=%i, n=%i, k=%i, p_intra=%s, p_inter=%s)"%(depth,n,k,p_intra,p_inter)],
        "name": "FractalGraph-depth=%i-n=%i-k=%i-pa=%s-pi=%s"%(depth,n,k,p_intra,p_inter),
        "directed": "false",
        "nodes": [],
        "links": []}

    for i in range(nbs) :
        graph["nodes"].append({"id": i, "label": str(i)})

    for i in range(len(edges)):
        graph["links"].append({"source": edges[i][0], "target": edges[i][1], "weight": 1})

    add_degrees(graph)
   
    return graph

# uses import igraph as ig ==================================================== 
def ig2json(g, name=None, inforamtion=None, weight=None, label=None):
    """
        ig2json(g, name=None, inforamtion=None, weight=None, label=None)
        igraph format --> json format
        need import igraph as ig
    """
    import igraph as ig
    gjson={"information":[],
            "name":"miserables",
            "directed":g.is_directed(),
            "nodes":[],
            "links":[]
           }
    if (name==None):
        gjson["name"]="anonymous"
    else:
        gjson["name"]=name

    if (inforamtion==None):
        gjson["information"]=[]
    else:
        gjson["information"]=inforamtion

    for i in range(g.vcount()):
        if label==None:
            x={"id":i, "label": "%i"%(i)}
        else:
            x={"id":i, "label": g.vs[i][label]}
        gjson["nodes"].append(x)
        
    for i in range(g.ecount()):
        if weight==None:
            x={"source": g.es[i].source, "target": g.es[i].target, "weight": 1}
        else:
            x={"source": g.es[i].source, "target": g.es[i].target, "weight": g.es[i][weight]}
            
        gjson["links"].append(x)
        
    return gjson

# uses import igraph as ig ====================================================
def json2ig(gjson): 
    """
        json2ig(gjson)
        json format-->igraph format
        need import igraph as ig
    """
    import igraph as ig
    g=ig.Graph( n=len(gjson["nodes"]),
                edges=[(x["source"], x["target"]) for x in gjson["links"]],
                directed=gjson["directed"])
    
    for x in gjson["nodes"]:
        for k in x:
            if (not k=="id"):
                g.vs[x["id"]][k]=x[k]
                
    ide=0
    for x in gjson["links"]:
        for k in x:
            if (not k in ["source", "target"]):
                g.es[ide][k]=x[k]
        ide=ide+1 

    g["name"]=gjson["name"]
    g["information"]=gjson["information"]
    return g

