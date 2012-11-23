import ctypes

from .error import handle_nonzero_success

CreateFileMapping = ctypes.windll.kernel32.CreateFileMappingW
CreateFileMapping.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.LPWSTR,
]
CreateFileMapping.restype = ctypes.wintypes.HANDLE

MapViewOfFile = ctypes.windll.kernel32.MapViewOfFile
MapViewOfFile.restype = ctypes.wintypes.HANDLE

class MemoryMap(object):
    """
    A memory map object which can have security attributes overrideden.
    """
    def __init__(self, name, length, security_attributes=None):
        self.name = name
        self.length = length
        self.security_attributes = security_attributes
        self.pos = 0

    def __enter__(self):
        p_SA = (
            ctypes.byref(self.security_attributes)
            if self.security_attributes else None
        )
        INVALID_HANDLE_VALUE = -1
        PAGE_READWRITE = 0x4
        FILE_MAP_WRITE = 0x2
        filemap = ctypes.windll.kernel32.CreateFileMappingW(
            INVALID_HANDLE_VALUE, p_SA, PAGE_READWRITE, 0, self.length,
            unicode(self.name))
        handle_nonzero_success(filemap)
        if filemap == INVALID_HANDLE_VALUE:
            raise Exception("Failed to create file mapping")
        self.filemap = filemap
        self.view = MapViewOfFile(filemap, FILE_MAP_WRITE, 0, 0, 0)
        return self

    def seek(self, pos):
        self.pos = pos

    def write(self, msg):
        ctypes.windll.msvcrt.memcpy(self.view + self.pos, msg, len(msg))
        self.pos += len(msg)

    def read(self, n):
        """
        Read n bytes from mapped view.
        """
        out = ctypes.create_string_buffer(n)
        ctypes.windll.msvcrt.memcpy(out, self.view + self.pos, n)
        self.pos += n
        return out.value

    def __exit__(self, exc_type, exc_val, tb):
        ctypes.windll.kernel32.UnmapViewOfFile(self.view)
        ctypes.windll.kernel32.CloseHandle(self.filemap)