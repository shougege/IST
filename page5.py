import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import numpy as np
import pandas as pd
import re
import csv
import os, shutil

class Page5:
    #------------------------------Tab5控件介绍-------------------------#
    # We are creating a container tab4 to hold all other widgets
    def __init__(self, master) -> None:
        self.monty = ttk.LabelFrame(master,text="多dat文件整合成excel文件")
        self.monty.grid(column=0,row=0,padx=40,pady=30)

        self.labelFolder = tk.Label(self.monty, text='dat文件夹路径')
        self.labelFolder.grid(column = 3,row= 5)
        self.entryFolder = tk.Entry(self.monty, width= 40)
        self.entryFolder.grid(column = 4,row= 5)
        self.selFolder = ttk.Button(self.monty, text='选择文件夹',width=12,command=self.get_folder_path)
        self.selFolder.grid(column = 5,row= 5)


        self.labelexcel = tk.Label(self.monty, text='excel 文件')
        self.labelexcel.grid(column = 3,row= 6)
        self.entryexcel = tk.Entry(self.monty, width= 40)
        self.entryexcel.grid(column = 4,row= 6)
        self.selExcel = ttk.Button(self.monty, text='选择文件',width=8,command= self.get_excel_path)
        self.selExcel.grid(column = 5,row= 6)

        self.action = ttk.Button(self.monty,text='生成excel文件',width=15,command = self.multiDat_to_excel)
        self.action.grid(column=4, row= 8,rowspan=2,ipady=7)

    def get_folder_path(self):
        self.dat_folder_path = filedialog.askdirectory()
        self.entryFolder.delete(0,tk.END) # 删除从开始到结束的文本
        self.entryFolder.insert(0,self.dat_folder_path)

    def get_excel_path(self):
        self.excel_file_path = filedialog.askopenfilename()
        self.entryexcel.delete(0,tk.END) # 删除从开始到结束的文本
        self.entryexcel.insert(0, self.excel_file_path)

    def write_to_excel(self,filename):

        # 创建数据
        new_data = []
        index = 0
        sum = 0
        with open(filename,'r',encoding='utf-8') as file:
            for line in file:
                index = index + 1
                #打印每一行
                if "'" in line:
                    sum = sum + 1
                    splitValue = line.split("'")
                    if len(splitValue) == 3:
                        new_data.append(splitValue[1])
                    elif len(splitValue) > 3:
                        result = re.search(r'\'(.*)\'',line)
                        result_str = result.group(1) if result else ""
                        new_data.append(result_str)
                    else:
                        #print('----------',line)
                        pass
                else:
                    #print("************",line)
                    pass
        print('index: ', index, 'sum: ', sum, "len: ", len(new_data))
        return new_data

    def multiDat_to_excel(self):
        print("dat 文件夹: ", self.dat_folder_path)
        # first 读取zh-CN_lang.dat

        # 遍历其他文件

        # excel_file
        df = pd.read_excel(self.excel_file_path)
        # 直接遍历文件夹每个文件
        data = {}
        for parent, dirnames, filenames in os.walk(self.dat_folder_path, followlinks=True):
            for filename in filenames:
                file_path = os.path.join(parent,filename)
                print('文件名称: %s' % filename)
                print('文件完整路径: %s\n' % file_path)
                header_name = filename.split("_")
                print('表头: %s\n' % header_name[0])
                col_list = self.write_to_excel(file_path)
                print('data length: ', len(col_list))
                #df[header_name[0]] = data
                data[header_name[0]] = col_list 

        # 保存为新的Excel 文件
        #df = pd.DataFrame(data)
        #df = pd.DataFrame.from_dict(data,orient='index')
        # 这样做可以避免 1. 数据过长问题 2. 数据每列长度不同问题
        df = pd.DataFrame(pd.DataFrame.from_dict(data,orient='index').values.T,columns=list(data.keys()))
        df.to_excel('output.xlsx',index=False)
        print("数据已成功写入指定列,并保存为新的Excel文件。")