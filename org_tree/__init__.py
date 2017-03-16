"""This module can be used to render a graph which represents the structure of an org file.
Definitions:
    Dictionary of attributes: a dict with the following structure
                              {NODE: node_attributes, LEVEL: {level: number_of_nodes_at_that_level} }
    Node attributes: a dict with the following structure
                     {WEIGHT: length_of_the_text_the_node_contains, LEVEL: level_of_the_node}
"""
import plotly as py
from plotly.graph_objs import *
import networkx as nx
import math
import os
import locale

from . import tree_pos

NODE_PREFIX = "*"
ROOT = "root"
WEIGHT = "weight"
LEVEL = "level"
NODE = "node"
TOTAL = "total"
CURRENT = "current"
NEWLINE = "\\n"

def _updateAttributes(node, nodeLevel, attributes):
    """Adds a node to the dictionary of node attributes.
    Args:
        node (str): Name of the node.
        nodeLevel (int): The level of the node.
        attributes (dict): The dictionary of attributes to update.
    """
    nodeAttributes = {}
    nodeAttributes[WEIGHT] = 0
    nodeAttributes[LEVEL] = nodeLevel
    attributes[NODE][node] = nodeAttributes
    if not nodeLevel in attributes[LEVEL]:
        attributes[LEVEL][nodeLevel] = 0
    attributes[LEVEL][nodeLevel] += 1

def _processNewNode(line, orgGraph, nodeStack, attributes, counter):
    """Adds a new node to the graph and processes its attributes.
    Args:
        line (str): The current line in the buffer.
        orgGraph (nx.Graph): The (partial) graph representation of the org file.
        nodeStack (list): The list of ancestors of the previously processed node.
        attributes (dict): The dictionary of attributes to update.
        counter (int): A number used to ensure uniqueness of the nodes' names.

    Returns:
        list: the list of ancestors of the new node (including the node itself).
    """
    nodeLevel = line.find(" ")
    # parses the level
    nodeStack = [x for x in nodeStack if attributes[NODE][x][LEVEL] < nodeLevel]
    # removes from the stack all nodes that are not ancestors of the current one
    parentNode = nodeStack[-1] if nodeStack else None
    # finds the parent
    node = line[nodeLevel + 1 : line.find(NEWLINE)] + " -- " + str(counter)
    # parses the node name (adding an additional value to prevent name collisions)
    orgGraph.add_node(node)
    if(parentNode is not None):
        orgGraph.add_edge(parentNode, node)
    else:
        orgGraph.add_edge(ROOT, node)
    # adds the node and an edge to the parent
    nodeStack.append(node)
    _updateAttributes(node, nodeLevel, attributes)
    # sets the attributes for the node
    return nodeStack

def _initAttributes():
    """Initialize the dictionary of attributes.
    
    Returns:
        dict: A basic dictionary of attributes only containing info about the root of the tree.
    """
    nodeAttributes = {}
    nodeAttributes[ROOT] = {}
    nodeAttributes[ROOT][WEIGHT] = 0
    nodeAttributes[ROOT][LEVEL] = 0

    levelAttributes = {}
    levelAttributes[0] = 1

    attributes = {NODE : nodeAttributes, LEVEL : levelAttributes}
    return attributes

def _readOrgfile(filename, enc):
    """Parses the org file and produces a graph and a corresponding dictionary of attributes.
    Args:
        filename (str): The absolute path to the org file.
        enc (str): The encoding of the org file.

    Returns:
        nx.Graph: a tree representation of the org file structure.
        dict: the dictionary of attributes.
    """
    orgGraph=nx.Graph()
    orgGraph.add_node(ROOT)
    nodeStack = []
    attributes = _initAttributes()
    with open(filename, encoding = enc) as orgFile:
        counter = 1
        # appended to the node name to prevent name collisions
        for line in orgFile:
            if(line):
                if(line.startswith(NODE_PREFIX)):
                    nodeStack = _processNewNode(line, orgGraph, nodeStack, attributes, counter)
                    counter += 1
                else:
                    length = len(line.strip())
                    for node in nodeStack:
                        attributes[NODE][node][WEIGHT] += length
                    attributes[NODE][ROOT][WEIGHT] += length
                    # the weight is added to the current node and to all its ancestors
    return (orgGraph, attributes)

def drawGraph(filename, encoding=locale.getpreferredencoding()):
    """Renders a graph representation of the structure of an org file.
    Args:
        filename (str): The absolute path to the org file.
        encoding (str): The encoding of the org file.
    """
    G, attributes = _readOrgfile(filename, encoding)
    if(nx.is_tree(G)):
        pos = tree_pos.hierarchy_pos(G,ROOT,attributes[LEVEL])
        edge_trace = Scatter(
            x=[],
            y=[],
            line=Line(width=0.5,color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0 = pos[edge[0]][0]
            y0 = pos[edge[0]][1]
            x1 = pos[edge[1]][0]
            y1 = pos[edge[1]][1]
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

        node_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=Marker(
                showscale=True,
                colorscale='YIGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Size',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        orgFileName = filename[filename.rfind(str(os.sep)) + 1:]
        for node in G.nodes():
            x = pos[node][0]
            y = pos[node][1]
            node_trace['x'].append(x)
            node_trace['y'].append(y)
            node_trace['text'].append(node)
            # marker color array: every element corresponds to the color of the node at the same position in the list (note that internally nodes are saved as a list)
            w = attributes[NODE][node][WEIGHT]
            # the color depends on the weight of the node
            c = math.ceil(pow(w,0.25)) if w > 0 else 0
            # a transform function is used in an attempt to obtain a better color distribution
            node_trace['marker']['color'].append(c)

        fig = Figure(data=Data([edge_trace, node_trace]),
                     layout=Layout(
                         title='<br>Node structure of ' + orgFileName,
                         titlefont=dict(size=16),
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(b=20,l=5,r=5,t=40),
                         annotations=[ dict(
                             text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                             showarrow=False,
                             xref="paper", yref="paper",
                             x=0.005, y=-0.002 ) ],
                         xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

        py.offline.plot(fig, filename=orgFileName.replace(".", "_") + ".html")
    else:
        print("Error parsing " + filename)
