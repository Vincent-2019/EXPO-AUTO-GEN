import os
import tkinter as tk
from tkinter import messagebox

def generate_runexpo_script(username, start_number):
    # 設定檔案路徑
    base_dir = f"/home/ntutmms/Documents/{username}"
    
    # 檢查使用者資料夾是否存在
    if not os.path.isdir(base_dir):
        messagebox.showerror("錯誤", f"找不到使用者資料夾：{base_dir}")
        return

    # 計算資料夾數量並設定 total_runs
    folder_count = len([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    if folder_count <= 1:
        messagebox.showerror("錯誤", "資料夾數量不足以進行迭代。")
        return

    total_runs = folder_count - 1
    filename_prefix = f"/home/ntutmms/Documents/{username}/"

    # 生成 runexpo.sh 的內容
    script_content = f"""#!/bin/bash

# 从参数中获取值
total_runs={total_runs}
filename_prefix={filename_prefix}
start_number={start_number}

run_count=0

# 循环运行命令
while [ $run_count -lt $total_runs ]
do
    run_count=$((run_count + 1))

    # 构造当前迭代的文件名
    current_filename="{{filename_prefix}}{{start_number}}/sa.exp"

    echo "Running iteration $run_count with filename: $current_filename"

    # 运行 mpirun 命令
    mpirun -np 12 expo $current_filename

    # 等待上一次命令完成
    wait

    # 更新下一个文件名的编号
    start_number=$((start_number + 1))
done
"""

    # 寫入 runexpo.sh 到指定的使用者目錄
    script_path = os.path.join(base_dir, "runexpo.sh")
    with open(script_path, "w") as file:
        file.write(script_content)

    messagebox.showinfo("成功", f"runexpo.sh 文件已生成並儲存於：{script_path}")

def on_generate_click():
    username = entry_username.get()
    start_number = entry_start_number.get()

    if not username:
        messagebox.showwarning("警告", "請輸入使用者名稱")
        return

    try:
        start_number = int(start_number)
        generate_runexpo_script(username, start_number)
    except ValueError:
        messagebox.showwarning("警告", "起始號碼必須是整數！")

# 建立主視窗
root = tk.Tk()
root.title("runexpo.sh 生成器")
root.geometry("300x200")

# 使用者名稱輸入
label_username = tk.Label(root, text="使用者名稱：")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# 起始號碼輸入
label_start_number = tk.Label(root, text="起始號碼：")
label_start_number.pack(pady=5)
entry_start_number = tk.Entry(root)
entry_start_number.pack(pady=5)

# 生成按鈕
button_generate = tk.Button(root, text="生成 runexpo.sh", command=on_generate_click)
button_generate.pack(pady=20)

# 啟動 GUI
root.mainloop()
