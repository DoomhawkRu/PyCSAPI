'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import ctypes
import ctypes.wintypes
import os
import struct

class MODULEENTRY32(ctypes.Structure): _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('th32ModuleID', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('GlblcntUsage', ctypes.wintypes.DWORD), ('ProccntUsage', ctypes.wintypes.DWORD), ('modBaseAddr', ctypes.POINTER(ctypes.wintypes.BYTE)), ('modBaseSize', ctypes.wintypes.DWORD), ('hModule', ctypes.wintypes.HMODULE), ('szModule', ctypes.c_char * 256), ('szExePath', ctypes.c_char * 260)]

def __get_subindex(list, sub_list):
    cache = []
    index = 0
    for elem in list:
        elem &= 0xFF
        if len(sub_list) == len(cache):
            return index - len(sub_list)
        if elem == sub_list[len(cache)] or sub_list[len(cache)] == -1:
            cache.append(elem if sub_list[len(cache)] != -1 else -1)
        else:
            cache = []
        index += 1
    return False

def find_pattern(pid, name, pattern, full_address = False):
    module = get_module_offset(get_module(pid, name))
    if not module or not pattern:
        return False
    data = read_memory(pid, module, None, get_module_size(pid, name))
    return __get_subindex(data, pattern) + (module if full_address else 0)

def get_process(name):
    count = 32
    while True:
        pids = (ctypes.wintypes.DWORD * count)()
        cb = ctypes.sizeof(pids)
        bytes_returned = ctypes.wintypes.DWORD()
        if ctypes.windll.psapi.EnumProcesses(ctypes.byref(pids), cb, ctypes.byref(bytes_returned)):
            if bytes_returned.value < cb:
                break
            else:
                count *= 2
    for pid in pids:
        hwnd = ctypes.windll.kernel32.OpenProcess(0x400, False, pid)
        if hwnd:
            process_name = (ctypes.c_char * 260)()
            if ctypes.windll.psapi.GetProcessImageFileNameA(hwnd, process_name, 260) > 0 and os.path.basename(process_name.value).decode().lower() == name.lower() and ctypes.windll.kernel32.CloseHandle(hwnd):
                return pid
        ctypes.windll.kernel32.CloseHandle(hwnd)
    return 0

def get_module(pid, name):
    hModule = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x18, pid)
    if hModule:
        module_entry = MODULEENTRY32()
        module_entry.dwSize = ctypes.sizeof(module_entry)
        success = ctypes.windll.kernel32.Module32First(hModule, ctypes.byref(module_entry))
        while success:
            if module_entry.th32ProcessID == pid and module_entry.szModule.decode() == name:
                return module_entry.modBaseAddr
            success = ctypes.windll.kernel32.Module32Next(hModule, ctypes.byref(module_entry))
        ctypes.windll.kernel32.CloseHandle(hModule)
    return 0

def get_module_size(pid, name):
    hModule = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x18, pid)
    if hModule:
        module_entry = MODULEENTRY32()
        module_entry.dwSize = ctypes.sizeof(module_entry)
        success = ctypes.windll.kernel32.Module32First(hModule, ctypes.byref(module_entry))
        while success:
            if module_entry.th32ProcessID == pid and module_entry.szModule.decode() == name:
                return module_entry.modBaseSize
            success = ctypes.windll.kernel32.Module32Next(hModule, ctypes.byref(module_entry))
        ctypes.windll.kernel32.CloseHandle(hModule)
    return 0

def get_module_offset(module):
    if not module:
        return None
    return ctypes.addressof(module.contents)

def read_memory(pid, address, type, size = None):
    type = None if size else type
    size = size if size else (4 if (type == 'i' or type == 'f') else 1)
    buffer = (ctypes.c_byte * size)()
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    ctypes.windll.kernel32.ReadProcessMemory(process, address, buffer, size, ctypes.byref(ctypes.c_ulonglong(0)))
    ctypes.windll.kernel32.CloseHandle(process)
    if type:
        return struct.unpack(type, buffer)[0]
    else:
        return struct.unpack('b' * size, buffer)

def write_memory(pid, address, data, type, size = None):
    type = None if size else type
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    if type:
        ctypes.windll.kernel32.WriteProcessMemory(process, address, struct.pack(type, data) if type == 'f' or type == 'i' else (bytes([data]) if type == 'b' else chr(data)), (4 if (type == 'i' or type == 'f') else 1), ctypes.byref(ctypes.c_ulong(0)))
    else:
        ctypes.windll.kernel32.WriteProcessMemory(process, address, bytes([data]), size, ctypes.byref(ctypes.c_ulong(0)))
    ctypes.windll.kernel32.CloseHandle(process)