from ebnf.metaidentifier import MetaIdentifier
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
