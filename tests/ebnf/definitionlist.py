from ebnf.definitionlist import DefinitionList
from tests.ebnf.base import TestCase


class DefinitionListTestCase(TestCase):
    cls = DefinitionList

    def test_one(self):
        self.assertNumChildren('valid - invalid , other', 1)
        self.assertNumChildren('"term" , "other" - "notother"', 1)
        self.assertNumChildren('"term" - "not term"', 1)

    def test_multi(self):
        test = self.assertNumChildren('v-"i" , c| blah blah| bob; blah| blah', 3)
        self.assertEqual(test.children[0].upto, 9)
        self.assertEqual(test.children[1].upto, 20)
        self.assertEqual(test.children[2].upto, 25)
        self.assertNumChildren('a,b,c| def| ghi; blah| blah', 3)

    def test_invalid(self):
        self.assertRaises(SyntaxError, self.create, 'blah| v , - invalid')

    def test_end(self):
        self.assertGoesTo('abc), def', 3)


class CompiledDefinitionListTestCase(TestCase):
    cls = DefinitionList

    def test_if(self):
        self.assertCompiles('"ab" | "cd"', 'abcd', 'ab')
        self.assertCompiles('"ab" | "cd"', 'cde', 'cd')
        self.assertCompiles('"ab" | "cd"', 'cd', 'cd')
        self.assertCompiles('"ab" | "cd", "ef"', 'abefg', 'ab')  # ab | (cd, ef), so compiles to ab
        self.assertCompiles('"ab" | "cd", "ef"', 'cdefg', 'cdef')
        self.assertNotCompiles('"ab" | "cd"', 'ac')
