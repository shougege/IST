import tkinter as tk
import time
from tkinter import ttk
import os
from tkinter import filedialog
import pandas as pd


monty2 = ttk.LabelFrame(tab2,tex='web 2.0 SideMenu')
monty2.grid(column=400,row=500,padx=40,pady=30)


# def on_select():
#     selected_options = [var.get() for var in vars]
#     print("Selected option: ", selected_options)


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
    
# button = tk.Button(monty2, text="Get Selected Options", command=on_select)
# button.grid(column = 4,row = jrow +1,padx = 5,pady = 5)

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

label = tk.Label(labelsFrame, text='js 文件')
label.grid(column = 3,row= 3)
entry = tk.Entry(labelsFrame, width= 40)
entry.grid(column = 4,row= 3)
selFile = ttk.Button(labelsFrame, text='选择文件',width=8,command=get_file_path)
selFile.grid(column = 5,row= 3)

excel_file_path  = ''
def get_excel_path():
    global excel_file_path
    excel_file_path = filedialog.askopenfilename()
    entryexcel.delete(0,tk.END) # 删除从开始到结束的文本
    entryexcel.insert(0, excel_file_path)

labelexcel = tk.Label(labelsFrame, text='excel 文件')
labelexcel.grid(column = 3,row= 4)
entryexcel = tk.Entry(labelsFrame, width= 40)
entryexcel.grid(column = 4,row= 4)
selExcel = ttk.Button(labelsFrame, text='选择文件',width=8,command=get_excel_path)
selExcel.grid(column = 5,row= 4)

js_folder_path = ''
def get_folder_path():
    global js_folder_path
    js_folder_path = filedialog.askdirectory()
    entryFolder.delete(0,tk.END) # 删除从开始到结束的文本
    entryFolder.insert(0,js_folder_path)

labelFolder = tk.Label(labelsFrame, text='生成文件夹路径')
labelFolder.grid(column = 3,row= 5)
entryFolder = tk.Entry(labelsFrame, width= 40)
entryFolder.grid(column = 4,row= 5)
selFolder = ttk.Button(labelsFrame, text='选择文件夹',width=10,command=get_folder_path)
selFolder.grid(column = 5,row= 5)


rtAvg = 'block1_respo.rt'
cond = 'block1_trigger'

def repStr(para,selVal):
    print("entry the repStr", para)
    df = pd.DataFrame(pd.read_excel(excel_file_path))
    #print(df)
    #print(df['词条中文'])
    if rtAvg not in df.columns:
        df[rtAvg] = 9999

    if cond not in df.columns:
        df[cond] = 9999

    #print(para, len(para),  type(para), type('打印设置'), len('打印设置'))
    #search_result =  df[df['词条中文'] ==  para]  # df.loc[df['A'].str.contains("颁发者",na=False)]
    # 找到para 关键字的行
    try:
        filtered_rows =  df[df['zh_CN'] ==  para]
        row_number = filtered_rows.index[0]
        value = df.iloc[row_number][selVal]
    except KeyError:
        value = ''

    print(value)
    return value


def fieldProcess(index):
    folder_name = os.path.basename(js_folder_path)
    combined_name = os.path.join(folder_name, options[index] + '.js')
    print("combined: " , combined_name)
    #print("folder:", js_folder_path)
    #print(js_folder_path + options[index] +'.js')
    with open(js_file_path, 'r', encoding='utf-8' ) as file:
        with open(combined_name,'w+',encoding='utf-8') as fileW:
            for line in file:
                #打印每一行
                    if "'" in line:
                        splitValue = line.split("'")
                        if len(splitValue) == 3:
                            val =  repStr(splitValue[1], file_header[index])
                            fileW.write(line.replace(splitValue[1],val))
                    else:
                        fileW.write(line)
        
# Modified Button Click Function
def jsMultipleLanguage():
    print(js_file_path)
    # 用UTF-8 打开文件
    #print("vars: " , vars)
    for index,var in enumerate(vars):
        #print(var.get(),index)
        if var.get() == 1:
            fieldProcess(index)
    #action.configure(state='disabled')
    action.configure(text='trans0000')


action = ttk.Button(labelsFrame,text='trans',width=10,command=jsMultipleLanguage)
action.grid(column=4, row= 8,rowspan=2,ipady=7)