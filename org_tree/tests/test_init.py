import random
import copy
import networkx as nx
import sys
sys.path.insert(0, "../..")

import org_tree as ot

def _init_attributes():
    attributes = {}
    attributes[ot.NODE] = {}
    attributes[ot.LEVEL] = {}
    return attributes

def test_update_attributes():
    attributes = _init_attributes()
    for i in range(1,100):
        node = "test" + str(i)
        nodeLevel = random.randint(0,500)
        tempAttr = copy.deepcopy(attributes)
        ot._updateAttributes(node, nodeLevel, tempAttr)
        assert node in tempAttr[ot.NODE]
        assert tempAttr[ot.LEVEL][nodeLevel] == 1 or tempAttr[ot.LEVEL][nodeLevel] == attributes[ot.LEVEL][nodeLevel] + 1
        attributes = tempAttr

def test_process_new_node():
    # test adding a node at level 3
    stars = "***"
    name = "only a test header"
    line = stars + " " + name + ot.NEWLINE
    G=nx.Graph()
    G.add_edges_from([(1,2), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9), (4,10),
                      (5,11), (5,12), (6,13)])
    nodeStack = [1,2,6]
    attributes = _init_attributes()
    attributes[ot.NODE][1] = {ot.LEVEL: 1}
    attributes[ot.NODE][2] = {ot.LEVEL: 2}
    attributes[ot.NODE][6] = {ot.LEVEL: 6}
    counter = 1
    nodeStack = ot._processNewNode(line, G, nodeStack, attributes, counter)
    assert 1 in nodeStack
    assert 2 in nodeStack
    assert not 6 in nodeStack
    nodeName = name + " -- " + str(counter)
    assert nodeName in nodeStack
    assert nodeName in G.nodes()
    assert nodeName in G.neighbors(2)
    assert attributes[ot.NODE][nodeName][ot.LEVEL] == 3

    # test adding a node at level 1
    stars = "*"
    name = "only another test header"
    line = stars + " " + name + ot.NEWLINE
    G.add_node(ot.ROOT)
    nodeStack = ot._processNewNode(line, G, [], attributes, counter)
    assert not 1 in nodeStack
    assert not 2 in nodeStack
    nodeName = name + " -- " + str(counter)
    assert nodeName in nodeStack
    assert nodeName in G.nodes()
    assert nodeName in G.neighbors(ot.ROOT)
    assert attributes[ot.NODE][nodeName][ot.LEVEL] == 1

def test_init_attributes():
    attributes = ot._initAttributes()
    assert ot.NODE in attributes
    assert ot.LEVEL in attributes    
    nodeAttributes = attributes[ot.NODE]
    assert ot.ROOT in nodeAttributes
    assert nodeAttributes[ot.ROOT][ot.WEIGHT] == 0
    assert nodeAttributes[ot.ROOT][ot.LEVEL] == 0
    levelAttributes = attributes[ot.LEVEL]
    assert levelAttributes[0] == 1
    
