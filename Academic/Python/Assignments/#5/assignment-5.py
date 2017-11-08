import os
import ctypes

class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        file_name = args[0]

        if file_name not in cls._instances:
            obj = super(Singleton, cls).__call__(*args, **kwargs)
            Singleton._instances[file_name] = obj
        else:
            Singleton._instances[file_name].__init__(*args, **kwargs)

        return Singleton._instances[file_name]


class TextFile(metaclass=Singleton):

    def __init__(self, filename, position = 0):

        self.filename = filename
        self.position = position

        try:

            self.file_handle = open(self.filename, 'r')
            self.file_handle.seek(self.position)

        except IOError as e:
            print("Can't access '{0}': {1}".format(self.filename, e))

    def seek(self, offset):
        self.position = offset
        self.file_handle.seek(self.position)

    def readline(self):
        read_str = self.file_handle.readline()
        self.position = self.file_handle.tell()
        return read_str

    def close(self):
        self.file_handle.close()

    def print_value(self):
        print(TextFileCollection._value)


    def __repr__(self):
        return "{}('{}',{})".format(self.__class__.__name__, self.filename, self.position)

class TextFileCollection:
    _me = "?? TextFileCollection.{}: ?? "    

    _e_value = lambda e: '' if 'value' not in dir(e) else ": " + e.value
    _value = None

    _global_dict = {}

    def __init__(self, *args):       
        if len(args): TextFileCollection._value = args[0]      

        rept = []
        fileList = []
        self.ownList = []
        self._fileListCollection = []

        # Local _dict is maintained to factilitate repr.
        # This could have been achieved just by the filename and the _global_dict
        # Searching through the key in _global_dict did not seem more clean
        self._dict = {}        

        for arg in args:
            if arg in fileList:
                rept.append(arg)
            else:
                fileList.append(arg)        

        if len(rept) > 0:
            self.assert_defined_collection("init",set(rept),"duplicate filename in filespec.{}")
        else:
            for file_obj in fileList:
                referenced_text_collections = []
                
                if isinstance(file_obj, tuple):
                    file_name = file_obj[0]
                    position = file_obj[1]['position']
                    
                    if 'references' in file_obj[1]:
                        for collection_obj in file_obj[1]['references']:
                            referenced_text_collections.append(ctypes.cast(id(collection_obj), ctypes.py_object).value)                        
                        
                    self.ownList.append(file_name)                
                    
                else:
                    file_name = file_obj
                    position = 0
                    self.ownList.append(file_name)

                txtFile = TextFile(file_name, position)

                if txtFile not in self._fileListCollection:
                    self._fileListCollection.append(txtFile)                                 

                if txtFile not in TextFileCollection._global_dict:
                    TextFileCollection._global_dict[txtFile] = [self]
                else:
                    TextFileCollection._global_dict[txtFile].append(self)
                    

                # Add all the referenced objects for this file into the collection for this key
                TextFileCollection._global_dict[txtFile].extend(referenced_text_collections)

                # Copy back the references to local copy of the dictionary                
                # E.g., If c0 = TextFileCollection(desid, invictus) and if c2 = TextFileCollection(invictus).
                # The references to invictus gets coped in c0 too (c0 kept object reference to collection object),
                # even though c0["invictus"] had only one reference before c2 was created.
                # This can be viewed by printing c0 and c2
                # Finding the key could have also been achieved with c0.searchkey but we liked the local _dict approach
                self._dict[txtFile] = TextFileCollection._global_dict[txtFile]                
                

    #def get(self):
    #    self.assert_defined('get')
    #    return TextFileCollection._value

    #def set(self, newValue=None):        
    #    TextFileCollection._value = newValue

    #def unset(self):  del TextFileCollection._value

    # Used for debugging
    def printstate(self):
        print("\n\nLocal dictionary:::::::::::::::::::::::::::::::\n")
        print(self._dict)

        print("\n\nLocal fileListCollection:::::::::::::::::::::::::::::::\n")
        print(self._fileListCollection)

        print("\n\nGlobal dictionary::::::::::::::::::::::::::::::::::::::::::\n")
        print(TextFileCollection._global_dict)

    def search(self, filename):
        found_file = None

        for file_object in self._fileListCollection:
            if (file_object.filename == filename):
                found_file = file_object
                break
        return found_file

    # To make sure file is not in the global dictionary
    def searchkey(self, filename):
        found_file = None

        for file_object in TextFileCollection._global_dict.keys():
            if (file_object.filename == filename):                
                found_file = file_object
                break
        return found_file

    def __eq__(self, other):
        if not isinstance(other, TextFileCollection): return False
		
        if (id(self) == id(other)):
            return True   
        else:
            return False    

    # Although equality of TextFileCollection was not achieved, format_str makes sure new TextFileCollection object is created when we eval repr.
    def format_str(self):        
        param_str = ""       
        
        if len(self._dict.keys()) > 0:
            for key in self._dict.keys():
                param_str += "('{0}',".format(key.filename)                
                reference_objects = self._dict[key]
                ids = []
                for reference_obj in reference_objects:
                    ids.append(id(reference_obj))
                    
                param_str += "{{'position':{0}, 'references': {1}}}),".format(key.position, ids)                

        param_str = "{}({})".format(self.__class__.__name__, param_str)

        key_size = len(self._dict.keys())
        
        return param_str

    def __repr__(self):        
        return self.format_str()
        
    def assert_defined(self, routine, file_error, err_msg):
        assert 'value' in dir(self), (TextFileCollection._me +  err_msg + " " + str(id(self))).format(routine, file_error)

    def assert_defined_collection(self, routine, file_error, err_msg):
        assert 'value' in dir(self), (TextFileCollection._me +  err_msg + " ").format(routine, file_error)

    def seek(self, filename, offset):
        file_obj = self.search(filename)

        assert file_obj != None, self.assert_defined('seek', filename, 'handle on {} not held by')
        file_obj.seek(offset)

    def readline(self, filename):
        file_obj = self.search(filename)
        file_obj_global = self.searchkey(filename)
        
        assert file_obj_global != None, self.assert_defined_collection('readline', filename, 'handle on {} not is collection')        
        assert file_obj != None, self.assert_defined('readline', filename, 'handle on {} not held by')
        return file_obj.readline()

    def close(self, filename):
        file_obj = self.search(filename)

        # First remove self from the local key (file) it was referenced
        exists = False
		
        if file_obj in self._dict:
            if self in self._dict[file_obj]:               
                exists = True
                self._dict[file_obj].remove(self)
                del self._dict[file_obj]
                self._fileListCollection.remove(file_obj)

	# If this object does not hold a reference show an error
        assert exists == True, self.assert_defined('close', filename, 'handle on {} not held by')        

	# We also need to remove this object from global reference
        if self in TextFileCollection._global_dict[file_obj]:            
            TextFileCollection._global_dict[file_obj].remove(self)
        
	# Now we need to make sure file gets closed, if all of its references have been deleted
        if file_obj in TextFileCollection._global_dict:
            if len(TextFileCollection._global_dict[file_obj]) == 0:                
                del TextFileCollection._global_dict[file_obj]
                file_obj.close()

# Comment all out

#desid = "desiderata.txt"
#invictus = "invictus.txt"
#no_enemies = "no enemies.txt"

#c0 = TextFileCollection(desid, invictus)
#c1 = TextFileCollection((desid, {'position':40}), no_enemies)
