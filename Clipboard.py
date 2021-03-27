import ctypes
from ctypes.wintypes import *
import win32clipboard
from win32con import *  

#-----从剪切板里获取图片,格式为BMP
class BITMAPFILEHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('bfType', WORD),  # file type ("BM")
        ('bfSize', DWORD),  # file size in bytes
        ('bfReserved1', WORD),  # must be zero
        ('bfReserved2', WORD),  # must be zero
        ('bfOffBits', DWORD),  # byte offset to the pixel array
    ]
class BITMAPINFOHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPLanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD)
    ]
SIZEOF_BITMAPFILEHEADER = ctypes.sizeof(BITMAPFILEHEADER)
SIZEOF_BITMAPINFOHEADER = ctypes.sizeof(BITMAPINFOHEADER)
class Extracting_clipboard():
    def __init__(self,path):
        self.img_save_path = path
    
    def extracting(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                self.processing_img(data)
                return (1,'成功获取')
            elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                txt = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                return (2,txt)
            else:
                return(0,'非指定格式')
        finally:
            win32clipboard.CloseClipboard()

    def extracting_img(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                self.processing_img(data)
                return (1,'成功获取')
            else:
                return(0,'非指定格式')
        finally:
            win32clipboard.CloseClipboard()

    def extracting_txt(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                txt = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                return (1,txt)
            else:
                return(0,'非指定格式')
        finally:
            win32clipboard.CloseClipboard()

    def write(self,content):
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT,content)
            return(1,'成功写入')
        finally:
            win32clipboard.CloseClipboard()

    def processing_img(self,data):
        bmih = BITMAPINFOHEADER()
        ctypes.memmove(ctypes.pointer(bmih), data, SIZEOF_BITMAPINFOHEADER)
        if bmih.biCompression == BI_BITFIELDS:  # RGBA?
            bmfh = BITMAPFILEHEADER()
            ctypes.memset(ctypes.pointer(bmfh), 0, SIZEOF_BITMAPFILEHEADER)  # zero structure
            bmfh.bfType = ord('B') | (ord('M') << 8)
            bmfh.bfSize = SIZEOF_BITMAPFILEHEADER + len(data)  # file size
            SIZEOF_COLORTABLE = 0
            bmfh.bfOffBits = SIZEOF_BITMAPFILEHEADER + SIZEOF_BITMAPINFOHEADER + SIZEOF_COLORTABLE
            #bmp_filename = 'D:/clipboard.bmp'
            with open(self.img_save_path, 'wb') as bmp_file:
                bmp_file.write(bmfh)
                bmp_file.write(data )


