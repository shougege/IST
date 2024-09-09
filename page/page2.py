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
# zh-TW中国台湾 ru-RU俄语 fr-FR法语 es-ES西班牙语 pt-PT葡萄牙语 ar-AE阿拉伯语 ko-KR韩语
# de-DE德语 he-IL希伯来语 tr-TR土耳其语 it-IT意大利语 ro-RO罗马尼亚语 th-TH泰语 el-GR希腊语 pl-PL波兰语 

# 全称名字含义  Turkish土耳其语 Hebrew希伯来语 Romanian罗马尼亚语 Thai泰国语 German德语 Greek希腊语
#              Czech捷克语 Ukrainian乌克兰语 Polish波兰语 Kazakh哈塞克语  Danish丹麦语 Norwegian挪威语
#              Swedish 瑞典语 Azerbaijani阿塞拜疆语 Hungarian匈牙利语 Vietnamese越南语 Bulgarian保加利亚语

class Page2:
    # ---------------Tab2 控件介绍 ------------------~#
    # We are creating a container tab3 to hold all other widgets
    def __init__(self, master) -> None:
        self.monty = ttk.LabelFrame(master,tex='Web 2.0 SideMenu')
        self.monty.grid(column=400,row=500,padx=40,pady=30)

        # 这个js文件前缀也是显示的内容
        self.cbt_options = ["en-US(英语美国)","zh-TW(中文繁体)","ru-RU(俄语)","fr-FR(法语法国)","es-ES(西班牙语传统)",
                        "pt-PT(葡萄牙语葡萄牙)","ar-AE(阿拉伯语阿联酋)","ko-KR(韩语朝鲜语)","de-DE(德语德国)","he-IL(希伯来语)",
                        "tr-TR(土耳其语)","it-IT(意大利语意大利)","ro-RO(罗马尼亚语)","th-TH(泰语)","el-GR(希腊语)",
                        "pl-PL(波兰语)","en-GB(英语英国)","en-PH(英语新加坡)","en-ZA(英语南非)","fr-MC(法语北非)",
                        "cs-CZ(捷克语)", "hu-HU(匈牙利语)","bg-BG(保加利亚语)","uk-UA(乌克兰语)"]
        
        self.Sheet_header = ["en_US", "zh_TW", "ru_RU", "fr_FR", "es_ES",
                            "pt_PT", "ar_AE", "ko_KR", "de_DE", "he_IL",
                            "tr_TR", "it_IT", "ro_RO", "th_TH", "el_GR",
                            "pl_PL", "en_GB", "en_PH", "en_ZA", "fr_MC",
                            "cs_CZ", "hu_HU", "bg_BG", "uk_UA"]
    
        self.prefix_name = ["en-US", "zh-TW", "ru-RU", "fr-FR", "es-ES",
                            "pt-PT", "ar-AE", "ko-KR", "de-DE", "he-IL",
                            "tr-TR", "it-IT", "ro-RO", "th-TH", "el-GR",
                            "pl-PL", "en-GB", "en-PH", "en-ZA", "fr-MC",
                            "cs-CZ", "hu-HU", "bg-BG", "uk-UA"]

        # cbt_vars 放入的值
        self.cbt_vars = []
        self.col_index = 1
        self.row_index = 1
        for option in self.cbt_options:
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.monty,text=option,variable=var)
            checkbutton.grid(column = self.col_index, row = self.row_index, sticky='W', padx='15', pady='8' )
            self.cbt_vars.append(var)

            # 一行六个
            self.col_index = self.col_index + 1
            if(self.col_index % 7 == 0):
                self.row_index = self.row_index + 1
                self.col_index = 1


        # Create a container to hold labels
        self.generate_labelframe = ttk.Labelframe(self.monty, text='  生成JS文件操作  ')
        self.generate_labelframe.grid(column=1,row = self.row_index + 2, sticky='W', columnspan= '30')

        self.label = tk.Label(self.generate_labelframe, text='js 文件')
        self.label.grid(column = 3,row= 3,  sticky='E')
        self.entry = tk.Entry(self.generate_labelframe, width= 40)
        self.entry.grid(column = 4,row= 3)
        self.selFile = ttk.Button(self.generate_labelframe, text='选择文件',width=10,command=self.get_file_path)
        self.selFile.grid(column = 5,row= 3)
    
        self.label_excel = tk.Label(self.generate_labelframe, text='excel 文件')
        self.label_excel.grid(column = 3,row= 4, sticky='E')
        self.entry_excel = tk.Entry(self.generate_labelframe, width= 40)
        self.entry_excel.grid(column = 4,row= 4)
        self.select_excel = ttk.Button(self.generate_labelframe, text='选择文件',width=10,command=self.get_excel_path)
        self.select_excel.grid(column = 5,row= 4)

        self.label_folder = tk.Label(self.generate_labelframe, text='生成文件夹路径')
        self.label_folder.grid(column = 3,row= 5, sticky='E')
        self.entry_folder = tk.Entry(self.generate_labelframe, width= 40)
        self.entry_folder.grid(column = 4,row= 5)
        self.select_folder = ttk.Button(self.generate_labelframe, text='选择文件夹',width=10,command=self.get_folder_path)
        self.select_folder.grid(column = 5,row= 5)

        self.action = ttk.Button(self.generate_labelframe,text='生成 JS',width=10,command = self.generate_js_file)
        self.action.grid(column=4, row= 8,rowspan=2,ipady=7)

        # 追加修改JS文件操作
        self.modify_labelframe = ttk.Labelframe(self.monty, text='  修改JS文件操作  ')
        self.modify_labelframe.grid(column=4,row = self.row_index + 2, sticky='W', columnspan= '30')

        self.modify_label_js = tk.Label(self.modify_labelframe, text='js 文件')
        self.modify_label_js.grid(column = 1,row= 3,  sticky='E')
        self.modify_entry_js = tk.Entry(self.modify_labelframe, width= 40)
        self.modify_entry_js.grid(column = 3,row= 3)
        self.modify_select_js = ttk.Button(self.modify_labelframe, text='选择文件',width=10,command=self.__get_js_file_path__)
        self.modify_select_js.grid(column = 5,row= 3)


        self.modify_label_excel = tk.Label(self.modify_labelframe, text='excel 文件')
        self.modify_label_excel.grid(column = 1,row= 4, sticky='E')
        self.modify_entry_excel = tk.Entry(self.modify_labelframe, width= 40)
        self.modify_entry_excel.grid(column = 3,row= 4)
        self.modify_select_excel = ttk.Button(self.modify_labelframe, text='选择文件',width=10,command=self.__modify_get_excel_path__)
        self.modify_select_excel.grid(column = 5,row= 4)

        self.modify_label_folder = tk.Label(self.modify_labelframe, text='JS文件夹路径')
        self.modify_label_folder.grid(column = 1,row= 5, sticky='E')
        self.modify_entry_folder = tk.Entry(self.modify_labelframe, width= 40)
        self.modify_entry_folder.grid(column = 3,row= 5)
        self.modify_select_folder = ttk.Button(self.modify_labelframe, text='选择文件夹',width=10,command=self.__modify_get_folder_path__)
        self.modify_select_folder.grid(column = 5,row= 5)

        self.modify_action = ttk.Button(self.modify_labelframe,text='修改 JS',width=10,command = self.__modify_js_file__)
        self.modify_action.grid(column=2, row= 8, sticky= 'W', columnspan= '2', ipady='7')

        self.check_action = ttk.Button(self.modify_labelframe,text='检查 JS',width=10,command = self.__check_js_file__)
        self.check_action.grid(column=2, row= 8, sticky='E', columnspan= '2', ipady='7')

    def get_file_path(self):
        self.js_file_path = filedialog.askopenfilename()
        self.entry.delete(0,tk.END) # 删除从开始到结束的文本S
        self.entry.insert(0, self.js_file_path)

    def __get_js_file_path__(self):
        self.modify_js_file_path = filedialog.askopenfilename()
        

    def get_excel_path(self):
        self.excel_file_path = filedialog.askopenfilename()
        self.entry_excel.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_excel.insert(0, self.excel_file_path)

    def __modify_get_excel_path__(self):
        self.modify_excel_file_path = filedialog.askopenfilename()
        self.modify_entry_excel.delete(0,tk.END) # 删除从开始到结束的文本
        self.modify_entry_excel.insert(0, self.modify_entry_excel)

    def get_folder_path(self):
        self.js_folder_path = filedialog.askdirectory()
        self.entry_folder.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_folder.insert(0,self.js_folder_path)

    def __modify_get_folder_path__(self):
        self.modify_js_folder_path = filedialog.askdirectory()
        self.modify_entry_folder.delete(0,tk.END) # 删除从开始到结束的文本
        self.modify_entry_folder.insert(0, self.modify_js_folder_path)

    # Modified Button Click Function
    def generate_js_file(self):   
        # 用UTF-8 打开文件
        logging.info("start generate_js_file")
        start = time.process_time()
        for index,var in enumerate(self.cbt_vars):
            if var.get() == 1:
                self.fieldProcess(index)

        end = time.process_time()
        mBox.showinfo('generate JS file', '耗时' + str(end-start) +'s')
        logging.info("end generate_js_file")

    def __modify_js_file__(self):
        logging.info("start modify_js_file")
        start = time.process_time()
        for index,var in enumerate(self.cbt_vars):
            if var.get() == 1:
                self.__modify_fields__(index)

        end = time.process_time()
        mBox.showinfo('modify JS file', '耗时' + str(end-start) + 's')
        logging.info("end modify_JS_file")

    def fieldProcess(self,index):
        #self.folder_name = os.path.basename(self.js_folder_path)
        folder_name = os.path.abspath(self.js_folder_path)
        combined_name = os.path.join(folder_name, self.prefix_name[index] + '.js')
        logging.info("生成js 文件名 " + combined_name)
   
        with open(self.js_file_path, 'r', encoding='utf-8' ) as file:
            with open(combined_name,'w+',encoding='utf-8') as fileW:
                for line in file:
                    #打印每一行
                    try:
                        if "'" in line:
                            splitValue = line.split("'")
                            if len(splitValue) == 3:
                                value =  self.repStr(splitValue[1], self.Sheet_header[index])
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

    # 增加字段的翻译
    def __modify_fields__(self, index):
        logging.info("start modify_fields")

        # 用来寻找表头
        #直接遍历文件夹下每一个JS文件
        for parent, dirnames, filenames in os.walk(self.modify_js_folder_path, followlinks=True):
            for filename in filenames:
                # logging.info('文件名称: ' + filename)
                file_path = os.path.join(parent, filename)
                # logging.info("文件完整路径: " + file_path)
                # prefixName = filename.split(".")
                if self.prefix_name[index] in filename:
                    logging.info("找到对应文件" + file_path)
                    self.__replace_fields__(file_path, index)
                else:
                    logging.info("未找到对应js 文件与列表相对应" + filename)

        logging.info("end modify_fields")      

    # 检查翻译是否正确
    def __replace_fields__(self):
        # 读取excel 遍历每个Sheet 找到
        # 如果'' 有值就遍历下一个，为空 就从zh_cn找到 key进行每个excel文件，每个sheet遍历查找
        pass


    #
    def __check_js_file__(self):
        pass