# coding: utf-8
from vdb import *
import sys
def set_trace():
    VDB().set_trace(sys._getframe().f_back)
__all__=[VDB, set_trace]
