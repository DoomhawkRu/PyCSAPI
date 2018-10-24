'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import ctypes
import math

class VECTOR(ctypes.Structure):
    _fields_ = [('x', ctypes.c_float), ('y', ctypes.c_float), ('z', ctypes.c_float)]
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def dotProduct(self, dot):
        return self.x * dot.x + self.y * dot.y + self.z * dot.z
    
    def distanceFrom(self, other):
        return math.sqrt(((self.x - other.x) * (self.x - other.x)) + ((self.y - other.y) * (self.y - other.y)) + ((self.z - other.z) * (self.z - other.z)))
    
    def __add__(self, other):
        return VECTOR(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return VECTOR(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __itruediv__(self, other):
        if type(other) is VECTOR:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        else:
            self.x /= other
            self.y /= other
            self.z /= other
        return self

class lump_t(ctypes.Structure):
    _fields_ = [('fileofs', ctypes.c_int), ('filelen', ctypes.c_int), ('version', ctypes.c_int), ('fourCC', ctypes.c_char * 4)]

class dheader_t(ctypes.Structure):
    _fields_ = [('ident', ctypes.c_int), ('version', ctypes.c_int), ('lumps', lump_t * 64), ('mapRevision', ctypes.c_int)]

class dplane_t(ctypes.Structure):
    _fields_ = [('normal', VECTOR), ('dist', ctypes.c_float), ('type', ctypes.c_int)]

class dnode_t(ctypes.Structure):
    _fields_ = [('planenum', ctypes.c_int), ('children', ctypes.c_int * 2), ('mins', ctypes.c_short * 3), ('maxs', ctypes.c_short * 3), ('firsface', ctypes.c_ushort), ('numfaces', ctypes.c_ushort), ('area', ctypes.c_short)]

class dleaf_t(ctypes.Structure):
    _fields_ = [('contents', ctypes.c_int), ('cluster', ctypes.c_short), ('pad_bitfields', ctypes.c_byte * 2), ('mins', ctypes.c_short * 3), ('maxs', ctypes.c_short * 3), ('firstleafface', ctypes.c_ushort), ('numleaffaces', ctypes.c_ushort), ('firstleafbrush', ctypes.c_ushort), ('numleafbrushes', ctypes.c_ushort), ('leafWaterDataID', ctypes.c_short)]