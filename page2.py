import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import numpy as np
import pandas as pd
import time
import re
import csv
import os
import logging

class Page2:
    # ---------------Tab2 控件介绍 ------------------~#
    # We are creating a container tab3 to hold all other widgets
    def __init__(self, master) -> None:
        self.monty = ttk.LabelFrame(master,tex='Web 2.0 SideMenu')
        self.monty.grid(column=400,row=500,padx=40,pady=30)

        # 这个js文件前缀也是显示的内容
        self.options = ["en-US","zh-TW","ru-RU","fr-FR","es-ES","pt-PT","ar-AE","ko-KR",
                "de-DE","he-IL","tr-TR","it-IT","ro-RO","th-TH","el-GR","pl-PL"]
        # zh-TW中国台湾 ru-RU俄语 fr-FR法语 es-ES西班牙语 pt-PT葡萄牙语 ar-AE阿拉伯语 ko-KR韩语
        # de-DE德语 he-IL希伯来语 tr-TR土耳其语 it-IT意大利语 ro-RO罗马尼亚语 th-TH泰语 el-GR希腊语 pl-PL波兰语 
        self.file_header = ["en_US","zh_TW","ru_RU","fr_FR","es_ES","pt_PT","ar_AE","ko_KR",
                "de_DE","he_IL","tr_TR","it_IT","ro_RO","th_TH","el_GR","pl_PL"]
        # 全称名字含义  Turkish土耳其语 Hebrew希伯来语 Romanian罗马尼亚语 Thai泰国语 German德语 Greek希腊语
        #              Czech捷克语 Ukrainian乌克兰语 Polish波兰语 Kazakh哈塞克语  Danish丹麦语 Norwegian挪威语
        #              Swedish 瑞典语 Azerbaijani阿塞拜疆语 Hungarian匈牙利语 Vietnamese越南语 Bulgarian保加利亚语

        self.vars = []
        self.icol = 1
        self.jrow = 1
        for option in self.options:
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.monty,text=option,variable=var)
            checkbutton.grid(column = self.icol, row = self.jrow, padx=8, pady=6 )
            self.vars.append(var)

            self.icol = self.icol + 1
            if(self.icol % 8 == 0):
                self.jrow = self.jrow + 1
                self.icol = 1

        # Create a container to hold labels
        self.labelsFrame = ttk.Labelframe(self.monty, text='  操作区域  ')
        self.labelsFrame.grid(column=3,row=self.jrow + 10,columnspan=4)

        self.label = tk.Label(self.labelsFrame, text='js 文件')
        self.label.grid(column = 3,row= 3)
        self.entry = tk.Entry(self.labelsFrame, width= 40)
        self.entry.grid(column = 4,row= 3)
        self.selFile = ttk.Button(self.labelsFrame, text='选择文件',width=10,command=self.get_file_path)
        self.selFile.grid(column = 5,row= 3)
    
        
        self.label_excel = tk.Label(self.labelsFrame, text='excel 文件')
        self.label_excel.grid(column = 3,row= 4)
        self.entry_excel = tk.Entry(self.labelsFrame, width= 40)
        self.entry_excel.grid(column = 4,row= 4)
        self.select_excel = ttk.Button(self.labelsFrame, text='选择文件',width=10,command=self.get_excel_path)
        self.select_excel.grid(column = 5,row= 4)


        self.label_folder = tk.Label(self.labelsFrame, text='生成文件夹路径')
        self.label_folder.grid(column = 3,row= 5)
        self.entry_folder = tk.Entry(self.labelsFrame, width= 40)
        self.entry_folder.grid(column = 4,row= 5)
        self.select_folder = ttk.Button(self.labelsFrame, text='选择文件夹',width=10,command=self.get_folder_path)
        self.select_folder.grid(column = 5,row= 5)

        self.action = ttk.Button(self.labelsFrame,text='生成 JS',width=10,command = self.generate_js_file)
        self.action.grid(column=4, row= 8,rowspan=2,ipady=7)


    def get_file_path(self):
        self.js_file_path = filedialog.askopenfilename()
        self.entry.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry.insert(0, self.js_file_path)


    def get_excel_path(self):
        self.excel_file_path = filedialog.askopenfilename()
        self.entry_excel.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_excel.insert(0, self.excel_file_path)


    def get_folder_path(self):
        self.js_folder_path = filedialog.askdirectory()
        self.entry_folder.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_folder.insert(0,self.js_folder_path)

    # Modified Button Click Function
    def generate_js_file(self):   
        # 用UTF-8 打开文件
        logging.info("start generate_js_file")
        start = time.process_time()
        for index,var in enumerate(self.vars):
            if var.get() == 1:
                self.fieldProcess(index)

        end = time.process_time()
        mBox.showinfo('generate JS file', '耗时' + str(end-start) +'s')
        logging.info("end generate_js_file")


    def fieldProcess(self,index):
        #self.folder_name = os.path.basename(self.js_folder_path)
        folder_name = os.path.abspath(self.js_folder_path)
        combined_name = os.path.join(folder_name, self.options[index] + '.js')
        logging.info("生成js 文件名 " + combined_name)
   
        with open(self.js_file_path, 'r', encoding='utf-8' ) as file:
            with open(combined_name,'w+',encoding='utf-8') as fileW:
                for line in file:
                    #打印每一行
                    try:
                        if "'" in line:
                            splitValue = line.split("'")
                            if len(splitValue) == 3:
                                value =  self.repStr(splitValue[1], self.file_header[index])
                                fileW.write(line.replace(splitValue[1], value))
                        else:
                            fileW.write(line)
                    except:
                        logging.info('file write 错误!')
    
    def repStr(self,keyWord, tab_header):
        
        df = pd.DataFrame(pd.read_excel(self.excel_file_path))
        
        #search_result =  df[df['词条中文'] ==  keyWord]  # df.loc[df['A'].str.contains("颁发者",na=False)]
        # 找到keyWord 关键字的行
        try:
            filtered_rows =  df[df['zh_CN'] ==  keyWord]
            if filtered_rows.empty:
                logging.info('未找到词条所在的行' + keyWord)
                return ''

            row_number = filtered_rows.index[0]
            value = df.iloc[row_number][tab_header]
            if value is np.nan:
                logging.info('未到找到替换的关键字')
                value = ''
        except:
            logging.info("表头 " + tab_header +  "  Key word " +  keyWord)
            value = ''

        return value




