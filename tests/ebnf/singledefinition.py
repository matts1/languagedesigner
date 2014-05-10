from ebnf.singledefinition import SingleDefinition
from tests.ebnf.base import TestCase


class SingleDefinitionTestCase(TestCase):
    cls = SingleDefinition

    def test_one(self):
        self.assertNumChildren('valid - invalid', 1)
        self.assertNumChildren('"term"', 1)
        self.assertNumChildren('"term" - "not term"', 1)

    def test_multi(self):
        self.assertNumChildren('valid - "invalid" , c', 2)
        self.assertNumChildren('a , "b" , c', 3)

    def test_invalid(self):
        self.assertRaises(SyntaxError, self.create, 'v , - invalid')

    def test_compiler(self):
        self.assertCompiles('"a", \'b\', "def"', 'abdef', 'abdef')
        self.assertCompiles('"a", \'b\', "def"', 'abdefg', 'abdef')
