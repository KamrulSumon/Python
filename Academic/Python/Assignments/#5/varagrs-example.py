def f(*args):
    for arg in args:
        print("arg is {0}".format(arg))

def f1(*args):
    for (argno, arg) in enumerate(args):
        print("vararg #{0} is {1}".format(argno, arg))

def f2(*args):
    for (argno, arg) in enumerate(args):
        print("vararg #{0} is {1} and type is: {2}".format(argno, arg, type(arg)))

class TextFile:
    
    def __init__(self, *args):
        
        assert(len(args) == 1 or len(args) == 2), "Length {0} is not expected".format(len(args))
            
        if (len(args) == 2):
            self.filename = args[0]
            self.position = args[1]
        else:
            self.filename = args
            self.position = 0
        

    def print(self):
        print("Name: {0}, Position: {1}".format(self.filename, self.position))
        

fileCollection = []

def f3(*args):
    for arg in args:        
        if isinstance(arg, str):
            textFile = TextFile(arg, 0)
        elif isinstance(arg, tuple):
            textFile = TextFile(arg[0], arg[1]['position'])
            
        fileCollection.append(textFile)
        



def print_file_collection():
    for tf in fileCollection:
        tf.print()

desid = "desiderata.txt"
invictus = "invictus.txt"
no_enemies = "no enemies.txt"
