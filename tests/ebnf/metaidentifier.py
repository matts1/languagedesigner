from ebnf.basenode import RuleError
from ebnf.metaidentifier import MetaIdentifier
from ebnf.syntax import Syntax
from tests.ebnf.base import TestCase


class MetaIdentifierTestCase(TestCase):
    cls = MetaIdentifier
    attr = 'identifier'

    def test_valid(self):
        tests = [
            ('abc', 'abc'),
            ('a=?blah', 'a'),
            ('a ?= blah', 'a'),  # it just matches the 'a' and the parent fails the ?
            ('Z_adc123', 'Z'),
            ('Zabc 123 ', 'Zabc 123'),
            ('Zabc 123 = blah', 'Zabc 123'),
        ]
        for test in tests:
            self.assertValid(*test)

        test = self.assertValid('abc- def', 'abc')
        self.assertEqual(test.get(), '-')

    def test_invalid(self):
        # a ' ' at the start of the string should never occur, because
        # its parent isn't whitespace sensitive
        tests = [
            '1bc',
            '_Zadc123',
            '?abc',
            '    ',
            ''
        ]
        for test in tests:
            self.assertInvalid(test)

class CompiledMetaIdentifierTestCase(TestCase):
    # have to use this because to test compilation of metaidents, you need multiple syntax rules
    cls = Syntax

    def test_metaident(self):
        ebnf = 'ebnf = "a", a, "b" | ""; a = "c" | "";'
        self.assertCompiles(ebnf, 'acbb', 'acb')
        self.assertCompiles(ebnf, 'ab')
        self.assertCompiles(ebnf, 'bcb', '')
        self.assertCompiles(ebnf, '', '')

    def test_recursive(self):
        ebnf = 'base="a", rec, "b"; rec = "a", rec, "b" | "";'
        self.assertNotCompiles(ebnf, 'bc')
        self.assertNotCompiles(ebnf, 'aab')
        self.assertCompiles(ebnf, 'abc', 'ab')
        self.assertCompiles(ebnf, 'abc', 'ab')
        self.assertCompiles(ebnf, 'aabbc', 'aabb')
        self.assertNotCompiles(ebnf, 'caabbc')

    def test_invalid(self):
        ebnfs = [
            'm=m;',
            'm=(m);',
            'm=a;a=m;',
            'm=a|m;'
        ]

        for ebnf in ebnfs:
            self.assertRaises(RuleError, self.create, ebnf)