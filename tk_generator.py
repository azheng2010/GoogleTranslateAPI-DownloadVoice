#！/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-03-17 20:59:06
@author: wangzheng
Sys_Env : Windows_AMD64 Python3.5.2
Email:yaoyao12348@126.com
Filename: tk_generator.py
Description : google翻译TK值的计算,纯python实现
This module creates the TK GET parameter for Google translate.
This is just a code port to python. All credits should go to the original
creators of the code @tehmaestro and @helen5106.
For more info see: https://github.com/Stichoza/google-translate-php/issues/32
Usage:
    Call this python script from the command line.
        $ python tk_generator.py <word>
    Use this module from another python script.
        >>> import tk_generator
        >>> tk_generator.get_tk('dog')
Attributes:
    _ENCODING (string): Default encoding to be used during the string
        encode-decode process.
"""

__all__ = ["getTk"]

import requests,re,sys


_ENCODING = "utf-8"


# Helper functions
def _mb_strlen(string):
    """Get the length of the encoded string."""
    return len(string.decode(_ENCODING))

def _mb_substr(string, start, length):
    """Get substring from the encoded string."""
    return string[start: start + length]
##################################################

def _shr32(x, bits):
    if bits <= 0:
        return x
    if bits >= 32:
        return 0
    x_bin = bin(x)[2:]
    x_bin_length = len(x_bin)
    if x_bin_length > 32:
        x_bin = x_bin[x_bin_length - 32: x_bin_length]
    if x_bin_length < 32:
        x_bin = x_bin.zfill(32)
    return int(x_bin[:32 - bits].zfill(32), 2)

def _char_code_at(string, index):
    return ord(_mb_substr(string, index, 1))

def _TKK():
    """TKK不是固定不变的，需联网提取"""
    def get_res(url):
        try:
            res = requests.get(url,timeout=1.5)
            res.raise_for_status()
            return res
        except Exception as ex:
            print('[-]ERROR: ' + str(ex))
            return res
    def find_tkk_fn(res):#查找tkk计算函数
        re_tkk = r"TKK=eval\('(\(\(function\(\)\{.+?\}\)\(\)\))'\);"
        tkk_fn = re.search(re_tkk, res)
        return tkk_fn
    url = 'https://translate.google.cn/'
    try:
        res = get_res(url)
        tkk_fn = find_tkk_fn(res.text)
        content = tkk_fn.group(1).encode('utf-8').decode('unicode_escape')
        #函数"function(){var a=1924354454;var b=1109038554;return 422626+'.'+(a+b)}"
        ma=re.search('(?<=a=)\s*(\d)+',content)#a=...
        if ma :value_a=int(ma.group())
        mb=re.search('(?<=b=)\s*(\d)+',content)#b=...
        if mb :value_b=int(mb.group())
        mc=re.search('(?<=return\s)\s*(\d)+',content)#return ...
        if mc:value_c=int(mc.group())
        #tkk=str(value_c)+'.'+str(value_a+value_b)
        #print('tkk:',tkk)
        return [value_c,value_a+value_b]
    except Exception as ex:
        print(ex)

def _RL(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        if d >= 'a':
            d = _char_code_at(d, 0) - 87
        else:
            d = int(d)
        if b[c + 1] == '+':
            d = _shr32(a, d)
        else:
            d = a << d
        if b[c] == '+':
            a = a + d & (pow(2, 32) - 1)
        else:
            a = a ^ d
    return a


def _TL(a):
    tkk = _TKK()
    b = tkk[0]
    d = []
    for f in range(0, _mb_strlen(a)):
        g = _char_code_at(a, f)
        if g < 128:
            d.append(g)
        else:
            if g < 2048:
                d.append(g >> 6 | 192)
            else:
                if ((g & 0xfc00) == 0xd800 and
                        f + 1 < _mb_strlen(a) and
                        (_char_code_at(a, f + 1) & 0xfc00) == 0xdc00):
                    f += 1
                    g = 0x10000 + ((g & 0x3ff) << 10) + (_char_code_at(a, f) & 0x3ff)
                    d.append(g >> 18 | 240)
                    d.append(g >> 12 & 63 | 128)
                else:
                    d.append(g >> 12 | 224)
                    d.append(g >> 6 & 63 | 128)
            d.append(g & 63 | 128)
    a = b
    for e in range(0, len(d)):
        a += d[e]
        a = _RL(a, "+-a^+6")
    a = _RL(a, "+-3^+b+-f")
    a = a ^ tkk[1]
    if a < 0:
        a = (a & (pow(2, 31) - 1)) + pow(2, 31)
    a %= pow(10, 6)
    return "%d.%d" % (a, a ^ b)

def getTk(word):
    """Returns the tk parameter for the given word."""
    if isinstance(word, str):
        word = word.encode(_ENCODING)
    return _TL(word)

if __name__ == '__main__':
    if len(sys.argv)==2:
        print(getTk(sys.argv[1]))
    elif len(sys.argv)>2:
        keywords=sys.argv[1:]
        for word in keywords:
            print(word,getTk(word))
    else:
        word='words'
        print('%s的TK值：%s'%(word,getTk(word)))