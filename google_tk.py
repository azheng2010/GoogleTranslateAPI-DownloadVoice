#！/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-03-17 20:59:06
@author: wangzheng
Sys_Env : Windows_AMD64 Python3.5.2
Email:yaoyao12348@126.com
Filename: xxx.py
Description : google翻译TK值的计算,两次调用js代码，有黑框两闪而过
Usage:
    Call this python script from the command line.
        $ python tk_generator.py <word>
        $ python tk_generator.py <word1> [word2] [word3] ...
    Use this module from another python script.
        >>> import tk_generator
        >>> tk_generator.get_tk('dog')
"""

import requests, re, sys, execjs


def get_tkk():
    '''从google服务器上获取tkk值，为计算tk值做准备'''
    def get_res(url):
        try:
            res = requests.get(url, timeout = 1.5)
            res.raise_for_status()
            #res.encoding = 'utf-8'
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
        #print(tkk_fn.group(1))
        content = tkk_fn.group(1).encode('utf-8').decode('unicode_escape')
        #print(content)
        tkk = execjs.eval(content)
        #print('tkk:',tkk)
        return tkk
    except Exception as ex:
        print(ex)

def get_tk(text):
    '''获取google的TK值,text为英文时可以，中文需转换'''
    #加载生成TK值得js代码
    try:
      with open('./Calcu_Google_TK.js','r',encoding='utf-8') as f:
          jscode=f.read()
    except:
          jscode='''
            function b(a, b) {
                for (var d = 0; d < b.length - 2; d += 3) {
                    var c = b.charAt(d + 2),
                        c = "a" <= c ? c.charCodeAt(0) - 87 : Number(c),
                        c = "+" == b.charAt(d + 1) ? a >>> c : a << c;
                    a = "+" == b.charAt(d) ? a + c & 4294967295 : a ^ c
                }
                return a
            }
            function tk(a,TKK) {
                for (var e = TKK.split("."), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {
                    var c = a.charCodeAt(f);
                    128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (c = 65536 + ((c & 1023) << 10) + (a.charCodeAt(++f) & 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 & 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 & 63 | 128), g[d++] = c & 63 | 128)
                }
                a = h;
                for (d = 0; d < g.length; d++) a += g[d], a = b(a, "+-a^+6");
                a = b(a, "+-3^+b+-f");
                a ^= Number(e[1]) || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + "." + (a ^ h)
            }'''
    ctx = execjs.compile(jscode)#编译
    tkk = get_tkk()  #连接服务器获取TKK
    tk = ctx.call('tk', text, tkk)#调用tk函数
    #第一个参数“tk”为方法名，第二个参数开始，为js方法所需的参数
    return tk

if __name__=="__main__":
    if len(sys.argv)==2:
        print(get_tk(sys.argv[1]))
    elif len(sys.argv)>2:
        keywords=sys.argv[1:]
        for word in keywords:
            print(word,get_tk(word))
    else:
        word='words'
        google_TK=get_tk(word)
        print('%s的TK值：%s'%(word,google_TK))