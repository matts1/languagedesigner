from ebnf.syntax import Syntax
from ebnf.basenode import RuleError
from ebnf.syntaxrule import SyntaxRule
from tests.ebnf.base import TestCase

example = '''syntax = (syntax rule)+;
syntax rule = meta identifier, '=', definition list, ';';
definition list = single definition, ('|', single definition)*;
single definition = term, (',', term)*;
term = primary, ('-', exception)?;
exception = primary;
primary = numbered sequence | grouped sequence | meta identifier | terminal string;
numbered sequence = grouped sequence, ('*' | '+' | '' | ('{', (integer)?, ',', integer, '}') | ('{', integer, ',', (integer)?, '}') | ('{', integer, '}')), ('?')?;
grouped sequence = '(', definition list, ')';
terminal string = "'", (character - "'")*, "'" | '"', (character - '"')*, '"';
meta identifier = letter, (letter | decimal digit | ' ')*;
integer = (decimal digit)+;
decimal digit = '1';
letter = 'a';'''  # these metaidents will do for now just for the sake of the test


class SyntaxRuleTestCase(TestCase):
    cls = SyntaxRule

    def test_ebnf_examples(self):
        for line in example.split('\n'):
            self.assertValid(line)


class SyntaxTestCase(TestCase):
    cls = Syntax

    def test_ebnf_example(self):
        self.assertValid(example)

    def test_no_children(self):
        self.assertRaises(RuleError, self.create, '')

    def test_invalid_children(self):
        self.assertRaises(RuleError, self.create, 'test = blah; test2 = blah2')  # no semicolon
