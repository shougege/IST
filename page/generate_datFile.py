import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import numpy as np
import pandas as pd
import re
import time
import csv
import os
import logging

class DataFrameSingleton:
    _instance = None
    df = None

    def __new__(cls, excel_file_path=None):
        if cls._instance is None:
            cls._instance = super(DataFrameSingleton, cls).__new__(cls)
            if excel_file_path:
                cls.df = pd.DataFrame(pd.read_excel(excel_file_path))
        return cls._instance

    def get_df(self):
        return self.df


class generateDatFile:
    #------------------------------Tab3控件介绍-------------------------#
    # We are creating a container tab3 to hold all other widgets
    def __init__(self,master) -> None:
        self.monty = ttk.LabelFrame(master,tex='web 2.0 dat')
        self.monty.grid(column=400,row=500,padx=40,pady=30)

        # 这个js文件前缀也是显示的内容
        self.options = ["en-US","zh-TW","ru-RU","fr-FR","es-ES","pt-PT","ar-AE","ko-KR",
                "de-DE","he-IL","tr-TR","it-IT","ro-RO","th-TH","el-GR","pl-PL"]
        # zh-TW中国台湾 ru-RU俄语 fr-FR法语 es-ES西班牙语 pt-PT葡萄牙语 ar-AE阿拉伯语 ko-KR韩语
        # de-DE德语 he-IL希伯来语 tr-TR土耳其语 it-IT意大利语 ro-RO罗马尼亚语 th-TH泰语 el-GR希腊语 pl-PL波兰语 
        # self.file_header = ["en_US","zh_TW","ru_RU","fr_FR","es_ES","pt_PT","ar_AE","ko_KR",
        #         "de_DE","he_IL","tr_TR","it_IT","ro_RO","th_TH","el_GR","pl_PL"]
        self.file_header = ["英语（en）","繁体中文（zh_TW）","俄语（ru）","法语（fr）","西班牙语（es）","葡萄牙语（pt）","阿拉伯语（ar）","韩语（ko）",
                 "德语（de）","希伯来语（he）","土耳其语（tr）","意大利语（it）","罗马尼亚语（ro）","泰语（th）","希腊语（el）","波兰语（pl）"]
        
        self.vars = []
        self.icol = 1
        self.jrow = 1
        for option in self.options:
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.monty,text=option,variable=var)
            #checkbutton.pack()
            checkbutton.grid(column = self.icol, row = self.jrow, padx=8, pady=5 )
            self.vars.append(var)

            self.icol = self.icol + 1
            if(self.icol % 8 == 0):
                self.jrow = self.jrow + 1
                self.icol = 1

        # Create a container to hold labels
        self.labelsFrame = ttk.Labelframe(self.monty, text=' Embedded area ')
        self.labelsFrame.grid(column=3,row = self.jrow + 10,columnspan=4)

        self.label = tk.Label(self.labelsFrame, text='dat 文件')
        self.label.grid(column = 3,row= 3)
        self.entry_dat = tk.Entry(self.labelsFrame, width= 40)
        self.entry_dat.grid(column = 4,row= 3)
        self.selFile = ttk.Button(self.labelsFrame, text='选择文件',width=8,command=self.get_file_path)
        self.selFile.grid(column = 5,row= 3)

        self.label_excel = tk.Label(self.labelsFrame, text='excel 文件')
        self.label_excel.grid(column = 3,row= 4)
        self.entry_excel = tk.Entry(self.labelsFrame, width= 40)
        self.entry_excel.grid(column = 4,row= 4)
        self.select_excel = ttk.Button(self.labelsFrame, text='选择文件',width=8,command= self.get_excel_path)
        self.select_excel.grid(column = 5,row= 4)

        self.label_folder = tk.Label(self.labelsFrame, text='生成文件夹路径')
        self.label_folder.grid(column = 3,row= 5)
        self.entry_folder = tk.Entry(self.labelsFrame, width= 40)
        self.entry_folder.grid(column = 4,row= 5)
        self.select_folder = ttk.Button(self.labelsFrame, text='选择文件夹',width=10,command=self.get_folder_path)
        self.select_folder.grid(column = 5,row= 5)

        self.action = ttk.Button(self.labelsFrame,text='生成 DAT',width=10,command = self.generate_dat_file)
        self.action.grid(column=4, row= 8,rowspan=2,ipady=7)

    def get_file_path(self):
        self.dat_file_path = filedialog.askopenfilename()
        self.entry_dat.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_dat.insert(0, self.dat_file_path)

    def get_excel_path(self):
        self.excel_file_path = filedialog.askopenfilename()
        self.entry_excel.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_excel.insert(0, self.excel_file_path)

    def get_folder_path(self):
        self.dat_folder_path = filedialog.askdirectory()
        self.entry_folder.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_folder.insert(0,self.dat_folder_path)

    # Modified Button Click Function
    def generate_dat_file(self):
        # 启动df的单例模式
        self.dataframe_instance = DataFrameSingleton(self.excel_file_path)
        # 用UTF-8 打开文件
        logging.info("开始生成dat文件")
        start = time.process_time()

        for index,var in enumerate(self.vars):
            if var.get() == 1:
                self.datfieldProcess(index)
        
        end = time.process_time()
        mBox.showinfo('生成dat文件', '耗时' + str(end-start) +'s')
        logging.info("结束生成dat文件")

    def datfieldProcess(self,index):
        #folder_name = os.path.basename(self.dat_folder_path)
        folder_name = os.path.abspath(self.dat_folder_path)
        combined_name = os.path.join(folder_name, self.options[index] + '_lang.dat')
        logging.info("生成dat 文件名 " + combined_name)

        with open(self.dat_file_path, 'r', encoding='utf-8' ) as file:
            with open(combined_name,'w+',encoding='utf-8') as fileW:
                for line in file:
                    if "'" in line:
                        splitValue = line.split("'")
                        if len(splitValue) == 3:
                            val =  self.repStr(splitValue[1], self.file_header[index])
                            fileW.write(line.replace(splitValue[1],val))
                        elif len(splitValue) > 3:
                            logging.info('分割之后字符串数量大于3: ' + line)
                            result = re.search(r'\'(.*)\'',line)
                            result_str = result.group(1) if result else ""
                            val =  self.repStr(result_str, self.file_header[index])
                            fileW.write(line.replace(result_str,val))
                        else:
                            # 这里需要补充 有'' 内容的逻辑
                            fileW.write(line)
                    else:
                            fileW.write(line)                
    
    def repStr(self,keyWord,tab_header):
        # 使用单例模式，频繁多文件进行io操作消耗资源
        df = self.dataframe_instance.get_df()
        
        #search_result =  df[df['词条中文'] ==  keyWord]  # df.loc[df['A'].str.contains("颁发者",na=False)]
        # keyWord 关键字的行
        try:
            filtered_rows =  df[df['词条中文'] ==  keyWord]
            if filtered_rows.empty:
                logging.info('未找到词条: ' + keyWord + ' 所在的行')
                return ''
            
            row_number = filtered_rows.index[0]
            value = df.iloc[row_number][tab_header]
            if value is np.nan:
                logging.info('未找到替换的关键字')
                value = ''
        except:
            logging.info("表头: " + tab_header +  "  Key word: " +  keyWord)
            value = ''

        return value





