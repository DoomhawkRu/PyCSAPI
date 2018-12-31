'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import ctypes
import ctypes.wintypes
import math

try:
    from pycsapi import constant
    from pycsapi import structures
except:
    import constant
    import structures

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    return abs(distancex), abs(distancey)

def check_angles(pitch, yaw):
    if pitch > 89 or pitch < -89 or yaw > 360 or yaw < -360:
        return False
    return True

def distance_to_angle(distance, punch = (0, 0)):
    pitch, yaw = 0, 0
    if not distance:
        return (pitch, yaw)
    yaw = (math.atan2(distance[1], distance[0]) * 180 / math.pi) - (punch[1] * 2)
    pitch = (math.atan2(-distance[2], math.sqrt(distance[0] * distance[0] + distance[1] * distance[1] + distance[2] * distance[2])) * 180 / math.pi) - (punch[0] * 2)
    pitch, yaw = normalize_angles(pitch, yaw)
    return (pitch, yaw)

def get_client_size(title):
    window_data = get_window(title)
    return (window_data[2] - window_data[0], window_data[3] - window_data[1])

def get_hitgroup_damage_mult(hitgroup):
    if hitgroup == constant.HITGROUP_GENERIC:
        return 1.0
    if hitgroup == constant.HITGROUP_HEAD:
        return 4.0
    if hitgroup == constant.HITGROUP_CHEAT:
        return 1.0
    if hitgroup == constant.HITGROUP_STOMACH:
        return 1.25
    if hitgroup == constant.HITGROUP_LEFTARM:
        return 1.0
    if hitgroup == constant.HITGROUP_RIGHTARM:
        return 1.0
    if hitgroup == constant.HITGROUP_LEFTLEG:
        return 0.75
    if hitgroup == constant.HITGROUP_RIGHTLEG:
        return 0.75
    if hitgroup == constant.HITGROUP_GEAR:
        return 1.0
    return 1.0

def get_scale_damage(hitgroup, entity, weapon_armor_ratio, current_damage):
    current_damage *= get_hitgroup_damage_mult(hitgroup)
    if entity.get_armor() > 0:
        if hitgroup == constant.HITGROUP_HEAD:
            if entity.is_has_helmet():
                current_damage *= weapon_armor_ratio * 0.5
        else:
            current_damage *= weapon_armor_ratio * 0.5
    return current_damage

def get_window(title):
    rect = ctypes.wintypes.RECT()
    client_rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(ctypes.windll.user32.FindWindowW(None, title), ctypes.byref(rect))
    ctypes.windll.user32.GetClientRect(ctypes.windll.user32.FindWindowW(None, title), ctypes.byref(client_rect))
    client = (client_rect.right, client_rect.bottom)
    window = ((rect.left, rect.top), (rect.right, rect.bottom))
    if window[1] == client:
        return window
    else:
        diffx = ctypes.windll.user32.GetSystemMetrics(0x6)
        diffy = ctypes.windll.user32.GetSystemMetrics(0x4)
        return (window[0][0] + diffx, window[0][1] + diffy, window[1][0], window[1][1])

def health_to_rgb(health):
    if health > 100 or health < 0:
        return (0, 0, 0)
    return (int(255 - health * 2.55), int(health * 2.55), 0)

def is_key_pressed(id):
    return ctypes.windll.user32.GetAsyncKeyState(id)

def normalize_angles(pitch, yaw):
    while pitch > 89:
        pitch -= 360
    while pitch < -89:
        pitch += 360
    while yaw > 180:
        yaw -= 360
    while yaw < -180:
        yaw += 360
    return (pitch, yaw)

def world_to_screen(_from, matrix, title):
    w = matrix[3][0] * _from[0] + matrix[3][1] * _from[1] + matrix[3][2] * _from[2] + matrix[3][3]
    if w < 0.01:
        return False
    width, height = get_client_size(title)
    x = width / 2 + 0.5 * (matrix[0][0] * _from[0] + matrix[0][1] * _from[1] + matrix[0][2] * _from[2] + matrix[0][3]) * (1 / w) * width + 0.5
    y = height / 2 - 0.5 * (matrix[1][0] * _from[0] + matrix[1][1] * _from[1] + matrix[1][2] * _from[2] + matrix[1][3]) * (1 / w) * height + 0.5
    return (x, y)

class ConvarFlags:
    def __init__(self, value):
        self.FCVAR_UNREGISTERED = bool(value & constant.FCVAR_UNREGISTERED)
        self.FCVAR_DEVELOPMENTONLY = bool(value & constant.FCVAR_DEVELOPMENTONLY)
        self.FCVAR_GAMEDLL = bool(value & constant.FCVAR_GAMEDLL)
        self.FCVAR_CLIENTDLL = bool(value & constant.FCVAR_CLIENTDLL)
        self.FCVAR_HIDDEN = bool(value & constant.FCVAR_HIDDEN)
        self.FCVAR_PROTECTED = bool(value & constant.FCVAR_PROTECTED)
        self.FCVAR_SPONLY = bool(value & constant.FCVAR_SPONLY)
        self.FCVAR_ARCHIVE = bool(value & constant.FCVAR_ARCHIVE)
        self.FCVAR_NOTIFY = bool(value & constant.FCVAR_NOTIFY)
        self.FCVAR_USERINFO = bool(value & constant.FCVAR_USERINFO)
        self.FCVAR_PRINTABLEONLY = bool(value & constant.FCVAR_PRINTABLEONLY)
        self.FCVAR_UNLOGGED = bool(value & constant.FCVAR_UNLOGGED)
        self.FCVAR_NEVERASSTRING = bool(value & constant.FCVAR_NEVERASSTRING)
        self.FCVAR_REPLICATED = bool(value & constant.FCVAR_REPLICATED)
        self.FCVAR_CHEAT = bool(value & constant.FCVAR_CHEAT)
        self.FCVAR_EMPTY1 = bool(value & constant.FCVAR_EMPTY1)
        self.FCVAR_DEMO = bool(value & constant.FCVAR_DEMO)
        self.FCVAR_DONOTRECORD = bool(value & constant.FCVAR_DONOTRECORD)
        self.FCVAR_EMPTY2 = bool(value & constant.FCVAR_EMPTY2)
        self.FCVAR_EMPTY3 = bool(value & constant.FCVAR_EMPTY3)
        self.FCVAR_RELOADMATERIALS = bool(value & constant.FCVAR_RELOADMATERIALS)
        self.FCVAR_RELOADTEXTURES = bool(value & constant.FCVAR_RELOADTEXTURES)
        self.FCVAR_NOTCONNECTED = bool(value & constant.FCVAR_NOTCONNECTED)
        self.FCVAR_MATERIALSYSTEMTHREAD = bool(value & constant.FCVAR_MATERIALSYSTEMTHREAD)
        self.FCVAR_ARCHIVEXBOX = bool(value & constant.FCVAR_ARCHIVEXBOX)
        self.FCVAR_ACCESSIBLEFROMTHREADS = bool(value & constant.FCVAR_ACCESSIBLEFROMTHREADS)
        self.FCVAR_EMPTY4 = bool(value & constant.FCVAR_EMPTY4)
        self.FCVAR_EMPTY5 = bool(value & constant.FCVAR_EMPTY5)
        self.FCVAR_SERVERCANEXECUTE = bool(value & constant.FCVAR_SERVERCANEXECUTE)
        self.FCVAR_SERVERCANNOTQUERY = bool(value & constant.FCVAR_SERVERCANNOTQUERY)
        self.FCVAR_CLIENTCOMMANDCANEXECUTE = bool(value & constant.FCVAR_CLIENTCOMMANDCANEXECUTE)
    
    def compile_to_str(self):
        str = 'Unregistered = {}'.format(self.FCVAR_UNREGISTERED) + '\n'
        str += 'DevelopmentOnly = {}'.format(self.FCVAR_DEVELOPMENTONLY) + '\n'
        str += 'GameDLL = {}'.format(self.FCVAR_GAMEDLL) + '\n'
        str += 'ClientDLL = {}'.format(self.FCVAR_CLIENTDLL) + '\n'
        str += 'Hidden = {}'.format(self.FCVAR_HIDDEN) + '\n'
        str += 'Protected = {}'.format(self.FCVAR_PROTECTED) + '\n'
        str += 'Sponly = {}'.format(self.FCVAR_SPONLY) + '\n'
        str += 'Archive = {}'.format(self.FCVAR_ARCHIVE) + '\n'
        str += 'Notify = {}'.format(self.FCVAR_NOTIFY) + '\n'
        str += 'UserInfo = {}'.format(self.FCVAR_USERINFO) + '\n'
        str += 'PrintableOnly = {}'.format(self.FCVAR_PRINTABLEONLY) + '\n'
        str += 'Unlogged = {}'.format(self.FCVAR_UNLOGGED) + '\n'
        str += 'NeverAsString = {}'.format(self.FCVAR_NEVERASSTRING) + '\n'
        str += 'Replicated = {}'.format(self.FCVAR_REPLICATED) + '\n'
        str += 'Cheat = {}'.format(self.FCVAR_CHEAT) + '\n'
        str += 'Empty1 = {}'.format(self.FCVAR_EMPTY1) + '\n'
        str += 'Demo = {}'.format(self.FCVAR_DEMO) + '\n'
        str += 'DoNotRecord = {}'.format(self.FCVAR_DONOTRECORD) + '\n'
        str += 'Empty2 = {}'.format(self.FCVAR_EMPTY2) + '\n'
        str += 'Empty3 = {}'.format(self.FCVAR_EMPTY3) + '\n'
        str += 'ReloadMaterials = {}'.format(self.FCVAR_RELOADMATERIALS) + '\n'
        str += 'ReloadTextures = {}'.format(self.FCVAR_RELOADTEXTURES) + '\n'
        str += 'NotConnected = {}'.format(self.FCVAR_NOTCONNECTED) + '\n'
        str += 'MaterialSystemThread = {}'.format(self.FCVAR_MATERIALSYSTEMTHREAD) + '\n'
        str += 'ArchiveBox = {}'.format(self.FCVAR_ARCHIVEXBOX) + '\n'
        str += 'AccessibleFromThreads = {}'.format(self.FCVAR_ACCESSIBLEFROMTHREADS) + '\n'
        str += 'Empty4 = {}'.format(self.FCVAR_EMPTY4) + '\n'
        str += 'Empty5 = {}'.format(self.FCVAR_EMPTY5) + '\n'
        str += 'ServerCanExecute = {}'.format(self.FCVAR_SERVERCANEXECUTE) + '\n'
        str += 'ServerCannotQuery = {}'.format(self.FCVAR_SERVERCANNOTQUERY) + '\n'
        str += 'ClientCommandCanExecute = {}'.format(self.FCVAR_CLIENTCOMMANDCANEXECUTE)
        return str
    
    def compile(self):
        value = constant.FCVAR_UNREGISTERED if self.FCVAR_UNREGISTERED else 0
        value += constant.FCVAR_DEVELOPMENTONLY if self.FCVAR_DEVELOPMENTONLY else 0
        value += constant.FCVAR_GAMEDLL if self.FCVAR_GAMEDLL else 0
        value += constant.FCVAR_CLIENTDLL if self.FCVAR_CLIENTDLL else 0
        value += constant.FCVAR_HIDDEN if self.FCVAR_HIDDEN else 0
        value += constant.FCVAR_PROTECTED if self.FCVAR_PROTECTED else 0
        value += constant.FCVAR_SPONLY if self.FCVAR_SPONLY else 0
        value += constant.FCVAR_ARCHIVE if self.FCVAR_ARCHIVE else 0
        value += constant.FCVAR_NOTIFY if self.FCVAR_NOTIFY else 0
        value += constant.FCVAR_USERINFO if self.FCVAR_USERINFO else 0
        value += constant.FCVAR_PRINTABLEONLY if self.FCVAR_PRINTABLEONLY else 0
        value += constant.FCVAR_UNLOGGED if self.FCVAR_UNLOGGED else 0
        value += constant.FCVAR_NEVERASSTRING if self.FCVAR_NEVERASSTRING else 0
        value += constant.FCVAR_REPLICATED if self.FCVAR_REPLICATED else 0
        value += constant.FCVAR_CHEAT if self.FCVAR_CHEAT else 0
        value += constant.FCVAR_EMPTY1 if self.FCVAR_EMPTY1 else 0
        value += constant.FCVAR_DEMO if self.FCVAR_DEMO else 0
        value += constant.FCVAR_DONOTRECORD if self.FCVAR_DONOTRECORD else 0
        value += constant.FCVAR_EMPTY2 if self.FCVAR_EMPTY2 else 0
        value += constant.FCVAR_EMPTY3 if self.FCVAR_EMPTY3 else 0
        value += constant.FCVAR_RELOADMATERIALS if self.FCVAR_RELOADMATERIALS else 0
        value += constant.FCVAR_RELOADTEXTURES if self.FCVAR_RELOADTEXTURES else 0
        value += constant.FCVAR_NOTCONNECTED if self.FCVAR_NOTCONNECTED else 0
        value += constant.FCVAR_MATERIALSYSTEMTHREAD if self.FCVAR_MATERIALSYSTEMTHREAD else 0
        value += constant.FCVAR_ARCHIVEXBOX if self.FCVAR_ARCHIVEXBOX else 0
        value += constant.FCVAR_ACCESSIBLEFROMTHREADS if self.FCVAR_ACCESSIBLEFROMTHREADS else 0
        value += constant.FCVAR_EMPTY4 if self.FCVAR_EMPTY4 else 0
        value += constant.FCVAR_EMPTY5 if self.FCVAR_EMPTY5 else 0
        value += constant.FCVAR_SERVERCANEXECUTE if self.FCVAR_SERVERCANEXECUTE else 0
        value += constant.FCVAR_SERVERCANNOTQUERY if self.FCVAR_SERVERCANNOTQUERY else 0
        value += constant.FCVAR_CLIENTCOMMANDCANEXECUTE if self.FCVAR_CLIENTCOMMANDCANEXECUTE else 0
        return value

class RayTracing:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
        self.direction_inverse = ((1 / self.direction[0]) if self.direction[0] != 0 else 0, (1 / self.direction[1]) if self.direction[1] != 0 else 0, (1 / self.direction[2]) if self.direction[2] != 0 else 0)
    
    def trace(self, left_bottom, right_top, distance):
        if self.direction[0] == 0 and (self.origin[0] < min(left_bottom[0], right_top[0]) or self.origin[0] > max(left_bottom[0], right_top[0])):
            return [False, distance]
        if self.direction[1] == 0 and (self.origin[1] < min(left_bottom[1], right_top[1]) or self.origin[1] > max(left_bottom[1], right_top[1])):
            return [False, distance]
        if self.direction[2] == 0 and (self.origin[2] < min(left_bottom[2], right_top[2]) or self.origin[2] > max(left_bottom[2], right_top[2])):
            return [False, distance]
        t1 = (left_bottom[0] - self.origin[0]) * self.direction_inverse[0]
        t2 = (right_top[0] - self.origin[0]) * self.direction_inverse[0]
        t3 = (left_bottom[1] - self.origin[1]) * self.direction_inverse[1]
        t4 = (right_top[1] - self.origin[1]) * self.direction_inverse[1]
        t5 = (left_bottom[2] - self.origin[2]) * self.direction_inverse[2]
        t6 = (right_top[2] - self.origin[2]) * self.direction_inverse[2]
        tmin = max(max(min(t1, t2), min(t3, t4)), min(t5, t6))
        tmax = min(min(max(t1, t2), max(t3, t4)), max(t5, t6))
        if tmax < 0:
            distance = tmax
            return [False, distance]
        if tmin > tmax:
            distance = tmax
            return [False, distance]
        distance = tmin
        return [True, distance]
    
    @staticmethod
    def angle_to_direction(angle):
        angle = (angle[0] * math.pi / 180, angle[1] * math.pi / 180)
        sinYaw = math.sin(angle[1])
        cosYaw = math.cos(angle[1])
        sinPitch = math.sin(angle[0])
        cosPitch = math.cos(angle[0])
        return (cosPitch * cosYaw, cosPitch * sinYaw, -sinPitch)

class BSPParsing:
    def __init__(self, bsp):
        self.handle = open(bsp, 'rb')
        self.header = structures.dheader_t()
        self.handle.readinto(self.header)
        self.planeLump = self.get_lump_from_id(1)
        self.nodeLump = self.get_lump_from_id(5)
        self.leafLump = self.get_lump_from_id(10)
    
    def get_lump_from_id(self, id):
        lump = []
        if id == 1:
            numLumps = self.header.lumps[id].filelen / ctypes.sizeof(structures.dplane_t)
            for i in range(int(numLumps)):
                lump.append(structures.dplane_t())
        elif id == 5:
            numLumps = self.header.lumps[id].filelen / ctypes.sizeof(structures.dnode_t)
            for i in range(int(numLumps)):
                lump.append(structures.dnode_t())
        elif id == 10:
            numLumps = self.header.lumps[id].filelen / ctypes.sizeof(structures.dleaf_t)
            for i in range(int(numLumps)):
                lump.append(structures.dleaf_t())
        for i in range(int(numLumps)):
            self.handle.seek(self.header.lumps[id].fileofs + (i * ctypes.sizeof(lump[i])))
            self.handle.readinto(lump[i])
        return lump
    
    def get_leaf_from_point(self, point):
        node = 0
        while node >= 0:
            pNode = self.nodeLump[node]
            pPlane = self.planeLump[pNode.planenum]
            d = point.dotProduct(pPlane.normal) - pPlane.dist
            if d > 0:
                node = pNode.children[0]
            else:
                node = pNode.children[1]
        return self.leafLump[-node - 1]
    
    def is_visible(self, vStart, vEnd):
        vStart = structures.VECTOR(vStart[0], vStart[1], vStart[2])
        vEnd = structures.VECTOR(vEnd[0], vEnd[1], vEnd[2])
        vDirection = vEnd - vStart
        vPoint = vStart
        iStepCount = int(vDirection.length())
        if not iStepCount:
            return False
        vDirection /= iStepCount
        while iStepCount:
            vPoint = vPoint + vDirection
            pLeaf = self.get_leaf_from_point(vPoint)
            if pLeaf and (pLeaf.contents & 0x1):
                break
            iStepCount -= 1
        return not (pLeaf.contents & 0x1)