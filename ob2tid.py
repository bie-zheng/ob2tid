import os
import datetime

# 读取md文件内容

def extract_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    in_code_block = False
    for i in range(len(lines)):
        line = lines[i]

        # check if in code block
        if line.startswith('```'):
            in_code_block = not in_code_block

        # process headers
        if not in_code_block and line.startswith('#'):
            level = line.count('#')
            lines[i] = '!' * level + line[level:]

        # process unordered lists
        if not in_code_block and line.startswith('-'):
            lines[i] = '#' + line[2:]

        # process ordered lists
        if not in_code_block and line[0].isdigit() and line[1] == '.':
            lines[i] = '*' + line[2:]
    return ''.join(lines)

def add_head(file_path,tags) :
    # 获取不带后缀的文件名
    basename = os.path.splitext(file_path)[0]
    result = []
    for s in basename.split('\\'):
        for ss in s.split('/'):
            result.append(ss)
    basename = result[-1]
    # 获取创建和修改日期
    now = datetime.datetime.now()
    timestamp = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.hour).zfill(2) + str(
        now.minute).zfill(2) + str(now.second).zfill(2) + str(now.microsecond).zfill(6)
    # 输出结果
    title="title:"+basename
    creat="created:"+str(timestamp)
    modified="modified:"+str(timestamp)
    return creat+'\n'+modified+'\n'+'tags:'+tags+'\n'+"title:"+basename+"\n"+"type: text/vnd.tiddlywiki"+"\n\n"

def allinone(file_path,tags):
    output=add_head(file_path,tags)+extract_code(file_path)
#    print(output)
    basename = os.path.splitext(file_path)[0]
    result = []
    for s in basename.split('\\'):
        for ss in s.split('/'):
            result.append(ss)
    basename = result[-1]
    print(basename)
    filename=str(basename)+".tid"
    #下面这个创建完就不能重新创建了
  #  os.makedirs(file_output)
    with open(file_output+"/"+filename, 'w', encoding='utf-8') as f:
        f.write(output)

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isdir(file_path):
            process_folder(file_path)
        elif file_name.endswith(".md"):
            tags = os.path.basename(folder_path)
            allinone(file_path, tags)

#allinone('example.md','love')
#process_folder("C:/Users/别正/Desktop/个人")

import tkinter as tk
from tkinter import filedialog
import os

def browse_file():
    global file_input
    file_input = filedialog.askdirectory()
    folder_name.set(os.path.basename(file_input))

def browse_output():
    global file_output
    file_output = filedialog.askdirectory()
    output_name.set(os.path.basename(file_output))

def run_all():
    process_folder(file_input)
    #文件夹模式

def run_allin():
    allinone(file_input,"")
    #单文件模式
# 创建GUI窗口
root = tk.Tk()
root.title("ob2md")
root.geometry("400x200")
# 创建文件夹选择区域
folder_frame = tk.Frame(root)
folder_frame.pack(pady=10)
folder_label = tk.Label(folder_frame, text="请选择文件夹：")
folder_label.pack(side=tk.LEFT)
folder_btn = tk.Button(folder_frame, text="选择", command=browse_file)
folder_btn.pack(side=tk.LEFT)
folder_name = tk.StringVar()
folder_name.set("")
folder_display = tk.Label(folder_frame, textvariable=folder_name)
folder_display.pack(side=tk.LEFT)

# 创建输出路径选择区域
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_label = tk.Label(output_frame, text="请选择输出路径：")
output_label.pack(side=tk.LEFT)
output_btn = tk.Button(output_frame, text="选择", command=browse_output)
output_btn.pack(side=tk.LEFT)
output_name = tk.StringVar()
output_name.set("")
output_display = tk.Label(output_frame, textvariable=output_name)
output_display.pack(side=tk.LEFT)

# 创建运行按钮
run_frame = tk.Frame(root)
run_frame.pack(pady=10)
run_all_btn = tk.Button(run_frame, text="文件夹运行", command=run_all)
run_all_btn.pack(side=tk.LEFT, padx=10)
run_allin_btn = tk.Button(run_frame, text="单文件运行", command=run_allin)
run_allin_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()
