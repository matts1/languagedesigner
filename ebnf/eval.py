class EvalNode():
    def __init__(self, tree):
        # the tree is the metaidentifier, so get the child, which is definition list
        self.metaident = tree
        self.tree = tree.children[0]
        self.children = self.tree.children
        self.is_root = tree.parent is None

    def setup(self):
        pass

    def execute(self):
        self.execute_children()

    def teardown(self):
        pass

    def __getitem__(self, item):
        return self.tree[item]

    @property
    def meta_children(self):
        return self.metaident.meta_children

    def execute_child(self, index, *args, **kwargs):
        return self.meta_children[index].executor.execute(*args, **kwargs)

    def execute_children(self, *args, **kwargs):
        return [self.execute_child(i, *args, **kwargs) for i in xrange(len(self.meta_children))]

    def get_text(self):
        return self.metaident.get_text()


class TextEvalNode(EvalNode):
    def setup(self):
        self.val = self.get_text()

    def execute(self):
        return self.val

    def pprint(self):
        return self.val
