#!python
import time
import base64
import hashlib, hmac
import win32clipboard  


def setclipboard(aString):
    win32clipboard.OpenClipboard()  
    win32clipboard.EmptyClipboard()  
    win32clipboard.SetClipboardText(aString)  
    win32clipboard.CloseClipboard()  


def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def get_auth_code(secret):
    t = int(time.time() / 30)
    t = t.to_bytes(8, 'big')
    key = base64.b64decode(secret)
    h = hmac.new(key, t, hashlib.sha1)
    signature = list(h.digest())
    start = signature[19] & 0xf
    fc32 = bytes_to_int(signature[start:start + 4])
    fc32 &= 2147483647
    fullcode = list('23456789BCDFGHJKMNPQRTVWXY')
    code = ''
    for i in range(5):
        code += fullcode[fc32 % 26]
        fc32 //= 26
    return code

auth_code = get_auth_code('YOUR_steam_shared_secret')
print(auth_code)
setclipboard(auth_code)