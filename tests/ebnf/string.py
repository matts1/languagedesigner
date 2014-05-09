from ebnf.string import String
from tests.ebnf.base import TestCase


# string = ('"', (anything - '"')*, '"') | ("'", (anything - "'")*, "'")
class StringTestCase(TestCase):
    cls = String
    attr = 'val'

    def test_valid(self):
        tests = [
            ('\'abc\' blah', 'abc'),
            ('"abc def" blah', 'abc def'),
            ('\'abc"def\'oeuaou', 'abc"def'),
            ('"a\'" "\'b"', 'a\''),
            ('"a" - "b"', 'a')
        ]
        for test in tests:
            self.assertValid(*test)

    def test_invalid(self):
        # a ' ' at the start of the string should never occur, because
        # its parent isn't whitespace sensitive
        self.assertInvalid('')
        tests = [
            '\'abc',
            '"abc',
            '\'',
            '"abc\'',
            '\'abc"',
        ]
        for test in tests:
            self.assertRaises(SyntaxError, self.create, test)
