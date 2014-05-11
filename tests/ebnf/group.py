from ebnf.group import Group
from tests.ebnf.base import TestCase


class GroupTestCase(TestCase):
    cls = Group
    attr = 'definition'

    def assertGrouping(self, arg, min=1, max=1):
        test = self.create(arg)
        self.assertEqual((min, max), (test.min_repeats, test.max_repeats))
        return test

    def test_brackets(self):
        self.assertValid('(a)')

    def test_recursive(self):
        self.assertValid('(b, (c))')

    def test_invalid(self):
        self.assertRaises(SyntaxError, self.create, '(b, - d)')
        self.assertRaises(SyntaxError, self.create, '(b){}')
        self.assertRaises(SyntaxError, self.create, '(b){')
        self.assertRaises(SyntaxError, self.create, '(bc')
        self.assertRaises(SyntaxError, self.create, '(bc){2,1')
        self.assertGoesTo('(b)??', 4)
        self.assertGoesTo('(b)?+', 4)

    def test_end(self):
        self.assertGoesTo('(blah), blah', 6)
        self.assertGoesTo('(a, (b))', 8)

    def test_kleene_star(self):
        self.assertGrouping('(abc)*, blah', 0, float('inf'))
        self.assertGrouping('((aou - "blah")?)*, blah', 0, float('inf'))

    def test_plus(self):
        self.assertGrouping('(abc)+, blah', 1, float('inf'))
        self.assertGrouping('((test)*)+, blah', 1, float('inf'))

    def test_nums(self):
        self.assertGrouping('(a){27, 42}', 27, 42)
        self.assertGrouping('(a){3}', 3, 3)
        self.assertGrouping('(a){2,}', 2, float('inf'))
        self.assertGrouping('(a){2}', 2, 2)
        self.assertGrouping('(a){,5}', 0, 5)


class CompiledGroupTestCase(TestCase):
    cls = Group

    def test_repetitions(self):
        ebnf = '("abc"){2, 5}'
        self.assertNotCompiles(ebnf, 'abc')
        self.assertNotCompiles(ebnf, 'a')
        self.assertCompiles(ebnf, 'abcabc', 'abcabc')
        self.assertCompiles(ebnf, 'abcabcabcabcabc', 'abcabcabcabcabc')
        self.assertCompiles(ebnf, 'abcabcabcabcabcabc', 'abcabcabcabcabc')
