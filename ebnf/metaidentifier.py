import re
from ebnf.basenode import Node, Compiled, RuleError
from ebnf.eval import EvalNode

identifier = re.compile('[a-z][a-z0-9 ]*', re.I)


class CompiledMetaIdentifier(Compiled):
    def create(self):
        self.ebnf.get_dl().compile(self, make_invalid=True)
        if self.parent is None and self.upto < len(self.text):
            raise RuleError('Program stopped matching EBNF early')

    def __getattr__(self, item):  # allow them to access the executor variables like they would access themselves
        return getattr(self.executor, item)

    def out(self):
        return self.ebnf.identifier

    def find_meta_children(self, nodes):
        self.meta_children = []
        executor_cls = nodes.get(self.ebnf.identifier, None)
        if executor_cls is not None:
            self.executor = executor_cls(self)
        else:
            self.executor = EvalNode(self)
        for child in self.children:
            self.meta_children.extend(child.find_meta_children(nodes))
        return [self]

    def setup_execute(self, nodes):
        for child in self.meta_children:
            child.setup_execute(nodes)
        self.executor.setup()

    def execute(self, nodes):
        self.executor.execute()

    def teardown_execute(self, nodes):
        for child in self.meta_children:
            child.teardown_execute(nodes)
        self.executor.teardown()

    def pprint(self, indent=0, *args, **kwargs):
        if self.executor is not None and getattr(self.executor, 'pprint', None) is not None:
            return ' ' * indent + '<%s> (%s)' % (self.ebnf.identifier, self.executor.pprint())
        else:
            return super(CompiledMetaIdentifier, self).pprint(indent=indent, *args, **kwargs)


# meta identifier = letter, (letter | decimal digit | ' ')*
class MetaIdentifier(Node):
    compiled_class = CompiledMetaIdentifier

    ignore = set('\f\n\r\t\v')
    def create(self):
        self.identifier = re.match(  # match goes from beginning of string only
            identifier,
            self.text[self.upto:]
        )
        if self.identifier is None:
            self.valid = False
        else:
            self.identifier = self.identifier.group(0).rstrip()
            self.next(len(self.identifier))

    def get_dl(self):
        return self.root[self.identifier]

    def out(self):
        return self.identifier
