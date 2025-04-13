import os
import webbrowser
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Tuple
import platform


class MinecraftCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Minecraft截图清理工具 v2.1')
        self.geometry('400x560')
        self.cancelled = False
        
        self.setup_ui()
        self.load_icon()
        self.setup_path_combobox()

    def setup_ui(self):
        """初始化用户界面"""
        # 标题区域
        tk.Label(
            self,
            text='欢迎使用CMPv2.1',
            font=('宋体', 20),
            bd=2,
            relief='solid',
            width=20,
            fg='green'
        ).pack(pady=10)

        tk.Label(self, text='作者: Lin_Ming_Si', font=('宋体', 12)).pack()

        # 路径选择区域
        path_frame = tk.Frame(self)
        path_frame.pack(pady=8, fill=tk.X, padx=10)

        tk.Label(
            path_frame,
            text='请选择.minecraft文件夹位置：',
            font=('微软雅黑', 10)
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=3)

        self.path_entry = ttk.Combobox(
            path_frame,
            font=('微软雅黑', 10),
            width=28
        )
        self.path_entry.grid(row=1, column=0, sticky=tk.EW, padx=(0, 5))

        ttk.Button(
            path_frame,
            text='浏览...',
            command=self.choose_path
        ).grid(row=1, column=1, sticky=tk.E)

        path_frame.columnconfigure(0, weight=1)

        # 操作按钮
        self.clean_btn = ttk.Button(
            self,
            text='开始清理',
            command=self.confirm_clean_action
        )
        self.clean_btn.pack(pady=15)

        # 底部链接
        self.create_link(
            'GitHub: github.com/LinMingSi/CMP',
            'https://github.com/LinMingSi/CMP'
        ).pack(side=tk.BOTTOM, pady=3)
        
        self.create_link(
            'Bilibili: space.bilibili.com/3494369153780199',
            'https://space.bilibili.com/3494369153780199'
        ).pack(side=tk.BOTTOM, pady=3)

        tk.Label(
            self,
            text='本程序采用MIT开源协议',
            font=('微软雅黑', 8),
            fg='gray'
        ).pack(side=tk.BOTTOM, pady=6)

    def create_link(self, text, url):
        """创建可点击链接"""
        link = tk.Label(
            self,
            text=text,
            font=('微软雅黑', 8),
            fg='blue',
            cursor='hand2'
        )
        link.bind('<Button-1>', lambda e: webbrowser.open(url))
        return link

    def load_icon(self):
        """加载程序图标"""
        
        if os.path.exists('icon.ico'):
            self.iconbitmap('icon.ico')

    def setup_path_history(self):
        """初始化路径历史记录"""
        self.path_entry['values'] = self.get_minecraft_paths() + self.load_history()
        self.path_entry.bind('<<ComboboxSelected>>', self.on_path_selected)

    def setup_path_combobox(self):
        """初始化路径下拉框"""
        self.path_entry['values'] = self.get_minecraft_paths()
        self.path_entry.bind('<<ComboboxSelected>>', self.on_path_selected)

    def on_path_selected(self, event):
        """路径选择事件处理"""
        pass

    # ----------------- 核心功能 -----------------
    def start_clean_thread(self):
        """启动清理线程"""
        self.cancelled = False
        self.clean_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.clean_screenshots).start()

    def clean_screenshots(self):
        """执行清理操作"""
        target_path = self.path_entry.get()
        
        if not self.validate_path(target_path):
            self.clean_btn.config(state=tk.NORMAL)
            return

        screenshot_dirs = self.find_dirs(target_path)
        if not screenshot_dirs:
            messagebox.showinfo('提示', '未找到任何截图文件夹')
            self.clean_btn.config(state=tk.NORMAL)
            return

        files_to_remove = self.collect_screenshot_files(screenshot_dirs)
        if not files_to_remove:
            messagebox.showinfo('提示', '未找到可清理的截图文件')
            self.clean_btn.config(state=tk.NORMAL)
            return
        self.clean_btn.config(text='正在清理...')
        self.show_progress(files_to_remove)

    def validate_path(self, path):
        """验证目标路径"""
        if not path:
            messagebox.showinfo('提示', '请先选择.minecraft文件夹路径')
            return False
        if not os.path.exists(path):
            messagebox.showerror('路径错误', '指定路径不存在或无法访问，请重新选择')
            return False
        return True

    def find_dirs(self, path, dir_name="screenshots"):
        """查找特点名称目录"""
        try:
            return {
                os.path.join(root, dir_name)
                for root, dirs, _ in os.walk(path)
                if dir_name in dirs
            }
        except Exception as e:
            messagebox.showerror('扫描错误', f'无法扫描目录: {str(e)}')
            return set()

    def limited_depth_find_dirs(self, path, dir_name="screenshots", max_depth=3):
        """有限深度目录搜索"""
        found = set()
        try:
            for root, dirs, _ in os.walk(path):
                current_depth = root[len(path):].count(os.sep)
                if current_depth >= max_depth:
                    del dirs[:]  # 停止深入
                if dir_name in dirs:
                    found.add(os.path.join(root, dir_name))
        except Exception as e:
            messagebox.showerror('扫描错误', f'无法扫描目录: {str(e)}')
            return set()
        return found

    def collect_screenshot_files(self, screenshot_dirs):
        """收集所有截图文件"""
        files_to_remove = []
        for dir_path in screenshot_dirs:
            if os.path.exists(dir_path) and self.check_permissions(dir_path):
                files = self.collect_png_files_info(dir_path)
                files_to_remove.extend(files)
        return files_to_remove

    def collect_png_files_info(self, directory):
        """收集PNG文件信息"""
        png_files = [
            os.path.join(directory, f) 
            for f in os.listdir(directory) 
            if f.endswith('.png')
        ]
        return png_files
    def cancel(self):
        self.cancelled = True

    def show_progress(self, files):
        """显示删除进度"""
        progress_frame = tk.Frame(self)
        progress_frame.pack(padx=10, pady=10)
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        progress_bar.pack(side="left", pady=8)
        cancel_button = tk.Button(progress_frame, text="取消", command=self.cancel)
        cancel_button.config(width=10, state=tk.NORMAL)
        cancel_button.pack(side="left", padx=10)
        try:
            error_count = 0
            total = len(files)
            total_size = sum(os.path.getsize(f) for f in files)
            for index, file_path in enumerate(files, 1):
                if self.cancelled:
                    break
                try:
                    os.remove(file_path)
                except Exception as e:
                    self.handle_deletion_error(file_path, e)
                    error_count+=1
                    total_size-=os.path.getsize(file_path)
                finally:
                    progress_bar['value'] = (index / total) * 100
                    self.update()
                    
            
            if not self.cancelled:
                if error_count > 0:
                    messagebox.showinfo(
                        '清理完成',
                        f'成功清理 {len(files)-error_count} 张截图文件\n'
                        f'释放空间: {total_size/1024**2:.2f}MB\n'
                        f'删除失败: {error_count} 张截图文件'
                    )
                else:
                    messagebox.showinfo(
                        '清理完成',
                        f'成功清理 {len(files)} 张截图文件\n'
                        f'释放空间: {total_size/1024**2:.2f}MB'
                    )
            else:
                messagebox.showinfo(
                    '提示',
                    '清理操作已取消'
                    f'{progress_bar['value']:.2f}%的截图文件被删除\n'
                    )
        finally:
            progress_frame.destroy()
            self.clean_btn.config(text="开始清理", state=tk.NORMAL)

    def handle_deletion_error(self, file_path, error):
        """处理删除错误"""
        if self.cancelled:
            return
        if os.path.exists(file_path):
            messagebox.showerror(
                '删除失败',
                f'无法删除文件: {os.path.basename(file_path)}\n错误: {str(error)}'
            )
        else:
            return

    # ------------------ 工具方法 ------------------
    def choose_path(self):
        """选择路径"""
        path = filedialog.askdirectory(title='请选择要清理的.minecraft文件夹')
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.add_to_session_history(path)
    
    def add_to_session_history(self, path):
        """添加路径到当前会话历史"""
        current_values = list(self.path_entry['values'])
        if path in current_values:
            current_values.remove(path)
        current_values.insert(0, path)
        self.path_entry['values'] = current_values[:5]  # 保留最近5条
    
    def get_minecraft_paths(self):
        """获取常见.minecraft路径"""
        paths = []
        if platform.system() == "Windows":
            # Windows
            paths = [os.path.join(os.getenv('APPDATA', ''), '.minecraft'),*self.limited_depth_find_dirs(os.environ['USERPROFILE'],".minecraft")]
        elif platform.system() == "Linux":
            # Unix路径
            paths = [os.path.expanduser('~/.minecraft')]
        
        return list(set(paths))

    def check_permissions(self, path):
        """检查写入权限"""
        if not os.access(path, os.W_OK):
            messagebox.showerror('权限错误', '没有写入权限，请以管理员身份运行')
            return False
        return True

    # ------------------ 确认对话框 ------------------
    def confirm_clean_action(self):
        """显示确认对话框"""
        if messagebox.askyesno(
            title="确认清理",
            icon="warning",
            message="即将永久删除所有截图文件，此操作不可恢复！\n\n确定要继续吗？"
        ):
            self.start_clean_thread()


if __name__ == '__main__':
    app = MinecraftCleanerApp()
    app.mainloop()
