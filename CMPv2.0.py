import os,webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox,ttk
# 清理文件夹函数
def clean_folder():
    num=0
    size=0
    path = path_entry.get()#得到.minecraft文件夹路经
    if not path:
        tk.messagebox.showinfo(title='提示', message='未选择.minecraft文件夹路径')
        return
    remove_file=[]
    screenshots_dirs=set()#创建一个集合，以免一个文件夹被多次记录
    for dirpath, dirnames, _ in os.walk(path):
        if 'screenshots'==os.path.basename(dirpath):
            screenshots_dirs.add(dirpath)
            print(f"发现screenshots文件夹:{dirpath}")
    for screenshots_dir in screenshots_dirs:
        if os.path.exists(screenshots_dir):#判断screenshots文件夹是否存在
            for filename in os.listdir(screenshots_dir):#遍历screenshots文件夹
                if filename.endswith('.png'):#判断文件末尾是否为png
                    num+=1#记录清理截图数
                    size+=os.path.getsize(os.path.join(screenshots_dir, filename))#记录被清理截图大小
                    remove_file.append(os.path.join(screenshots_dir, filename))#记录被清理截图路经
    for i in remove_file:
        print(f"remove:{i}")
        os.remove(i)
    tk.messagebox.showinfo(title='提示', message=f'清理完成！\n本次清理了{num}张截图\n增加了{size/1024}kb空间')

# 添加警告弹窗
def show_warning():
    warning = tk.Toplevel()
    warning.title('警告')
    warning.geometry('700x300')
    warning_label = tk.Label(warning, text='注意:这将清理游戏截图文件夹(名为screenshots的目录)下所有后缀名为.png的文件（应该没人会把重要的图片放在这里吧）\n声明:作者不会承担任何因为CMP而造成的图片丢失的责任', font=('微软雅黑', 12))
    warning_label.pack(pady=10)
    confirm_button = tk.Button(warning, text='我已知晓，重要图片已转移，启动清理！', font=('微软雅黑', 12), command=lambda : [warning.destroy(), clean_folder()])
    confirm_button.pack(pady=20)
    cancel_button = tk.Button(warning, text='有重要的图片需要转移，等我一下', font=('微软雅黑', 12), command=warning.destroy)
    cancel_button.pack()

# 创建主窗口
root = tk.Tk()
root.title('欢迎使用CMPv2.0')
root.geometry('400x560')  # 调整窗口大小
# 设置窗口图标
if os.path.exists('icon.ico') :#判断图标文件是否存在
    root.iconbitmap('icon.ico')  
# 添加标题
title = tk.Label(root, text='欢迎使用CMPv2.0', font=('宋体', 20), bd=2, relief='solid', width=20, fg='green')
title.pack(pady=10)

# 添加作者信息
author = tk.Label(root, text='作者:Lin_Ming_Si', font=('宋体', 12))
author.pack()

# 添加路径选择说明
path_label = tk.Label(root, text='请选择要清理的.minecraft文件夹', font=('微软雅黑', 10))
path_label.pack(pady=10)

# 添加路径选择输入框
path_entry = tk.Entry(root, font=('微软雅黑', 10), width=30)
path_entry.pack()

# 打开文件对话框选择路径
def choose_path():
    path = filedialog.askdirectory(title='请选择要清理的.minecraft文件夹')
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

# 添加路径选择按钮
path_button = tk.Button(root, text='选择路径', font=('微软雅黑', 10), command=choose_path)
path_button.pack()

# 添加清理按钮
clean_button = tk.Button(root, text='开始清理', font=('微软雅黑', 12), command=show_warning)
clean_button.pack(pady=20)


# 添加链接
def open_web(URL):
    webbrowser.open(URL)

github_link = tk.Label(root, text='Github:github.com/LinMingSi/CMP', font=('微软雅黑', 8), fg='blue',
                       cursor='hand2')
bilibili_link = tk.Label(root, text='作者B站：space.bilibili.com/3494369153780199', font=('微软雅黑', 8),
                         fg='blue', cursor='hand2')

bilibili_link.bind('<Button-1>', lambda event: open_web("space.bilibili.com/3494369153780199"))
github_link.bind('<Button-1>', lambda event: open_web("github.com/LinMingSi/CMP"))

# 添加版权声明
copyright_label = tk.Label(
    root, text='本程序采用GPLv3开源协议', font=('微软雅黑', 8), fg='gray', anchor='se'
)
copyright_label.pack(
    side='bottom', fill='x', padx=5, pady=5
)
github_link.pack(side=tk.BOTTOM,pady=5)
bilibili_link.pack(side=tk.BOTTOM,pady=5)

root.mainloop()

