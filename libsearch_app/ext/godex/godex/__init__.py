import os

from ctypes import *
class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

# class GoSlice(Structure):
#     _fields_ = [("data", POINTER(c_void_p)), 
#                 ("len", c_longlong), ("cap", c_longlong)]

lib = cdll.LoadLibrary(os.path.dirname(__file__) + "/godexlib.so")
lib.GetLib.argtypes = [GoString]
lib.GetLib.restype = GoString 

def getClasses(classes):
    modules = []
    print "getting classes for", classes
    try:
        msg = GoString(classes, len(classes))
        
        
        d = lib.GetLib(msg)
        # import code
        # code.interact(local=locals())
        print "size of string", len(getattr(d,"p"))
        
        if len(getattr(d,"p")) > 0:
            modules = getattr(d, "p").split('\n')
    except Exception as e:
        print "Exception", e
        pass

    return filter(None,modules)
