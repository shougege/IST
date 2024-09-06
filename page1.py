import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mBox
import pandas as pd
import time
import csv
import logging
import os

def modify_csv_column_width(input_file,output_file,column_index,width):
    with open(input_file,'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        with open(output_file,'w+',newline='', encoding='utf8') as output:
            for i in range(len(rows)):
                rows[i][column_index] = rows[i][column_index].ljust(width)
                write = csv.writer(output)
                print("rows: " , rows[i])
                logging.info("rows: ", rows[i])
                write.writerow(rows[i])
                #break

class Page1:
    #---------------------------Tab1控件介绍-------------------#
    # We are creating a container tab3 to hold all other widgets
    def __init__(self, master) -> None:

        # Excel to CSV 
        self.monty = ttk.LabelFrame(master,text='Excel to CSV')
        self.monty.grid(column=0, row=0, padx=60, pady=20)

        self.label_excel = tk.Label(self.monty, text='Excel文件路径')
        self.label_excel.grid(column=0,row=8, pady=10)
        self.entry_excel = tk.Entry(self.monty,width=40)
        self.entry_excel.grid(column=1,row=8, pady=10)
        self.selFile_excel = ttk.Button(self.monty,text='选择文件',width = 10,command=self.get_excel_file_path)
        self.selFile_excel.grid(column=3,row=8, pady=10)

        self.label_excel_csv = tk.Label(self.monty, text='生成*.csv文件名')
        self.label_excel_csv.grid(column=0,row=10,pady=10)
        self.generate_csv_filename = tk.Entry(self.monty,width=40)
        self.generate_csv_filename.grid(column=1,row=10,pady=10)

        self.action_csv = ttk.Button(self.monty,text='to CSV',width=10,command=self.excel_to_csv)
        self.action_csv.grid(column=1, row=12, ipady= 5, pady=10)

       # CSV to Excel
        self.monty1 = ttk.LabelFrame(master, text='CSV to Excel')
        self.monty1.grid(column=0, row=2,padx=60,pady=20)

        self.label_csv = tk.Label(self.monty1, text='CSV 文件路径')
        self.label_csv.grid(column=0, row=8,pady=10)
        self.entry_csv = tk.Entry(self.monty1, width=40)
        self.entry_csv.grid(column=1,row=8,pady=10)
        self.selFile_csv = ttk.Button(self.monty1, text='选择文件', width = 10, command=self.get_csv_file_path)
        self.selFile_csv.grid(column=3,row=8,pady=10)

        self.label_csv_excel = tk.Label(self.monty1, text='生成*.xlsx文件名')
        self.label_csv_excel.grid(column=0,row=10,pady=10)
        self.entry_excel_filename = tk.Entry(self.monty1,width=40)
        self.entry_excel_filename.grid(column=1,row=10,pady=10)

        self.action_excel = ttk.Button(self.monty1,text='to Excel',width=10,command=self.csv_to_excel)
        self.action_excel.grid(column=1, row=12, ipady= 5, pady=10)

    def get_excel_file_path(self):
        self.excel_file_path = filedialog.askopenfilename()
        self.entry_excel.delete(0,tk.END) # 删除从开始到结束的文本
        self.entry_excel.insert(0,self.excel_file_path)

    # Modified Button Click Function
    def excel_to_csv(self):
        # Read and store content
        logging.info("excel_to_csv start")
        logging.info(self.generate_csv_filename.get())
        try:
            directory, filename = os.path.split(self.excel_file_path)
        except:
            logging.info("os.path ssplit excel_file_path 错误!")

        new_filename = os.path.join(directory,self.generate_csv_filename.get())
        start = time.process_time()

         # into csv file
        try: 
            read_file = pd.read_excel(self.excel_file_path)
        except:
            logging.info("read_excel 错误!")

        try:
            read_file.to_csv(new_filename, index=False)
        except:
            logging.info("to_csv 错误!")
        end = time.process_time()

        mBox.showinfo('Excel to CSV','耗时'+ str(end-start) + 's')
        logging.info("excel_to_csv end")

    def get_csv_file_path(self):
        self.csv_file_path = filedialog.askopenfilename()
        self.entry_csv.delete(0, tk.END) # 删除从开始到结束的文本
        self.entry_csv.insert(0,self.csv_file_path)

    def csv_to_excel(self):
        # Read and store content
        logging.info("csv_to_excel start")
        logging.info(self.entry_excel_filename.get())

        try:
            directory, filename = os.path.split(self.csv_file_path)
        except:
            logging.info("os.path.split csv_file_path 错误!")
        
        new_filename = os.path.join(directory,self.entry_excel_filename.get())
        start = time.process_time()
        # of an CSV file

        try:
            df = pd.read_csv(self.csv_file_path)
        except:
            logging.info("read_csv 错误!")
        
        # into excel file
        try:
            df.to_excel(new_filename,index=False)
        except:
            logging.info("to excel 错误")

        end = time.process_time()

        mBox.showinfo('CSV to Excel','耗时'+ str(end-start) + 's')
        logging.info("csv_to_excel end")

     