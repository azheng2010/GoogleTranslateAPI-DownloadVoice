# -谷歌翻译API-
谷歌翻译，读音下载，最主要的就是google tk值的计算
这里提供两个版本的tk计算方法。一是在python中调用js代码。二是用python改写js代码。
适用python3
Usage:
    Call this python script from the command line.
        $ python tk_generator.py <word>
    Use this module from another python script.
        >>> import tk_generator
        >>> tk_generator.get_tk('dog')
