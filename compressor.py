import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import io
import webbrowser

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片压缩v1.0")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.file_path = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.quality = tk.IntVar(value=85)
        self.max_size_mb = tk.IntVar(value=10)
        self.include_subfolders = tk.BooleanVar(value=True)
        self.compression_in_progress = False
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        title = ttk.Label(main_frame, text="压缩工具", font=('Arial', 16))
        title.grid(row=0, column=0, pady=(0, 10), sticky="n")
        
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        notebook.grid_rowconfigure(0, weight=1)
        notebook.grid_columnconfigure(0, weight=1)
        
        single_tab = ttk.Frame(notebook)
        notebook.add(single_tab, text="单文件压缩")
        self.create_single_tab(single_tab)
        
        batch_tab = ttk.Frame(notebook)
        notebook.add(batch_tab, text="批量压缩")
        self.create_batch_tab(batch_tab)
        
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="设置")
        self.create_settings_tab(settings_tab)
        
        # 底部状态栏和GitHub按钮区域
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(bottom_frame, textvariable=self.status_var, 
                                  relief="sunken", padding=(5, 2), foreground="black")
        self.status_bar.grid(row=0, column=0, sticky="ew")
        
        # GitHub按钮
        github_button = ttk.Button(bottom_frame, text="GitHub", command=self.open_github)
        github_button.grid(row=0, column=1, padx=(5, 0), pady=2)
    
    def open_github(self):
        """打开GitHub个人主页"""
        webbrowser.open("https://github.com/SorakageMeiou")
    
    # 其余代码保持不变...
    def create_single_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="选择图片文件:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        file_frame = ttk.Frame(frame)
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        file_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Entry(file_frame, textvariable=self.file_path, state='readonly').grid(row=0, column=0, sticky="ew")
        ttk.Button(file_frame, text="浏览...", command=self.select_file).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(frame, text="压缩质量 (0-100):").grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        quality_frame = ttk.Frame(frame)
        quality_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        quality_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Scale(quality_frame, from_=10, to=100, orient="horizontal", 
                 variable=self.quality).grid(row=0, column=0, sticky="ew")
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=1, padx=5)
        
        ttk.Button(frame, text="压缩图片", command=self.compress_single, 
                  style="Accent.TButton").grid(row=4, column=0, pady=15)
        
        self.file_info = tk.Text(frame, height=6, width=40, state='disabled')
        self.file_info.grid(row=5, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.file_info.yview)
        scrollbar.grid(row=5, column=1, sticky="ns")
        self.file_info['yscrollcommand'] = scrollbar.set
        
        frame.grid_rowconfigure(5, weight=1)
    
    def create_batch_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="选择图片文件夹:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        folder_frame = ttk.Frame(frame)
        folder_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        folder_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Entry(folder_frame, textvariable=self.folder_path, state='readonly').grid(row=0, column=0, sticky="ew")
        ttk.Button(folder_frame, text="浏览...", command=self.select_folder).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Checkbutton(frame, text="包含子目录", variable=self.include_subfolders).grid(
            row=2, column=0, sticky="w", pady=(5, 10))
        
        ttk.Label(frame, text="压缩质量 (0-100):").grid(row=3, column=0, sticky="w", pady=(5, 5))
        
        quality_frame = ttk.Frame(frame)
        quality_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        quality_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Scale(quality_frame, from_=10, to=100, orient="horizontal", 
                 variable=self.quality).grid(row=0, column=0, sticky="ew")
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=1, padx=5)
        
        ttk.Button(frame, text="开始批量压缩", command=self.compress_batch, 
                  style="Accent.TButton").grid(row=5, column=0, pady=15)
        
        self.progress = ttk.Progressbar(frame, orient="horizontal", mode='determinate')
        self.progress.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        
        self.batch_info = tk.Text(frame, height=6, width=40, state='disabled')
        self.batch_info.grid(row=7, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.batch_info.yview)
        scrollbar.grid(row=7, column=1, sticky="ns")
        self.batch_info['yscrollcommand'] = scrollbar.set
        
        frame.grid_rowconfigure(7, weight=1)
    
    def create_settings_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="最大文件大小 (MB):").grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        size_frame = ttk.Frame(frame)
        size_frame.grid(row=1, column=0, sticky="w", pady=(0, 20))
        ttk.Spinbox(size_frame, from_=1, to=100, textvariable=self.max_size_mb, width=5).grid(row=0, column=0)
        ttk.Label(size_frame, text="MB").grid(row=0, column=1, padx=5)
        
        ttk.Label(frame, text="PNG转换策略:").grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        self.png_strategy = tk.StringVar(value="auto")
        ttk.Radiobutton(frame, text="自动转为JPEG (压缩率更高)", 
                       variable=self.png_strategy, value="auto").grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(frame, text="保持PNG格式 (保留透明度)", 
                       variable=self.png_strategy, value="keep").grid(row=4, column=0, sticky="w", pady=(0, 20))
        
        ttk.Button(frame, text="恢复默认设置", command=self.reset_settings).grid(row=5, column=0)
    
    def reset_settings(self):
        self.quality.set(85)
        self.max_size_mb.set(10)
        self.png_strategy.set("auto")
        messagebox.showinfo("提示", "已恢复默认设置")
        self.status_var.set("已恢复默认设置")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择要压缩的图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.file_path.set(file_path)
            self.update_file_info(file_path)
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择包含图片的文件夹")
        if folder_path:
            self.folder_path.set(folder_path)
            self.status_var.set(f"已选择文件夹: {folder_path}")
    
    def update_file_info(self, file_path):
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            with Image.open(file_path) as img:
                width, height = img.size
                format = img.format
            
            info_text = (
                f"文件名: {os.path.basename(file_path)}\n"
                f"大小: {file_size:.2f} MB\n"
                f"尺寸: {width} x {height}\n"
                f"格式: {format}\n"
                f"路径: {file_path}"
            )
            
            self.file_info.config(state='normal')
            self.file_info.delete(1.0, tk.END)
            self.file_info.insert(tk.END, info_text)
            self.file_info.config(state='disabled')
            
            if file_size < self.max_size_mb.get():
                self.status_var.set(f"提示: 文件已小于{self.max_size_mb.get()}MB，无需压缩")
            else:
                self.status_var.set("已选择文件，可以开始压缩")
        except Exception as e:
            self.status_var.set(f"更新文件信息失败: {str(e)}")
            self.set_error_status(f"更新文件信息失败: {str(e)}")
    
    def compress_single(self):
        if self.compression_in_progress:
            return
        
        input_path = self.file_path.get()
        if not input_path:
            messagebox.showerror("错误", "请先选择图片文件")
            self.set_error_status("请先选择图片文件")
            return
        
        try:
            original_size = os.path.getsize(input_path) / (1024 * 1024)
            if original_size < self.max_size_mb.get():
                messagebox.showinfo("提示", f"原始文件已经小于{self.max_size_mb.get()}MB，无需压缩")
                self.status_var.set(f"提示: 原始文件已小于{self.max_size_mb.get()}MB")
                return
            
            directory, filename = os.path.split(input_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_compressed_q{self.quality.get()}{ext}"
            output_path = os.path.join(directory, output_filename)
            
            self.compression_in_progress = True
            success, final_quality = self.compress_image(input_path, output_path, self.quality.get())
            self.compression_in_progress = False
            
            if success:
                compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                message = (
                    f"图片压缩成功!\n\n"
                    f"原始大小: {original_size:.2f} MB\n"
                    f"压缩后大小: {compressed_size:.2f} MB\n"
                    f"最终质量: {final_quality}\n\n"
                    f"保存在: {output_path}"
                )
                messagebox.showinfo("完成", message)
                self.status_var.set(f"压缩完成! 最终质量: {final_quality}")
                self.update_file_info(output_path)
            else:
                messagebox.showerror("压缩失败", f"图片压缩过程中出现错误")
                self.set_error_status("图片压缩过程中出现错误")
        except Exception as e:
            messagebox.showerror("错误", f"压缩过程中发生错误: {str(e)}")
            self.compression_in_progress = False
            self.set_error_status(f"压缩错误: {str(e)}")
    
    def compress_batch(self):
        if self.compression_in_progress:
            return
        
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showerror("错误", "请先选择图片文件夹")
            self.set_error_status("请先选择图片文件夹")
            return
        
        try:
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
            image_files = []
            
            if self.include_subfolders.get():
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file.lower().endswith(image_extensions):
                            image_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(folder_path):
                    if file.lower().endswith(image_extensions):
                        image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                messagebox.showerror("错误", "选择的文件夹中没有找到图片文件")
                self.set_error_status("文件夹中没有找到图片文件")
                return
            
            confirm = messagebox.askyesno("确认", f"找到 {len(image_files)} 张图片，是否开始批量压缩?")
            if not confirm:
                return
            
            self.compression_in_progress = True
            self.progress['maximum'] = len(image_files)
            self.progress['value'] = 0
            
            total_original_size = 0
            total_compressed_size = 0
            success_count = 0
            skip_count = 0
            
            for i, input_path in enumerate(image_files):
                self.root.update()
                self.status_var.set(f"正在处理: {os.path.basename(input_path)} ({i+1}/{len(image_files)})")
                
                try:
                    original_size = os.path.getsize(input_path) / (1024 * 1024)
                    total_original_size += original_size
                    
                    if original_size < self.max_size_mb.get():
                        skip_count += 1
                    else:
                        directory, filename = os.path.split(input_path)
                        name, ext = os.path.splitext(filename)
                        output_filename = f"{name}_compressed_q{self.quality.get()}{ext}"
                        output_path = os.path.join(directory, output_filename)
                        
                        success, final_quality = self.compress_image(input_path, output_path, self.quality.get())
                        
                        if success:
                            compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                            total_compressed_size += compressed_size
                            success_count += 1
                    
                    self.progress['value'] = i + 1
                except Exception as e:
                    self.status_var.set(f"处理 {os.path.basename(input_path)} 时出错: {str(e)}")
                    self.set_error_status(f"处理图片出错: {str(e)}")
            
            self.compression_in_progress = False
            self.status_var.set(f"批量压缩完成! 成功: {success_count}, 跳过: {skip_count}")
            
            info_text = (
                f"处理完成!\n\n"
                f"总图片数: {len(image_files)}\n"
                f"成功压缩: {success_count}\n"
                f"跳过(已小于{self.max_size_mb.get()}MB): {skip_count}\n\n"
                f"原始总大小: {total_original_size:.2f} MB\n"
                f"压缩后总大小: {total_compressed_size:.2f} MB\n"
                f"节省空间: {total_original_size - total_compressed_size:.2f} MB"
            )
            
            self.batch_info.config(state='normal')
            self.batch_info.delete(1.0, tk.END)
            self.batch_info.insert(tk.END, info_text)
            self.batch_info.config(state='disabled')
            
            messagebox.showinfo("完成", f"批量压缩完成!\n\n成功压缩 {success_count} 张图片\n跳过 {skip_count} 张已小于{self.max_size_mb.get()}MB的图片")
        except Exception as e:
            messagebox.showerror("错误", f"批量压缩过程中发生错误: {str(e)}")
            self.compression_in_progress = False
            self.set_error_status(f"批量压缩错误: {str(e)}")
    
    def compress_image(self, input_path, output_path, quality):
        max_size_bytes = self.max_size_mb.get() * 1024 * 1024
        
        try:
            with Image.open(input_path) as img:
                original_format = img.format
                file_base, file_ext = os.path.splitext(output_path)
                
                if original_format in ('PNG', 'GIF') and self.png_strategy.get() == "auto":
                    img = img.convert('RGB')
                    output_path = f"{file_base}.jpg"
                    output_format = 'JPEG'
                else:
                    output_format = original_format
                
                with io.BytesIO() as buffer:
                    img.save(buffer, format=output_format, quality=quality, optimize=True)
                    buffer_size = buffer.tell()
                    
                    if buffer_size <= max_size_bytes:
                        with open(output_path, 'wb') as f:
                            f.write(buffer.getvalue())
                        return True, quality
                
                for q in range(quality - 5, 10, -5):
                    with io.BytesIO() as buffer:
                        img.save(buffer, format=output_format, quality=q, optimize=True)
                        buffer_size = buffer.tell()
                        
                        if buffer_size <= max_size_bytes:
                            with open(output_path, 'wb') as f:
                                f.write(buffer.getvalue())
                            return True, q
                
                temp_img = img.copy()
                adjusted_quality = max(quality, 70)
                
                while True:
                    new_width = int(temp_img.width * 0.9)
                    new_height = int(temp_img.height * 0.9)
                    temp_img = temp_img.resize((new_width, new_height), Image.LANCZOS)
                    
                    with io.BytesIO() as buffer:
                        temp_img.save(buffer, format=output_format, quality=adjusted_quality, optimize=True)
                        buffer_size = buffer.tell()
                        
                        if buffer_size <= max_size_bytes:
                            with open(output_path, 'wb') as f:
                                f.write(buffer.getvalue())
                            return True, adjusted_quality
                    
                    if new_width < 100 or new_height < 100:
                        self.status_var.set(f"无法将 {os.path.basename(input_path)} 压缩到指定大小")
                        return False, quality
        
        except Exception as e:
            self.status_var.set(f"处理 {os.path.basename(input_path)} 时出错: {str(e)}")
            return False, quality
    
    def set_error_status(self, message):
        self.status_var.set(message)
        self.status_bar.config(foreground="red")
        self.root.after(5000, lambda: self.status_bar.config(foreground="black"))

if __name__ == "__main__":
    root = tk.Tk()
    
    if os.path.exists('icon.ico'):
        try:
            root.iconbitmap(default='icon.ico')
        except Exception as e:
            print(f"图标加载失败: {e}")
    
    app = ImageCompressorApp(root)
    root.mainloop()    