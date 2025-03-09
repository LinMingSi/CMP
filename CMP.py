import os
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def remove_png_files_from_screenshot(screenshots_dir):
    """记录screenshots文件夹中的所有.png文件并返回应当删除的文件数量和文件大小"""
    num = 0
    size = 0
    remove_file = []
    for filename in os.listdir(screenshots_dir):
        if filename.endswith('.png'):
            file_path = os.path.join(screenshots_dir, filename)
            try:
                num += 1
                size += os.path.getsize(file_path)
                remove_file.append(file_path)
            except OSError as e:
                print(f"Error accessing file {file_path}: {e}")
    return num, size, remove_file


def clean_folder():
    """清理指定路径下的.minecraft文件夹中的截图"""
    path = path_entry.get()  # 获取文件夹路径
    if not path:
        messagebox.showinfo(title='提示', message='未选择.minecraft文件夹路径')
        return

    if not os.path.exists(path):
        messagebox.showerror(title="错误", message="指定的路径不存在，请重新选择！")
        return

    screenshots_dirs = set()
    for dirpath, dirnames, _ in os.walk(path):
        if 'screenshots' == os.path.basename(dirpath):
            screenshots_dirs.add(dirpath)

    if not screenshots_dirs:
        messagebox.showinfo(title='提示', message='未发现截图文件夹！')
        return

    num, size, remove_file = 0, 0, []
    for screenshots_dir in screenshots_dirs:
        if os.path.exists(screenshots_dir):
            d_num, d_size, d_remove_files = remove_png_files_from_screenshot(screenshots_dir)
            num += d_num
            size += d_size
            remove_file.extend(d_remove_files)

    if remove_file:
        for file in remove_file:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except OSError as e:
                print(f"Error removing {file}: {e}")
        
        messagebox.showinfo(
            title='清理完成',
            message=f'清理完成！\n本次清理了{num}张截图\n释放了{size / 1024 / 1024:.2f}MB空间'
        )
    else:
        messagebox.showinfo(title='提示', message='没有可删除的截图文件！')


def show_warning():
    """显示清理确认的警告框"""
    warning = tk.Toplevel()
    warning.title('警告')
    warning.geometry('700x300')

    warning_label = tk.Label(
        warning,
        text='注意:这将清理所有游戏截图文件夹(名为screenshots的目录)下的.png文件，无法恢复。',
        font=('微软雅黑', 12)
    )
    warning_label.pack(pady=10)

    confirm_button = tk.Button(
        warning, 
        text='我已知晓，启动清理！', 
        font=('微软雅黑', 12), 
        command=lambda: [warning.destroy(), clean_folder()]
    )
    confirm_button.pack(pady=20)

    cancel_button = tk.Button(
        warning, 
        text='取消清理', 
        font=('微软雅黑', 12), 
        command=warning.destroy
    )
    cancel_button.pack()


# 主窗口创建
root = tk.Tk()
root.title('CMPv2.0')
root.geometry('400x560')

# 设置图标
if os.path.exists('icon.ico'):
    root.iconbitmap('icon.ico')

# 窗口内容
title = tk.Label(root, text='欢迎使用CMPv2.0', font=('宋体', 20), bd=2, relief='solid', width=20, fg='green')
title.pack(pady=10)

author = tk.Label(root, text='作者:Lin_Ming_Si', font=('宋体', 12))
author.pack()

path_label = tk.Label(root, text='请选择要清理的.minecraft文件夹', font=('微软雅黑', 10))
path_label.pack(pady=10)

path_entry = tk.Entry(root, font=('微软雅黑', 10), width=30)
path_entry.pack()

def choose_path():
    path = filedialog.askdirectory(title='请选择要清理的.minecraft文件夹')
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

path_button = tk.Button(root, text='选择路径', font=('微软雅黑', 10), command=choose_path)
path_button.pack()

clean_button = tk.Button(root, text='开始清理', font=('微软雅黑', 12), command=show_warning)
clean_button.pack(pady=20)

# 链接
def open_web(URL):
    webbrowser.open(URL)

github_link = tk.Label(root, text='Github: github.com/LinMingSi/CMP', font=('微软雅黑', 8), fg='blue', cursor='hand2')
bilibili_link = tk.Label(root, text='B站：space.bilibili.com/3494369153780199', font=('微软雅黑', 8), fg='blue', cursor='hand2')

bilibili_link.bind('<Button-1>', lambda event: open_web("https://space.bilibili.com/3494369153780199"))
github_link.bind('<Button-1>', lambda event: open_web("https://github.com/LinMingSi/CMP"))

github_link.pack(side=tk.BOTTOM, pady=5)
bilibili_link.pack(side=tk.BOTTOM, pady=5)

# 版权声明
copyright_label = tk.Label(root, text='本程序采用MIT开源协议', font=('微软雅黑', 8), fg='gray')
copyright_label.pack(side='bottom', pady=5)


root.mainloop()
