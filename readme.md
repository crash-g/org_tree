# Org Tree
## A package that draws org files as weighted graphs
### Description
	This package can be used to render the structure of org files as a weighted graph. The rendering leverages _plotly_ and produces an html file. The color of the node is directly proportional to the amount of text the node and its children contain: the darker the more.
### Installation
	Download this repository and use
	> pip install /path/to/local/repository/
### Usage
	Just import the package and call _drawGraph_ passing to it the absolute path of an org file.
	> import org_tree as ot
	> ot.drawGraph("path/to/org/file.org", "file_encoding")
