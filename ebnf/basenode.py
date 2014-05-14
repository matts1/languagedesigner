class Node(object):
    ignore = set(' \f\n\r\t\v')  # whitespace

    def __init__(self, parent=None, text=None, make_invalid=False, root=None):
        self.parent = parent
        if parent is None:  # required for non-root nodes for testing specific elements
            self.upto = 0
            self.text = text
            self.root = self if root is None else root
        else:
            self.upto = parent.upto
            self.text = parent.text
            self.root = parent.root
        self.children = []

        self.checked = set()
        self.start = self.upto
        self.valid = True
        self.create()
        if self.valid and parent is not None:
            parent.upto = self.upto
            parent.skip_ignore()
            parent.children.append(self)
        if not self.valid and make_invalid:
            parent.valid = False
        self.end = self.upto
        while self.end > self.start and self.text[self.end - 1] in self.ignore:
            self.end -= 1

    def get(self, move=False):
        val = self.text[self.upto] if self.upto < len(self.text) else None
        if move:
            self.next()
        return val

    def getn(self, size, move=False):
        val = self.text[self.upto:min(self.upto + size, len(self.text) - 1)]
        if move:
            self.next(size)
        return val

    def next(self, num=1):
        for i in range(num):
            self.upto += 1  # potential bugs - maybe skipping things that were counted before
            self.skip_ignore()

    def skip_ignore(self):
        while self.get() in self.ignore:
            self.upto += 1

    def is_end(self):
        return self.upto == len(self.text)

    def match(self, char, set_invalid=True):
        if self.get() == char:
            self.next()
            return True
        elif set_invalid:
            self.valid = False
            return False

    def matchn(self, chars, set_invalid=True):
        for c in chars:
            self.match(c, set_invalid)

    def create(self):
        raise NotImplementedError

    def out(self):
        return ''

    def pprint(self, indent=0, children=True):
        return '%s<%s> (%s)%s%s' % (
            ' ' * indent,
            self.__class__.__name__,
            self.out(),
            '\n' if self.children and children else '',
            '\n'.join(child.pprint(indent + 2) for child in self.children_out()) if children else ''
        )

    def children_out(self):
        return self.children

    def __repr__(self):
        return self.pprint()

    def compile(self, *args, **kwargs):
        return self.compiled_class(self, *args, **kwargs)

    def get_text(self):
        return self.text[self.start:self.end]

    def check_invalid(self, ident):
        if ident in self.checked:
            return
        self.checked.add(ident)
        if self.children:
            from .metaidentifier import MetaIdentifier
            if isinstance(self.children[0], MetaIdentifier):
                if self.children[0].identifier == ident:
                    raise RuleError("You cannot recurse MetaIdentifiers unless you prefix your definition (used in %s)!" % ident)
                elif self.children[0].identifier not in self.root.rules:
                    raise RuleError("Metaidentifier %s is undefined" % self.children[0].identifier)
                else:
                    self.root[self.children[0].identifier].check_invalid(ident)
            else:
                self.children[0].check_invalid(ident)

    def __getitem__(self, item):
        return self.children[item]


class Compiled(Node):
    def __init__(self, ebnf, *args, **kwargs):
        self.ebnf = ebnf
        super(Compiled, self).__init__(*args, **kwargs)

    def create(self):
        for child in self.ebnf.children:
            # make invalid means compiled only valid if all sub-nodes are valid
            if not child.compile(self, make_invalid=True).valid:
                break

    def should_delete(self):
        return False

    def delete_self(self):
        for child in self.children:
            child.delete_self()
        if self.should_delete() and self.parent is not None:
            self.children[0].parent = self.parent
            self.parent.children[self.parent.children.index(self)] = self.children[0]

    def out(self):
        return self.ebnf.__class__.__name__ + ',' + self.ebnf.pprint(children=False)

    def find_meta_children(self, nodes):
        children = []
        for child in self.children:
            children.extend(child.find_meta_children(nodes))
        self.meta_children = children
        return children


class InvisibleCompiled(Compiled):
    def should_delete(self):
        return True


class RuleError(SyntaxError):
    pass
