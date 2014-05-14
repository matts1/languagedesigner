from unittest import TestCase


class TestCase(TestCase):
    def create(self, arg):
        return self.cls(None, arg)

    def assertValid(self, arg, correct=None, **kwargs):
        res = self.create(arg)
        if not res.valid:
            raise AssertionError('%s should have been valid given the input %s' % (
                self.cls.__name__,
                arg
            ))
        if correct is not None:
            self.assertEqual(getattr(res, self.attr), correct)
        for arg in kwargs:
            self.assertEqual(getattr(res, arg), kwargs[arg])
        return res

    def assertCompiles(self, ebnf, program, correct=None, **kwargs):
        res = self.create(ebnf).compile(parent=None, text=program)
        if not res.valid:
            raise AssertionError('%s should have compiled given the ebnf "%s" and program "%s"' % (
                self.cls.__name__,
                ebnf,
                program
            ))
        if correct is not None:
            try:
                self.assertEqual(getattr(res, self.attr), correct)
            except AttributeError:
                self.assertEqual(res.get_text(), correct)
        for arg in kwargs:
            self.assertEqual(getattr(res, arg), kwargs[arg])
        return res

    def assertNotCompiles(self, ebnf, program):
        try:
            res = self.create(ebnf).compile(parent=None, text=program)
            if res.valid:
                raise AssertionError('%s should not have been compiled given the ebnf "%s" and '
                                     'program "%s". Compiled to %s' % (
                    self.cls.__name__,
                    ebnf,
                    program,
                    res
                ))
            return res
        except SyntaxError as e:
            if e.message not in ['The program is not valid', 'Program stopped matching EBNF early']:
                raise e

    def assertInvalid(self, arg):
        res = self.create(arg)
        if res.valid:
            raise AssertionError('%s should not have been valid given the input %s' % (
                self.cls.__name__,
                arg
            ))
        return res

    def assertChild(self, arg, cls, attr, correct):
        children = self.assertValid(arg).children
        self.assertGreater(children, 0)
        child = children[0]
        self.assertEqual(child.__class__, cls)
        self.assertEqual(getattr(child, attr), correct)

    def assertNumChildren(self, arg, num):
        res = self.assertValid(arg)
        self.assertEqual(num, len(res.children))
        return res

    def assertGoesTo(self, arg, num):
        res = self.assertValid(arg)
        self.assertEqual(res.upto, num)
        return res

    def assertRaises(self, excClass, callableObj=None, *args, **kwargs):
        try:
            return super(TestCase, self).assertRaises(excClass, callableObj, *args, **kwargs)
        except AssertionError as e:
            print 'args are', args, 'kwargs are', kwargs
            raise e
