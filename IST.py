import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
import logging
import base64
import os

from page.page1 import Page1
from page.page2 import Page2
from page.page3 import Page3
from page.page4 import Page4
from page.page5 import Page5

from img.rabbit import imgBase64

'''
标准控件
0 cbt CheckButton
1 btn Button
2 chk CheckBox
3 ckl CheckedListBox
4 cmb ComboBox
5 dtp DateTimePicker
6 lbl Label
7 llb LinkLabel
8 lst ListBox
9 lvw ListView
10 mtx MaskedTextBox
11 cdr MonthCalendar
12 icn NotifyIcon
13 nud NumeircUpDown
14 pic PictureBox
15 prg ProgressBar

函数开头用__xx__
变量开头用a_b_c  小写开头

表头要和文件名称 有直接对应关系
'''


class App:
    def __init__(self,master):
        # Tab Control introduced here ----------- ------------------------
        tabControl = ttk.Notebook(master)          # Create Tab Control

        tab1 = ttk.Frame(tabControl)            # Create a tab
        tabControl.add(tab1, text='File format conversion') # Add the tab

        tab2 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab2,text='Web2.0 generate JS file') 

        tab3 = ttk.Frame(tabControl)            # Add a third tab
        tabControl.add(tab3,text='Web2.0 generate DAT file')  

        tab4 = ttk.Frame(tabControl)            # Add a fifth tab
        tabControl.add(tab4,text='Keyword Extraction')  # 

        tab5 = ttk.Frame(tabControl)            # Add a fiveth tab
        tabControl.add(tab5,text="mutil dat to excel")

        tabControl.pack(expand=1, fill="both")  # Pack to make tab visible
        # ~ Tab Control introduced here ----------------------------------

        Page1(tab1)
        Page2(tab2)
        Page3(tab3)
        Page4(tab4)
        Page5(tab5)

# 创建临时logo
def createTempLogo():  #处理图片
    tmp = open("temp.ico", "wb+") #创建temp.ico 临时文件
    tmp.write(base64.b64decode(imgBase64)) #写入img的base64
    tmp.close()  #关闭文件

if __name__ == '__main__':

    #Configure logging parameters
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s -Line: %(lineno)d - %(levelname)s -  %(message)s',
                        datefmt='%Y-%M-%d %H:%M:%S',
                        filename='IST_APP.log',
                        filemode='w')
    # 'w' 是每次运行脚本都会情况旧的日志 'a'以追加模式写入日志
    logging.info('create a windows')
    # Create instance
    win = tk.Tk()

    # Add as title
    win.title("Internationalizatioin Script Tool")

    # Disable resizing the GUI 设置窗口不可变
    # win.resizable(0,0) 

    # 设置左上角小图标
    createTempLogo()
    win.iconbitmap('temp.ico') 
    if os.path.exists("temp.ico"):
        os.remove("temp.ico") #创建logo后需要删除临时logo

    logging.info('setting a ico')

    App(win)

    win.mainloop()
    logging.info('Program ends')
    