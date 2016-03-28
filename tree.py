"""
    Tree class, which will be used in the Minimax Algorithm.
"""
class Tree(object):
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def get_children(self):
        return self.children

def traverse(Tree):
    """
        An ugly traverse function, will be beautified later.
        ---> represents branching
        ---| represents leaf node
    """
    if Tree:
        print Tree
    if Tree.get_children():
        children = Tree.get_children()
        print '--->', children
        for child in children:
            traverse(child)
    else:
        print '---|'

"""
# Remove docstrings to see an example.
def main():
    root = Tree()
    c1 = Tree('c1')
    c2 = Tree('c2')
    c3 = Tree('c3')
    c4 = Tree('c4')
    root.add_child(c1)
    root.add_child(c2)
    c1.add_child(c3)
    c2.add_child(c4)
    traverse(root)

if __name__ == '__main__':
    main()
"""
