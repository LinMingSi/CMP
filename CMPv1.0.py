import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 清理文件夹函数
def clean_folder():
    path = path_entry.get()
    if not path:
        return

    # 获取用户选择的选项
    option_value = option.get()

    # 根据选项执行不同的操作
    screenshots_path = os.path.join(path, 'screenshots')
    if option_value in [2, 3, 4, 5]:
        versions_path = os.path.join(path, 'versions')
        for version_folder in os.listdir(versions_path):
            version_path = os.path.join(versions_path, version_folder)
            if os.path.isdir(version_path):
                version_screenshots_path = os.path.join(version_path, 'screenshots')
                if os.path.exists(version_screenshots_path):
                    for filename in os.listdir(version_screenshots_path):
                        if filename.endswith('.png'):
                            os.remove(os.path.join(version_screenshots_path, filename))
        tk.messagebox.showinfo(title='提示', message='清理完成！')
    elif option_value == 6:
        screenshots_path = os.path.join(path, 'screenshots')
        if os.path.exists(screenshots_path):
            for filename in os.listdir(screenshots_path):
                if filename.endswith('.png'):
                    os.remove(os.path.join(screenshots_path, filename))
        versions_path = os.path.join(path, 'versions')
        if os.path.exists(versions_path):
            for version_folder in os.listdir(versions_path):
                version_path = os.path.join(versions_path, version_folder)
                if os.path.isdir(version_path):
                    version_screenshots_path = os.path.join(version_path, 'screenshots')
                    if os.path.exists(version_screenshots_path):
                        for filename in os.listdir(version_screenshots_path):
                            if filename.endswith('.png'):
                                os.remove(os.path.join(version_screenshots_path, filename))
        tk.messagebox.showinfo(title='提示', message='清理完成！')
    else:
        # 其他选项的处理逻辑...
        pass

# 添加警告弹窗
def show_warning():
    warning = tk.Toplevel()
    warning.title('警告')
    warning.geometry('700x300')
    warning_label = tk.Label(warning, text='注意:这将清理游戏截图文件夹下所有后缀名为.png的文件（应该没人会把重要的图片放在这里吧）\n声明:作者不会承担任何因为CMP而造成的图片丢失的责任', font=('微软雅黑', 12))
    warning_label.pack(pady=10)
    confirm_button = tk.Button(warning, text='我已知晓，重要图片已转移，启动清理！', font=('微软雅黑', 12), command=lambda : [warning.destroy(), clean_folder()])
    confirm_button.pack(pady=20)
    cancel_button = tk.Button(warning, text='有重要的图片需要转移，等我一下', font=('微软雅黑', 12), command=warning.destroy)
    cancel_button.pack()

# 创建主窗口
root = tk.Tk()
root.title('欢迎使用CMPv1.0')
root.geometry('400x560')  # 调整窗口大小

# 添加标题
title = tk.Label(root, text='欢迎使用CMPv1.0', font=('宋体', 20), bd=2, relief='solid', width=20, fg='green')
title.pack(pady=10)

# 添加作者信息
author = tk.Label(root, text='作者是Lin_Ming_Si', font=('宋体', 12))
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

# 添加Radiobutton
option = tk.IntVar()  # 定义变量
option.set(-1)  # 设置默认值

option_frame = tk.Frame(root)
option_frame.pack(pady=10)

options = [('不隔离任何版本', 1),
           ('隔离可安装mod的版本', 2),
           ('隔离非正式版', 3),
           ('隔离可安装mod的版本和非正式版', 4),
           ('隔离所有版本', 5),
           ('删除所有截图', 6)]

for text, value in options:
    option_button = tk.Radiobutton(option_frame, text=text, variable=option, value=value)
    option_button.pack(anchor='w')

# 添加清理按钮
clean_button = tk.Button(root, text='开始清理', font=('微软雅黑', 12), command=show_warning)
clean_button.pack(pady=20)

# 添加作者爱发电信息和链接
donate_label = tk.Label(root, text='作者爱发电:', font=('微软雅黑', 8))
donate_label.pack()

def open_afdian():
    import webbrowser
    webbrowser.open('https://afdian.net/a/cmpexe')

afdian_link = tk.Label(root, text='https://afdian.net/a/cmpexe', font=('微软雅黑', 8), fg='blue', cursor='hand2')
afdian_link.pack()
afdian_link.bind('<Button-1>', lambda event: open_afdian())

# 添加Github链接
def open_github():
    import webbrowser
    webbrowser.open('https://github.com/LinMingSi/CMP')

github_link = tk.Label(root, text='Github:https://github.com/LinMingSi/CMP', font=('微软雅黑', 8), fg='blue',
                       cursor='hand2')
github_link.pack()
github_link.bind('<Button-1>', lambda event: open_github())

# 添加B站链接
def open_bilibili():
    import webbrowser
    webbrowser.open('https://space.bilibili.com/3494369153780199')

bilibili_link = tk.Label(root, text='作者B站：https://space.bilibili.com/3494369153780199', font=('微软雅黑', 8),
                         fg='blue', cursor='hand2')
bilibili_link.pack()
bilibili_link.bind('<Button-1>', lambda event: open_bilibili())

# 添加版权声明
copyright_label = tk.Label(
    root, text='本程序采用GPLv3开源协议', font=('微软雅黑', 8), fg='gray', anchor='se'
)
copyright_label.pack(
    side='bottom', fill='x', padx=5, pady=5
)

root.mainloop()

