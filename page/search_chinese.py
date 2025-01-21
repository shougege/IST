import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import numpy as np
import pandas as pd
import re
import csv
import os, shutil
import logging
import time

#正则表达式，匹配非注释部分的正则表达式（排除以 // 开头的注释）
CODE_REGEX = re.compile(r'^(?!\s*//).*')
# ^(?!\s*//).*: 它表示匹配那些没有以 // （可选空格后）开头的行。该正则表达式是一个负向前瞻，意味着这一行不应该以注释开始。
"""
def contains_chinese(text):
    # 检查文本是否包含中文字符（排除 // 注释行
    # 去除 // 开头的注释行
    non_comment_lines = [line for line in text.splitlines() if CODE_REGEX.match(line)]
    
    # 检查非注释行是否包含中文字符
    for line in non_comment_lines:
        if CHINESE_REGEX.search(line):
            return True
    return False
"""

#正则表达式，匹配中文字符
CHINESE_REGEX = re.compile(r'[\u4e00-\u9fa5]')

def contains_chinese(text):
    """检查文本是否包含中文字符"""
    return bool(CHINESE_REGEX.search(text))


class SearchChinese:

    def __init__(self, master) -> None:
        self.monty = ttk.LabelFrame(master, text="寻找文件中的中文字符串")
        self.monty.grid(column=0,row=0,padx=40,pady=30)


        self.labelFolder = tk.Label(self.monty, text='项目文件夹路径')
        self.labelFolder.grid(column = 3,row= 5)
        self.entryFolder = tk.Entry(self.monty, width= 40)
        self.entryFolder.grid(column = 4,row= 5)
        self.selFolder = ttk.Button(self.monty, text='选择文件夹',width=12,command=self.get_folder_path)
        self.selFolder.grid(column = 5,row= 5)

        self.action = ttk.Button(self.monty,text='开始检测',width=15,command = self.check_files_for_chinese)
        self.action.grid(column=4, row= 8,rowspan=2,ipady=7)


    def get_folder_path(self):
        self.root_dir = filedialog.askdirectory()
        self.entryFolder.delete(0,tk.END) # 删除从开始到结束的文本
        self.entryFolder.insert(0,self.root_dir)


    def check_files_for_chinese(self):

        # Disable the button and change its appearance to gray
        self.action.config(state='disabled')
        start = time.process_time()
        """遍历目录，检查文件中是否包含中文字符"""
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # 排除 .git 目录
            if '.git' in dirpath:
                continue

            if 'dist' in dirpath:
                continue
            if 'node_modules' in dirpath:
                continue

            if 'images' in dirpath:
                continue

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # 跳过一些常见的文件（如临时文件，缓存文件等）
                if filename.endswith('.pyc') or filename.endswith('.log'):
                    continue

                try:
                    line_number = 0
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line_number, line in enumerate(file):
                            if(contains_chinese(line)):
                                logging.info(f'文件 "{file_path} Line:{line_number + 1}" 包含中文字符: {line.strip()}')
                        # content = file.read()
                        # if contains_chinese(content):
                        #     logging.info(f'文件 "{file_path}" 包含中文字符')
                except (UnicodeDecodeError, IOError) as e:
                    # 如果读取文件出错，跳过该文件
                    logging.info(f'无法读取文件 "{file_path}": {e}')

        # Re-enable the button after the function completes
        end = time.process_time()
        self.action.config(state='normal')
        mBox.showinfo('搜索项目中文词条','耗时' + str(end-start) + 's')