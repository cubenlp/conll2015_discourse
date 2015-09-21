#coding:utf-8
import re
from ete2 import Tree
import config
import copy

class Syntax_tree:
    def __init__(self, parse_tree):
        
        # parse_tree = parse_tree.encode("utf-8", errors="replace")
        
        newick_text = self.to_newick_format(parse_tree)
        
        if newick_text == None:
            self.tree = None
        else:
            # newick_text = newick_text.encode("utf-8")
            # self.tree = Tree(newick_text, format=1)

            try:
                newick_text = newick_text.encode("utf-8")
                self.tree = Tree(newick_text, format=1)
            except:
                self.tree = None
        pass

    def print_tree(self):
        print self.tree.get_ascii(show_internal=True)

    def get_node_path_to_root(self, node):
        path = ""
        while (not node.is_root()):
            path += node.name + "-->"
            node = node.up
        path += node.name
        return path

    def get_leaf_node_by_token_index(self, token_index):
        leaves = self.tree.get_leaves()
        if token_index >= len(leaves) :
            return None
        return leaves[token_index]

    #根据词的indices ,获取 common_ancestor
    def get_self_category_node_by_token_indices(self, token_indices):
        if len(token_indices) == 1:
            return self.get_leaf_node_by_token_index(token_indices[0]).up

        nodes = []
        for token_index in token_indices:
            node = self.get_leaf_node_by_token_index(token_index)
            nodes.append(node)
        return self.tree.get_common_ancestor(nodes)

    def get_common_ancestor_by_token_indices(self, token_indices):
        nodes = []
        for token_index in token_indices:
            node = self.get_leaf_node_by_token_index(token_index)
            nodes.append(node)
        return self.tree.get_common_ancestor(nodes)


    def get_left_sibling_category_node_by_token_indices(self, token_indices):
        self_category_node = self.get_self_category_node_by_token_indices(token_indices)
        node_id = id(self_category_node)

        if self_category_node.up == None:
            return None

        children = self_category_node.up.get_children()
        for i, child in enumerate(children):
            if node_id == id(child):
                if i == 0:
                    return None
                else:
                    return children[i - 1]

    def get_right_sibling_category_node_by_token_indices(self, token_indices):
        self_category_node = self.get_self_category_node_by_token_indices(token_indices)
        node_id = id(self_category_node)

        if self_category_node.up == None:
            return None

        children = self_category_node.up.get_children()
        for i, child in enumerate(children):
            if node_id == id(child):
                if i == len(children) - 1:
                    return None
                else:
                    return children[i + 1]


    def get_parent_category_node_by_token_indices(self, token_indices):
        self_category_node = self.get_self_category_node_by_token_indices(token_indices)
        return self_category_node.up

    def get_arg1_arg2_None_nodes_list(self,Arg1_token_indices, Arg2_token_indices):
        for node in self.tree.traverse():
            node.add_feature("label","NONE")
        for node in self.tree.get_leaves():
            node.label = "X"
            node.up.label ="X"
        nodes = []
        for token_index in Arg1_token_indices:
            node = self.get_leaf_node_by_token_index(token_index)
            nodes.append(node)
        self.tree.get_common_ancestor(nodes).label = "Arg1_node"
        nodes = []
        for token_index in Arg2_token_indices:
            node = self.get_leaf_node_by_token_index(token_index)
            nodes.append(node)
        self.tree.get_common_ancestor(nodes).label = "Arg2_node"

        arg1_arg2_None_nodes_list = []
        for node in self.tree.traverse():
           if node.label != "X":
               arg1_arg2_None_nodes_list.append(node)
        return arg1_arg2_None_nodes_list


    def to_newick_format(self, parse_tree):
        # 替换 parse_tree 中的 ,

        parse_tree = parse_tree.replace(",", "*COMMA*")
        parse_tree = parse_tree.replace(":", "*COLON*")

        tree_list = self.load_syntax_tree(parse_tree)
        if tree_list == None:
            return None
        tree_list = tree_list[1] #去 root
        s = self.syntax_tree_to_newick(tree_list)
        s = s.replace(",)",")")
        if s[-1] == ",":
            s = s[:-1] + ";"
        return s

    def load_syntax_tree(self, raw_text):
        stack = ["ROOT"]
        text = re.sub(r"\(", " ( ", raw_text)
        text = re.sub(r"\)", " ) ", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"^\(\s*\(\s*", "", text)
        text = re.sub(r"\s*\)\s*\)$", "", text)
        for c in text.strip(" ").split(" "):
            if c == ")":
                node = []
                while(1):
                    popped = stack.pop()
                    if popped == "(":
                        break
                    node.append(popped)
                node.reverse()
                if len(node) > 1:
                    stack.append(node)
                else:
                    if node == []:
                        return None
                    stack.append(node[0])
            else:
                stack.append(c)
        return stack

    def syntax_tree_to_newick(self,syntax_tree):
        s = "("
        for child in syntax_tree[1:]:
            if not isinstance(child,list):
                s += child
            else:
                s += self.syntax_tree_to_newick(child)
        s += ")" + str(syntax_tree[0]) + ","
        return s

    #获取的内部节点的位置，不包括pos—tag节点
    def get_internal_node_location(self, node):
        leaves = self.tree.get_leaves()
        if len(node.get_children()) > 1:
            child1 = node.get_children()[0]
            child2 = node.get_children()[1]
            #移至叶子节点
            while not child1.is_leaf():
                child1 = child1.get_children()[0]
            while not child2.is_leaf():
                child2 = child2.get_children()[0]
            index1 = leaves.index(child1)
            index2 = leaves.index(child2)
            return [index1, index2]
        if len(node.get_children()) == 1:
            child1 = node.get_children()[0]
            #移至叶子节点
            while not child1.is_leaf():
                child1 = child1.get_children()[0]
            index1 = leaves.index(child1)
            return [index1]
    def get_node_by_internal_node_location(self, location):
        if len(location) > 1:
            nodes = []
            for token_index in location:
                node = self.get_leaf_node_by_token_index(token_index)
                nodes.append(node)
            return self.tree.get_common_ancestor(nodes)
        if len(location) == 1:
            return self.get_leaf_node_by_token_index(location[0]).up.up

    def get_right_siblings(self, node):
        if node.is_root():
            return []
        children = node.up.get_children()
        for i, child in enumerate(children):
            if child == node:
                if i == len(children) - 1:
                    return []
                return children[i+1:]

    def get_left_siblings(self, node):
        if node.is_root():
            return []
        children = node.up.get_children()
        for i, child in enumerate(children):
            if child == node:
                if i == 0:
                    return []
                return children[:i]

    def get_siblings(self, node):
        if node.is_root():
            return []
        siblings = []
        children = node.up.get_children()
        for i, child in enumerate(children):
            if child != node:
                siblings.append(child)
        return siblings

    def get_relative_position(self, node1, node2):
        if node1 == node2 or node2.is_root():
            return "middle"
        curr = node1
        rsibs = []
        lsibs = []
        while not curr.is_root():
            rsibs.extend(self.get_right_siblings(curr))
            lsibs.extend(self.get_left_siblings(curr))
            curr = curr.up
            if curr == node2:
                return "middle"
        for node in rsibs:
             if node2 in node.get_descendants():
                 return "right"
        for node in lsibs:
             if node2 in node.get_descendants():
                 return "left"

    def get_node_to_node_path(self, node1, node2):
        common_ancestor = self.tree.get_common_ancestor([node1, node2])

        path = ""
        # node1->common_ancestor
        temp = node1
        while temp != common_ancestor:
            path += temp.name +">"
            temp = temp.up
        path += common_ancestor.name
        ## common_ancestor -> node
        p = ""
        temp = node2
        while temp != common_ancestor:
            p = "<" + temp.name + p
            temp = temp.up
        path += p

        return path

    #获取他在syntax_tree的叶子节点的indices，也就是句子中的index
    def get_leaves_indices(self, node):
        leaves = self.tree.get_leaves()
        node_leaves = node.get_leaves()
        indices = sorted([leaves.index(leaf) for leaf in node_leaves])
        return indices




if __name__ == "__main__":

    parse_tree = "( (S (S (NP (DT Some)) (VP (MD may) (VP (VB have) (VP (VBN forgotten))))) (: --) (CC and) (S (NP (DT some) (JJR younger) (NNS ones)) (VP (MD may) (ADVP (RB never)) (VP (VB have) (ADJP (JJ experienced)) (: --) (SBAR (WHNP (WP what)) (S (NP (PRP it)) (VP (VBZ 's) (VP (VB like) (S (VP (TO to) (VP (VB invest) (PP (IN during) (NP (DT a) (NN recession))))))))))))) (. .)) )"
    print parse_tree




    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree != None:
        syntax_tree.print_tree()

    print syntax_tree.tree.get_distance(syntax_tree.tree, syntax_tree.get_leaf_node_by_token_index(0))




