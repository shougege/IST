import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import numpy as np
import pandas as pd
import re
import csv
import os
import logging
import time


class Page4:
    #------------------------------Tab4控件介绍-------------------------#
    # We are creating a container tab4 to hold all other widgets
    def __init__(self, master) -> None:
        self.monty = ttk.LabelFrame(master,text='提取中文关键字')
        self.monty.grid(column=0,row=0,padx=60,pady=20) 

        self.label_dat = tk.Label(self.monty, text='dat file path')
        self.label_dat.grid(column=3, row=5, ipadx=8,ipady= 6)
        self.entry_dat = tk.Entry(self.monty,width=40)
        self.entry_dat.grid(column=5,row=5)
        self.select_dat = ttk.Button(self.monty,text='选择文件',width=10,command=self.get_dat_file_path)
        self.select_dat.grid(column=7,row=5)

        self.label_excel = tk.Label(self.monty, text='生成*.xlsx文文件名')
        self.label_excel.grid(column=3,row=6, ipadx=8, ipady=6)
        self.entry_excel_filename = tk.Entry(self.monty,width=40)
        self.entry_excel_filename.grid(column=5,row=6)

        action_csv = ttk.Button(self.monty,text='Extraction',width = 10,command = self.generate_excel_file)
        action_csv.grid(column=5,row=7,rowspan=2,ipady=7)

        # 去除已经翻译字段
        self.monty1 = ttk.LabelFrame(master, text='去除已经翻译字段')
        self.monty1.grid(column=0,row=2,padx=60,pady=20)

        self.label_remove_excel = tk.Label(self.monty1, text='已经查重excel文件')
        self.label_remove_excel.grid(column=3,row=5,ipadx=8,ipady=6)
        self.entry_remove_excel = tk.Entry(self.monty1,width=40)
        self.entry_remove_excel.grid(column=5,row=5)
        self.select_remove_excel = ttk.Button(self.monty1,text='选择文件',width=10,command=self.get_remove_excel_file_path)
        self.select_remove_excel.grid(column=7,row=5)

        self.label_after_removal_excel = tk.Label(self.monty1, text='生成*.xlsx文文件名')
        self.label_after_removal_excel.grid(column=3,row=6, ipadx=8, ipady=6)
        self.entry_after_excel_filename = tk.Entry(self.monty1,width=40)
        self.entry_after_excel_filename.grid(column=5,row=6)

        action_remove_excel = ttk.Button(self.monty1,text="ReMove",width=10,command= self.generate_remove_file)
        action_remove_excel.grid(column=5,row=7,rowspan=2,ipady=7)

    def get_dat_file_path(self):
        self.dat_file_path = filedialog.askopenfilename()
        self.entry_dat.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_dat.insert(0,self.dat_file_path)

    # Modified Button Click Function
    def generate_excel_file(self):

        logging.info("generate_excel_file start")
        logging.info(self.entry_excel_filename.get())

        # pattern = re.compile(r"'((?:[^'\\]|\\.|\\\\)*)'")
        save_data = {}
        str_array = []
        start = time.process_time()
        with open(self.dat_file_path,'r', encoding="utf-8") as file:
            for line in file:
                if "'" in line:
                    splitValue = line.split("'")
                    if len(splitValue) == 3:
                        str_array.append(splitValue[1])
                    elif len(splitValue) > 3:
                        logging.info('分割之后字符串数量大于3: ' + line)
                        result = re.search(r'\'(.*)\'',line)
                        result_str = result.group(1) if result else ""
                        logging.info('分割之后字符串数量大于3 原字符串: ' + line)
                        logging.info('分割之后字符串数量大于3 替换字符串: ' + result_str)
                        str_array.append(result_str)
                    else:
                        logging.error("提取的错误字符串: " + line)
    
        # 使用set进行去重
        logging.info("提取词条个数: " + str(len(str_array)))
        unique_str_array = list(set(str_array))
        logging.info("提取词条去重后个数: " + str( len(unique_str_array) ))
        save_data["词条（简体中文或者英文）"] = unique_str_array
        save_data["限制长度（字符）"] = ''

        try:
            directory, filename = os.path.split(self.dat_file_path)
        except:
            logging.info("os.path.split dat_file_path 错误!")

        new_filename = os.path.join(directory,self.entry_excel_filename.get())
        #df = pd.read_excel(new_filename) 可以不用读取excel文件
        # 这样做可以避免 1. 数据过长问题 2. 数据每列长度不同问题
        df = pd.DataFrame(pd.DataFrame.from_dict(save_data,orient='index').values.T,columns=list(save_data.keys()))
        df.to_excel(new_filename,index=False)

        end = time.process_time()
        mBox.showinfo('提取词条完成','耗时' + str(end-start) + 's')


    def get_remove_excel_file_path(self):
        self.remove_excel_file_path = filedialog.askopenfilename()
        self.entry_remove_excel.delete(0,tk.END) #删除从开始到结束的文本
        self.entry_remove_excel.insert(0,self.remove_excel_file_path)


    def has_data_or_empty(self,row):
        return all(pd.notna(row) & (row.astype(str).str.strip()==''))

    def generate_remove_file(self):
        df = pd.read_excel(self.remove_excel_file_path)

        cols_of_interest = ['en_US','es_ES']
        rows_to_delete = df[df[cols_of_interest].apply(self.has_data_or_empty,axis=1)]

        rows_to_delete.to_excel(self.entry_after_excel_filename.get(),index=False)
