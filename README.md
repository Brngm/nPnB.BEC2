       #=======================================#
       #  bec v2.2                             #
       #  Copyright (C) 2025-2026 Bruno Gaume  #
       #=======================================#

1) DESCRIPTION
   ===========
Networks are one of the main conceptual structures for modeling complex systems, where
nodes represent the basic lowest-level entities of the system and edges represent their
interactions. Graph clustering algorithms are then used to identify modules: over-densely
connected sets of nodes of these networks as representations of entities at higher scales
of description in these systems.

bec is a C++ graph clustering program that finds the entities of a network with a hand on
the description scale within the nPnB framework.

2) REFERENCES
   ==========
## nPnB:
    B. GAUME, I. ACHITOUV, AND D. CHAVALARIAS: Two antagonistic objectives for one multi-scale graph clustering framework
    Nature Scientific Reports, 15 (2025), p. 13368.
    https://hal.science/hal-05046050v1

## bec:
    B. GAUME: Find Optimal clusterings in nPnB framework is hard, BEC.2: an algorithm to find high-performing ones
    Forthcoming (2026)

## description scales:
    B. GAUME: Defining the appropriate scales for describing a complex system
    Forthcoming (2026)

3) AUTHOR & COPYRIGHT
   ==================
This program is copyright (C) 2025-2026 by Bruno Gaume:
    Email:	gaume.bruno@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation;

This program is distributed in the hope that it will be useful,
but WITHOUT ANY GUARANTEE OF ANY KIND.

4) COMPILING
   =========
To compile the program type the command "make".

5) USAGE
   =====
command line usage:

    bec [scaleP] [input_graph_file] [output_clustering_file] [options]

scaleP:

    The description scale in [0,1] for clustering by partition (see The nPnB framework REFERENCE).

input_graph_file:

    The file in which the network is stored (see INPUT GRAPH FORMAT).

output_clustering_file:

    The file in which the community structure will be stored (see OUPUT CLUSTERING FORMAT).

options:

    -ox	set  scaleO to x in [0,1]. The stickiness scale, overlap amount for the gluant extension of the partition modules into overlapping modules. (default = "no" do not extend to save time).
	
    -ex	set  epsilon to x in [0,1]. The smaller epsilon, the better the quality of the output clustering, but the slower the computing. (default = 0.01).
	
    -rx	set  rankedEdeges to x. (default = '0', the edges are not ranked in the input graph, the program will take care of it).
	
    -zx	set  clustZero to x. Read the INITIAL PARTITION to amend from the x file (default = '0', the programm will take care of it: each node in its own module)
	
    -vx	set  verbose to x.  Display the progress. (default = '0', silent)

example of command line:

   ./bin/bec 0.49 ./GraphExample.txt ./clustOutput.txt -o0.1 -e0.01 -r0 -z0

6) Information on input/output formats
   ===================================
   see 

8) COMMENTS & BUG REPORT
   =====================
If you find a bug, please send a bug report to gaume.bruno@gmail.com
including the input files and the line command that caused the bug.

You can also send me any comment or suggestion about the program.

	May 6, 2026. Bruno Gaume.
