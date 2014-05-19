import re
from ebnf.basenode import Node, Compiled, RuleError

identifier = re.compile('[a-z][a-z0-9 ]*', re.I)


class CompiledMetaIdentifier(Compiled):
    def __init__(self, *args, **kwargs):
        super(CompiledMetaIdentifier, self).__init__(*args, **kwargs)
        self.is_root = self.parent is None
        if kwargs.get('output_textbox') is not None:
            self.output_text = ''
            self.output_textbox = kwargs['output_textbox']

    def create(self):
        self.ebnf.get_dl().compile(self, make_invalid=True)
        if self.parent is None and self.upto < len(self.text):
            raise RuleError('Program stopped matching EBNF early')

    def out(self):
        return self.ebnf.identifier

    def find_meta_children(self):
        self.meta_children = []
        for child in self.children:
            self.meta_children.extend(child.find_meta_children())
        return [self]

    def setup(self):
        pass

    def execute(self, *args, **kwargs):
        return self.execute_children(*args, **kwargs)

    def execute_children(self, *args, **kwargs):
        return [child.execute(*args, **kwargs) for child in self.meta_children]

    def teardown(self):
        pass

    def repr(self):
        pass

    def run_tree(self, fn_name, *args, **kwargs):
        for child in self.meta_children:
            child.run_tree(fn_name, *args, **kwargs)
        getattr(self, fn_name, None)(*args, **kwargs)

    def pprint(self, indent=0, *args, **kwargs):
        out = self.repr()
        if out is not None:
            return ' ' * indent + '<%s> (%s)' % (self.ebnf.identifier, out)
        else:
            return super(CompiledMetaIdentifier, self).pprint(indent=indent, *args, **kwargs)

    def rdraw(self, children):
        return self.get_text

    def output(self, *args):
        output = ' '.join(map(str, args)) + '\n'
        self.root._output(output)

    def input(self, msg):
        return raw_input(msg)

    def _output(self, output):
        self.output_text += output
        self.output_textbox.set_text(self.output_text)


# meta identifier = letter, (letter | decimal digit | ' ')*
class MetaIdentifier(Node):
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
        self.compiled_class = self.execute_nodes.get(self.identifier, CompiledMetaIdentifier)

    def get_dl(self):
        return self.root[self.identifier]

    def out(self):
        return self.identifier


# execution classes
class TextNode(CompiledMetaIdentifier):
    def setup(self):
        self.val = self.get_text()

    def execute(self, *args, **kwargs):
        return self.val

    def repr(self):
        return self.val
