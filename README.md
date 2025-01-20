https://zhuanlan.zhihu.com/p/664509495  python编译成excel文件指导文章。

打包方法: 1. pyinstaller -F main.py   生成的main.spec文件需要在entitlemants_file=None, 增加一行 icon=['img\\rabbit.ico']
         2. pyinstaller main.py
         即可在.\dist路径下找到打包好的main.exe.
