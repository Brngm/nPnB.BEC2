
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
import os
import sys
import time
from matplotlib import pyplot as plt

sys.path.append("nPnB/")
import nPnBinterface as nPnB

# =============================================================================
def generate_contrasting_colors(INPUT={}): 
    """
    TODO
    """
    if INPUT:
        n=INPUT["n"]; L1=INPUT["L1"]; L2==INPUT["L2"]; resolution=INPUT["resolution"]; seed=INPUT["seed"]
        if seed is not None:
            np.random.seed(seed)

        # Espace RGB discret
        space = np.linspace(0, 255, resolution)
        candidates = np.array(np.meshgrid(space, space, space)).T.reshape(-1, 3)

        # Filtrage par luminosité
        lumin = candidates.sum(axis=1)
        mask = (lumin > L1) & (lumin < L2)
        candidates = candidates[mask]

        if len(candidates) == 0:
            raise ValueError("Aucune couleur ne correspond aux contraintes de luminosité données.")

        # Choix initial aléatoire
        colors = [candidates[np.random.randint(len(candidates))]]

        for _ in range(1, n):
            # Calcul de la distance minimale de chaque candidat aux couleurs choisies
            dists = np.min(
                np.linalg.norm(candidates[:, None, :] - np.array(colors)[None, :, :], axis=2),
                axis=1
            )
            # Choisir la couleur la plus éloignée
            next_color = candidates[np.argmax(dists)]
            colors.append(next_color)

        # Conversion en tuples d'entiers
        L=[list(map(int, c)) for c in colors]
    else:
      if False:
          L=[
              [0, 255, 49], [0, 49, 255], [255, 0, 49], [205, 0, 255], [16, 255, 255], [255, 255, 0], [8, 148, 148], [123, 115, 246], [131, 255, 90], [255, 82, 156], [131, 24, 148], [246, 123, 0], [131, 255, 255], [222, 189, 82], [238, 123, 255], [90, 213, 0], [98, 0, 246], [41, 255, 148], [115, 172, 156], [24, 148, 255], [57, 74, 180], [205, 82, 74], [180, 197, 0], [57, 189, 82], [222, 0, 139], [172, 106, 172], [255, 255, 131], [148, 255, 172], [74, 205, 222], [172, 180, 255], [156, 49, 222], [74, 115, 115], [0, 205, 197], [197, 255, 49], [255, 156, 148], [255, 49, 230], [246, 197, 255], [172, 139, 106], [74, 65, 255], [205, 255, 238], [255, 49, 0], [172, 123, 8], [148, 189, 65], [172, 205, 131], [0, 106, 205], [65, 139, 197], [246, 189, 16], [65, 255, 65], [123, 123, 57],
              [0, 170, 50], [170, 0, 50], [136, 0, 50], [10, 170, 50], [170, 170, 50], [5, 98, 50], [82, 76, 50], [87, 170, 50], [170, 54, 50], [87, 16, 50], [164, 82, 50], [87, 170, 50], [148, 126, 50], [158, 82, 50], [60, 142, 50], [65, 0, 50], [27, 170, 50], [76, 114, 50], [16, 98, 50], [38, 49, 50], [136, 54, 50], [120, 131, 50], [38, 126, 50], [148, 0, 50], [114, 70, 50], [170, 170, 50], [98, 170, 50], [49, 136, 50], [114, 120, 50], [104, 32, 50], [49, 76, 50], [0, 136, 50], [131, 170, 50], [170, 104, 50], [170, 32, 50], [164, 131, 50], [114, 92, 50], [49, 43, 50], [136, 170, 50], [170, 32, 50], [114, 82, 50], [98, 126, 50], [114, 136, 50], [0, 70, 50], [43, 92, 50], [164, 126, 50], [43, 170, 50], [82, 82, 50],
              [50, 170, 32], [50, 32, 170], [50, 0, 170], [50, 170, 170], [50, 170, 0], [50, 98, 98], [50, 76, 164], [50, 170, 60], [50, 54, 104], [50, 16, 98], [50, 82, 0], [50, 170, 170], [50, 126, 54], [50, 82, 170], [50, 142, 0], [50, 0, 164], [50, 170, 98], [50, 114, 104], [50, 98, 170], [50, 49, 120], [50, 54, 49], [50, 131, 0], [50, 126, 54], [50, 0, 92], [50, 70, 114], [50, 170, 87], [50, 170, 114], [50, 136, 148], [50, 120, 170], [50, 32, 148], [50, 76, 76], [50, 136, 131], [50, 170, 32], [50, 104, 98], [50, 32, 153], [50, 131, 170], [50, 92, 70], [50, 43, 170], [50, 170, 158], [50, 82, 5], [50, 126, 43], [50, 136, 87], [50, 70, 136], [50, 92, 131], [50, 126, 10], [50, 170, 43], [50, 82, 38],
              [0, 50, 170], [170, 50, 32], [136, 50, 170], [10, 50, 170], [170, 50, 0], [5, 50, 98], [82, 50, 164], [87, 50, 60], [170, 50, 104], [87, 50, 98], [164, 50, 0], [87, 50, 170], [148, 50, 54], [158, 50, 170], [60, 50, 0], [65, 50, 164], [27, 50, 98], [76, 50, 104], [16, 50, 170], [38, 50, 120], [136, 50, 49], [120, 50, 0], [38, 50, 54], [148, 50, 92], [114, 50, 114], [170, 50, 87], [98, 50, 114], [49, 50, 148], [114, 50, 170], [104, 50, 148], [49, 50, 76], [0, 50, 131], [131, 50, 32], [170, 50, 98], [170, 50, 153], [164, 50, 170], [114, 50, 70], [49, 50, 170], [136, 50, 158], [170, 50, 0], [114, 50, 5], [98, 50, 43], [114, 50, 87], [0, 50, 136], [43, 50, 131], [164, 50, 10], [43, 50, 43], [82, 50, 38]
          ]
      else: # To change the colors if needed: for example, to have more contrast between modules on clusters with few modules
        L=[
              [255, 0, 0], [0, 255, 0], [0, 0, 255],     [255, 255, 0], [255, 0, 255], [0, 255, 255],     [200, 100, 100], [100, 200, 100], [100, 100, 200],
              [255, 82, 156], [131, 24, 148], [246, 123, 0], [131, 255, 255], [222, 189, 82], [238, 123, 255], [90, 213, 0], [98, 0, 246], [41, 255, 148], [115, 172, 156], [24, 148, 255], [57, 74, 180], [205, 82, 74], [180, 197, 0], [57, 189, 82], [222, 0, 139], [172, 106, 172], [255, 255, 131], [148, 255, 172], [74, 205, 222], [172, 180, 255], [156, 49, 222], [74, 115, 115], [0, 205, 197], [197, 255, 49], [255, 156, 148], [255, 49, 230], [246, 197, 255], [172, 139, 106], [74, 65, 255], [205, 255, 238], [255, 49, 0], [172, 123, 8], [148, 189, 65], [172, 205, 131], [0, 106, 205], [65, 139, 197], [246, 189, 16], [65, 255, 65], [123, 123, 57],
              [0, 170, 50], [170, 0, 50], [136, 0, 50], [10, 170, 50], [170, 170, 50], [5, 98, 50], [82, 76, 50], [87, 170, 50], [170, 54, 50], [87, 16, 50], [164, 82, 50], [87, 170, 50], [148, 126, 50], [158, 82, 50], [60, 142, 50], [65, 0, 50], [27, 170, 50], [76, 114, 50], [16, 98, 50], [38, 49, 50], [136, 54, 50], [120, 131, 50], [38, 126, 50], [148, 0, 50], [114, 70, 50], [170, 170, 50], [98, 170, 50], [49, 136, 50], [114, 120, 50], [104, 32, 50], [49, 76, 50], [0, 136, 50], [131, 170, 50], [170, 104, 50], [170, 32, 50], [164, 131, 50], [114, 92, 50], [49, 43, 50], [136, 170, 50], [170, 32, 50], [114, 82, 50], [98, 126, 50], [114, 136, 50], [0, 70, 50], [43, 92, 50], [164, 126, 50], [43, 170, 50], [82, 82, 50],
              [50, 170, 32], [50, 32, 170], [50, 0, 170], [50, 170, 170], [50, 170, 0], [50, 98, 98], [50, 76, 164], [50, 170, 60], [50, 54, 104], [50, 16, 98], [50, 82, 0], [50, 170, 170], [50, 126, 54], [50, 82, 170], [50, 142, 0], [50, 0, 164], [50, 170, 98], [50, 114, 104], [50, 98, 170], [50, 49, 120], [50, 54, 49], [50, 131, 0], [50, 126, 54], [50, 0, 92], [50, 70, 114], [50, 170, 87], [50, 170, 114], [50, 136, 148], [50, 120, 170], [50, 32, 148], [50, 76, 76], [50, 136, 131], [50, 170, 32], [50, 104, 98], [50, 32, 153], [50, 131, 170], [50, 92, 70], [50, 43, 170], [50, 170, 158], [50, 82, 5], [50, 126, 43], [50, 136, 87], [50, 70, 136], [50, 92, 131], [50, 126, 10], [50, 170, 43], [50, 82, 38],
              [0, 50, 170], [170, 50, 32], [136, 50, 170], [10, 50, 170], [170, 50, 0], [5, 50, 98], [82, 50, 164], [87, 50, 60], [170, 50, 104], [87, 50, 98], [164, 50, 0], [87, 50, 170], [148, 50, 54], [158, 50, 170], [60, 50, 0], [65, 50, 164], [27, 50, 98], [76, 50, 104], [16, 50, 170], [38, 50, 120], [136, 50, 49], [120, 50, 0], [38, 50, 54], [148, 50, 92], [114, 50, 114], [170, 50, 87], [98, 50, 114], [49, 50, 148], [114, 50, 170], [104, 50, 148], [49, 50, 76], [0, 50, 131], [131, 50, 32], [170, 50, 98], [170, 50, 153], [164, 50, 170], [114, 50, 70], [49, 50, 170], [136, 50, 158], [170, 50, 0], [114, 50, 5], [98, 50, 43], [114, 50, 87], [0, 50, 136], [43, 50, 131], [164, 50, 10], [43, 50, 43], [82, 50, 38]
          ]
    return L
    
# =============================================================================
def show_colors(colors):
    """
    TODO
    """
    n = len(colors)
    fig, ax = plt.subplots(figsize=(n, 1))
    for i, (r, g, b) in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=(r/255, g/255, b/255)))
        ax.text(i + 0.5, -0.2, f"{i+1}", ha='center', va='center', fontsize=10)
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis("off")
    plt.tight_layout()
    plt.show()

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def build_XX0(graph, CS):
    """
    """
    timedeb=time.time()
    nbv=len(graph["nodes"])

    IS0=[]
    for DX in CS:
        sp=float("%.10f"%float(DX["input_sp"]))
        Pp=float(DX["P_p"]); Rp=float(DX["R_p"]); F1p=float(DX["F0.5_p"]); Fpsp=float(DX["Fsp_p"]); OMEGAp=int(DX["omega_p"])
        scoreP='"|Cp(sp=%.4f)|=%i: P=%.2f, R=%.2f, F0.50=%.2f, F%.4f=%.2f, OMEGA=%i"'%(sp,len(DX["Cp"]),Pp,Rp,F1p,sp,Fpsp, OMEGAp)
        
        so=float("%.10f"%float(DX["input_so"]))
        Po=float(DX["P_o"]); Ro=float(DX["R_o"]); F1o=float(DX["F0.5_o"]); Fosp=float(DX["Fsp_o"]); OMEGAo=int(DX["omega_o"])
        scoreO='"|Co(so=%.4f)|=%i: P=%.2f, R=%.2f, F0.50=%.2f, F%.4f=%.2f, OMEGA=%i"'%(so,len(DX["Cp"]),Po,Ro,F1o,sp,Fosp, OMEGAo)       

        member=[[] for _ in range(nbv)] # Cp
        for i in range(len(DX["Cp"])): 
            for j in DX["Cp"][i]:
                member[j].append(i)

        for i in range(len(DX["Cp"])): # Co = Cp + extention
            for j in DX["Ext"][i]:
                member[j].append(i)

        IS0.append({"sp":sp, "N":len(DX["Cp"]), "member":member, "P":DX["P_p"], "R":DX["R_p"], "F1":DX["P_p"], "Fs":DX["Fsp_p"], "OMEGA":DX["omega_p"],
        "scoreP": scoreP, "scoreO": scoreO, "so":sp})

    timefin=time.time()
    return IS0

  
# =============================================================================
def makeJsonGraphGroups(g, C):
    """
    """
    nbv=len(g["nodes"]); nbe=len(g["links"])

    XX=build_XX0(g, C)
      
    # name =================
    CH='  {\n            "name": "%s",\n'%(g["name"])

    # scales
    CH=CH+'              "scales": [\n'
    nbscale=len(XX)
    for i in range(nbscale):

        lastc=("," if i<(nbscale-1) else "")
        CH=CH+'                    {"s":%s, "scoreP": %s, "scoreO": %s}%s\n'%(str(XX[i]["sp"]), XX[i]["scoreP"], XX[i]["scoreO"], lastc)
    CH=CH+'            ],\n'

    # nodes =================
    CH=CH+'            "nodes": [\n'
    for i in range(nbv):
        lastc=("," if i<(nbv-1) else "")
        name=g["nodes"][i]["label"]; name=name.encode('UTF-8'); name=name.decode('UTF-8')

        member=[]
        for ii in range(nbscale):
          member.append(XX[ii]["member"][i])

        CH=CH+'               {"id": %i, "name": "%s", "group": %s}%s\n'%(g["nodes"][i]["id"], name, member,lastc)
    CH=CH+'            ],\n'

    # links =================
    CH=CH+'            "links": [\n'
    for i in range(nbe):
        lastc=("," if i<(nbe-1) else "")
        CH=CH+'               {"id": %i, "source": %i, "target": %i, "value": %.2f}%s\n'%(i, g["links"][i]["source"],
                                                                            g["links"][i]["target"],g["links"][i]["weight"],lastc)
    CH=CH+'            ]\n        }\n'
    return CH

# =============================================================================
def make3DHTML(graph, C, OutfileHTML, input_colors={}):
  """
  """
  CH=""; nl="\n"

  CH="""
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">

    <!-- Local library -->
    <script src="../VascoAsturiano-libs/three.147.min.js"></script>
    <script src="../VascoAsturiano-libs/three-spritetext.min.js"></script>
    <script src="../VascoAsturiano-libs/3d-force-graph.js"></script>

    <!-- local KaTeX -->
    <script src="../VascoAsturiano-libs/KaTeX/katex.min.js"></script>
    <script src="../VascoAsturiano-libs/KaTeX/auto-render.min.js"></script>
    <link rel="stylesheet" href="../VascoAsturiano-libs/KaTeX/katex.min.css">

    <style>
        html {
            margin-left: 0;
            margin-right: 0;
            height: 100%;
            font-size: 12px;
            font-family: Arial;
            background: #f9f9f9;
        }

        body {
            margin-left: 15%;
            margin-right: 0;
            height: 100%;
            font-size: 12px;
            font-family: Arial;
            background: #f9f9f9;
        }

        #graph-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
            border: none;
            overflow: hidden;
        }

        h1 {
            position: relative;
            margin-top: 0px;
            margin-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
            color: #333;
            font-size: 24px;
            margin-top: 0px;
            margin-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
            padding: 0px 0px 0px 0px;
        }

        h2 {
            margin-left: 0px;
            margin-top: 0px;
            margin-bottom: 0px;
            color: #333;
        }

        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            font-size: 40px;
            font-style: italic;
            color: #777;
            background-color: transparent;
        }

        /* DESCRITION SCALES ----------------------------------------------------------------------------------------------*/
        .scale-button {
            margin-top: 2px;
            margin-bottom: 4px;
            font-size: 14px;
            font-weight: bold;
            padding: 1px 8px;
            margin-right: 2px;
            background-color: #757575;
            border: none;
            color: white;
            border-radius: 2px;
            cursor: pointer;
        }

        .scale-button:hover {
            background-color: #4F4F4F;
            color: white;
        }

        .scale-button.active {
            background-color: #050505;
            color: white;
        }

        /* SCORES -----------------------------------------------------------------------------------------------------------*/
        .updated.glow {
            /* Gentle animation */
            transform: scale(1.05);
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.25);
        }

        .updated.burst {
            /* More vibrant animation */
            transform: scale(1.18);
            box-shadow: 0 0 12px rgba(0, 0, 0, 0.35);
        }

        /* clustering scores per partition */
        #scoreP {
            display: inline-block;
            margin-top: 2px;
            margin-bottom: 4px;
            margin-left: 0px;
            font-weight: bold;
            font-size: 16px;
            color: white;
            background-color: #757575;
            padding: 3px 9px;
            border-radius: 3px;
            transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .scoreP:hover {
            background-color: #4F4F4F;
            color: white;
        }

        .scoreP.active {
            background-color: #050505;
            color: white;
        }

        /* overlapping clustering scores */
        #scoreO {
            display: inline-block;
            margin-top: 2px;
            margin-bottom: 4px;
            margin-left: 0px;
            font-weight: bold;
            font-size: 16px;
            color: white;
            background-color: #757575;
            padding: 3px 9px;
            border-radius: 3px;
            transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .scoreO:hover {
            background-color: #4F4F4F;
            color: white;
        }

        .scoreO.active {
            background-color: #050505;
            color: white;
        }

        /* --------------------------------------------------------------------------------------------------------------*/
        #dragNodeToggle {
            background-color: transparent;
            border: transparent;
            color: white;
            font-size: 29px;
            font-weight: bold;
            cursor: pointer;
        }

        /* --------------------------------------------------------------------------------------------------------------*/
        #freezeColorToggle {
            background-color: transparent;
            border: transparent;
            color: white;
            font-size: 29px;
            font-weight: bold;
            cursor: pointer;
        }

        /* --------------------------------------------------------------------------------------------------------------*/
        /* generic button +/-*/

        .buttonPM {
            display: flex;
            align-items: flex-start;
        }

        .buttonPM button {
            background: transparent;
            border: transparent;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }

        .buttonPM .titre {
            font-size: 29px;
            padding: 0 2px;
        }

        .buttonPM .pm {
            display: flex;
            flex-direction: column;
            margin-left: 4px;
            margin-right: 4px;
        }

        .buttonPM .plus,
        .buttonPM .moins {
            font-size: 16px;
            line-height: 16px;
            padding: 0;
            height: 16px;
        }

        /* ROTATION --------------------------------------------------------------------------------------------------------------*/
        #rotationToggle {
            position: absolute;
            top: 98px;
            left: 150px;
            transform: translateX(-50%);
            background-color: transparent;
            border: transparent;
            color: white;
            font-size: 29px;
            font-weight: bold;
            cursor: pointer;
            padding: 0px 2px;
        }

        #faster {
            position: absolute;
            top: 98px;
            left: 226px;
            background-color: transparent;
            border: 2px solid transparent;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            padding: 0px 0px;
        }

        #slower {
            position: absolute;
            top: 115px;
            left: 226px;
            background-color: transparent;
            border: 2px solid transparent;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            padding: 0px 0px;
        }

        /* EXPORT -----------------------------------------------------------------------------------------------------------------*/
        #export {
            background-color: transparent;
            border: transparent;
            color: white;
            font-weight: bold;
            font-size: 30px;
            cursor: pointer;
        }

        #export-menu {
            padding: 0px 0px;
            position: absolute;
            z-index: 50;
            background: #e6e6e6;
            color: black;
            border: white;
            display: none;
        }

        .export-option {
            padding: 3px 20px;
            cursor: pointer;
            border: white;
            font-size: 14px;
            z-index: 51;
        }

        .export-option:hover {
            padding: 3px 20px;
            background: white;
            color: black;
            font-weight: bold;
        }

        /* FOCUS -----------------------------------------------------------------------------------------------------------*/
        /* FOCUS buttons */
        .FOCUSbutton {
            background-color: transparent;
            border: transparent;
            color: white;
            font-size: 29px;
            font-weight: bold;
            cursor: pointer;
        }

        .FOCUSbuttonFree {
            padding: 10px 10px;
            margin: 10px;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background-color: #757575;
            color: white;
            transition: 0.3s;
        }

        .FOCUSbuttonFree:hover {
            background: #050505;
            color: white;
        }

        .FOCUSbuttonFree.active {
            background-color: #050505;
            color: white;
        }

        .FOCUSbutton:hover {
            background-color: transparent;
        }

        /* Floating window */
        .FOCUSpopup {
            position: fixed;
            display: none;
            top: 100px;
            left: 7px;
            width: 14%;
            height: 80%;
            background: #e6e6e6;
            border: 2px solid #757575;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            resize: both;
            overflow: auto;
        }

        .FOCUSpopup-header {
            background-color: #757575;
            color: white;
            font-weight: bold;
            padding: 0px 0px 0px 13px;
            cursor: move;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .FOCUScloseBtn {
            cursor: pointer;
            font-weight: bold;
            background: none;
            border: none;
            color: white;
            font-size: 18px;
        }

        .FOCUS_GO {
            cursor: pointer;
            font-weight: bold;
            background: #757575;
            border-radius: 100px;
            border: none;
            color: white;
            font-size: 18px;
            margin-bottom: 10px;
        }

        .FOCUS_GO:hover {
            background: #050505;
            color: white;
        }

        .FOCUSpopup-content {
            padding: 15px;
            text-align: center;
        }

        /* Radio selection */
        .FOCUSchoices {
            font-weight: bold;
            display: flex;
            justify-content: space-around;
            margin-bottom: 15px;
        }

        .FOCUSchoices input[type="radio"][value="LABEL"],
        .FOCUSchoices input[type="radio"][value="ID"],
        .FOCUSchoices input[type="radio"][value="FocusRadio3"],
        .FOCUSchoices input[type="radio"][value="FocusRadio4"] {
            accent-color: #050505;
        }

        .FOCUSchoices label {
            margin: 0 5px;
            cursor: pointer;
        }

        /* Text field */
        .FOCUSinput {
            width: 90%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            outline: none;
            border-radius: 4px;
            font-size: 16px;
        }

        .FOCUSinput_COM {
            background: #757575;
            margin-bottom: 15px;
            padding-top: 10px;
            min-height: 30px;
            font-weight: bold;
            text-align: center;
            font-size: 14px;
            color: white;
            z-index: 1000;
        }

        /* Table buttons B.i.j */
        .FOCUStable {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 0px;
            background-color: transparent;
        }

        .FOCUStable td {
            padding: 0px;
            text-align: center;
            background-color: transparent;
        }

        .FOCUStable button {
            padding-left: 0px;
            padding-right: 0px;
            width: 100px;
            margin-bottom: 10px;
            background-color: #878787;
            /* 3px solid white; // #f2f2f2 #e6e6e6 #d9d9d9 #c3c3c3 #a4a4a4 #878787 #6a6a6a*/
            color: white;
            font-weight: bold;
            border: transparent;
            /* 4px solid white;*/
        }

        .FOCUStable button.active {
            background-color: #050505;
            border: 2px solid white;
        }

        /* Results area*/
        .FOCUSresult {
            border-top: 1px solid #ddd;
            background: white;
            padding-top: 10px;
            min-height: 30px;
            font-weight: bold;
            text-align: left;
            font-size: 14px;
            color: #333;
            z-index: 1000;
        }

        /* completion on the labels ========*/
        .FOCUS-suggestions {
            position: absolute;
            background: white;
            border: 1px solid #aaa;
            max-height: 130px;
            overflow-y: auto;
            width: 235px;
            display: none;
            z-index: 9999;
        }

        .FOCUS-suggestion-item {
            padding: 4px 8px;
            cursor: pointer;
        }

        .FOCUS-suggestion-item:hover {
            background: #eee;
        }

        /* Context menu on node ===========*/
        #menuRCON {
            position: absolute;
            display: none;
            background: #fff;
            color: black;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            border: 1px solid #ccc;
            border-radius: 2px;
            padding: 15px;
            width: 300px;
            /* largeur totale */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            z-index: 20;
            cursor: move;
        }

        #menuRCON {
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            font-size: inherit;
        }

        #menuRCON h2 {
            margin: 2px 2px 2px;
            border-radius: 2px;
            padding: 5px;
            font-size: 12px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-align: left;
            background: #616060;
            /* #757575;  color:#F54927 */
            color: #fff;
        }

        .action-blocRCONkRCON {
            margin-bottom: 5px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
        }

        .action-blocRCON h3 {
            margin: 0 0 2px 0;
            font-size: 10px;
            font-weight: bold;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-decoration: underline;
        }

        /* Buttons and descriptions aligned in row */
        #menuRCON {
            position: absolute;
            display: none;
            background: #fff;
            color: black;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            border: 1px solid #ccc;
            border-radius: 2px;
            padding: 5px;
            width: 300px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            z-index: 20;
        }

        .action-blocRCONkRCON {
            margin-bottom: 2px;
        }

        .action-blocRCON h3 {
            margin: 0 0 2px 0;
            font-size: 10px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-decoration: underline;
        }

        /* Button line + aligned descriptions + latex*/
        .btn-desc-rowRCON {
            display: flex;
            gap: 8px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            /* horizontal space */
        }

        .btn-desc-itemRCON {
            display: flex;
            flex-direction: column;
            max-width: 90px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            /* by default it's wider */
            flex: 1;
        }

        .btn-desc-itemRCON .ctx-btnRCON {
            width: 50%;
            padding: 1px 1px;
            color: #eee;
            background: #757575;
            /* #616060;  #757575;  color:#F54927 */
            border-radius: 2px;
            cursor: pointer;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            box-sizing: border-box;
        }

        .btn-desc-itemRCON .ctx-btnRCON:hover {
            background: #4F4F4F;
            color: white;
        }

        .btn-desc-itemRCON .desc-textRCON {
            font-size: 11px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            color: #444;
            text-align: left;
            margin-top: 2px;
            margin-left: 0px;
        }

        /*Context menu on background ===================================================================*/
        #menuLDCON {
            position: absolute;
            display: none;
            background: #fff;
            color: black;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            border: 1px solid #ccc;
            border-radius: 2px;
            padding: 15px;
            width: 350px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            z-index: 20;
            cursor: move;
        }

        #menuLDCON {
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            font-size: inherit;
        }

        #menuLDCON h2 {
            margin: 2px 2px 2px;
            border-radius: 2px;
            padding: 5px;
            font-size: 12px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-align: left;
            background: #616060;
            /* #757575;  color:#F54927 */
            color: #fff;
        }

        .action-blocLDCONkLDCON {
            margin-bottom: 5px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
        }

        .action-blocLDCON h3 {
            margin: 0 0 2px 0;
            font-size: 10px;
            font-weight: bold;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-decoration: underline;
        }

        /* Line of buttons + descriptions aligned */
        #menuLDCON {
            position: absolute;
            display: none;
            background: #fff;
            color: black;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            border: 1px solid #ccc;
            border-radius: 2px;
            padding: 5px;
            width: 350px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            z-index: 20;
        }

        .action-blocLDCONkLDCON {
            margin-bottom: 2px;
        }

        .action-blocLDCON h3 {
            margin: 0 0 2px 0;
            font-size: 10px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            text-decoration: underline;
        }

        /* Button line + aligned descriptions + latex*/
        .btn-desc-rowLDCON {
            display: flex;
            gap: 8px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
        }

        .btn-desc-itemLDCON {
            display: flex;
            flex-direction: column;
            max-width: 90px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            /* by default it's wider */
            flex: 1;
        }

        .btn-desc-itemLDCON .ctx-btnLDCON {
            width: 50%;
            padding: 1px 1px;
            color: #eee;
            background: #757575;
            /* #616060;  #757575;  color:#F54927 */
            border-radius: 2px;
            cursor: pointer;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            box-sizing: border-box;
        }

        .btn-desc-itemLDCON .ctx-btnLDCON:hover {
            background: #4F4F4F;
            color: white;
        }

        .btn-desc-itemLDCON .desc-textLDCON {
            font-size: 11px;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            color: #444;
            text-align: left;
            margin-top: 2px;
            margin-left: 0px;
        }

        /* --------------------------------------------------------------------------------------------------- */
        /* objects attached to a node*/
        #menuAttachedObj {
            position: absolute;
            display: none;

            background: white;
            color: black;

            width: 300px;

            border: 1px solid #ccc;
            border-radius: 2px;

            padding: 10px;

            font-family: Verdana, Geneva, Tahoma, sans-serif;
            font-size: 12px;

            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);

            z-index: 30;
        }

        #menuAttachedObj h2 {
            margin: 0 0 10px 0;
            padding: 5px;

            background: #616060;
            color: white;

            font-size: 12px;
        }

        .obj-line {
            margin: 8px 0;
        }

        .obj-line label {
            cursor: pointer;
        }

        #AO_header {
            cursor: move;
            user-select: none;
        }

        #LOGO_nPnB {
            position: absolute;
            top: 15px;
            left: 105px;
            width: 80px;
            height: auto;
            margin-top: 0px;
            margin-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
            padding: 0px 0px 0px 0px;
        }

        #userguide {
            background-color: transparent;
            border: transparent;
            color: white;
            font-weight: bold;
            font-size: 30px;
            cursor: pointer;
        }

        #toolbar {
            position: absolute;
            top: 98px;
            box-sizing: border-box;
            
            left: 20px;

            display: flex;
            justify-content: space-between;
            
            gap: 500px;
            
        }

        #toolbar-left{
            left:0;
            display: flex;
            align-items: center;
            gap: 20px;
        }

        #toolbar-right {
            left:0;
            display: flex;
            align-items: center;
            gap: 20px;
        }

    </style>
</head>

<body>

    <!-- page structure ------------------------------------------------------------------------------>
    <a href="https://www.nature.com/articles/s41598-025-90454-w" target="_blank">
        <img id="LOGO_nPnB" src="./LOGO_nPnB_R.png" alt="LOGO">
    </a>

    <div id="graph-wrapper">

        <h1 id="NamePedig"></h1>

        <div>
            <h1 id="TScales" style="display:inline-block; margin-left:0px; padding: 0px; font-size: 14px"></h1>
            <div id="Scale-buttonS" style="display:inline-block; margin-left:0px;"></div>
        </div>

        <div>
            <h1 id="TScores" style="display:inline-block; margin-left:0px; padding: 0px; font-size: 14px"></h1>
            <h1 id="scoreP"></h1>
            <h2 id="scoreO"></h2>
            <h1 id="WWW" style="display:inline-block; margin-left:0px; padding: 0px; font-size: 20px"></h1>
        </div>

        <div id="Graph3D"></div>

        <div id="toolbar">
            <div id="toolbar-left">

                <button class="FOCUSbutton FOCUSopenBtn">&#x1F50D</button>

                <button id="dragNodeToggle">✣</button>

                <div class="buttonPM" id="rotationControl">  <!--  /* $+*/ -->
                    <button class="titre">↻</button>
                
                    <div class="pm">
                        <button class="plus">+</button>
                        <button class="moins">-</button>
                    </div>
                </div>

                <div class="buttonPM" id="awareControl">  <!--  /* $+*/ -->
                    <button class="titre">Smart</button>
                
                    <div class="pm">
                        <button class="plus">+</button>
                        <button class="moins">-</button>
                    </div>
                </div>

                <button id="freezeColorToggle">UnFrozCol</button>

                <div class="buttonPM" id="LabelControl"> <!-- /* $+*/ -->
                    <button class="titre">SizLab</button>
                </div>
            </div> <!-- <div id="toolbar-left"> -->
            
            <div id="toolbar-right"s>
                <button id="userguide">USER-GUIDE</button>
                <div>
                    <button id="export">EXPORT</button> <!-- /* $+*/ -->

                    <div id="export-menu">
                        <div class="export-option" data-format="jpg">JPG</div>
                        <div class="export-option" data-format="png2">PNG 2×</div>
                        <div class="export-option" data-format="png4">PNG 4×</div>
                    </div>
                </div>

            </div> <!-- <div id="toolbar-right"> -->
        </div> <!-- <div id="toolbar"> -->

        <div class="FOCUSpopup">
            <div class="FOCUSpopup-header">
                <span>FOCUS</span>
                <button class="FOCUScloseBtn">✖</button>
            </div>
            <div class="FOCUSpopup-content">
                <!-- Exclusive choices -->
                <div class="FOCUSchoices">
                    <label><input type="radio" name="FOCUSchoix" value="LABEL" checked> LABEL</label>
                    <label><input type="radio" name="FOCUSchoix" value="ID"> ID</label>
                </div>
        
                <!-- Text field to enter -->
                <input type="text" class="FOCUSinput" placeholder="Enter the reference of a node (LABEL or ID)">
                <!--  <input type="text" class="FOCUSinput" autocomplete="off"> -->
                <div class="FOCUS-suggestions"></div>
        
                <div class="FOCUSinput_COM"></div>
        
                <button class="FOCUS_GO">GO</button>
        
                <!-- B.i.j button array -->
                <table class="FOCUStable">
                    <tr>
                        <td><button class="FOCUSbuttonFree zoom_N" data-i="0" data-j="0">My Neig.</button></td>
                        <td><button class="FOCUSbuttonFree zoom_M" data-i="0" data-j="1">My Cp Mod.</button></td>
                    </tr>
                </table>
        
                <!-- Result display area -->
                <div class="FOCUSresult"></div>
            </div>
        </div>

        <div id="menuRCON"></div>

        <div id="menuLDCON"></div>

        <div id="menuAttachedObj"></div>

        <div id="loading">Loading the graph...</div>
    </div> <!-- <div id="graph-wrapper">-->
    <!------------------------------------------------------------------------------------------------>
  """+nl


  CH=CH+"""<!-- $$$$ -->"""+nl
  CH=CH+"""     <title>%s_3D</title>"""%(graph['name'])+nl
  CH=CH+"""     <script>"""+nl
  CH=CH+"""        // building the basic colors -->\n        const colorRGB=%s;\n      </script>\n"""%(generate_contrasting_colors(input_colors))+nl
  CH=CH+""" 

      <script>
        TScales.textContent = 'Description Scales: ';
        TScores.textContent = 'Scores: ';
      </script>

      <script type="application/json" id="graph-data">\n"""
      
  CH=CH+"""     %s           </script>\n"""%(makeJsonGraphGroups(graph, C))
  CH=CH+"""<!-- $$$$ -->"""+nl



  CH=CH+"""
<!-- $$$$ -->

    <script>
        const colorHEX = colorRGB.map(([r, g, b]) => '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join(''));
        const LCH = colorHEX.length;


        window.addEventListener("load", event => {
            document.getElementById('loading').style.display = 'none';
            working = document.getElementById('loading');

            window.addEventListener("load", updateGraphHeight);
            window.addEventListener("resize", updateGraphHeight);
            // ====== minimal change ======
            window.ForceGraph3DInstance = new ForceGraph3D(document.getElementById('Graph3D'));

            const NODE_R = 1;
            const highlightNodes = new Set();
            const highlightLinks = new Set();
            let hoverNode = null;
            let D = {}; let str_mod = "!"; let str1 = "!";
            let distance = 500;
            let CamPos, CamPos0;
            let clickedNodeId = null;
            let nodeDrag = false;
            let ScaleFrozenColor = -1;

            let coef_weak_strength = 1;
            let freezeAfterSimulation = true;

            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*GRAPH*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            const rawData = document.getElementById("graph-data").textContent;
            const gData = JSON.parse(rawData);
            const Graph = window.ForceGraph3DInstance;
            const myTitle = gData.name + ": |V|=" + gData.nodes.length + ", |E|=" + gData.links.length;

            const WinnerWidth = window.innerWidth;

            Graph
                .width(WinnerWidth * 0.5 * 1.618)
                .height(WinnerWidth * 0.5)


                .onEngineStop(() => {
                    if (!freezeAfterSimulation) { return };

                    freezeAfterSimulation = false;

                    Graph.graphData().nodes.forEach(n => {
                        n.fx = n.x;
                        n.fy = n.y;
                        n.fz = n.z;
                    });

                    //let D = Barycenter("all_visible")
                    //STATE.R.LKA.x = D.x
                    //STATE.R.LKA.y = D.y
                    //STATE.R.LKA.z = D.z

                    Graph.onEngineStop(() => { }); // disables the callb-ack
                })

                .graphData(gData)

                .nodeResolution(8)

                .nodeRelSize(1)

                .nodeOpacity(0.9)

                .backgroundColor("#e6e6e6") // #f2f2f2 #e6e6e6 #d9d9d9 #c3c3c3 #a4a4a4 #878787 #6a6a6a

                .showNavInfo(true)

                .linkDirectionalParticleWidth(4)

                .nodeVisibility(node => getNodVis(node.id))

                // .nodeColor(node => myColorNode(node.id))

                .onNodeHover(node => {
                    //
                    // no state change
                    if ((!node && !highlightNodes.size) || (node && hoverNode === node)) return;
                    highlightNodes.clear();
                    highlightLinks.clear();
                    if (node) {
                        highlightNodes.add(node);
                        node.neighbors.forEach(i => highlightNodes.add(gData.nodes[i]));
                        node.links.forEach(i => highlightLinks.add(gData.links[i]));
                    }
                    hoverNode = node || null;
                    updateHighlight();
                })

                .enableNodeDrag(false)

                .onNodeClick((node, event) => {
                    CLickKEY_node_L(event, node)
                })

                .onNodeRightClick((node, event) => {
                    CLickKEY_node_R(event, node)
                })

                .onBackgroundClick((event) => {
                    CLickKEY_ground_L(event)
                })

                .onBackgroundRightClick((event) => {
                    CLickKEY_ground_R(event)
                })

                // .linkColor(link => myColorLink(link))

                .linkDirectionalParticles(link => highlightLinks.has(link) ? 4 : 0)

                .linkVisibility(link => (typeof link.source === "object" && typeof link.target === "object") ?
                    (getNodVis(link.source.id) && getNodVis(link.target.id)) : true)

                .linkWidth(link => highlightLinks.has(link) ? 4 : 1)

                .onLinkHover(link => {
                    //
                    highlightNodes.clear();
                    highlightLinks.clear();
                    if (link) {
                        highlightLinks.add(link);
                        highlightNodes.add(link.source);
                        highlightNodes.add(link.target);
                    }
                    updateHighlight();
                })

                .cameraPosition({ z: distance })

                // TO DISPLAY THE LABELS
                .nodeThreeObject(node => {
                    if ((!getNodVis(node.id)) || (!getNodLabVis(node.id))) { return null; }

                    // LABEL
                    const sprite = new SpriteText(node.name);

                    // clear the depth buffer before drawing the label
                    sprite.onBeforeRender = (renderer) => renderer.clearDepth();

                    // Prevents the sprite from being hidden by links/nodes
                    sprite.material.depthWrite = false;
                    sprite.material.depthTest = false;
                    sprite.material.transparent = true;
                    sprite.material.needsUpdate = true;

                    // Make sure it is drawn last
                    sprite.renderOrder = 9999;

                    sprite.color = "black" // myColorNode(node.id);

                    if (node.prop.BL) {
                        sprite.textHeight = 2 * LabelSize;
                    }
                    else {
                        sprite.textHeight = LabelSize;
                    }

                    sprite.textAlign = 'left';
                    sprite.center.set(0, 0);
                    sprite.position.x = 5;

                    return sprite;
                })

                .nodeThreeObjectExtend(true);
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            function RefreshGraph() {
                Graph.refresh()
            }
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // INITIALIZATION
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            gData.nodes.forEach(node => {
                node.deg = 0;
                node.val = 0;
                node.neighbors = [];
                node.links = [];
                node.prop = { V: true, L: false, BL: false, C: [] };
            });

            gData.links.forEach(link => {
                const a = gData.nodes[link.source];
                const b = gData.nodes[link.target];

                a.deg = a.deg + 1;
                b.deg = b.deg + 1;

                a.val = a.val + NODE_R;
                b.val = b.val + NODE_R;

                !a.neighbors && (a.neighbors = []);
                !b.neighbors && (b.neighbors = []);
                a.neighbors.push(b.id);
                b.neighbors.push(a.id);

                !a.links && (a.links = []);
                !b.links && (b.links = []);
                a.links.push(link.id);
                b.links.push(link.id);
            });

            const renderer = Graph.renderer();
            const camera = Graph.camera();
            const mainScene = Graph.scene();
            const baseRender = renderer.render.bind(renderer);
            renderer.render = function (scene, cam) {
                baseRender(scene, cam);        // normal graph
            };

            gData.nodes.forEach(node => {
                node.val = node.val ** 2;

            });

            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            // INTERFACE STATE
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            FOCUS_cross = false;
            LabelSize = 16;

            let STATE = { // STATE 
                s: 0, // id of current scale

                p: true, // on Cp or on Co

                R: { // Rotation statut
                    Bary: false,
                    active: false,
                    CamPos0: { x: 0, y: 0, z: 100 + Math.pow(Math.log(gData.nodes.length), 4) },
                    distance0: 100 + Math.pow(Math.log(gData.nodes.length), 4),
                    LKA0: { x: 0, y: 0, z: 0 },
                    LKA: { x: 0, y: 0, z: 0 },
                    dist: 100,
                    angle: 0,
                    ms: 0,
                    speed: 2000,
                    interval: 10
                },

                FOC: { // FOCUS status
                    active: false,
                    btn: "",
                    id: -1,
                    idPartner: [],
                    validNode: false,
                },

                lback: [],

                PLOT: {
                    aware: false,
                    nbVisibleNodes: 0
                },
            }
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            STATE.PLOT.nbVisibleNodes = nbVisibleNodes()
            STATE.lback.push({ T: "INIT", ARO: "", ID: "", s: "", a: "", b: "" })

            const scales = gData.scales || [];
            const maxNumScale = Math.max(...gData.nodes.map(n => n.group.length));
            const numScaleButton = Math.min(scales.length, maxNumScale);

            const scaleButtonS = document.getElementById("Scale-buttonS");

            const scoreP_Btn = document.getElementById("scoreP");
            const scoreO_Btn = document.getElementById("scoreO");
            const scoreDisplayP = document.getElementById("scoreP");
            const scoreDisplayO = document.getElementById("scoreO");

            const DisplayWWW = document.getElementById("WWW");


            // ROTATION setInterval --------------------------------------------------
            ROTATIONtimerId = setInterval(() => {
                if (STATE.R.active) {
                    // Camera position around CAM_LookAt at a distance of CAM_dist

                    if (STATE.R.Bary) {
                        let D = Barycenter("all_visible")
                        STATE.R.LKA.x = D.x
                        STATE.R.LKA.y = D.y
                        STATE.R.LKA.z = D.z
                    }

                    x = Math.cos(STATE.R.angle);
                    y = Math.sin(STATE.R.angle);
                    z = 0;
                    C = rotateMap(x, y, z);

                    CamPos = Graph.cameraPosition()
                    let CaRotix = (CamPos.x - STATE.R.LKA.x)
                    let CaRotiy = (CamPos.y - STATE.R.LKA.y)
                    let CaRotiz = (CamPos.z - STATE.R.LKA.z)

                    STATE.R.dist = Math.sqrt((CaRotix * CaRotix) + (CaRotiy * CaRotiy) + (CaRotiz * CaRotiz));

                    let camX = STATE.R.LKA.x + STATE.R.dist * C[0];
                    let camY = STATE.R.LKA.y + STATE.R.dist * C[1];
                    let camZ = STATE.R.LKA.z + STATE.R.dist * C[2];

                    Graph.cameraPosition(
                        { x: camX, y: camY, z: camZ },   // position around point STATE.R.LKA
                        STATE.R.LKA,                     // lookAt towards STATE.R.LKA
                        STATE.R.ms                       // transition time (0 = instantaneous)
                    );

                    STATE.R.angle += Math.PI / STATE.R.speed;
                }
            }, STATE.R.interval)

            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION ACTION 
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // firts time display of the graph cluster_unaware
            STATE.s = 0;
            PLOT_Vastur_Geometry_Unaware(Graph);
            Graph.nodeLabel(node => `<span style="font-size:16px">${myLNeigS(node.id)}</span>`);
            UPDATE_s_p("s")
            UPDATE_s_p("p")
            UPDATE_Color()
            Graph.cameraPosition({ z: distance })
            //CLICK_rotationToggle({ ctrlKey: true, metaKey: true })
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // WHEN I CLICK
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            function CLickKEY_node_L(event, node) {
                // node, left
                if (event.ctrlKey) {
                    if (event.shiftKey) {
                        CLick_node_L_11(event, node)
                    }
                    else {
                        CLick_node_L_10(event, node)
                    }
                }
                else {
                    if (event.shiftKey) {
                        CLick_node_L_01(event, node)
                    }
                    else {
                        CLick_node_L_00(event, node)
                    }
                }
                event.preventDefault();
                event.stopPropagation();
            }

            function CLickKEY_node_R(event, node) {
                // node, right
                if (event.ctrlKey) {
                    if (event.shiftKey) {
                        CLick_node_R_11(event, node)
                    }
                    else {
                        CLick_node_R_10(event, node)
                    }
                }
                else {
                    if (event.shiftKey) {
                        CLick_node_R_01(event, node)
                    }
                    else {
                        CLick_node_R_00(event, node)
                    }
                }
                event.preventDefault();
                event.stopPropagation();
            }

            function CLickKEY_ground_L(event) {
                // ground, left
                if (event.ctrlKey) {
                    if (event.shiftKey) {
                        CLick_ground_L_11(event)
                    }
                    else {
                        CLick_ground_L_10(event)
                    }
                }
                else {
                    if (event.shiftKey) {
                        CLick_ground_L_01(event)
                    }
                    else {
                        CLick_ground_L_00(event)
                    }
                }
                event.preventDefault();
                event.stopPropagation();
            }

            function CLickKEY_ground_R(event) {
                // ground, right
                if (event.ctrlKey) {
                    if (event.shiftKey) {
                        CLick_ground_R_11(event)
                    }
                    else {
                        CLick_ground_R_10(event)
                    }
                }
                else {
                    if (event.shiftKey) {
                        CLick_ground_R_01(event)
                    }
                    else {
                        CLick_ground_R_00(event)
                    }
                }
                event.preventDefault();
                event.stopPropagation();
            }
            // ------------------------------------------------
            // ------------------------------------------------   

            function CLick_node_L_00(event, node) {
                // node, left, {ctrl: false, shift: false}
                FOCUS_cross = zoom_on_xyz(node.x, node.y, node.z, 100, 1000);
            }
            function CLick_node_L_01(event, node) {
                // node, left, {ctrl: false, shift: true}
            }
            function CLick_node_L_10(event, node) {
                // node, left, {ctrl: true, shift: false}
                node.prop.L = !node.prop.L;
                RefreshGraph()
            }
            function CLick_node_L_11(event, node) {
                // node, left, {ctrl: true, shift: true}
            }
            //
            function CLick_node_R_00(event, node) {
                // node, right, {ctrl: false, shift: false}
                updateVisFromNode(event, node)
            }
            function CLick_node_R_01(event, node) {
                // node, right, {ctrl: false, shift: true}
            }
            function CLick_node_R_10(event, node) {
                // node, right, {ctrl: true, shift: false}
                showMenuAttachedObj(event, node);
            }
            function CLick_node_R_11(event, node) {
                // node, right, {ctrl: true, shift: true}
            }
            // ------------------------------------------------
            // ------------------------------------------------
            let lastCLick_ground_L_00 = 0;
            function CLick_ground_L_00(event) {
                const now = performance.now();
                // ground, left, {ctrl: false, shift: false}
                if (now - lastCLick_ground_L_00 < 500) {
                    if (STATE.R.active) {
                        rotationControl.style.border = "transparent";
                        STATE.R.speed = 2000;
                        STATE.R.active = false;
                    }
                    else {
                        rotationControl.style.border = "4px solid white";

                        CamPos = Graph.cameraPosition()

                        CaRot0x = (CamPos.x - STATE.R.LKA.x)
                        CaRot0y = (CamPos.y - STATE.R.LKA.y)
                        CaRot0z = (CamPos.z - STATE.R.LKA.z)

                        STATE.R.dist = Math.sqrt((CaRot0x * CaRot0x) + (CaRot0y * CaRot0y) + (CaRot0z * CaRot0z));

                        CaRot0x = CaRot0x / STATE.R.dist;
                        CaRot0y = CaRot0y / STATE.R.dist;
                        CaRot0z = CaRot0z / STATE.R.dist;

                        STATE.R.angle = 0

                        STATE.R.Bary = true
                        STATE.R.active = true;
                    }
                    lastCLick_ground_L_00 = 0;
                    return;
                }
                lastCLick_ground_L_00 = now;
            }
            function CLick_ground_L_01(event) {
                // round, left, {ctrl: false, shift: true}
                console.log("«Propaganda is to a democracy what the bludgeon is to a totalitarian state.»" +
                    "Noam Chomsky (2002), in «Media Control: The Spectacular Achievements of Propaganda»")
                
            }
            function CLick_ground_L_10(event) {
                // ground, left, {ctrl: true, shift: false}
                for (let i = 0; i < gData.nodes.length; i++) {
                    if (getNodVis(i)) {
                        gData.nodes[i].prop.L = false;
                    }
                }
                RefreshGraph()
            }
            function CLick_ground_L_11(event) {
                // ground, left, {ctrl: true, shift: true}
                console.log("«Propaganda is to a democracy what the bludgeon is to a totalitarian state.»" +
                        "Noam Chomsky (2002), in «Media Control: The Spectacular Achievements of Propaganda»")
            }
            function CLick_ground_R_00(event) {
                // ground, right, {ctrl: false, shift: false}
                onBackgroundRightClick(event);
            }
            function CLick_ground_R_01(event) {
                console.log("«Propaganda is to a democracy what the bludgeon is to a totalitarian state.»" +
                    "Noam Chomsky (2002), in «Media Control: The Spectacular Achievements of Propaganda»")
                // ground, right, {ctrl: false, shift: true}
            }
            function CLick_ground_R_10(event) {
                // ground, right, {ctrl: true, shift: false}
                for (let i = 0; i < gData.nodes.length; i++) {
                    if (getNodVis(i)) {
                        gData.nodes[i].prop.L = true;
                    }
                }
                RefreshGraph()
            }
            function CLick_ground_R_11(event) {
                console.log("«Propaganda is to a democracy what the bludgeon is to a totalitarian state.»" +
                    "Noam Chomsky (2002), in «Media Control: The Spectacular Achievements of Propaganda»")
                // background, right, {ctrl: true, shift: true}
            }
            // ------------------------------------------------
            // ------------------------------------------------
            function CLick_button_L_00(event) {
                // button, left, {ctrl: false, shift: false}
            }
            function CLick_button_L_01(event) {
                // button, left, {ctrl: false, shift: true}
            }
            function CLick_button_L_10(event) {
                // button, left, {ctrl: true, shift: false}
            }
            function CLick_button_L_11(event) {
                // button, left, {ctrl: true, shift: true}
            }
            function CLick_button_R_00(event) {
                // button, right, {ctrl: false, shift: false}
            }
            function CLick_button_R_01(event) {
                // button, right, {ctrl: false, shift: true}
            }
            function CLick_button_R_10(event) {
                // button, right, {ctrl: true, shift: false}
            }
            function CLick_button_R_11(event) {
                // button, right, {ctrl: true, shift: true}
            }
            // ------------------------------------------------

            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // WHEN I CLICK ON A BUTTON
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            function plugButtonPM(id, actions) {

                const bloc = document.getElementById(id);

                // Empêche le menu contextuel du navigateur
                bloc.addEventListener("contextmenu", event => {
                    event.preventDefault();
                });

                bloc.querySelector(".titre")
                    .addEventListener("mousedown", event => actions.toggle(bloc, event));

                bloc.querySelector(".plus")
                    .addEventListener("mousedown", event => actions.plus(bloc, event));

                bloc.querySelector(".moins")
                    .addEventListener("mousedown", event => actions.moins(bloc, event));
            }

            function plugButtonKey(id, actions) {

                const bloc = document.getElementById(id);

                // empêche le menu du navigateur
                bloc.addEventListener("contextmenu", event => {
                    event.preventDefault();
                });

                const bind = (selector) => {

                    bloc.querySelector(selector)
                        .addEventListener("mousedown", event => {

                            event.preventDefault();
                            event.stopPropagation();

                            actions.toggle(bloc, event);
                        });
                };

                bind(".titre");
            }

            plugButtonKey("LabelControl", {

                toggle(bloc, event) {
                    switch (event.button) {
                        case 0: //console.log("GAUCHE");
                            LabelSize = LabelSize / 1.2
                            break;
                        case 1: //console.log("MOLETTE");
                            break;
                        case 2: //console.log("DROIT");
                            LabelSize = LabelSize * 1.2
                            break;
                    }
                    RefreshGraph()
                }
            });

            // =============================================================================================================
            // when I click the button: SCORES BUTTONS
            // =============================================================================================================

            scoreP_Btn.onclick = () => { // CLICK Button score 
                CLICK_scoreP_Btn()
            };
            function CLICK_scoreP_Btn() { // CLICK soreP
                STATE.p = true;
                UPDATE_s_p("p");
                UPDATE_Color()
            }

            scoreO_Btn.onclick = () => { // CLICK scoreO
                CLICK_scoreO_Btn()
            };
            function CLICK_scoreO_Btn() {
                STATE.p = false;
                UPDATE_s_p("p");
                UPDATE_Color()
            }

            // =============================================================================================================
            // when I click the button: SCALES BUTTONS
            // =============================================================================================================
            /* const scaleButtonS = document.getElementById("Scale-buttonS");*/

            for (let i = 0; i < numScaleButton; i++) {
                const btn = document.createElement("button");
                btn.textContent = scales[i]["s"];
                btn.classList.add("scale-button");
                if (i === STATE.s) {
                    btn.classList.add("active");
                    AnimateScore("s");
                }

                btn.addEventListener("click", event => {
                    CLICK_scaleButtonS_btn(i)
                });
                scaleButtonS.appendChild(btn);
            };

            function CLICK_scaleButtonS_btn(i) {
                STATE.s = i;
                if (STATE.PLOT.aware) {
                    PLOT_Vastur()
                }
                UPDATE_s_p("s")
                UPDATE_s_p("p")
                UPDATE_Color()
            }

            // =============================================================================================================
            // when I click the button: Smart BUTTON
            // =============================================================================================================

            plugButtonPM("awareControl", {
                toggle(bloc, event) {

                    if (STATE.PLOT.aware) {
                        // bloc.querySelector(".titre").style.border = "transparent";
                        awareControl.style.border = "transparent";

                        //coef_weak_strength = 1
                        STATE.PLOT.aware = false;
                    }
                    else {
                        //bloc.querySelector(".titre").style.border = "2px solid white";
                        awareControl.style.border = "2px solid white";
                        //coef_weak_strength = 1;
                        STATE.PLOT.aware = true;
                    }
                    PLOT_Vastur();
                },

                plus() {

                    if (STATE.PLOT.aware) {
                        coef_weak_strength = coef_weak_strength + 1;
                        PLOT_Vastur();
                    }
                },

                moins() {

                    if (STATE.PLOT.aware) {
                        coef_weak_strength = Math.max(coef_weak_strength - 1, 1);
                        PLOT_Vastur();
                    }
                }
            });

            // =============================================================================================================
            // when I click the button: ROTATION BUTTON
            // =============================================================================================================
            plugButtonPM("rotationControl", {
                toggle(bloc, event) {

                    if (STATE.R.active) {
                        rotationControl.style.border = "transparent";
                        STATE.R.speed = 2000;
                        STATE.R.active = false;
                    }
                    else {
                        rotationControl.style.border = "2px solid white";

                        CamPos = Graph.cameraPosition()

                        CaRot0x = (CamPos.x - STATE.R.LKA.x)
                        CaRot0y = (CamPos.y - STATE.R.LKA.y)
                        CaRot0z = (CamPos.z - STATE.R.LKA.z)

                        STATE.R.dist = Math.sqrt((CaRot0x * CaRot0x) + (CaRot0y * CaRot0y) + (CaRot0z * CaRot0z));

                        CaRot0x = CaRot0x / STATE.R.dist;
                        CaRot0y = CaRot0y / STATE.R.dist;
                        CaRot0z = CaRot0z / STATE.R.dist;

                        STATE.R.angle = 0

                        STATE.R.Bary = false
                        STATE.R.active = true;
                    }
                },

                plus() {

                    if (STATE.R.active) {
                        STATE.R.speed /= 1.2;
                    }
                },

                moins() {

                    if (STATE.R.active) {
                        STATE.R.speed *= 1.2;
                    }
                }
            });


            //===================================================================================================
            // Rotation matrix on the unit sphere such that rotateMap(1, 0, 0) --> (CaRot0x, CaRot0y, CaRot0z)
            // To ensure the ROTATION sequence is smooth and without sudden movements (the rotation starts where it is initiated)
            function rotateMap(x, y, z) {
                const s2 = CaRot0y * CaRot0y + CaRot0z * CaRot0z;

                // Special case : CaRot0 = (±1,0,0)
                if (s2 === 0) {
                    if (CaRot0x > 0) {
                        return [x, y, z];        // identity
                    } else {
                        return [-x, y, -z];      // rotation of π around y
                    }
                }

                const c = CaRot0x;              // cos(theta)
                const one_c = 1 - c;

                const A = one_c * (CaRot0z * CaRot0z) / s2;
                const B = - one_c * (CaRot0y * CaRot0z) / s2;
                const D = one_c * (CaRot0y * CaRot0y) / s2;

                const fx = c * x - CaRot0y * y - CaRot0z * z;
                const fy = CaRot0y * x + (c + A) * y + B * z;
                const fz = CaRot0z * x + B * y + (c + D) * z;

                return [fx, fy, fz];
            };


            // =============================================================================================================
            // when I click the button: dragNodeToggle
            // =============================================================================================================
            const freezeColorToggle = document.getElementById("freezeColorToggle");
            document.getElementById('freezeColorToggle').addEventListener('click', event => {

                if (ScaleFrozenColor > -1) {
                    ScaleFrozenColor = -1
                    document.getElementById("freezeColorToggle").style.border = "transparent";
                    freezeColorToggle.textContent = "UnFrozCol";
                }
                else {
                    ScaleFrozenColor = STATE.s
                    document.getElementById("freezeColorToggle").style.border = "2px solid white";
                    freezeColorToggle.textContent = "FrozCol " + scales[ScaleFrozenColor]['s'];
                }
                RefreshGraph()
            });

            // =============================================================================================================
            // when I click the button: dragNodeToggle
            // =============================================================================================================
            const dragNodeToggle = document.getElementById("dragNodeToggle");
            document.getElementById('dragNodeToggle').addEventListener('click', event => {

                if (nodeDrag) {
                    nodeDrag = false
                    document.getElementById("dragNodeToggle").style.border = "transparent";
                    Graph.enableNodeDrag(false)
                }
                else {
                    nodeDrag = true
                    document.getElementById("dragNodeToggle").style.border = "2px solid white";
                    Graph.enableNodeDrag(true)
                }
            });

            // =============================================================================================================
            // when I click the button: GUIDE BUTTON
            // =============================================================================================================
            const userguide = document.getElementById('userguide');
            userguide.onclick = () => {

                const lien = document.createElement("a");
                lien.href = "../userGuide.pdf";
                lien.target = "_blank";
                lien.click();
            };

            // =============================================================================================================
            // when I click the button: EXPORT BUTTON
            // =============================================================================================================
            const exportBtn = document.getElementById('export');
            const exportMenu = document.getElementById('export-menu');

            exportBtn.onclick = () => {

                exportMenu.style.display = exportMenu.style.display === 'block' ? 'none' : 'block';
            };

            document.querySelectorAll('.export-option').forEach(option => {
                option.addEventListener('click', event => {

                    const format = option.dataset.format;
                    const canvas = Graph.renderer().domElement;
                    const link = document.createElement('a');

                    const renderer = Graph.renderer();
                    let scale = 1;

                    if (format === 'png2') scale = 2;
                    else if (format === 'png4') scale = 4;

                    const originalWidth = renderer.domElement.width;
                    const originalHeight = renderer.domElement.height;

                    // temporarily resize
                    renderer.setSize(originalWidth * scale, originalHeight * scale, false);
                    renderer.render(Graph.scene(), Graph.camera());

                    // save the original color
                    const originalBg = Graph.backgroundColor();

                    // temporarily set the background to white
                    Graph.backgroundColor('#ffffff');

                    // force the rendering with the correct clear
                    renderer.setClearColor(0xffffff, 1); // white color, opacity 1
                    renderer.render(Graph.scene(), Graph.camera());

                    // capture according to the format
                    if (format === 'jpg') {
                        link.href = renderer.domElement.toDataURL('image/jpeg', 0.92);
                    } else {
                        link.href = renderer.domElement.toDataURL('image/png');
                    }

                    // return to normal
                    Graph.backgroundColor(originalBg);
                    renderer.setClearColor(originalBg, 1);
                    renderer.render(Graph.scene(), Graph.camera());
                    renderer.setSize(originalWidth, originalHeight, false);
                    renderer.render(Graph.scene(), Graph.camera());

                    const namesave = `viz3D.nPnB.${gData.name}.${STATE.p ? 'Cp' : 'Co'}.${scales[STATE.s]["s"]}`;

                    link.download = `${namesave}.${format.startsWith('jpg') ? 'jpg' : 'png'}`;
                    link.click();
                    exportMenu.style.display = 'none';
                });
            });


            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /* when I click: ON BACKGROUND   */
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            function onBackgroundRightClick(event) {

                event.preventDefault();
                event.stopPropagation();

                const contextData = {
                    title: "\\\\textbf{UPDATE~NODES-VISIBILITY}",
                    ACTIONSonBackgroundRightClick: [
                        { id: "degrees", title: "\\\\blacksquare\\\\textbf{~ON~DEGREES (deg within an INTERVAL)}" },
                        { id: "regexLabel", title: "\\\\blacksquare\\\\textbf{~ON~LABELS (lab matching with a REGEX)}" },
                        {
                            id: "modules", title: "\\\\blacksquare\\\\textbf{~ON~MODDULE (Cp modules at scale "
                                + scales[STATE.s]['s'] + ")}"
                        }
                    ]
                };

                showmenuLDCON(event, contextData);
            }



            // =========================================================
            function updateVisFromNode(event, node) {
                event.preventDefault();
                event.stopPropagation();
                clickedNodeId = node.id;

                let ME_A = getNodVis(clickedNodeId) ? STATE.PLOT.nbVisibleNodes : STATE.PLOT.nbVisibleNodes + 1;
                let ME_R = getNodVis(clickedNodeId) ? STATE.PLOT.nbVisibleNodes - 1 : STATE.PLOT.nbVisibleNodes;
                let ME_I = 1;

                let MYN = myNeig_V_UNV(clickedNodeId);
                let MYN_A = STATE.PLOT.nbVisibleNodes + MYN[1].length;
                let MYN_R = STATE.PLOT.nbVisibleNodes - MYN[0].length;
                let MYN_I = MYN[0].length + MYN[1].length + 1; // unreflexif graph
                if (getNodVis(clickedNodeId)) { MYN_R = MYN_R - 1; } else { MYN_A = MYN_A + 1; };

                let MCP = myCpModuleNode_V_UNV(clickedNodeId, gData.nodes[clickedNodeId].group[STATE.s][0]);
                let MCP_A = STATE.PLOT.nbVisibleNodes + MCP[1].length;
                let MCP_R = STATE.PLOT.nbVisibleNodes - MCP[0].length;
                let MCP_I = MCP[0].length + MCP[1].length;

                const contextData = {
                    title: "\\\\textbf{UPDATE~NODES-VISIBILITY} \\\\newline" + "\\\\textbf{FROM:~~}  " + myLabelString(clickedNodeId),
                    actions: [
                        {
                            title: "\\\\blacksquare\\\\textbf{~ME}",
                            buttons: ["\\\\textbf{ADD}", "\\\\textbf{REM}", "\\\\textbf{ONL}"],
                            descriptions: ["|V_N|\\\\rightarrow" + ME_A, "|V_N|\\\\rightarrow" + ME_R, "|V_N|\\\\rightarrow" + ME_I]
                        },
                        {
                            title: "\\\\blacksquare\\\\textbf{~MY~NEIGHBORS~\\\\&~ME}",
                            buttons: ["\\\\textbf{ADD}", "\\\\textbf{REM}", "\\\\textbf{ONL}"],
                            descriptions: ["|V_N|\\\\rightarrow" + MYN_A, "|V_N|\\\\rightarrow" + MYN_R, "|V_N|\\\\rightarrow" + MYN_I]
                        },
                        {
                            title: "\\\\blacksquare\\\\textbf{~MY~PROXEMIE}~(TODO)",
                            buttons: ["\\\\textbf{ADD}", "\\\\textbf{REM}", "\\\\textbf{ONL}"],
                            descriptions: ["|V_N|\\\\rightarrow ", "|V_N|\\\\rightarrow ", "|V_N|\\\\rightarrow "]
                        },
                        {
                            title: "\\\\blacksquare\\\\textbf{~MY~\\\\(C_p\\\\)~Module~at~s=}" + scales[STATE.s]["s"],
                            buttons: ["\\\\textbf{ADD}", "\\\\textbf{REM}", "\\\\textbf{ONL}"],
                            descriptions: ["|V_N|\\\\rightarrow" + MCP_A, "|V_N|\\\\rightarrow" + MCP_R, "|V_N|\\\\rightarrow" + MCP_I]
                        },
                    ]
                };
                showmenuRCON(clickedNodeId, contextData);
            };

            function updateMenuAttachedObj(node) {

                const menu = document.getElementById("menuAttachedObj");

                menu.innerHTML = `<h2 id="AO_header">HOW TO SEE THE NODE: ${myLabelString(node.id)}</h2>

                                        <div class="obj-line">
                                            <label><input type="checkbox" id="AO_visible"> NODE VISIBLE</label>
                                        </div>

                                        <div class="obj-line">
                                            <label><input type="checkbox" id="AO_label"> WITH LABEL</label>
                                        </div>

                                        <div class="obj-line">
                                            <label><input type="checkbox" id="AO_biglabel"> BIG LABEL</label>
                                        </div>

                                        <hr>

                                        <button id="AO_apply">APPLY</button>
                                    `;

                // initial
                document.getElementById("AO_visible").checked = gData.nodes[node.id].prop.V;
                document.getElementById("AO_label").checked = gData.nodes[node.id].prop.L;
                document.getElementById("AO_biglabel").checked = gData.nodes[node.id].prop.BL;

                // checked
                document.getElementById("AO_apply").onclick = () => {

                    setNodVis(node.id, document.getElementById("AO_visible").checked);
                    gData.nodes[node.id].prop.L = document.getElementById("AO_label").checked;
                    gData.nodes[node.id].prop.BL = document.getElementById("AO_biglabel").checked;

                    if (!gData.nodes[node.id].prop.V) {
                        STATE.lback.push({ T: "ME", ARO: "REM", ID: node.id, s: STATE.s, a: "", b: "" });
                    }
                    RefreshGraph()
                    hideMenuAttachedObj();
                };
            }

            function showMenuAttachedObj(event, node) {
                updateMenuAttachedObj(node);
                const menu = document.getElementById("menuAttachedObj");
                const vec = new THREE.Vector3(node.x, node.y, node.z);
                vec.project(Graph.camera());
                const widthHalf = Graph.renderer().domElement.clientWidth / 2;
                const heightHalf = Graph.renderer().domElement.clientHeight / 2;
                const screenX = (vec.x * widthHalf) + widthHalf;
                const screenY = -(vec.y * heightHalf) + heightHalf;

                menu.style.left = screenX + "px";
                menu.style.top = (screenY - 150) + "px";
                menu.style.display = "block";
            }

            function hideMenuAttachedObj() {
                document.getElementById("menuAttachedObj").style.display = "none";
            }

            document.addEventListener("click", (e) => {

                const menu = document.getElementById("menuAttachedObj");
                if (
                    menu.style.display === "block"
                    && !menu.contains(e.target)
                ) {
                    hideMenuAttachedObj();
                }
            });

            (function enableAttachedObjDrag() {
                const menu = document.getElementById("menuAttachedObj");

                let dragging = false;
                let offsetX = 0;
                let offsetY = 0;

                menu.addEventListener("mousedown", (e) => {
                    if (e.target.id !== "AO_header") return;
                    dragging = true;
                    offsetX = e.clientX - menu.offsetLeft;
                    offsetY = e.clientY - menu.offsetTop;
                    e.preventDefault();
                });

                document.addEventListener("mousemove", (e) => {
                    if (!dragging) return;
                    menu.style.left = (e.clientX - offsetX) + "px";
                    menu.style.top = (e.clientY - offsetY) + "px";
                });

                document.addEventListener("mouseup", event => {
                    dragging = false;
                });

            })();

            // =============================================================================================================
            // FOCUS BUTTONS
            // FOCUS BUTTONS
            // =============================================================================================================
            const FOCUSpopup = document.querySelector('.FOCUSpopup');

            const FOCUSbtn = document.querySelector('.FOCUSopenBtn');
            const FOCUScloseBtn = document.querySelector('.FOCUScloseBtn');

            document.querySelector(".FOCUSresult").style.fontSize = "14px"
            document.querySelector(".FOCUSinput_COM").style.fontSize = "14px"

            const FOCUSresult = document.querySelector('.FOCUSresult');
            const FOCUSinput_COM = document.querySelector('.FOCUSinput_COM');

            const FOCUSinput = document.querySelector('.FOCUSinput');
            const FOCUSpopupHeader = document.querySelector('.FOCUSpopup-header');

            // Popup movement limited to the window
            let FOCUSisDragging = false;
            let FOCUSoffsetX, FOCUSoffsetY;

            FOCUSpopupHeader.addEventListener('mousedown', (e) => {
                FOCUSisDragging = true;
                FOCUSoffsetX = e.clientX - FOCUSpopup.offsetLeft;
                FOCUSoffsetY = e.clientY - FOCUSpopup.offsetTop;
                FOCUSpopupHeader.style.cursor = 'grabbing';
            });

            document.addEventListener('mouseup', event => {
                FOCUSisDragging = false;
                FOCUSpopupHeader.style.cursor = 'move';
            });

            document.addEventListener('mousemove', (e) => {
                if (FOCUSisDragging) {
                    let newLeft = e.clientX - FOCUSoffsetX;
                    let newTop = e.clientY - FOCUSoffsetY;

                    const maxLeft = window.innerWidth - FOCUSpopup.offsetWidth;
                    const maxTop = window.innerHeight - FOCUSpopup.offsetHeight;

                    if (newLeft < 0) newLeft = 0;
                    if (newTop < 0) newTop = 0;
                    if (newLeft > maxLeft) newLeft = maxLeft;
                    if (newTop > maxTop) newTop = maxTop;

                    FOCUSpopup.style.left = newLeft + 'px';
                    FOCUSpopup.style.top = newTop + 'px';
                }
            });

            // AUTO-COMPLETION FOR .FOCUSinput
            // container for suggestions
            const FOCUSsuggestions = document.querySelector(".FOCUS-suggestions");

            // All labels of nodes in the graph
            const LABELS = gData.nodes.map(n => n.name);

            // Listen to user input
            FOCUSinput.addEventListener("input", event => {

                const mode = document.querySelector('input[name="FOCUSchoix"]:checked').value;

                // Disable autocomplete if mode = ID
                if (mode === "ID") {
                    FOCUSsuggestions.style.display = "none";
                    return;
                }

                const str = FOCUSinput.value.trim();
                if (str === "") {
                    FOCUSsuggestions.style.display = "none";
                    return;
                }

                const matches = LABELS.filter(lab =>
                    lab.toLowerCase().startsWith(str.toLowerCase())
                );

                if (matches.length === 0) {
                    FOCUSsuggestions.style.display = "none";
                    return;
                }

                FOCUSsuggestions.innerHTML = "";
                matches.forEach(label => {
                    const div = document.createElement("div");
                    div.classList.add("FOCUS-suggestion-item");
                    div.textContent = label;

                    // ------------------------------
                    // When clicked: fill field ONLY
                    // ------------------------------
                    div.onclick = () => { // CLICK TO VALID THIS LABEL

                        FOCUSinput.value = label;
                        FOCUSsuggestions.style.display = "none";

                        // VALIDATION HERE
                        const X = FOCUSinputStrOK(label);
                        STATE.FOC.validNode = true;
                        STATE.FOC.id = X[1];
                        CLICK_FOCUSinputStr({ key: "Enter" })
                        // VALIDATION HERE
                    };

                    FOCUSsuggestions.appendChild(div);
                });
                FOCUSsuggestions.style.display = "block";
            });

            // Close suggestions when clicking outside
            document.addEventListener("click", (e) => {

                if (!FOCUSsuggestions.contains(e.target) &&
                    e.target !== FOCUSinput) {
                    FOCUSsuggestions.style.display = "none";
                }
            });

            // FOCUS Button: Open popup -----------------------------------------------------
            FOCUSbtn.onclick = () => {

                if (STATE.FOC.active) {
                    CLICK_FOCUScloseBtn()
                }
                else {
                    CLICK_FOCUSbtn()
                }
            };
            function CLICK_FOCUSbtn() {
                document.querySelectorAll(".FOCUStable button").forEach(b => {
                    b.classList.remove("active");
                });

                STATE.FOC = {
                    active: true,
                    btn: "",
                    id: -1,
                    idPartner: [],
                    validNode: false,
                    orbit: false
                }

                // reset
                FOCUSpopup.style.display = 'none';
                FOCUSresult.textContent = '';
                FOCUSinput.value = '';

                FOCUSinput_COM.textContent = '';

                // open
                FOCUSpopup.style.display = 'block';
                document.querySelector(".FOCUSopenBtn").style.border = "2px solid white";
            };

            // FOCUS Button: Close popup ------------------------------------------------------
            FOCUScloseBtn.onclick = () => {

                CLICK_FOCUScloseBtn()
            };
            function CLICK_FOCUScloseBtn() {
                document.querySelectorAll(".FOCUStable button").forEach(b => {
                    b.classList.remove("active");
                });

                STATE.FOC = {
                    active: false,
                    btn: "",
                    id: -1,
                    idPartner: [],
                    validNode: false,
                    orbit: false
                }
                FOCUSpopup.style.display = 'none';
                FOCUSresult.textContent = '';
                FOCUSinput.value = '';
                FOCUSinput_COM.textContent = '';
                document.querySelector(".FOCUSopenBtn").style.border = "transparent";

                Graph.cameraPosition(
                    STATE.R.CamPos0,
                    STATE.R.LKA0,
                    2000
                );
            }

            // FOCUS Button: .FOCUSinput ----------------------------------------------
            const FOCUSinputStr = document.querySelector(".FOCUSinput");

            FOCUSinputStr.addEventListener("keydown", (e) => {

                CLICK_FOCUSinputStr(e);
            });
            function CLICK_FOCUSinputStr(e) {
                if (e.key === "Enter") {
                    const RadioID_LAB = document.querySelector('input[name="FOCUSchoix"]:checked').value;
                    const str = FOCUSinputStr.value.trim();
                    if (str == "") {
                        FOCUSinput_COM.textContent = 'Please enter a node reference.';
                        UPDATE_FOCUSresult(-1)
                    }
                    else {
                        const X = FOCUSinputStrOK(str);
                        if (X[0]) {
                            STATE.FOC.validNode = true;
                            STATE.FOC.id = X[1];
                            FOCUSinput_COM.textContent = X[2];
                            n = gData.nodes[X[1]]
                            if (getNodVis(X[1])) {
                                // setNodVis(X[1], true);
                                FOCUS_cross = zoom_on_xyz(n.x, n.y, n.z, 100, 1000)
                            }
                            UPDATE_FOCUSresult(X[1])
                        }
                        else {
                            STATE.FOC.btn = ""
                            STATE.FOC.validNode = false;
                            STATE.FOC.id = -1;
                            FOCUSinput_COM.textContent = X[2];
                            UPDATE_FOCUSresult(-1)
                        }
                    }
                }
                FOCUSsuggestions.style.display = "none";
            }

            //===================================================================================================
            function FOCUSinputStrOK(str) {
                const RadioID_LAB = document.querySelector('input[name="FOCUSchoix"]:checked').value;
                if (RadioID_LAB == "ID") {
                    myid = parseInt(str);
                    if ((isNaN(myid)) || (myid < 0) || (myid > gData.nodes.length - 1)) {
                        //UPDATE_FOCUSresult(-1)
                        return [false, -1, "ID missing"];
                    }
                    else {
                        //UPDATE_FOCUSresult(myid)
                        if (getNodVis(myid)) {
                            return [true, myid, myLabelString(myid) + " Visible"];
                        }
                        else {
                            return [true, myid, myLabelString(myid) + " INvisible"];
                        }
                    }
                }
                else {
                    let candidat = []
                    let candidatSTR = "";
                    for (let i = 0; i < gData.nodes.length; i++) {
                        if (gData.nodes[i].name == str) {
                            candidat.push(i);
                            candidatSTR = candidatSTR + i + (getNodVis(i) ? ":visible, " : ":INvisible, ");
                        }
                    }
                    if (candidat.length == 0) {
                        //UPDATE_FOCUSresult(-1)
                        return [false, -1, "LABEL missing"];
                    }
                    else {
                        if (candidat.length > 1) {
                            return [false, -1, "IDs of nodes with this LABEL: " + candidatSTR];
                        }
                        else {
                            myid = candidat[0];
                            //UPDATE_FOCUSresult(myid)
                            if (getNodVis(myid)) {
                                return [true, myid, myLabelString(myid)];
                            }
                            else {
                                return [true, myid, myLabelString(myid)];
                            }
                        }
                    }
                }
            }

            // FOCUS Button:  B.i.j buttons -------------------------------------------------------------------
            const FOCUSbuttons = FOCUSpopup.querySelectorAll('.FOCUSbuttonFree');
            FOCUSbuttons.forEach(btn => {
                btn.addEventListener('click', function () {

                    CLICK_FOCUSbuttons_btn(this);
                });
            });
            function CLICK_FOCUSbuttons_btn(me) {
                if (!STATE.FOC.validNode) {
                    FOCUSinput_COM.textContent = 'invalid reference';
                    STATE.FOC = {
                        active: true,
                        btn: "",
                        id: -1,
                        idPartner: [],
                        validNode: false,
                        orbit: false
                    };
                    UPDATE_FOCUSresult(-1)
                }
                else {
                    myid = STATE.FOC.id;
                    let TABi = parseInt(me.dataset.i);
                    let TABj = parseInt(me.dataset.j);
                    let CHOIX = TABi + "-" + TABj

                    document.querySelectorAll(".FOCUStable button").forEach(b => {
                        if (b == me) {
                            b.classList.add("active");
                        }
                        else {
                            b.classList.remove("active");
                        }
                    });
                    STATE.FOC.btn = CHOIX;
                    UPDATE_FOCUSresult(myid)
                }
            };

            // FOCUS Button: GO -------------------------------------------------------------------
            const FOCUS_GO = document.querySelector('.FOCUS_GO');
            FOCUS_GO.onclick = () => {
                CLICK_FOCUS_GO()
            };
            function CLICK_FOCUS_GO() {
                if (!STATE.FOC.validNode) {
                    FOCUSinput_COM.textContent = 'invalid reference';
                    UPDATE_FOCUSresult(-1)
                }
                else {
                    myid = STATE.FOC.id;
                    gData.nodes[myid].prop.L = true;
                    setNodVis(myid, true);
                    RefreshGraph()
                    FOCUS_cross = zoom_on_xyz(gData.nodes[myid].x, gData.nodes[myid].y, gData.nodes[myid].z, 100, 1000);
                }
            };

            function UPDATE_FOCUSresult(myid) { // todo mettre à sa place
                if (myid == -1) {
                    document.querySelector(".FOCUSresult").innerHTML = "";
                    document.querySelectorAll(".FOCUStable button").forEach(b => {
                        b.classList.remove("active");
                    });
                }
                switch (STATE.FOC.btn) {
                    case "": // Neighboors on the selected node
                        document.querySelector(".FOCUSresult").innerHTML = "";
                        document.querySelectorAll(".FOCUStable button").forEach(b => {
                            b.classList.remove("active");
                        });
                        break;

                    case "0-0": // Neighboors on the selected node
                        document.querySelector(".FOCUSresult").innerHTML = myLNeigS(myid);
                        break;

                    case "0-1": // Cp module on the selected node at selected description scale
                        document.querySelector(".FOCUSresult").innerHTML = MyCpModString(myid);
                        break;
                }
            }

            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            // FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            function PLOT_Vastur() {

                if (STATE.PLOT.aware) {
                    freezeAfterSimulation = true;

                    Graph.graphData().nodes.forEach(n => {
                        n.fx = undefined;
                        n.fy = undefined;
                        n.fz = undefined;
                    });
                    // Force of attraction cluster-aware

                    const linkForce = Graph.d3Force('link');
                    linkForce
                        .strength(link => {
                            const ns = link.source;
                            const nt = link.target;
                            const group1 = ns.group[STATE.s][0];
                            const group2 = nt.group[STATE.s][0];
                            if (group1 === group2) {
                                return link.value * 1.0; // same cluster => strong attraction
                            }
                            return link.value * (0.5 ** coef_weak_strength) // weak attraction otherwise
                        });
                    Graph.d3ReheatSimulation();
                }
                else {
                    freezeAfterSimulation = true;

                    Graph.graphData().nodes.forEach(n => {
                        n.x = n.g0x;
                        n.y = n.g0y;
                        n.z = n.g0z;

                        n.fx = n.g0x;
                        n.fy = n.g0y;
                        n.fz = n.g0z;
                    });
                    Graph.d3ReheatSimulation();
                }

                document.querySelector("#NamePedig").innerHTML = myTitle + " (Visible Nodes: \\\\(|V_N|\\\\)=" + STATE.PLOT.nbVisibleNodes + ")";
                renderMathInElement(document.querySelector("#NamePedig"));
                document.getElementById('loading').style.display = 'none';
                RefreshGraph()
            };

            function PLOT_Vastur_Geometry_Unaware() {
                // =========================================================================
                epsilon = 1, stableTicks = 5;
                let stableCount = 0;
                let prev = [];

                let NodeVis = [];
                for (let i = 0; i < gData.nodes.length; i++) {
                    if (getNodVis(i)) {
                        NodeVis.push(i);
                    }
                }
                for (let i = 0; i < NodeVis.length; i++) {
                    prev.push([gData.nodes[NodeVis[i]].x, gData.nodes[NodeVis[i]].y, gData.nodes[NodeVis[i]].z])
                }
                let COUNTER = 0;

                function loop() {
                    const working = document.getElementById("loading");

                    if (working) {
                        working.style.display = "block";

                        working.innerHTML =
                            "Computing the 3D Graph Geometry<br>"
                            + "<b>Unawaring the description scales</b>"
                            + "<br>ITERATION: " + COUNTER;
                    }

                    let maxDisp = 0;
                    let px = 0, py = 0, pz = 0;
                    for (let i = 0; i < NodeVis.length; i++) {
                        n = gData.nodes[NodeVis[i]]
                        px = prev[i][0]; py = prev[i][1]; pz = prev[i][2];

                        const dx = n.x - px;
                        const dy = n.y - py;
                        const dz = n.z - pz;
                        const disp = Math.sqrt(dx * dx + dy * dy + dz * dz);

                        if (disp > maxDisp) maxDisp = disp;

                        prev[i] = [n.x, n.y, n.z]
                    }

                    if (maxDisp < epsilon) {
                        stableCount++
                    }
                    else {
                        stableCount = 0
                        COUNTER = COUNTER + 1
                        /*
                        working.innerHTML = "«Propaganda is to a democracy what the bludgeon is to a totalitarian state.» <br>"+
                        "Noam Chomsky (2002), in «Media Control: The Spectacular Achievements of Propaganda»<br><br>"+
                        */
                    };

                    if (stableCount >= stableTicks) {
                        Graph.graphData().nodes.forEach(n => {
                            n.fx = n.x;
                            n.fy = n.y;
                            n.fz = n.z;
                            // Geometry cluster-unaware
                            n.g0x = n.x;
                            n.g0y = n.y;
                            n.g0z = n.z;
                        });

                        document.querySelector("#NamePedig").innerHTML = myTitle + " (Visible Nodes: \\\\(|V_N|\\\\)=" + STATE.PLOT.nbVisibleNodes + ")";
                        renderMathInElement(document.querySelector("#NamePedig"));
                        document.getElementById('loading').style.display = 'none';
                        return;
                    }
                    requestAnimationFrame(loop);
                }
                loop();
                // =========================================================================
            };

            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*COLORS FUNCTIONS*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            //===================================================================================================
            function myColorNode(id) {
                let group = gData.nodes[id].group[STATE.s];
                if (ScaleFrozenColor > -1) {
                    group = gData.nodes[id].group[ScaleFrozenColor]
                }
                if (STATE.p) { return myColorNodeP(group); }
                else { return myColorNodeO(group); }
                return true;
            };

            //===================================================================================================
            function myColorNodeP(group) {
                const coef = 3;
                const color = colorRGB[group[0] % LCH]
                return "rgba(" + color[0] / coef + "," + color[1] / coef + "," + color[2] / coef + "," + 0.95 + ")";
            };

            //===================================================================================================
            function myColorNodeO(group) {
                const coef = 3;
                l = group.length;
                let r = 0, g = 0, b = 0;
                for (let i = 0; i < l; i++) {
                    let [ri, gi, bi] = colorRGB[group[i] % LCH];
                    r += ri; g += gi; b += bi;
                }
                r = Math.round(r / l); g = Math.round(g / l); b = Math.round(b / l);
                return "rgba(" + r / coef + "," + g / coef + "," + b / coef + "," + 0.95 + ")";
            };


            //===================================================================================================
            function myColorLink(link) {
                let c1 = myColorNode(link.source.id);
                let c2 = myColorNode(link.target.id);
                return averageColor(c1, c2);
            };

            // ============================================================================================
            function hexToRgb(hex) {
                const res = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(hex);
                return res ? [
                    parseInt(res[1], 16),
                    parseInt(res[2], 16),
                    parseInt(res[3], 16)
                ] : [0, 0, 0];
            };

            //===================================================================================================
            function rgbToHex(r, g, b) {
                const toHex = x => x.toString(16).padStart(2, "0");
                return "#" + toHex(r) + toHex(g) + toHex(b);
            };

            //===================================================================================================
            function averageColor(x, y) {
                let rx, vx, bx, tx; let ry, vy, by, ty;
                const regex_x = /rgba\\(\\x*([\\d.]+)\\x*,\\x*([\\d.]+)\\x*,\\x*([\\d.]+)\\x*,\\x*([\\d.]+)\\x*\\)/;
                const match_x = x.match(regex_x);
                if (match_x) {
                    rx = parseFloat(match_x[1]);
                    vx = parseFloat(match_x[2]);
                    bx = parseFloat(match_x[3]);
                    tx = parseFloat(match_x[4]);
                }
                else {
                    rx = 0;
                    vx = 0;
                    bx = 0;
                    tx = 0;
                }

                const regex_y = /rgba\\(\\y*([\\d.]+)\\y*,\\y*([\\d.]+)\\y*,\\y*([\\d.]+)\\y*,\\y*([\\d.]+)\\y*\\)/;
                const match_y = y.match(regex_y);
                if (match_y) {
                    ry = parseFloat(match_y[1]);
                    vy = parseFloat(match_y[2]);
                    by = parseFloat(match_y[3]);
                    ty = parseFloat(match_y[4]);
                }
                else {
                    ry = 0;
                    vy = 0;
                    by = 0;
                    ty = 0;
                }

                const r = Math.round((rx + ry) / 2);
                const v = Math.round((vx + vy) / 2);
                const b = Math.round((bx + by) / 2);
                const t = Math.round((tx + ty) / 2);
                return "rgba(" + r + "," + v + "," + b + "," + t + ")";
            };

            //===================================================================================================
            function nbVisibleNodes() {
                let NBV = 0;
                for (let i = 0; i < gData.nodes.length; i++) {
                    if (getNodVis(i)) {
                        NBV = NBV + 1;
                    }
                }
                return NBV
            }

            //===================================================================================================
            function getNodVis(id) {
                return gData.nodes[id].prop.V;
            }

            function setNodVis(id, x) {
                if (!(gData.nodes[id].prop.V == x)) {
                    gData.nodes[id].prop.V = x;
                    if (x) {
                        STATE.PLOT.nbVisibleNodes = STATE.PLOT.nbVisibleNodes + 1
                    }
                    else {
                        STATE.PLOT.nbVisibleNodes = STATE.PLOT.nbVisibleNodes - 1
                    }
                    RefreshGraph();
                    document.querySelector("#NamePedig").innerHTML = myTitle + " (Visible Nodes: \\\\(|V_N|\\\\)=" + STATE.PLOT.nbVisibleNodes + ")";
                }
            }

            function getNodLabVis(id) {
                return gData.nodes[id].prop.L;
            }

            function setNodLabVis(id, x) {
                gData.nodes[id].prop.L = x;
            }

            function getNodLabBIG(id) {
                return gData.nodes[id].prop.BL;
            }

            function setNodLabBIG(id, x) {
                gData.nodes[id].prop.BL = x;
            }

            function zoom_on_xyz(x, y, z, distance, ms) {
                if (FOCUS_cross) {
                    scene.remove(FOCUS_cross)
                }
                STATE.R.active = false;
                STATE.R.LKA.x = x
                STATE.R.LKA.y = y
                STATE.R.LKA.z = z
                rotationControl.style.border = "transparent";
                const distRatio = 1 + distance / Math.hypot(x, y, z);
                const newPos = x || y || z
                    ? { x: x * distRatio, y: y * distRatio, z: z * distRatio }
                    : { x: 0, y: 0, z: distance }; // special case if (0,0,0)
                Graph.cameraPosition(
                    newPos, // new position
                    { x: x, y: y, z: z }, // lookAt ({ x, y, z })
                    ms  // ms transition duration
                );
                return cross_forward(x, y, z)
            };


            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            // COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR COLOR 
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            //===================================================================================================
            function updateHighlight() {
                // trigger update of highlighted objects in scene
                Graph
                    .nodeColor(Graph.nodeColor())
                    .linkWidth(Graph.linkWidth())
                    .linkDirectionalParticles(Graph.linkDirectionalParticles());
            };


            //===================================================================================================
            // To export
            function updateGraphHeight() {
                const headerHeight =
                    document.querySelector("h1").offsetHeight +
                    document.getElementById("scoreP").offsetHeight +
                    document.getElementById("scoreO").offsetHeight;

                document.documentElement.style.setProperty("--header-height", headerHeight + "px");

                //===================================================================================================
                // Force Three.js to resize properly
                const graph = document.getElementById("Graph3D");
                if (graph && graph.__forceResize) {
                    graph.__forceResize();
                }
            };

            function UPDATE_s_p(BY) {
                // updating scores
                scoreDisplayP.textContent = scales[STATE.s]["scoreP"];
                scoreDisplayO.textContent = scales[STATE.s]["scoreO"];

                // scale
                if (BY == "s") {
                    document.querySelectorAll(".scale-button").forEach(btn => btn.classList.remove("active"));
                    document.querySelectorAll(".scale-button").forEach(btn => {
                        if (btn.textContent == scales[STATE.s]["s"]) {
                            btn.classList.add("active");
                        }
                    });
                    AnimateScore("s");
                }
                else {
                    if (STATE.p) { // Cp (clustering by partition)
                        scoreP_Btn.classList.add("active");
                        scoreO_Btn.classList.remove("active");
                    }
                    else {  // Co (overlaping clustering)
                        scoreO_Btn.classList.add("active");
                        scoreP_Btn.classList.remove("active");
                    }
                    AnimateScore("p");
                }
            };

            function UPDATE_Color() {
                // Graph
                gData.nodes.forEach(n => delete n.color);
                Graph.nodeColor(node => myColorNode(node.id));
                setTimeout(() => {
                    Graph.linkColor(link => myColorLink(link));
                }, 500);
            };


            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*SETS OF NODES FUNCTIONS*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            //===================================================================================================
            function myNeig_V_UNV(id) {
                const x = [[], []];
                for (let i = 0; i < gData.nodes[id].neighbors.length; i++) {
                    if (getNodVis(gData.nodes[id].neighbors[i])) {
                        x[0].push(gData.nodes[id].neighbors[i]);
                    }
                    else {
                        x[1].push(gData.nodes[id].neighbors[i]);
                    }
                }
                return x
            };

            //===================================================================================================
            function myCpModuleNode_V_UNV(id, x) {
                let mod = [[], []];
                for (let i = 0; i < gData.nodes.length; i++) {
                    if (gData.nodes[i].group[STATE.s][0] == x) {
                        if (getNodVis(i)) {
                            mod[0].push(i);
                        }
                        else {
                            mod[1].push(i);
                        }
                    }
                }
                return mod;
            };
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/
            /*STRING FUNCTIONS*/
            /*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*/

            //===================================================================================================
            function myLNeigS(id) {
                return "<b>" + myLabelStringATSCALE(id) + "</b>" + "<br>" + myNeighborsString(id);
            };
            //===================================================================================================
            function myLabelString(id) { return gData.nodes[id].id + ":" + gData.nodes[id].name }

            //===================================================================================================
            function myNeighborsString(id) {
                const neighbors = myNeig_V_UNV(id)
                const TOTneigh = neighbors[0].length + neighbors[1].length
                let TOTneighStr = ((TOTneigh) <= 1) ? " NEIGHBOR" : " NEIGHBORS";
                TOTneighStr = "<br><b>" + TOTneigh + TOTneighStr + "</b><br><br>"

                let VneighborsString = "["
                    + neighbors[0].map(id => "(" + gData.nodes[id].id + ":" + gData.nodes[id].name + ")").join(', ')
                    + "]";

                if ((neighbors[0].length) > 0) {
                    VneighborsString = "<br>" + VneighborsString
                }

                let UNVneighborsString = "["
                    + neighbors[1].map(id => gData.nodes[id].id + ": " + gData.nodes[id].name).join(', ')
                    + "]";
                if ((neighbors[1].length) > 0) {
                    UNVneighborsString = "<br>" + UNVneighborsString
                }

                let Vn = " Visible: "
                let UNVn = " UNvisible: "

                return TOTneighStr + "<b>" + neighbors[0].length + Vn + "</b>" + VneighborsString +
                    "<br><br>" + "<b>" + neighbors[1].length + UNVn + "</b>" + UNVneighborsString;
            }

            //===================================================================================================
            function MyCpModString(myid) {
                Dmod = myCpModuleNode_V_UNV(myid, gData.nodes[myid].group[STATE.s][0]);
                // str
                L0L1 = Dmod[0].length + Dmod[1].length
                str_mod = "<br><br>" + L0L1 + " NODES in Cp mod. " + gData.nodes[myid].group[STATE.s][0] + "<br>";

                // VISIBLE NODES
                if (Dmod[0].length > 0) {
                    str_mod = str_mod + "<br>" + Dmod[0].length + " Visible: <br>";
                    str_mod = str_mod + "[";
                    for (let i = 0; i < Dmod[0].length - 1; i++) {
                        str_mod = str_mod + "(" + gData.nodes[Dmod[0][i]].id + ':' + gData.nodes[Dmod[0][i]].name + '), '
                    }
                    str_mod = str_mod + "(" + gData.nodes[Dmod[0][Dmod[0].length - 1]].id + ': ' + gData.nodes[Dmod[0][Dmod[0].length - 1]].name + ')]'
                }
                else {
                    str_mod = str_mod + "<br>" + Dmod[0].length + " Visible: []";
                }

                // INVISIBLE NODES
                if (Dmod[1].length > 0) {
                    str_mod = str_mod + "<br><br>" + Dmod[1].length + " UNvisible:<br>";
                    str_mod = str_mod + "[";
                    for (let i = 0; i < Dmod[1].length - 1; i++) {
                        str_mod = str_mod + "(" + gData.nodes[Dmod[1][i]].id + ': ' + gData.nodes[Dmod[1][i]].name + '), '
                    }
                    str_mod = str_mod + "(" + gData.nodes[Dmod[1][Dmod[1].length - 1]].id + ': ' + gData.nodes[Dmod[1][Dmod[1].length - 1]].name + ')]'
                }
                else {
                    str_mod = str_mod + "<br><br>" + Dmod[1].length + " UNvisible: []<br>";
                }

                // NODE ID + NODE LABEL
                str1 = myLabelStringATSCALE(myid)

                str1 = str1 + str_mod
                return str1;
            }

            function myLabelStringATSCALE(myid) {
                str = "<b>" + myLabelString(myid) + "</b>" + "<br>"
                    + "[Cp: " + gData.nodes[myid].group[STATE.s][0] + "]"
                    + " [Co: " + gData.nodes[myid].group[STATE.s].join(", ")
                    + "]"
                    + " at scale " + scales[STATE.s]["s"]
                return str
            }



            //===================================================================================================
            function AnimateScore(BY) {
                scoreDisplayP.textContent = scales[STATE.s]["scoreP"]
                scoreDisplayO.textContent = scales[STATE.s]["scoreO"]
                if (BY == "s") { // score button
                    // We remove all animation classes before restarting
                    scoreDisplayP.classList.remove("updated", "glow");
                    scoreDisplayO.classList.remove("updated", "glow");

                    // gentle animation
                    scoreDisplayP.classList.add("updated", "glow");
                    scoreDisplayO.classList.add("updated", "glow");
                    setTimeout(() => {
                        scoreDisplayP.classList.remove("updated", "glow");
                        scoreDisplayO.classList.remove("updated", "glow");
                    }, 600);
                }
                else {
                    // We remove all animation classes before restarting
                    scoreDisplayP.classList.remove("updated", "burst");
                    scoreDisplayO.classList.remove("updated", "burst");

                    if (STATE.p) { // Cp (partition)
                        scoreDisplayP.style.backgroundColor = "#050505";
                        scoreDisplayO.style.backgroundColor = "#757575";
                    } else { // Co (with overlaos)
                        scoreDisplayO.style.backgroundColor = "#050505";
                        scoreDisplayP.style.backgroundColor = "#757575";
                    }

                    // More vibrant animation 
                    scoreDisplayP.classList.add("updated", "burst");
                    scoreDisplayO.classList.add("updated", "burst");
                    setTimeout(() => {
                        scoreDisplayP.classList.remove("updated", "burst");
                        scoreDisplayO.classList.remove("updated", "burst");
                    }, 600);
                }
            };

            // =============================================================================================================
            // =============================================================================================================
            // CONTEXTUAL MENU BUTTONS ON NODE
            // =============================================================================================================
            // =============================================================================================================

            // Click outside the menu → close it
            document.addEventListener("click", (e) => {

                if (!menu.contains(e.target)) {
                    menu.style.display = "none";
                }
                if (!isDraggingMenu && !menuLDCON.contains(e.target)) menuLDCON.style.display = "none";
            });

            /* // Click outside menu → close
            document.addEventListener("click", (e) => {
 
                if (!isDraggingMenu && !menuLDCON.contains(e.target)) hidemenuLDCON();
            });
            */

            function updatemenuRCON(context) {
                const menu = document.getElementById("menuRCON");
                menu.innerHTML = "";  // reset contenu précédent

                // ---- GENERAL TITLE ----
                const h2 = document.createElement("h2");
                h2.innerHTML = katex.renderToString(context.title, { throwOnError: false });
                menu.appendChild(h2);

                // ---- ACTIONS ----
                context.actions.forEach((action, i) => {
                    const block = document.createElement("div");
                    block.className = "action-blocRCONk";

                    // Title of the action
                    const h3 = document.createElement("h3");
                    h3.innerHTML = katex.renderToString(action.title, { throwOnError: false });
                    block.appendChild(h3);

                    // Buttons and descriptions aligned in row
                    const btnDescRow = document.createElement("div");
                    btnDescRow.className = "btn-desc-rowRCON";

                    for (let j = 0; j < action.buttons.length; j++) {
                        const container = document.createElement("div");
                        container.className = "btn-desc-itemRCON";

                        const btn = document.createElement("div");
                        btn.className = "ctx-btnRCON";
                        btn.innerHTML = katex.renderToString(action.buttons[j], { throwOnError: false });
                        btn.onclick = () => {

                            let T = "";
                            switch (i) {
                                case 0:
                                    T = "ME";
                                    break;
                                case 1:
                                    T = "NEIG";
                                    break;
                                case 2:
                                    T = "PROX";
                                    break;
                                case 3:
                                    T = "MOD";
                                    break;
                            }

                            let ARO = "";
                            switch (j) {
                                case 0:
                                    ARO = "ADD";
                                    break;
                                case 1:
                                    ARO = "REM";
                                    break;
                                case 2:
                                    ARO = "ONL";
                                    break;
                            }

                            if (!(T == "PROX")) { // TODO
                                let D = { T: T, ARO: ARO, ID: clickedNodeId, s: STATE.s, a: "", b: "" }
                                let Builded = BuildSelection(D)
                                if (Builded[0] === "") {
                                    STATE.lback.push(D);
                                    Upate_ARO_selection_visible(ARO, Builded[1]);
                                    PLOT_Vastur();
                                    //hidemenuRCON();
                                }
                                else {
                                    // console.error
                                };
                            }
                        };

                        const desc = document.createElement("div");
                        desc.className = "desc-textRCON";
                        desc.innerHTML = katex.renderToString(action.descriptions[j], { throwOnError: false });

                        container.appendChild(btn);
                        container.appendChild(desc);

                        btnDescRow.appendChild(container);
                    }

                    block.appendChild(btnDescRow);
                    menu.appendChild(block);
                });
            }

            // =========================================================
            //  Opening management and positioning
            // =========================================================

            const menu = document.getElementById("menuRCON");

            (function enableMenuDrag() {
                const menu = document.getElementById("menuRCON");
                let offsetX = 0, offsetY = 0;
                let isDragging = false;

                menu.addEventListener("mousedown", (e) => {
                    isDragging = true;

                    // Offset between the mouse and the top left corner of the menu
                    offsetX = e.clientX - menu.offsetLeft;
                    offsetY = e.clientY - menu.offsetTop;

                    // Prevents text selection during dragging
                    e.preventDefault();
                });

                document.addEventListener("mousemove", (e) => {
                    if (!isDragging) return;

                    // Moving the menu
                    menu.style.left = (e.clientX - offsetX) + "px";
                    menu.style.top = (e.clientY - offsetY) + "px";
                });

                document.addEventListener("mouseup", event => {
                    isDragging = false;
                });
            })();

            function showmenuRCON(clickedNodeId, contextData) {
                updatemenuRCON(contextData);

                node = gData.nodes[clickedNodeId]
                // Position: top right corner of the menu at the click point / node
                const vec = new THREE.Vector3(node.x, node.y, node.z);
                vec.project(Graph.camera());

                const widthHalf = Graph.renderer().domElement.clientWidth / 2;
                const heightHalf = Graph.renderer().domElement.clientHeight / 2;

                const screenX = (vec.x * widthHalf) + widthHalf;
                const screenY = -(vec.y * heightHalf) + heightHalf;

                menuRCON.style.left = (screenX) + "px";
                menuRCON.style.top = (screenY - 300) + "px";

                menuRCON.style.display = "block";
            }



            // =============================================================================================================
            // =============================================================================================================
            //  MENU — BACKGROUND CONTEXTUAL MENU
            // =============================================================================================================
            // =============================================================================================================

            function BuildSelection(D) {
                // {T:T, ARO:ARO, ID:clickedNodeId, s:STATE.s, a:"", b:""}
                const T = D.T; // "ME", "NEIG", "PROX", "MOD", "DEG", "LAB"
                const ARO = D.ARO; // "ADD", "REM", "ONL"
                const ID = D.ID; // ID is the id node
                const s = D.s; // WHEN T="MOD" --> s is the index of scale description 
                const a = D.a; // WHEN T="DEG" --> a is the STRmin_deg, WHEN T="LAB" --> a is the STRregex
                const b = D.b; // WHEN T="DEG" --> a is the STRmax_deg

                let selection = []
                switch (T) {
                    case "ME": // Me
                        selection.push(ID);
                        return ["", selection]
                        break;

                    case "NEIG": // My neighbors & Me
                        const myN = myNeig_V_UNV(ID);
                        selection = [].concat(myN[0], myN[1]); // My neighbors
                        selection.push(ID); // Me
                        return ["", selection]
                        break;

                    case "PROX": // My proxemie
                        //TODO
                        break;

                    case "MOD": // My CURRENTLY selected Cp Module
                        const myCpM = myCpModuleNode_V_UNV(ID, gData.nodes[ID].group[s][0]);
                        selection = [].concat(myCpM[0], myCpM[1]);
                        return ["", selection]
                        break;

                    case "DEG": // degrees
                        const min = parseInt(a); const max = parseInt(b);
                        for (let i = 0; i < gData.nodes.length; i++) {
                            if ((min <= gData.nodes[i].neighbors.length) && (gData.nodes[i].neighbors.length <= max)) {
                                selection.push(i);
                            }
                        }
                        return ["", selection]
                        break;

                    case "LAB": // labels

                        try {
                            const regex = new RegExp(a, "u");

                            for (let i = 0; i < gData.nodes.length; i++) {
                                if (regex.test(gData.nodes[i].name)) {
                                    selection.push(i);
                                }
                            }
                            return ["", selection]

                        } catch (e) {
                            return [e.message, selection]
                        }
                        break;

                    case "CpMODofNodeVis": // les modules
                        selection = []
                        for (let i = 0; i < gData.nodes.length; i++) {
                            if (getNodVis(i)) {
                                const myCpM = myCpModuleNode_V_UNV(i, gData.nodes[i].group[s][0]);
                                selection = selection.concat(myCpM[0], myCpM[1]);
                            }
                        }
                        selection = [...new Set(selection)]
                        break;
                }
                return ["", selection]
            }

            function Upate_ARO_selection_visible(ARO, selection) {
                switch (ARO) {
                    case "ADD": // ADD"
                        for (let i = 0; i < selection.length; i++) {
                            setNodVis(selection[i], true);
                        }
                        break;

                    case "REM": // "REMove"
                        for (let i = 0; i < selection.length; i++) {
                            setNodVis(selection[i], false);
                        }
                        break;

                    case "ONL": // "ONLy"
                        let selectedVisible = [];
                        for (let i = 0; i < selection.length; i++) {
                            let x = selection[i]
                            if (getNodVis(x)) {
                                selectedVisible.push(x);
                            }
                        }

                        for (let i = 0; i < gData.nodes.length; i++) { gData.nodes[i].prop.V = false; }
                        STATE.PLOT.nbVisibleNodes = 0;

                        for (let i = 0; i < selectedVisible.length; i++) {
                            setNodVis(selection[i], true);
                        }
                        break;
                }
            }

            function updatemenuLDCON(context) {
                const menuLDCON = document.getElementById("menuLDCON");
                menuLDCON.innerHTML = ""; // reset content

                // ---- GENERAL TITLE ----
                const h2 = document.createElement("h2");
                h2.innerHTML = katex.renderToString(context.title, { throwOnError: false });
                menuLDCON.appendChild(h2);

                const backBtn = document.createElement("button");

                let nbBACK = STATE.lback.length - 1;
                backBtn.innerHTML = katex.renderToString("\\\\leftarrow~\\\\text{BACK}", { throwOnError: false }) + " [" + nbBACK + "]";
                backBtn.style.display = "block";
                backBtn.style.margin = "10px 0";
                backBtn.style.cursor = "pointer";
                backBtn.style.padding = "6px 12px";
                backBtn.style.background = "#757575";
                backBtn.style.color = "white";
                backBtn.style.border = "none";
                backBtn.style.fontWeight = "bold";
                backBtn.style.margin = "10px auto";
                backBtn.onmouseenter = () => backBtn.style.background = "#4F4F4F";
                backBtn.onmouseleave = () => backBtn.style.background = "#757575";

                backBtn.addEventListener("click", event => {

                    if (STATE.lback.length > 1) {
                        MakeOneBack();
                        PLOT_Vastur();
                        let nbBACK = STATE.lback.length - 1;
                        backBtn.innerHTML = katex.renderToString("\\\\leftarrow~\\\\text{BACK}", { throwOnError: false }) + " [" + nbBACK + "]";
                    }
                });
                menuLDCON.appendChild(backBtn);

                // === ACTIONS ===
                context.ACTIONSonBackgroundRightClick.forEach((action) => {
                    const block = document.createElement("div");
                    block.style.margin = "12px 0";

                    // ===== TITLE =====
                    const title = document.createElement("div");
                    title.innerHTML = katex.renderToString(action.title, { throwOnError: false });
                    title.style.fontWeight = "bold";
                    title.style.marginBottom = "6px";
                    block.appendChild(title);

                    // =========================================
                    //  DEGREES BETWEEN
                    // =========================================
                    if (action.id === "degrees") {

                        // --- line : min < deg < max ---
                        const row = document.createElement("div");
                        row.style.display = "flex";
                        row.style.alignItems = "center";
                        row.style.gap = "10px";

                        const inpD1 = document.createElement("input");
                        inpD1.type = "number";
                        inpD1.id = "degMinInput";
                        inpD1.style.width = "60px";
                        inpD1.addEventListener("mousedown", ev => ev.stopPropagation());

                        const midD = document.createElement("span");
                        midD.innerHTML = katex.renderToString("\\\\;\\\\leqslant\\\\;deg\\\\;\\\\leqslant\\\\;", { throwOnError: false });

                        const inpD2 = document.createElement("input");
                        inpD2.type = "number";
                        inpD2.id = "degMaxInput";
                        inpD2.style.width = "60px";
                        inpD2.addEventListener("mousedown", ev => ev.stopPropagation());

                        row.appendChild(inpD1);
                        row.appendChild(midD);
                        row.appendChild(inpD2);
                        block.appendChild(row);

                        // --- Line butons ADD / REM / ONL ---
                        const btnRow = document.createElement("div");
                        btnRow.style.display = "flex";
                        btnRow.style.gap = "10px";
                        btnRow.style.marginTop = "6px";

                        ["ADD", "REM", "ONL"].forEach(mode => {
                            const b = document.createElement("button");
                            b.style.border = "none";
                            b.style.background = "#757575";
                            b.style.color = "white";
                            b.style.fontWeight = "bold";
                            b.style.background = "#757575"; // normal
                            b.style.cursor = "pointer";
                            b.onmouseenter = () => { b.style.background = "#4F4F4F"; };// hover
                            b.onmouseleave = () => { b.style.background = "#757575"; }; // back

                            b.innerHTML = mode;
                            b.onclick = () => {

                                let min = document.getElementById("degMinInput").value;
                                let max = document.getElementById("degMaxInput").value;
                                if (min == "") { min = 0; }
                                if (max == "") { max = gData.nodes.length; }

                                let D = { T: "DEG", ARO: mode, ID: "", s: "", a: "" + min, b: "" + max };
                                let Builded = BuildSelection(D)
                                if (Builded[0] === "") {
                                    STATE.lback.push(D);
                                    Upate_ARO_selection_visible(mode, Builded[1]);
                                    PLOT_Vastur()
                                    hidemenuLDCON();
                                }
                                else {
                                    // console.error
                                };
                            };
                            btnRow.appendChild(b);
                        });

                        block.appendChild(btnRow);
                        menuLDCON.appendChild(block);
                        return;
                    }

                    // =========================================
                    //  LABELS CONTAINING
                    // =========================================
                    if (action.id === "regexLabel") {

                        const row = document.createElement("div");
                        row.style.display = "flex";
                        row.style.alignItems = "center";
                        row.style.gap = "10px";

                        const midL1 = document.createElement("span");
                        midL1.innerHTML = katex.renderToString("lab.match(", { throwOnError: false });

                        const inpL = document.createElement("input");
                        inpL.type = "text";
                        inpL.id = "regex";
                        inpL.style.width = "220px";
                        inpL.addEventListener("mousedown", ev => ev.stopPropagation());

                        const midL2 = document.createElement("span");
                        midL2.innerHTML = katex.renderToString(")", { throwOnError: false });

                        row.appendChild(midL1);
                        row.appendChild(inpL);
                        row.appendChild(midL2);
                        block.appendChild(row);

                        const midLex0 = document.createElement("span");
                        midLex0.style.marginLeft = "80px";
                        midLex0.style.fontSize = "14px";
                        midLex0.textContent = "Equal to 'forêt': ^forêt$";
                        midLex0.style.display = "block";
                        block.appendChild(midLex0);

                        const midLex1 = document.createElement("span");
                        midLex1.style.marginLeft = "80px";
                        midLex1.style.fontSize = "14px";
                        midLex1.textContent = "Starting with 'forest': ^forest";
                        midLex1.style.display = "block";
                        block.appendChild(midLex1);

                        const midLex2 = document.createElement("span");
                        midLex2.style.marginLeft = "80px";
                        midLex2.style.fontSize = "14px";
                        midLex2.textContent = "Containing '森林': 森林";
                        midLex2.style.display = "block";
                        block.appendChild(midLex2);

                        const midLex3 = document.createElement("span");
                        midLex3.style.marginLeft = "80px";
                        midLex3.style.fontSize = "14px";
                        midLex3.textContent = "Ending with 'जंगल': जंगल$";
                        midLex3.style.display = "block";
                        block.appendChild(midLex3);

                        const midLex4 = document.createElement("span");
                        midLex4.style.marginLeft = "80px";
                        midLex4.style.fontSize = "14px";
                        midLex4.textContent = "Not containing 'bosque': ^(?!.*bosque).*$";
                        midLex4.style.display = "block";
                        block.appendChild(midLex4);

                        // --- Line buttons ADD / REM / ONL ---
                        const btnRow = document.createElement("div");
                        btnRow.style.display = "flex";
                        btnRow.style.gap = "10px";
                        btnRow.style.marginTop = "6px";

                        ["ADD", "REM", "ONL"].forEach(mode => {
                            const b = document.createElement("button");
                            b.style.border = "none";
                            b.style.background = "#757575";
                            b.style.color = "white";
                            b.style.fontWeight = "bold";
                            b.style.background = "#757575"; // normal
                            b.style.cursor = "pointer";
                            b.onmouseenter = () => { b.style.background = "#4F4F4F"; };// hover
                            b.onmouseleave = () => { b.style.background = "#757575"; }; // back

                            b.innerHTML = mode;
                            b.onclick = () => {

                                let strREGEX = document.getElementById("regex").value;

                                let D = { T: "LAB", ARO: mode, ID: "", s: "", a: strREGEX, b: "" };
                                let Builded = BuildSelection(D)
                                if (Builded[0] === "") {
                                    STATE.lback.push(D);
                                    Upate_ARO_selection_visible(mode, Builded[1]);
                                    PLOT_Vastur()
                                    hidemenuLDCON();
                                }
                                else {
                                    document.getElementById("regex").value = "'" + strREGEX + "' " + "Invalid Regex: " + Builded[0]
                                };
                            };
                            btnRow.appendChild(b);
                        });

                        block.appendChild(btnRow);
                        menuLDCON.appendChild(block);
                        return;
                    }

                    if (action.id === "modules") {
                        // --- Line butons ADD / REM / ONL ---
                        const btnRow = document.createElement("div");
                        btnRow.style.display = "flex";
                        btnRow.style.gap = "10px";
                        btnRow.style.marginTop = "6px";

                        ["ADD", "REM", "ONL"].forEach(mode => {
                            const b = document.createElement("button");
                            b.style.border = "none";
                            b.style.background = "#757575";
                            b.style.color = "white";
                            b.style.fontWeight = "bold";
                            b.style.background = "#757575"; // normal
                            b.style.cursor = "pointer";
                            b.onmouseenter = () => { b.style.background = "#4F4F4F"; };// hover
                            b.onmouseleave = () => { b.style.background = "#757575"; }; // back

                            b.innerHTML = mode;
                            b.onclick = () => {
                                /*
                                let min = document.getElementById("degMinInput").value;
                                let max = document.getElementById("degMaxInput").value;
                                if (min == "") { min = 0; }
                                if (max == "") { max = gData.nodes.length; }
                                */

                                let D = { T: "CpMODofNodeVis", ARO: "", ID: "", s: STATE.s, a: "", b: "" };
                                let Builded = BuildSelection(D)
                                if (Builded[0] === "") {
                                    STATE.lback.push(D);
                                    Upate_ARO_selection_visible(mode, Builded[1]);
                                    PLOT_Vastur()
                                }
                                else {
                                    // console.error
                                };
                            };
                            btnRow.appendChild(b);
                        });

                        block.appendChild(btnRow);
                        menuLDCON.appendChild(block);
                        return;




                    }

                });
            }

            function MakeOneBack() {
                // at begining all nodes are visibles
                for (let id = 0; id < gData.nodes.length; id++) { gData.nodes[id].prop.V = true; }
                STATE.PLOT.nbVisibleNodes = gData.nodes.length;

                if (STATE.lback.length > 1) {
                    for (let i = 1; i < STATE.lback.length - 1; i++) {
                        let D = STATE.lback[i]
                        let Builded = BuildSelection(D)
                        Upate_ARO_selection_visible(D.ARO, Builded[1]);
                    }
                    STATE.lback.pop();
                }
            };

            // ===============
            //  DRAG OF MENU
            // ===============

            const menuLDCON = document.getElementById("menuLDCON");
            /*
            document.addEventListener("mousedown", (e) => {
 
                if (
                    menuLDCON.style.display !== "none" &&
                    !menuLDCON.contains(e.target)
                ) {
                    menuLDCON.style.display = "none";
                }
 
            });
            */
            let isDragging = false;
            let isDraggingMenu = false;
            let offsetX = 0, offsetY = 0;

            (function enableMenuDrag() {

                menuLDCON.addEventListener("mousedown", (e) => {

                    // Prevent dragging if clicked in input
                    if (e.target.tagName === "INPUT") return;

                    isDragging = true;
                    isDraggingMenu = true;

                    offsetX = e.clientX - menuLDCON.offsetLeft;
                    offsetY = e.clientY - menuLDCON.offsetTop;

                    e.preventDefault();
                });

                document.addEventListener("mousemove", (e) => {

                    if (!isDragging) return;
                    menuLDCON.style.left = (e.clientX - offsetX) + "px";
                    menuLDCON.style.top = (e.clientY - offsetY) + "px";
                });

                document.addEventListener("mouseup", event => {

                    isDragging = false;
                    setTimeout(() => { isDraggingMenu = false; }, 50);
                });

            })();

            // ==================
            //  DISPLAY / CLOSE
            // ==================

            function showmenuLDCON(e, contextData) {
                const menuLDCON = document.getElementById("menuLDCON");
                updatemenuLDCON(contextData);
                menuLDCON.style.left = (e.clientX - 280) + "px";
                menuLDCON.style.top = e.clientY + "px";
                menuLDCON.style.display = "block";
            }

            function hidemenuLDCON() {
                menuLDCON.style.display = "none";
            }



            function Barycenter(ListNodes) {
                if (ListNodes == "all_visible") {

                    if (STATE.PLOT.nbVisibleNodes == 0) {
                        return { x: 0, y: 0, z: 0, dmean: 0, dmin: 0, dmax: 0 };
                    }

                    let an_i_vis = 0;
                    let X = 0, Y = 0, Z = 0;
                    for (let i = 0; i < gData.nodes.length; i++) {
                        if (getNodVis(i)) {
                            an_i_vis = i
                            n = gData.nodes[i]
                            X = X + n.x; Y = Y + n.y; Z = Z + n.z;
                        }
                    }
                    // barycenter
                    X = X / STATE.PLOT.nbVisibleNodes;
                    Y = Y / STATE.PLOT.nbVisibleNodes;
                    Z = Z / STATE.PLOT.nbVisibleNodes;

                    let dmean = 0, dmin = 0, dmax = 0;
                    dmin = Math.hypot(X - gData.nodes[an_i_vis].x, Y - gData.nodes[an_i_vis].y, Z - gData.nodes[an_i_vis].z);
                    dmax = dmin;

                    for (let i = 0; i < gData.nodes.length; i++) {
                        n = gData.nodes[i]
                        const d = Math.hypot(X - n.x, Y - n.y, Z - n.z);
                        dmean = dmean + d; dmin = Math.min(d, dmin); dmax = Math.max(d, dmax);
                    }
                    dmean = dmean / STATE.PLOT.nbVisibleNodes;
                    return { x: X, y: Y, z: Z, dmean: dmean, dmin: dmin, dmax: dmax };
                }

                if (ListNodes.length == 0) {
                    return { x: 0, y: 0, z: 0, dmean: 0, dmin: 0, dmax: 0 };
                }
                else {
                    let X = 0, Y = 0, Z = 0;
                    for (let i = 0; i < ListNodes.length; i++) {
                        n = gData.nodes[ListNodes[i]]
                        X = X + n.x; Y = Y + n.y; Z = Z + n.z;
                    }
                    X = X / ListNodes.length; Y = Y / ListNodes.length; Z = Z / ListNodes.length;  // barycenter

                    let dmean = 0, dmin = 0, dmax = 0;
                    dmin = Math.hypot(X - gData.nodes[ListNodes[0]].x, Y - gData.nodes[ListNodes[0]].y, Z - gData.nodes[ListNodes[0]].z);
                    dmax = dmin;

                    for (let i = 0; i < ListNodes.length; i++) {
                        n = gData.nodes[ListNodes[i]]
                        const d = Math.hypot(X - n.x, Y - n.y, Z - n.z);
                        dmean = dmean + d; dmin = Math.min(d, dmin); dmax = Math.max(d, dmax);
                    }
                    dmean = dmean / ListNodes.length
                    return { x: X, y: Y, z: Z, dmean: dmean, dmin: dmin, dmax: dmax };
                }
            };

            function addCheckAt(x, y, z, size11, size12, size13, size21, size22, size23, color1, color2) {

                const mat1 = new THREE.MeshBasicMaterial({
                    color: color1,
                    depthTest: false,
                    depthWrite: false,
                    transparent: true
                });

                const mat2 = new THREE.MeshBasicMaterial({
                    color: color2,
                    depthTest: false,
                    depthWrite: false,
                    transparent: true
                });

                const bar1 = new THREE.Mesh(new THREE.BoxGeometry(size11, size12, size13), mat1);
                const bar2 = new THREE.Mesh(new THREE.BoxGeometry(size21, size22, size23), mat2);

                // very high rendering order
                bar1.renderOrder = 9999;
                bar2.renderOrder = 9999;

                const cross = new THREE.Group();
                cross.add(bar1);
                cross.add(bar2);

                // draw AFTER everything else
                cross.renderOrder = 9999;

                // clear the depth buffer
                cross.onBeforeRender = (renderer) => {
                    renderer.clearDepth();
                };

                cross.position.set(x, y, z);
                return cross;
            };

            function cross_forward(x, y, z,
                size11 = 100, size12 = 1, size13 = 1,
                size21 = 1, size22 = 100, size23 = 1,
                color1 = 'black', color2 = 'white') {

                const cross = addCheckAt(x, y, z, size11, size12, size13, size21, size22, size23, color1, color2);
                scene.add(cross);
                setTimeout(() => {
                    scene.remove(cross);
                }, 3000);
                return cross;
            };

            function UPDATE_ACTION(BY) {
            };


            function randomInt(x, y) {
                return Math.floor(Math.random() * (y - x + 1)) + x;
            }
        })
    </script>
</body>

</html>
  """+nl
  saveChemCH(OutfileHTML, CH)

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
        


