class EvalNode():
    def __init__(self, tree):
        # the tree is the metaidentifier, so get the child, which is definition list
        self.tree = tree.children[0]
