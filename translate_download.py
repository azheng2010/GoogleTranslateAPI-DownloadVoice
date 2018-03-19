#！/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-03-17 20:55:09
@author: wangzheng
Sys_Env : Windows_AMD64 Python3.5.2
Email:yaoyao12348@126.com
Filename: xxx.py
Description : 把谷歌翻译的内容的音频文件mp3下载到本地,不需用到header
"""
import requests
import google_tk as tk

def dic2str(dic,sep=';'):
    '''dic格式转换成str格式，分隔符用；'''
    lst=[key+"="+dic[key] for key in dic.keys()]
    return sep.join(lst)

def translate(text,sl='zh-CN',tl='en'):
    '''sl:source_language源语言
       tl:target_language目标语言
       text:翻译文本
       sl,tl取值:  en(英语),zh-CN(中文简体),zh-TW(中文繁体),fr(法语),ru(俄语),
                  de(德语),ja(日语),ko(韩语)'''
    #url='https://translate.google.cn/translate_a/single'
    url='https://translate.google.cn/translate_a/single?dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t'
    tk_value=tk.get_tk(text)
#    headers={'accept':'*/*',
#            'accept-encoding':'gzip, deflate, br',
#            'accept-language':'zh-CN,zh;q=0.9',
#            'referer':'https://translate.google.cn/',
#            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
#            'x-chrome-uma-enabled':'1',
#            'x-client-data':'CJK2yQEIpbbJAQjBtskBCKmdygEIqKPKAQ==',}
    params ={'client':'t',
            'sl':sl,#'zh-CN',
            'tl':tl,#'en',
            'hl':'zh-CN',
            #'dt':有多个取值,不能放字典里，直接放到url中
                #t - 源text的翻译
                #at - 会额外返回一些近义词
                #ex - examples
                #ss - 如果翻译的是单个词，会返回与该词相关的动词、形容词、名词
                #md - 如果翻译的是单个词，返回该词的定义  
                #rw - 组词 
                #bd - 
                #ld - 
                #qca - 
                #rm - 
            'ie':'UTF-8',
            'oe':'UTF-8',
            'ssel':'3',
            'tsel':'3',
            'kc':'0',
            'tk':tk_value,#'982078.560781',
            'q':text,}
    #r=requests.get(url,headers=headers,params=params)
    r=requests.get(url,params=params)
    #r=requests.get(url,headers=headers)
    #return r
    if r.status_code==200:
        r.encoding='utf-8'
        print(r.text)
        j=r.json()
        if not j[0] : return "Can't translate!"
        return j[0][0][0]

def voice_download(text,fp='',sl='zh-CN',tl='en'):
    '''fp:mp3文件保存目录
       sl:source_language源语言
       tl:target_language目标语言
       text:翻译文本
       sl,tl取值:  en(英语),zh-CN(中文简体),zh-TW(中文繁体),fr(法语),ru(俄语),
                  de(德语),ja(日语),ko(韩语)'''
    url='https://translate.google.cn/translate_tts'
    #url='https://translate.google.cn/translate_tts?ie=UTF-8&q=sugar%20cane&tl=en&total=1&idx=0&textlen=10&tk=360211.200348&client=t'
    tk_value=tk.get_tk(text)
    params ={'ie':'UTF-8',
            'q':text,
            'tl':tl,
            'total':1,
            'idx':'0',
            'textlen':len(text),
            'tk':tk_value,
            'client':'t',}
    #r=requests.get(url,headers=headers,params=params)
    r=requests.get(url,params=params)
    #return r
    if r.status_code==200:
        with open(fp+'%s.mp3'%text,'wb') as f:
            f.write(r.content)
        print(fp+'%s.mp3'%text,'saved successfully')
    
if __name__=="__main__":
    
    wordlist=['菠萝','香蕉','桔子','苹果','梨','花生','火龙果','柚子','葡萄',
               '西瓜','哈密瓜','芹菜']
    #word_cn='桔子'
    mp3path='d:/test/'
    for word_cn in wordlist:
        word_en=translate(word_cn)
        r=voice_download(word_en,mp3path)
    print('over')
