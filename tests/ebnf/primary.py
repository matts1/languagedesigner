from ebnf.metaidentifier import MetaIdentifier
from ebnf.primary import Primary
from ebnf.string import String
from tests.ebnf.base import TestCase


class PrimaryTestCase(TestCase):
    cls = Primary

    def test_valid(self):
        self.assertChild('Abc 123 =', MetaIdentifier, 'identifier', 'Abc 123')
        self.assertChild('"bob \' blah" blah\' =', String, 'val', 'bob \' blah')

    def test_not_hungry(self):
        test = self.create('abc - def')
        self.assertEqual(test.get(), '-')

    def test_invalid(self):
        self.assertInvalid('')
        self.assertInvalid('?"abc"')
        self.assertInvalid('1b')
