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

#正则表达式，匹配中文字符
CHINESE_REGEX = re.compile(r'[\u4e00-\u9fa5]')

def contains_chinese(text):
    """检查文本是否包含中文字符"""
    return bool(CHINESE_REGEX.search(text))


class Page6:

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
        """遍历目录，检查文件中是否包含中文字符"""
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
                   # 排除 .git 目录
            if '.git' in dirpath:
                continue

            if 'dist' in dirpath:
                continue
            if 'node_modules' in dirpath:
                continue

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # 跳过一些常见的文件（如临时文件，缓存文件等）
                if filename.endswith('.pyc') or filename.endswith('.log'):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if contains_chinese(content):
                            logging.info(f'文件 "{file_path}" 包含中文字符')
                except (UnicodeDecodeError, IOError) as e:
                    # 如果读取文件出错，跳过该文件
                    logging.info(f'无法读取文件 "{file_path}": {e}')