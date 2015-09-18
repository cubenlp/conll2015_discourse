#coding:utf-8
from syntax_tree import Syntax_tree
class Constituent:
    def __init__(self, syntax_tree, node):
        self.syntax_tree = syntax_tree
        self.node = node
        self.label = None # Arg1, Arg2, None
        self.connective = None
        self.indices = self.get_indices()

    # get the indices of the leaves of the constituent in syntax tree,
    def get_indices(self):
        leaves = self.syntax_tree.tree.get_leaves()
        const_leaves = self.node.get_leaves()
        indices = sorted([leaves.index(leaf) for leaf in const_leaves])
        return indices