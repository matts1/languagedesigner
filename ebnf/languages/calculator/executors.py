class Digit():
    identifier = 'digit'

    def setup(self):
        print "setting up"

    def execute(self):
        return self.val  # define this first

    def teardown(self):
        return

    def pprint(self):
        return self.val

class Expression():
    identifier = 'expression'

    def setup(self):
        return

    def execute(self):
        if self.tree.selected == 0:
            print "number", self.tree
        else:
            print "expressions", self.tree

    def teardown(self):
        return

class Number(Digit):
    identifier = 'number'

    def setup(self):
        return

    def execute(self):
        if self.tree.selected == 0:
            print "number", self.tree
        else:
            print "expressions", self.tree

    def teardown(self):
        return

class Operator():
    identifier = 'operator'

    def setup(self):
        return

    def execute(self):
        return

    def teardown(self):
        return

    def pprint(self):
        return

bob = 'blah'  # testing that it doesn't try and import this
