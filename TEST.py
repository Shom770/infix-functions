# coding: infix-functions


class Test:
    def __init__(self, value):
        self.value = value

    def plus(self, other):
        return self.value + other


test = Test()
test plus 4
