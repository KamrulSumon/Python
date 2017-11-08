class OneValue(object):
    def __init__(self, *args):
        if len(args):
            self._value = args[0]

    def get(self):        
        return self._value

    def set(self, newValue=None):
        self._value = newValue

    # equality by equivalence
    def __eq__(self, other):
        if not isinstance(other, OneValue):
            return False

        if (self._value == other.get()):
            return True

        return False
        
    # momento
    def __repr__(self):        
        return "{}('{}')".format(self.__class__.__name__, self._value)
        

desid = "desiderata.txt"
invictus = "invictus.txt"
no_enemies = "no enemies.txt"

a = OneValue(desid, 40)
b = OneValue(desid)
c = OneValue(no_enemies)

print(a == b)
print(b == c)



