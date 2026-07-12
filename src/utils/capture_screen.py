import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


class BITMAPFILEHEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('bfType', wintypes.WORD), ('bfSize', wintypes.DWORD), ('bfReserved1',
                                                                        wintypes.WORD), ('bfReserved2', wintypes.WORD), ('bfOffBits', wintypes.DWORD)]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG), ('biHeight', wintypes.LONG), ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
                ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG), ('biYPelsPerMeter', wintypes.LONG), ('biClrUsed', wintypes.DWORD), ('biClrImportant', wintypes.DWORD)]


def capture_screen(filename):
    """截取全屏并保存到文件"""
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbmp = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
    gdi32.SelectObject(hdc_mem, hbmp)
    gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_screen, 0, 0, 13369376)
    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = width
    bmi.biHeight = -height
    bmi.biPlanes = 1
    bmi.biBitCount = 24
    bmi.biCompression = 0
    bmi.biSizeImage = 0
    row_bytes = width * 3 + 3 & (-4)
    image_size = row_bytes * height
    buffer = ctypes.create_string_buffer(image_size)
    gdi32.GetDIBits(hdc_mem, hbmp, 0, height,
                    ctypes.byref(buffer), ctypes.byref(bmi), 0)
    bmfh = BITMAPFILEHEADER()
    bmfh.bfType = 19778
    bmfh.bfSize = ctypes.sizeof(BITMAPFILEHEADER) + \
        ctypes.sizeof(BITMAPINFOHEADER) + image_size
    bmfh.bfOffBits = ctypes.sizeof(
        BITMAPFILEHEADER) + ctypes.sizeof(BITMAPINFOHEADER)
    with open(filename, 'wb') as f:
        f.write(bmfh)
        f.write(bmi)
        f.write(buffer)
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)
    return True
