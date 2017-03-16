import math
import networkx as nx
import sys
sys.path.insert(0, "../..")

import tree_pos as tp

def test_hierarchy_pos():
    G=nx.Graph()
    G.add_edges_from([(1,2), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9), (4,10),
                      (5,11), (5,12), (6,13)])
    width = 1.
    height = 1.
    pos = tp.hierarchy_pos(G, 1, width=width, height=height)
    _assert_pos(pos, width, height)
    width = 0.3
    height = 45.2
    pos = tp.hierarchy_pos(G, 1, width=width, height=height)
    _assert_pos(pos, width, height)

def _assert_pos(pos, width, height):
    for i in range(1,13):
        assert i in pos
        if i == 1:
            x = width / 2
            y = 0
        elif i < 5:
            dx = width / 3
            x = dx/2 + dx*(i-2)
            y = -0.25 * height
        elif i < 11:
            dx = width / 6
            x = dx/2 + dx*(i-5)
            y = -0.5 * height
        else:
            dx = width / 3
            x = dx/2 + dx*(i-11)
            y = -0.75 * height
        assert math.isclose(pos[i][0], x, rel_tol=1e-5)
        assert math.isclose(pos[i][1], y, rel_tol=1e-5)
    
