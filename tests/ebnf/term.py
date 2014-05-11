from ebnf.basenode import Compiled
from ebnf.term import Term
from tests.ebnf.base import TestCase


# string = ('"', (anything - '"')*, '"') | ("'", (anything - "'")*, "'")
class TermTestCase(TestCase):
    cls = Term

    def test_no_exception(self):
        term = self.create('"abc def" blah')
        self.assertEqual('abc def', term.primary.children[0].val)
        self.assertEqual(None, term.exception)

    def test_valid(self):
        # don't bother testing what kinds of primaries are valid - that is done in primary
        string = self.create('"abc def" - "blah"')
        self.assertEqual('abc def', string.primary.children[0].val)
        self.assertEqual('blah', string.exception.children[0].val)

        meta = self.create('bo b -     geo rge "blah"')
        self.assertEqual('bo b', meta.primary.children[0].identifier)
        self.assertEqual('geo rge', meta.exception.children[0].identifier)

    def test_invalid(self):
        self.assertInvalid('- "blah"')
        self.assertRaises(SyntaxError, self.create, 'rule - ')
        self.assertRaises(SyntaxError, self.create, 'rule - 1Invalid')

    def test_ending(self):
        self.assertEqual(self.create('term | blah').upto, 5)
        self.assertEqual(self.create('a - b | b - c').upto, 6)


class CompiledTermTestCase(TestCase):
    cls = Term

    def test_exception(self):
        self.assertNotCompiles('"abc" - "abc"', 'abc')
        self.assertNotCompiles('"abc" - "def"', 'def')
        self.assertCompiles('"abc" - "def"', 'abc', 'abc')
