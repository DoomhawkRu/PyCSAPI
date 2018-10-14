'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import ctypes
import ctypes.wintypes
import psutil
import struct

class MODULEENTRY32(ctypes.Structure): _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('th32ModuleID', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('GlblcntUsage', ctypes.wintypes.DWORD), ('ProccntUsage', ctypes.wintypes.DWORD), ('modBaseAddr', ctypes.POINTER(ctypes.wintypes.BYTE)), ('modBaseSize', ctypes.wintypes.DWORD), ('hModule', ctypes.wintypes.HMODULE), ('szModule', ctypes.c_char * 256), ('szExePath', ctypes.c_char * 260)]

def get_process(name):
    data = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == name.lower()]
    return data[0] if data else 0

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

def get_module_offset(module):
    if not module:
        return None
    return ctypes.addressof(module.contents)

def read_memory(pid, address, type):
    size = (4 if (type == 'i' or type == 'f') else 1)
    buffer = (ctypes.c_byte * size)()
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    ctypes.windll.kernel32.ReadProcessMemory(process, address, buffer, size, ctypes.byref(ctypes.c_ulonglong(0)))
    ctypes.windll.kernel32.CloseHandle(process)
    return struct.unpack(type, buffer)[0]

def write_memory(pid, address, data, type):
    process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, 0, pid)
    ctypes.windll.kernel32.WriteProcessMemory(process, address, struct.pack(type, data) if type == 'f' or type == 'i' else (bytes([data]) if type == 'b' else chr(data)), (4 if (type == 'i' or type == 'f') else 1), ctypes.byref(ctypes.c_ulong(0)))
    ctypes.windll.kernel32.CloseHandle(process)