import tkinter as tk
import time
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
from tkinter import filedialog
import numpy as np
import pandas as pd
import re
import csv

def modify_csv_column_width(input_file,output_file,column_index,width):
    with open(input_file,'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        with open(output_file,'w+',newline='', encoding='utf8') as output:
            for i in range(len(rows)):
                rows[i][column_index] = rows[i][column_index].ljust(width)
                write = csv.writer(output)
                print("rows: " , rows[i])
                write.writerow(rows[i])
                #break


# Create instance
win = tk.Tk()

# Add as title
win.title("Internationalizatioin Script Tool")

# Disable resizing the GUI
#win.resizable(0,0)

# Tab Control introduced here ----------- ------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab1, text='first page') # Add the tab

tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2,text='second page') # Make second tab visible

tab3 = ttk.Frame(tabControl)            # Add a third tab
tabControl.add(tab3,text='third page')  # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make tab visible
# ~ Tab Control introduced here ----------------------------------


#---------------------------Tab1控件介绍-------------------#
# We are creating a container tab3 to hold all other widgets
monty = ttk.LabelFrame(tab1,text='excel to csv')
monty.grid(column=0,row=0,padx=10,pady=4)

excel_file_path  = ''
def get_excel_file_path():
    global excel_file_path
    excel_file_path = filedialog.askopenfilename()
    entry_csv.delete(0,tk.END) # 删除从开始到结束的文本
    entry_csv.insert(0,excel_file_path)

label_csv = tk.Label(monty, text='template file path')
label_csv.grid(column=0,row=8)
entry_csv = tk.Entry(monty,width=40)
entry_csv.grid(column=1,row=8)
selFile_csv = ttk.Button(monty,text='sel File',width=5,command=get_excel_file_path)
selFile_csv.grid(column=3,row=8)

# Create a container to hold labels
labelsFrame_csv = ttk.Labelframe(monty, text=' Embedded area ')
labelsFrame_csv.grid(column=0,row=10,columnspan=4)

# Modified Button Click Function
def clickCsv():
    action_csv.configure(text='trans over')

    # Read and store content
    # of an excel file
    read_file = pd.read_excel(excel_file_path)
    # Write the dataframe object
    # into csv file
    read_file.to_csv("Test.csv",
                    index=None,
                    header=True)
    

    print(pd.options.display.max_rows)
    # modify_csv_column_width("Test.csv", "newTest.csv",2, 30)

    # read csv file and convert
    # inot a dataframe object
    # df = pd.read_csv("Test.csv")
    
    # print(df.head())
    # 设置列宽和对齐方式
    # show the dataframe
    # print(df.head())

action_csv = ttk.Button(labelsFrame_csv,text='trans',width=10,command=clickCsv)
action_csv.grid(column=0,row=1,rowspan=2,ipady=7)


# ---------------Tab2 控件介绍 ------------------~#
# We are creating a container tab3 to hold all other widgets
monty2 = ttk.LabelFrame(tab2,tex='web 2.0 SideMenu')
monty2.grid(column=400,row=500,padx=40,pady=30)


def on_select():
    selected_options = [var.get() for var in vars]
    print("Selected option: ", selected_options)


# 这个js文件前缀也是显示的内容
options = ["en-US","zh-TW","ru-RU","fr-FR","es-ES","pt-PT","ar-AE","ko-KR",
           "de-DE","he-IL","tr-TR","it-IT","ro-RO","th-TH","el-GR","pl-PL"]
# zh-TW中国台湾 ru-RU俄语 fr-FR法语 es-ES西班牙语 pt-PT葡萄牙语 ar-AE阿拉伯语 ko-KR韩语
# de-DE德语 he-IL希伯来语 tr-TR土耳其语 it-IT意大利语 ro-RO罗马尼亚语 th-TH泰语 el-GR希腊语 pl-PL波兰语 
file_header = ["en_US","zh_TW","ru_RU","fr_FR","es_ES","pt_PT","ar_AE","ko_KR",
           "de_DE","he_IL","tr_TR","it_IT","ro_RO","th_TH","el_GR","pl_PL"]


# 全称名字含义  Turkish土耳其语 Hebrew希伯来语 Romanian罗马尼亚语 Thai泰国语 German德语 Greek希腊语
#              Czech捷克语 Ukrainian乌克兰语 Polish波兰语 Kazakh哈塞克语  Danish丹麦语 Norwegian挪威语
#              Swedish 瑞典语 Azerbaijani阿塞拜疆语 Hungarian匈牙利语 Vietnamese越南语 Bulgarian保加利亚语
vars = []
icol = 1
jrow = 1
for option in options:
    var = tk.IntVar()
    checkbutton = tk.Checkbutton(monty2,text=option,variable=var)
    #checkbutton.pack()
    checkbutton.grid(column=icol, row=jrow, padx=8, pady=5 )
    vars.append(var)
    print(vars)
    icol = icol + 1
    if(icol % 8 == 0):
        jrow = jrow + 1
        icol = 1
    
button = tk.Button(monty2, text="Get Selected Options", command=on_select)
button.grid(column = 4,row = jrow +1,padx = 5,pady = 5)

# Creating all three Radiobutton widgets within one Loop

js_file_path  = ''
def get_file_path():
    global js_file_path
    js_file_path = filedialog.askopenfilename()
    entry.delete(0,tk.END) # 删除从开始到结束的文本
    entry.insert(0, js_file_path)

# Create a container to hold labels
labelsFrame = ttk.Labelframe(monty2, text=' Embedded area ')
labelsFrame.grid(column=3,row=jrow + 10,columnspan=4)

label = tk.Label(labelsFrame, text='template file path')
label.grid(column = 3,row= 3)
entry = tk.Entry(labelsFrame, width= 40)
entry.grid(column = 4,row= 3)
selFile = ttk.Button(labelsFrame, text='sel File',width=8,command=get_file_path)
selFile.grid(column = 5,row= 3)

rtAvg = 'block1_respo.rt'
cond = 'block1_trigger'

def repStr(para,selVal):
    print("entry the repStr", para)
    df = pd.DataFrame(pd.read_excel(r'C:\Users\pantum\Desktop\国际化小工具\Entry.xlsx',sheet_name="Sheet2"))
    #print(df)
    #print(df['词条中文'])
    if rtAvg not in df.columns:
        df[rtAvg] = 9999

    if cond not in df.columns:
        df[cond] = 9999

    #print(para, len(para),  type(para), type('打印设置'), len('打印设置'))
    #search_result =  df[df['词条中文'] ==  para]  # df.loc[df['A'].str.contains("颁发者",na=False)]
    # 找到para 关键字的行
    filtered_rows =  df[df['zh_CN'] ==  para]
    row_number = filtered_rows.index[0]
    value = df.iloc[row_number][selVal]
    #print(filtered_rows, row_number, value)
    print(value)
    return value
    #print("index" ,  search_result.index)
    #row_numbers = search_result.index
    #print("number: " ,  df.loc[row_numbers])
   
    print("-----------------------------------------------")
    #print(df['词条中文'])
    #print(df['词条中文'][100])
    #row_indices =  np.where(df['词条中文'] == '列')[0]
    #print([df['词条中文'] == para])
    #print(df['词条中文'].str.contains('列',na=False))
    #print(df.loc[5])
# Modified Button Click Function
def clickMe():
    print(js_file_path)
    flag = False
    # 用UTF-8 打开文件
    index = 0
    print("vars: " , vars)
    for index,var in enumerate(vars):
        print(var.get(),index)
        if var.get() == 1:
            with open(js_file_path, 'r', encoding='utf-8' ) as file:
                with open(r'C:\Users\pantum\Desktop\国际化小工具\en_US.js','w+',encoding='utf-8') as fileW:
                    for line in file:
                        #打印每一行
                        # // 不处理
                        if flag or '//' in line:
                            fileW.write(line)
                            flag = True
                            continue
                        # 使用正则表达式
                        pattern = re.compile(r'{|}|^\s*$')
                        if pattern.search(line):
                            #print('pass: ')
                            fileW.write(line)
                            ''''''
                        else:
                            #print(line, len(line))
                            # 去除:后面的空格
                            delimiters = [": ", ","]
                            pattern = '|'.join(map(re.escape,delimiters))
                            
                            lineStr = re.split(pattern,line)

                            # 因为字串中'' 所有这里的分隔符需要用“” 表示
                            val =  repStr(lineStr[1][1:-1],file_header[index])
                            newLine = line.replace(lineStr[1][1:-1],val)
                            print(newLine)
                            fileW.write(newLine)
    #action.configure(state='disabled')
    action.configure(text='trans0000')
action = ttk.Button(labelsFrame,text='trans',width=10,command=clickMe)
action.grid(column=4, row= 5,rowspan=2,ipady=7)

#------------------------------Tab3控件介绍-------------------------#
# We are creating a container tab3 to hold all other widgets
monty3 = ttk.LabelFrame(tab3,text='提取中文关键字')
monty3.grid(column=0,row=0,padx=40,pady=30)

dat_file_path  = ''
def get_dat_file_path():
    global dat_file_path
    dat_file_path = filedialog.askopenfilename()
    dat_entry_path.delete(0,tk.END) # 删除从开始到结束的文本
    dat_entry_path.insert(0,dat_file_path)

label_csv = tk.Label(monty3, text='dat file path')
label_csv.grid(column=3,row=8)
dat_entry_path = tk.Entry(monty3,width=40)
dat_entry_path.grid(column=5,row=8)
selFile_csv = ttk.Button(monty3,text='选择文件',width=10,command=get_dat_file_path)
selFile_csv.grid(column=10,row=8)

# Create a container to hold labels
labelsFrame_dat = ttk.Labelframe(monty3, text=' Embedded area ')
labelsFrame_dat.grid(column=5,row=15,columnspan=4)

# Modified Button Click Function
def clickDat():
    print(dat_file_path)


    pattern = re.compile(r"'((?:[^'\\]|\\.|\\\\)*)'")
    save_data = []
    with open(dat_file_path,'r', encoding="utf-8") as file:
        with open("test.txt","w+", encoding="utf-8") as wFile:
            str_array = []
            for line in file:
                if  '//om' in line:
                    break
                if "'" in line:
                    splitValue = line.split("'")
                    if len(splitValue) == 3:
                        str_array.append(splitValue[1])

                    elif len(splitValue) > 3:
                        print("len: ", len(splitValue))
                    else:
                        print("---------over-------------")
                    #print("len: " , len(splitValue))
                    
                    dic = {"词条（简体中文或者英文）": splitValue[1],"限制长度（字符）" :''}
                    save_data.append(dic)
 
            # 使用set进行去重
            unique_str_array = list(set(str_array))
            for i in unique_str_array:
                wFile.write(i)
                wFile.write('\n')
    mBox.showinfo('词条提取','完成')
    
    #df2 = pd.DataFrame(save_data)
    #df2.to_excel('导入.xlsx',index=False)

action_csv = ttk.Button(labelsFrame_dat,text='trans',width=10,command=clickDat)
action_csv.grid(column=0,row=1,rowspan=2,ipady=7)


# Add some space around each Label
# for child in labelsFrame.winfo_children():
#     child.grid_configure(padx=8,pady=4)

# def on_select():
#     selected_options = [var.get() for var in vars]
#     print("Selected option:",selected_options)

# options = ["en_US", "zh_TW", "ru_RU", "Italian"]

# vars = []
# for option in options:
#     var = tk.IntVar()
#     checkbutton = tk.Checkbutton(win,text=option, variable=var)
#     checkbutton.pack()
#     vars.append(var)

# button = tk.Button(win, text="Get Selected Optioins", command=on_select)
# button.pack()

win.mainloop()

