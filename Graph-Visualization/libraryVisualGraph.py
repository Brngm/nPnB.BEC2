
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
            name=g["nodes"][i]["label"]; name=name.encode('UTF-8'); name=name.decode('UTF-8');
        else:
            name=""; name=name.encode('UTF-8'); name=name.decode('UTF-8');
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
def make3DHTML(g, member, score, title="GRAPH", label=False):
    """
        make3DHTML(g, c, pagetitle="GRAPH", title="GRAPH", subtitle="GROUPE", label=False)
        Builds the HTML page to 3D-display the clustered graph g by the clusterings builded with member
    """
    CH='<!DOCTYPE html>\n'
    CH=CH+'<html lang="fr">\n'
    CH=CH+'<head>\n'
    CH=CH+'  <meta charset="UTF-8">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+'  <title>%s 3D</title>\n'%(g["name"])
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'  <style>\n'
    CH=CH+'    body {\n'
    CH=CH+'      margin: 0;\n'
    CH=CH+'      padding: 20px;\n'
    CH=CH+'      font-family: Arial, sans-serif;\n'
    CH=CH+'      background-color: #f9f9f9;\n'
    CH=CH+'    }\n'
    CH=CH+'    .container {\n'
    CH=CH+'      max-width: 1200px;\n'
    CH=CH+'      margin: 0 auto;\n'
    CH=CH+'    }\n'
    CH=CH+'    h1 {\n'
    CH=CH+'      color: #333;\n'
    CH=CH+'    }\n'
    CH=CH+'    #3d-graph {\n'
    CH=CH+'      width: 100%;\n'
    CH=CH+'      height: 800px;\n'
    CH=CH+'      border: 1px solid #ccc;\n'
    CH=CH+'    }\n'
    CH=CH+'    #loading {\n'
    CH=CH+'      text-align: center;\n'
    CH=CH+'      font-style: italic;\n'
    CH=CH+'      color: #777;\n'
    CH=CH+'    }\n'
    CH=CH+'    #controls {\n'
    CH=CH+'      margin-bottom: 15px;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button {\n'
    CH=CH+'      padding: 8px 16px;\n'
    CH=CH+'      margin-right: 10px;\n'
    CH=CH+'      background-color: #757575;\n'
    CH=CH+'      border: none;\n'
    CH=CH+'      color: white;\n'
    CH=CH+'      border-radius: 6px;\n'
    CH=CH+'      cursor: pointer;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button:hover {\n'
    CH=CH+'      background-color: #4F4F4F;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button.active {\n'
    CH=CH+'      background-color: #050505;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* === SCORE DISPLAY avec animation === */\n'
    CH=CH+'    #score-display {\n'
    CH=CH+'      display: inline-block;\n'
    CH=CH+'      margin-top: 10px;\n'
    CH=CH+'      margin-left: 10px;\n'
    CH=CH+'      font-weight: bold;\n'
    CH=CH+'      font-size: 20px;          \n'
    CH=CH+'      color: #FFFFFF;\n'
    CH=CH+'      background-color: #050505;\n'
    CH=CH+'      padding: 5px 10px;        /* épaisseur autour du texte */\n'
    CH=CH+'      border-radius: 5px;\n'
    CH=CH+'      transition: transform 0.0s ease, #757575 0.0s ease;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* Animation lors de la mise à jour */\n'
    CH=CH+'    #score-display.updated {\n'
    CH=CH+'      transform: scale(1.0);\n'
    CH=CH+'      background-color: #757575;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* effet de lueur douce */\n'
    CH=CH+'    @keyframes glow {\n'
    CH=CH+'      0% { box-shadow: 0 0 0px #757575; }\n'
    CH=CH+'      50% { box-shadow: 0 0 20px #757575; }\n'
    CH=CH+'      100% { box-shadow: 0 0 0px #757575; }\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    #score-display.glow {\n'
    CH=CH+'      animation: glow 0.0s ease;\n'
    CH=CH+'    }\n'
    CH=CH+'  </style>\n'
    CH=CH+'</head>\n'
    CH=CH+'\n'
    CH=CH+'<body>\n'
    CH=CH+'  <div class="container">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+'    <h1>%s: |V|=%i, |E|=%i</h1>\n'%(g["name"],len(g["nodes"]), len(g["links"]))
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'\n'
    CH=CH+'    <div id="controls">\n'
    CH=CH+'      <span>Description scales :</span>\n'
    CH=CH+'      <div id="group-buttons" style="display:inline-block; margin-left:10px;"></div>\n'
    CH=CH+'      <span id="score-display"></span>\n'
    CH=CH+'    </div>\n'
    CH=CH+'\n'
    CH=CH+'    <div id="loading">Chargement du graphe...</div>\n'
    CH=CH+'    <div id="3d-graph"></div>\n'
    CH=CH+'  </div>\n'
    CH=CH+'\n'
    CH=CH+'  <!-- Librairie locale -->\n'
    CH=CH+'  <script src="../VascoAsturiano-libs/3d-force-graph.js"></script>\n'
    CH=CH+'\n'
    CH=CH+'  <!-- Données intégrées -->\n'
    CH=CH+'  <script type="application/json" id="graph-data">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+makeJsonGraphGroups(g, member,score, label)
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'  </script>\n'
    CH=CH+'\n'
    CH=CH+'  <script>\n'
    CH=CH+'    window.addEventListener("load", () => {\n'
    CH=CH+'      const rawData = document.getElementById("graph-data").textContent;\n'
    CH=CH+'      const data = JSON.parse(rawData);\n'
    CH=CH+'\n'
    CH=CH+'      const NODE_R = 8;\n'
    CH=CH+'      data.nodes.forEach(n => n.val = n.deg*NODE_R);\n'
    CH=CH+'\n'
    CH=CH+'      const Graph = ForceGraph3D()(document.getElementById("3d-graph"))\n'
    CH=CH+'        .graphData(data)\n'
    CH=CH+'        .nodeLabel(node => `${node.name}`)\n'
    CH=CH+'        .nodeAutoColorBy(node => node.group[0])\n'
    CH=CH+'        .nodeResolution(8)\n'
    CH=CH+'        .nodeRelSize(1)\n'
    CH=CH+'        .nodeOpacity(0.9)\n'
    CH=CH+'        .linkOpacity(0.8)\n'
    CH=CH+'        .linkWidth(0.8)\n'
    CH=CH+'        .backgroundColor("#ffffff")\n'
    CH=CH+'        .showNavInfo(true);\n'
    CH=CH+'\n'
    CH=CH+'      function hexToRgb(hex) {\n'
    CH=CH+'        const res = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);\n'
    CH=CH+'        return res ? [\n'
    CH=CH+'          parseInt(res[1], 16),\n'
    CH=CH+'          parseInt(res[2], 16),\n'
    CH=CH+'          parseInt(res[3], 16)\n'
    CH=CH+'        ] : [0, 0, 0];\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      function rgbToHex(r, g, b) {\n'
    CH=CH+'        const toHex = x => x.toString(16).padStart(2, "0");\n'
    CH=CH+'        return "#" + toHex(r) + toHex(g) + toHex(b);\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      function averageColor(c1, c2) {\n'
    CH=CH+'        const [r1, g1, b1] = hexToRgb(c1);\n'
    CH=CH+'        const [r2, g2, b2] = hexToRgb(c2);\n'
    CH=CH+'        const r = Math.round((r1 + r2) / 2);\n'
    CH=CH+'        const g = Math.round((g1 + g2) / 2);\n'
    CH=CH+'        const b = Math.round((b1 + b2) / 2);\n'
    CH=CH+'        return rgbToHex(r, g, b);\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      function updateLinkColors() {\n'
    CH=CH+'        data.links.forEach(link => {\n'
    CH=CH+'          const srcNode = typeof link.source === "object" ? link.source : data.nodes.find(n => n.id === link.source);\n'
    CH=CH+'          const tgtNode = typeof link.target === "object" ? link.target : data.nodes.find(n => n.id === link.target);\n'
    CH=CH+'          const c1 = srcNode.color || "#000000";\n'
    CH=CH+'          const c2 = tgtNode.color || "#000000";\n'
    CH=CH+'          link.color = averageColor(c1, c2);\n'
    CH=CH+'        });\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      setTimeout(() => {\n'
    CH=CH+'        updateLinkColors();\n'
    CH=CH+'        Graph.graphData(data);\n'
    CH=CH+'        document.getElementById("loading").style.display = "none";\n'
    CH=CH+'      }, 500);\n'
    CH=CH+'\n'
    CH=CH+'      // --- Création des boutons ---\n'
    CH=CH+'      const groupButtonsContainer = document.getElementById("group-buttons");\n'
    CH=CH+'      const scoreDisplay = document.getElementById("score-display");\n'
    CH=CH+'      const scales = data.scales || [];\n'
    CH=CH+'      const maxGroupLength = Math.max(...data.nodes.map(n => n.group.length));\n'
    CH=CH+'      const numButtons = Math.min(scales.length, maxGroupLength);\n'
    CH=CH+'      const initButtons = ~~(numButtons / 2);\n'
    CH=CH+'      Graph.nodeAutoColorBy(node => node.group[initButtons]);\n'
    CH=CH+'\n'
    CH=CH+'      function setScoreText(index) {\n'
    CH=CH+'        if (scales[index]) {\n'
    CH=CH+'          scoreDisplay.textContent = scales[index]["score"];\n'
    CH=CH+'\n'
    CH=CH+'          // --- Animation du score ---\n'
    CH=CH+'          scoreDisplay.classList.add("updated", "glow");\n'
    CH=CH+'          setTimeout(() => {\n'
    CH=CH+'            scoreDisplay.classList.remove("updated", "glow");\n'
    CH=CH+'          }, 600);\n'
    CH=CH+'        } else {\n'
    CH=CH+'          scoreDisplay.textContent = "";\n'
    CH=CH+'        }\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      for (let i = 0; i < numButtons; i++) {\n'
    CH=CH+'        const btn = document.createElement("button");\n'
    CH=CH+'        btn.textContent = scales[i]["s"];\n'
    CH=CH+'        btn.classList.add("group-button");\n'
    CH=CH+'        if (i === initButtons) {\n'
    CH=CH+'          btn.classList.add("active");\n'
    CH=CH+'          setScoreText(i);\n'
    CH=CH+'        }\n'
    CH=CH+'\n'
    CH=CH+'        btn.addEventListener("click", () => {\n'
    CH=CH+'          document.querySelectorAll(".group-button").forEach(b => b.classList.remove("active"));\n'
    CH=CH+'          btn.classList.add("active");\n'
    CH=CH+'\n'
    CH=CH+'          data.nodes.forEach(n => delete n.color);\n'
    CH=CH+'\n'
    CH=CH+'          Graph.nodeAutoColorBy(node => node.group[i]);\n'
    CH=CH+'          Graph.graphData(data);\n'
    CH=CH+'\n'
    CH=CH+'          setTimeout(() => {\n'
    CH=CH+'            updateLinkColors();\n'
    CH=CH+'            Graph.graphData(data);\n'
    CH=CH+'          }, 300);\n'
    CH=CH+'\n'
    CH=CH+'          setScoreText(i);\n'
    CH=CH+'        });\n'
    CH=CH+'\n'
    CH=CH+'        groupButtonsContainer.appendChild(btn);\n'
    CH=CH+'      }\n'
    CH=CH+'    });\n'
    CH=CH+'  </script>\n'
    CH=CH+'</body>\n'
    CH=CH+'</html>\n'
    return CH

# =============================================================================
def make2DHTML(g, member, score, title="GRAPH", label=False):
    """
        make2DHTML(g, c, pagetitle="GRAPH", title="GRAPH", subtitle="GROUPE", label=False)
        Builds the HTML page to 2D-display the clustered graph g by the clusterings builded with member
    """
    CH='<!DOCTYPE html>\n'
    CH=CH+'<html lang="fr">\n'
    CH=CH+'<head>\n'
    CH=CH+'  <meta charset="UTF-8">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+'  <title>%s 2D</title>\n'%(g["name"])
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'  <style>\n'
    CH=CH+'    body {\n'
    CH=CH+'      margin: 0;\n'
    CH=CH+'      padding: 20px;\n'
    CH=CH+'      font-family: Arial, sans-serif;\n'
    CH=CH+'      background-color: #f9f9f9;\n'
    CH=CH+'    }\n'
    CH=CH+'    .container {\n'
    CH=CH+'      max-width: 1200px;\n'
    CH=CH+'      margin: 0 auto;\n'
    CH=CH+'    }\n'
    CH=CH+'    h1 {\n'
    CH=CH+'      color: #333;\n'
    CH=CH+'    }\n'
    CH=CH+'    #2d-graph {\n'
    CH=CH+'      width: 100%;\n'
    CH=CH+'      height: 800px;\n'
    CH=CH+'      border: 1px solid #ccc;\n'
    CH=CH+'    }\n'
    CH=CH+'    #loading {\n'
    CH=CH+'      text-align: center;\n'
    CH=CH+'      font-style: italic;\n'
    CH=CH+'      color: #777;\n'
    CH=CH+'    }\n'
    CH=CH+'    #controls {\n'
    CH=CH+'      margin-bottom: 15px;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button {\n'
    CH=CH+'      padding: 8px 16px;\n'
    CH=CH+'      margin-right: 10px;\n'
    CH=CH+'      background-color: #757575;\n'
    CH=CH+'      border: none;\n'
    CH=CH+'      color: white;\n'
    CH=CH+'      border-radius: 6px;\n'
    CH=CH+'      cursor: pointer;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button:hover {\n'
    CH=CH+'      background-color: #4F4F4F;\n'
    CH=CH+'    }\n'
    CH=CH+'    .group-button.active {\n'
    CH=CH+'      background-color: #050505;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* === SCORE DISPLAY avec animation === */\n'
    CH=CH+'    #score-display {\n'
    CH=CH+'      display: inline-block;\n'
    CH=CH+'      margin-top: 10px;\n'
    CH=CH+'      margin-left: 10px;\n'
    CH=CH+'      font-weight: bold;\n'
    CH=CH+'      font-size: 20px;          \n'
    CH=CH+'      color: #FFFFFF;\n'
    CH=CH+'      background-color: #050505;\n'
    CH=CH+'      padding: 5px 10px;        /* épaisseur autour du texte */\n'
    CH=CH+'      border-radius: 5px;\n'
    CH=CH+'      transition: transform 0.0s ease, #757575 0.0s ease;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* Animation lors de la mise à jour */\n'
    CH=CH+'    #score-display.updated {\n'
    CH=CH+'      transform: scale(1.0);\n'
    CH=CH+'      background-color: #757575;\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    /* effet de lueur douce */\n'
    CH=CH+'    @keyframes glow {\n'
    CH=CH+'      0% { box-shadow: 0 0 0px #757575; }\n'
    CH=CH+'      50% { box-shadow: 0 0 20px #757575; }\n'
    CH=CH+'      100% { box-shadow: 0 0 0px #757575; }\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    #score-display.glow {\n'
    CH=CH+'      animation: glow 0.0s ease;\n'
    CH=CH+'    }\n'
    CH=CH+'  </style>\n'
    CH=CH+'</head>\n'
    CH=CH+'\n'
    CH=CH+'<body>\n'
    CH=CH+'  <div class="container">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+'    <h1>%s: |V|=%i, |E|=%i</h1>\n'%(g["name"],len(g["nodes"]), len(g["links"]))
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'\n'
    CH=CH+'    <div id="controls">\n'
    CH=CH+'      <span>Description scales :</span>\n'
    CH=CH+'      <div id="group-buttons" style="display:inline-block; margin-left:10px;"></div>\n'
    CH=CH+'      <span id="score-display"></span>\n'
    CH=CH+'    </div>\n'
    CH=CH+'\n'
    CH=CH+'    <div id="loading">Chargement du graphe...</div>\n'
    CH=CH+'    <div id="2d-graph"></div>\n'
    CH=CH+'  </div>\n'
    CH=CH+'\n'
    CH=CH+'  <!-- Librairie locale -->\n'
    CH=CH+'  <script src="../VascoAsturiano-libs/2d-force-graph.min.js"></script>\n'
    CH=CH+'\n'
    CH=CH+'  <!-- Données intégrées -->\n'
    CH=CH+'  <script type="application/json" id="graph-data">\n'

    # --------------------------------------------------------------------------------------------------------------
    CH=CH+makeJsonGraphGroups(g, member,score, label)
    # --------------------------------------------------------------------------------------------------------------

    CH=CH+'  </script>\n'
    CH=CH+'\n'
    CH=CH+'  <script>\n'
    CH=CH+'    window.addEventListener("load", () => {\n'
    CH=CH+'      const rawData = document.getElementById("graph-data").textContent;\n'
    CH=CH+'      const data = JSON.parse(rawData);\n'
    CH=CH+'\n'
    CH=CH+'      const NODE_R = 8;\n'
    CH=CH+'      data.nodes.forEach(n => n.val = n.deg*NODE_R);\n'
    CH=CH+'\n'

    CH=CH+'      const Graph = ForceGraph()(document.getElementById("2d-graph"))\n'
    CH=CH+'        .graphData(data)\n'
    CH=CH+'        .nodeAutoColorBy(node => node.group[0])\n'
    CH=CH+'        .nodeRelSize(1)\n'
    CH=CH+'        .backgroundColor("#fff")\n'
    CH=CH+'        .linkWidth(0.5)\n'
    CH=CH+'        .enableNodeDrag(true)\n'
    CH=CH+'        .nodeCanvasObject((node, ctx, globalScale) => {\n'
    CH=CH+'          const label = node.name;\n'
    CH=CH+'          const fontSize = 12 / globalScale;\n'
    CH=CH+'          ctx.fillStyle = node.color;\n'
    CH=CH+'          ctx.beginPath();\n'
    CH=CH+'          ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);\n'
    CH=CH+'          ctx.fill();\n'
    CH=CH+'\n'
    CH=CH+'          ctx.font = `${fontSize}px Sans-Serif`;\n'
    CH=CH+'          ctx.textAlign = "left";\n'
    CH=CH+'          ctx.textBaseline = "top";\n'
    CH=CH+'          ctx.fillStyle = "black";\n'
    CH=CH+'          ctx.fillText(label, node.x, node.y + 6);\n'
    CH=CH+'        })\n'
    CH=CH+'        .nodePointerAreaPaint((node, color, ctx) => {\n'
    CH=CH+'          ctx.fillStyle = color;\n'
    CH=CH+'          ctx.beginPath();\n'
    CH=CH+'          ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI, false);\n'
    CH=CH+'          ctx.fill();\n'
    CH=CH+'        })\n'
    CH=CH+'        function hexToRgb(hex) {\n'
    CH=CH+'      const res = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);\n'
    CH=CH+'      return res ? [\n'
    CH=CH+'        parseInt(res[1], 16),\n'
    CH=CH+'        parseInt(res[2], 16),\n'
    CH=CH+'        parseInt(res[3], 16)\n'
    CH=CH+'      ] : [0, 0, 0];\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    function rgbToHex(r, g, b) {\n'
    CH=CH+'      const toHex = x => x.toString(16).padStart(2, "0");\n'
    CH=CH+'      return "#" + toHex(r) + toHex(g) + toHex(b);\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    function averageColor(c1, c2) {\n'
    CH=CH+'      const [r1, g1, b1] = hexToRgb(c1);\n'
    CH=CH+'      const [r2, g2, b2] = hexToRgb(c2);\n'
    CH=CH+'      const r = Math.round((r1 + r2) / 2);\n'
    CH=CH+'      const g = Math.round((g1 + g2) / 2);\n'
    CH=CH+'      const b = Math.round((b1 + b2) / 2);\n'
    CH=CH+'      return rgbToHex(r, g, b);\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'    function updateLinkColors() {\n'
    CH=CH+'      data.links.forEach(link => {\n'
    CH=CH+'        const srcNode = typeof link.source === "object" ? link.source : data.nodes.find(n => n.id === link.source);\n'
    CH=CH+'        const tgtNode = typeof link.target === "object" ? link.target : data.nodes.find(n => n.id === link.target);\n'
    CH=CH+'        const c1 = srcNode.color || "#000000";\n'
    CH=CH+'        const c2 = tgtNode.color || "#000000";\n'
    CH=CH+'        link.color = averageColor(c1, c2);\n'
    CH=CH+'      });\n'
    CH=CH+'    }\n'
    CH=CH+'\n'
    CH=CH+'      setTimeout(() => {\n'
    CH=CH+'        updateLinkColors();\n'
    CH=CH+'        Graph.graphData(data);\n'
    CH=CH+'        document.getElementById("loading").style.display = "none";\n'
    CH=CH+'      }, 500);\n'
    CH=CH+'\n'
    CH=CH+'      // --- Création des boutons ---\n'
    CH=CH+'      const groupButtonsContainer = document.getElementById("group-buttons");\n'
    CH=CH+'      const scoreDisplay = document.getElementById("score-display");\n'
    CH=CH+'      const scales = data.scales || [];\n'
    CH=CH+'      const maxGroupLength = Math.max(...data.nodes.map(n => n.group.length));\n'
    CH=CH+'      const numButtons = Math.min(scales.length, maxGroupLength);\n'
    CH=CH+'      const initButtons = ~~(numButtons / 2);\n'
    CH=CH+'      Graph.nodeAutoColorBy(node => node.group[initButtons]);\n'
    CH=CH+'\n'
    CH=CH+'      function setScoreText(index) {\n'
    CH=CH+'        if (scales[index]) {\n'
    CH=CH+'          scoreDisplay.textContent = scales[index]["score"];\n'
    CH=CH+'\n'
    CH=CH+'          // --- Animation du score ---\n'
    CH=CH+'          scoreDisplay.classList.add("updated", "glow");\n'
    CH=CH+'          setTimeout(() => {\n'
    CH=CH+'            scoreDisplay.classList.remove("updated", "glow");\n'
    CH=CH+'          }, 600);\n'
    CH=CH+'        } else {\n'
    CH=CH+'          scoreDisplay.textContent = "";\n'
    CH=CH+'        }\n'
    CH=CH+'      }\n'
    CH=CH+'\n'
    CH=CH+'      for (let i = 0; i < numButtons; i++) {\n'
    CH=CH+'        const btn = document.createElement("button");\n'
    CH=CH+'        btn.textContent = scales[i]["s"];\n'
    CH=CH+'        btn.classList.add("group-button");\n'
    CH=CH+'        if (i === initButtons) {\n'
    CH=CH+'          btn.classList.add("active");\n'
    CH=CH+'          setScoreText(i);\n'
    CH=CH+'        }\n'
    CH=CH+'\n'
    CH=CH+'        btn.addEventListener("click", () => {\n'
    CH=CH+'          document.querySelectorAll(".group-button").forEach(b => b.classList.remove("active"));\n'
    CH=CH+'          btn.classList.add("active");\n'
    CH=CH+'\n'
    CH=CH+'          data.nodes.forEach(n => delete n.color);\n'
    CH=CH+'\n'
    CH=CH+'          Graph.nodeAutoColorBy(node => node.group[i]);\n'
    CH=CH+'          Graph.graphData(data);\n'
    CH=CH+'\n'
    CH=CH+'          setTimeout(() => {\n'
    CH=CH+'            updateLinkColors();\n'
    CH=CH+'            Graph.graphData(data);\n'
    CH=CH+'          }, 300);\n'
    CH=CH+'\n'
    CH=CH+'          setScoreText(i);\n'
    CH=CH+'        });\n'
    CH=CH+'\n'
    CH=CH+'        groupButtonsContainer.appendChild(btn);\n'
    CH=CH+'      }\n'
    CH=CH+'    });\n'
    CH=CH+'  </script>\n'
    CH=CH+'</body>\n'
    CH=CH+'</html>\n'
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

    # json format
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

