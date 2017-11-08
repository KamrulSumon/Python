import os
class MyClass(object):
    def __init__(self, rdfile, wrtfile):
        try:
            #self.readList = []
            #self.writeList = []
            self.unreadList = self.getAttributList(rdfile)
            self.unwriteList = self.getAttributList(wrtfile)
        except IOError:
            print("Exception Part")

    def getAttributList(self, fileToAttributeName):        
        try:
            fileName, fileExtension = os.path.splitext(fileToAttributeName)           
            if(fileExtension == '.txt'):                
                file = open(fileToAttributeName,'r')
                readList = []                    
                for line in file:                    
                    readList.extend(line.split())                   
                file.close()
                return readList             
            else:                
                print("File is not text mode")
        except:
             print('error inside try')


    def __getattribute__(self, attr_name):
        return super().__getattribute__(attr_name)

    def __setattr__(self, attr_name,value):
        return super().__setattr__(attr_name,value)

    def get_v(self, attr_name):
        try:
            if attr_name in self.unreadList:
                return "{0} is not readable".format(attr_name)          
            else:
                return super().__getattribute__(attr_name)
        except AttributeError:
            return 'Attribute is not available'  
            
    def set_v(self, attr_name,value):
        if attr_name in self.unwriteList:
            return "{0} is not writeable".format(attr_name)    
        else:
            super().__setattr__(attr_name, value)
            return "Successfully set"
            
        
        
    
c = MyClass('12.txt', 'hi.txt')
c.set_v('attr1',45)
