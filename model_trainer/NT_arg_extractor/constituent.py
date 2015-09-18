#coding:utf-8
from syntax_tree import Syntax_tree
class Constituent:
    def __init__(self, syntax_tree, node):
        self.syntax_tree = syntax_tree
        self.node = node
        self.label = None # Arg1, Arg2, None
        self.connective = None
        self.indices = self.get_indices()

    #获取他在syntax_tree的叶子节点的indices，也就是句子中的index
    def get_indices(self):
        leaves = self.syntax_tree.tree.get_leaves()
        const_leaves = self.node.get_leaves()
        indices = sorted([leaves.index(leaf) for leaf in const_leaves])
        return indices