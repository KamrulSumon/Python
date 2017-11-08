class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:      # instantiate shared class instance on first object instantiation 
          Singleton._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:   # reinvoke __init__ for the lone instance on subsequent instantiations.  remove clause if re-init not desired
          Singleton._instances[cls].__init__(*args, **kwargs) 
        return Singleton._instances[cls]


class TextFile(metaclass=Singleton):
    def __init__(self, name, position): # This is variable *args
        self.name = name
        self.position = position
        
        try:
            self.file_handle = open(name)
            self.file_handle.seek(self.position)
            
        except IOError as e:
            print ("File error")

    def readline(self):
        self.file_handle.readline()
        
    def close(self):
        self.file_handle.close()
        
    def get_name(self):
        return self.name
    
    def get_position(self):
        return self.position
    
    def seek(self, position):
        self.position = position
        
    def __eq__(self, other):
        return self.name == other.name

class TextFileCollection:
    #_me = "?? TextFileCollection.{}: "
    _fileListCollection = []
    _dict = {}

    def __init__(self, *args, **kwargs):        
        for key, value in kwargs.items():
            print ("Key: {0}, Value: {1}".format(key, value))
            TextFileCollection._fileListCollection.append(TextFile(key, value))

    def search(self, filename):
        found_file = None
        for fileobj in TextFileCollection._fileListCollection:
            if filename == fileobj.get_name():
                found_file = fileobj
                break
        return found_file
            

    def print_files(self):
        for file in TextFileCollection._fileListCollection:
            print("Name: {0}, Position: {1}".format(file.get_name(), file.get_position()))

    def file_list(self):
        return TextFileCollection._fileListCollection

    def seek(self, filename, position):
        fileobj = self.search(filename)

        print(fileobj)
        
        if (fileobj is not None):        
            fileobj.seek(position)

fc = TextFileCollection(a=2, b = 5)

