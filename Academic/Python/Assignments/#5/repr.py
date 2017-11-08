class MyClass:
    def __init__(self, iv_1, iv_2):
        self.iv_1, self.iv_2 = iv_1, iv_2

    def __repr__(self):
        return "{0}({1!r},{2!r})".format(self.__class__.__name__, self.iv_1, self.iv_2)
        #return "MyClass([1,2], {'three': 3})"

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.iv_1 == other.iv_1 and self.iv_2 == other.iv_2

    def __ne__(self, other):
        return not(self.__eq__(other))
