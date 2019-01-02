from ctypes import *
import os

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), 
                ("len", c_longlong), ("cap", c_longlong)]

lib = cdll.LoadLibrary(os.path.dirname(__file__) + "/godexlib.so")
lib.getlib.argtypes = [GoString]
lib.getlib.restype = GoString 

def getClasses(classes):
    msg = GoString(classes, len(classes))
    d = lib.getlib(msg)
    # for name, dtype in d._fields_:
    #     print name, getattr(d, name)

    modules = getattr(d, d._fields_[0][0]).split('\n')
    return modules
