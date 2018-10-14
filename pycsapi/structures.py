'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from ctypes import *
import math

class VECTOR(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def dotProduct(self, dot):
        return self.x * dot.x + self.y * dot.y + self.z * dot.z
    
    def distanceFrom(self, other):
        return math.sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2))
    
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

class lump_t(Structure):
    _fields_ = [('fileofs', c_int), ('filelen', c_int), ('version', c_int), ('fourCC', c_char * 4)]

class dheader_t(Structure):
    _fields_ = [('ident', c_int), ('version', c_int), ('lumps', lump_t * 64), ('mapRevision', c_int)]

class dplane_t(Structure):
    _fields_ = [('normal', VECTOR), ('dist', c_float), ('type', c_int)]

class dnode_t(Structure):
    _fields_ = [('planenum', c_int), ('children', c_int * 2), ('mins', c_short * 3), ('maxs', c_short * 3), ('firsface', c_ushort), ('numfaces', c_ushort), ('area', c_short)]

class dleaf_t(Structure):
    _fields_ = [('contents', c_int), ('cluster', c_short), ('pad_bitfields', c_byte * 2), ('mins', c_short * 3), ('maxs', c_short * 3), ('firstleafface', c_ushort), ('numleaffaces', c_ushort), ('firstleafbrush', c_ushort), ('numleafbrushes', c_ushort), ('leafWaterDataID', c_short)]