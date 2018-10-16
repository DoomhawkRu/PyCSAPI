'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from ctypes import *
import math
import tkinter
import win32api
import win32con
import win32gui

import threading
import time

try:
    from pycsapi import structures
except:
    import structures

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0:
        distancex = -distancex
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0:
        distancey = -distancey
    return distancex, distancey

def check_angles(pitch, yaw):
    if pitch > 89 or pitch < -89 or yaw > 360 or yaw < -360:
        return False
    return True

def get_window(title):
    x1, y1, x2, y2 = win32gui.GetWindowRect(win32gui.FindWindow(None, title))
    w, h, x, y = win32gui.GetClientRect(win32gui.FindWindow(None, title))
    client = (x, y)
    window = ((x1, y1), (x2, y2))
    if window[1] == client:
        return window
    else:
        SM_CXSIZEFRAME = win32api.GetSystemMetrics(win32con.SM_CXSIZEFRAME)
        SM_CYBORDER = win32api.GetSystemMetrics(win32con.SM_CYBORDER)
        SM_CYCAPTION = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)
        diffx = SM_CYBORDER
        diffy = SM_CYCAPTION
        return ((window[0][0] + diffx, window[0][1] + diffy), (window[1][0], window[1][1]))

def get_client_size(title):
    window_data = get_window(title)
    return (window_data[1][0] - window_data[0][0], window_data[1][1] - window_data[0][1])

def is_key_pressed(id):
    return win32api.GetAsyncKeyState(id)

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
            numLumps = self.header.lumps[id].filelen / sizeof(structures.dplane_t)
            for i in range(int(numLumps)):
                lump.append(structures.dplane_t())
        elif id == 5:
            numLumps = self.header.lumps[id].filelen / sizeof(structures.dnode_t)
            for i in range(int(numLumps)):
                lump.append(structures.dnode_t())
        elif id == 10:
            numLumps = self.header.lumps[id].filelen / sizeof(structures.dleaf_t)
            for i in range(int(numLumps)):
                lump.append(structures.dleaf_t())
        for i in range(int(numLumps)):
            self.handle.seek(self.header.lumps[id].fileofs + (i * sizeof(lump[i])))
            self.handle.readinto(lump[i])
        return lump
    
    def get_leaf_from_point(self, point):
        node = 0
        pNode = None
        pPlane = None
        d = 0
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
        vDirection /= iStepCount
        pLeaf = None
        while iStepCount:
            vPoint = vPoint + vDirection
            pLeaf = self.get_leaf_from_point(vPoint)
            if pLeaf and (pLeaf.contents & 0x1):
                break
            iStepCount -= 1
        return not (pLeaf.contents & 0x1)

class ScreenDrawer:
    def __init__(self, title, redraw_delay = .2):
        self.update_delay = redraw_delay
        self.title = title
        self.lines = {}
        self._lines = {}
        self.load()
        self.last_pos = get_window(self.title)

    def _update(self, hwnd):
        time.sleep(1)
        while True:
            if self.lines:
                win32gui.RedrawWindow(hwnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
            time.sleep(self.update_delay)
    
    def _load(self):
        hInstance = win32api.GetModuleHandle()
        wndClass = win32gui.WNDCLASS()
        wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc = self.update
        wndClass.hInstance = hInstance
        wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName = 'PyCSAPI-ScreenDrawer'
        wndClassAtom = win32gui.RegisterClass(wndClass)
        hWindow = win32gui.CreateWindowEx(win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT, wndClassAtom, None, win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE, 0, 0, win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN), None, None, hInstance, None)
        update_thread = threading.Thread(target = self._update, args = (hWindow,))
        update_thread.daemon = True
        update_thread.start()
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        win32gui.PumpMessages()
    
    def load(self):
        load_thread = threading.Thread(target = self._load)
        load_thread.daemon = True
        load_thread.start()
    
    def update(self, hwnd, message, wParam, lParam):
        if message == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != self.title:
            return win32gui.DefWindowProc(hwnd, message, wParam, lParam)
        if message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hwnd)
            for line in self._lines.values():
                pos = get_window(self.title)
                win32gui.MoveToEx(hdc, line[0] + pos[0][0], line[1] + pos[0][1])
                win32gui.BeginPath(hdc)
                win32gui.LineTo(hdc, line[2] + pos[0][0], line[3] + pos[0][1])
                win32gui.EndPath(hdc)
                win32gui.StrokeAndFillPath(hdc)
            self._lines = self.lines
            win32gui.EndPaint(hwnd, paintStruct)
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, message, wParam, lParam)
    
    def draw_line(self, line1, line2):
        self.lines[len(self.lines.keys())] = [int(line1[0]), int(line1[1]), int(line2[0]), int(line2[1])]
        return len(self.lines.keys()) - 1
    
    def remove_line(self, index):
        del self.lines[index]