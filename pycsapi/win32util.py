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
    subindex = __get_subindex(data, pattern)
    return subindex + ((module if full_address else 0) if subindex else 0)

def get_process(name):
    pids = (ctypes.wintypes.DWORD * 256)()
    ctypes.windll.psapi.EnumProcesses(ctypes.byref(pids), ctypes.sizeof(pids), ctypes.byref(ctypes.wintypes.DWORD()))
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
        result = struct.unpack(type, buffer)[0]
    else:
        result = struct.unpack('{}b'.format(size), buffer)
    return result

def write_memory(pid, address, data, type, size = None):
    type = None if size else type
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    if type:
        ctypes.windll.kernel32.WriteProcessMemory(process, address, struct.pack(type, data) if type == 'f' or type == 'i' else (bytes([data]) if type == 'b' else chr(data)), (4 if (type == 'i' or type == 'f') else 1), ctypes.byref(ctypes.c_ulong(0)))
    else:
        ctypes.windll.kernel32.WriteProcessMemory(process, address, bytes([data]), size, ctypes.byref(ctypes.c_ulong(0)))
    ctypes.windll.kernel32.CloseHandle(process)

def write_in_thread(pid, address, data, type, size):
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    vCommand = ctypes.windll.kernel32.VirtualAllocEx(process, None, size + (1 if data is str else 0), 8192 | 4096, 4)
    ctypes.windll.kernel32.WriteProcessMemory(process, vCommand, bytes(data.encode()) if isinstance(data, str) else struct.pack(type, data), size, None)
    hThread = ctypes.windll.kernel32.CreateRemoteThread(process, None, None, address, vCommand, None, None)
    ctypes.windll.kernel32.WaitForSingleObject(hThread, -1)
    ctypes.windll.kernel32.CloseHandle(process)
    ctypes.windll.kernel32.VirtualFreeEx(process, vCommand, size + (1 if data is str else 0), 32768)