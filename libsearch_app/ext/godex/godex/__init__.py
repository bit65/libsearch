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
    modules = []
    try:
        msg = GoString(classes, len(classes))
        d = lib.getlib(msg)
        modules = getattr(d, d._fields_[0][0]).split('\n')
    except e:
        pass
    return modules
