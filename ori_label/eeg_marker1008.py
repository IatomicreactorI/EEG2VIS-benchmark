import tkinter as tk
import time
import keyboard
import os
from datetime import datetime
from psychopy import parallel

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前 .py 脚本的绝对路径
output_file = "new_recording.vmrk"
output_path = os.path.join(script_dir, output_file)  # 将文件保存到脚本所在的目录

# 初始化变量
markers = ['S 1', 'S 2', 'S 3']
marker_index = 0
event_count = 0
start_time = None
recorded_markers = []

# 初始化并行端口，用于与BrainVision交互
p_port = parallel.ParallelPort(address='0x3FF8')

# Function to get current timestamp for Mk1
def get_current_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

# Write the header for the vmrk file
def write_vmrk_header():
    with open(output_path, 'w') as file:
        file.write("BrainVision Data Exchange Marker File Version 1.0\n\n")
        file.write("[Common Infos]\n")
        file.write("Codepage=UTF-8\n")
        file.write(f"DataFile=xxx.eeg\n\n")  # Assuming the same EEG file name
        file.write("[Marker Infos]\n")
        file.write("; Each entry: Mk<Marker number>=<Type>,<Description>,<Position in data points>,\n")
        file.write("; <Size in data points>, <Channel number (0 = marker is related to all channels)>\n")
        file.write("; Fields are delimited by commas, some fields might be omitted (empty).\n")
        file.write('; Commas in type or description text are coded as "\\1".\n')
        file.write(f"Mk1=New Segment,,1,1,0,{get_current_timestamp()}\n")

# Function to record marker event and append to vmrk file
def record_marker():
    global marker_index, event_count, start_time
    if start_time is not None:
        # Calculate elapsed time and convert to position in data points
        current_time = time.time()
        elapsed_time = current_time - start_time
        sampling_rate = 1000  # Assuming sampling rate is 1000Hz
        position = int(elapsed_time * sampling_rate)

        # Create marker
        marker = markers[marker_index % 3]  # Alternate between S1, S2, and S3
        marker_entry = f'Mk{event_count + 2}=Stimulus,{marker},{position},1,0\n'
        recorded_markers.append(marker_entry)
        event_count += 1
        marker_index += 1

        # Write marker to file
        with open(output_path, 'a') as file:
            file.write(marker_entry)

        # Update the counter label
        counter_label.config(text=f"Event Count: {event_count}")

        # 通过并行端口发送标记（按顺序发送 S1, S2, S3）
        marker_value = (marker_index % 3) + 1  # 1 for S1, 2 for S2, 3 for S3
        p_port.setData(marker_value)
        # 短暂延时后清除标记
        time.sleep(0.01)  # 10毫秒的延时确保设备可以接收标记
        p_port.setData(0)
    else:
        print("Recording has not started yet")

# Start the recording by initializing start_time and writing header
def start_recording():
    global start_time, event_count, marker_index
    start_time = time.time()
    event_count = 0
    marker_index = -1
    write_vmrk_header()  # Create or overwrite vmrk file with header
    counter_label.config(text="Event Count: 0")
    status_label.config(text="●", fg="red")  # 显示红色的状态指示点
    update_timer()  # Start updating timer

# Function to update the timer label
def update_timer():
    if start_time is not None:
        current_time = time.time() - start_time
        # 精确到毫秒
        timer_label.config(text=f"Elapsed Time: {current_time:.3f} seconds")
    window.after(100, update_timer)  # Call this function every 100 milliseconds

# Function to handle key press and call record_marker
def on_enter_key(event):
    record_marker()

# Function to display file save path when program ends
def on_closing():
    print(f"The .vmrk file has been saved at: {output_path}")
    window.destroy()

# 创建 GUI 窗口
window = tk.Tk()
window.title("EEG Marker Recorder")

# 显示记录数量的标签
counter_label = tk.Label(window, text="Event Count: 0", font=("Arial", 14))
counter_label.pack(pady=20)

# 显示计时器的标签
timer_label = tk.Label(window, text="Elapsed Time: 0.000 seconds", font=("Arial", 14))
timer_label.pack(pady=20)

# 显示开始按钮
start_button = tk.Button(window, text="Start", font=("Arial", 14), command=start_recording)
start_button.pack(pady=20)

# 显示红色状态指示器
status_label = tk.Label(window, text="", font=("Arial", 30))  # 空文本，点击开始后变成红点
status_label.pack(pady=10)

# 绑定 Enter 键的全局监控
keyboard.on_press_key("enter", lambda _: record_marker())

# 捕获窗口关闭事件，输出文件路径
window.protocol("WM_DELETE_WINDOW", on_closing)

# 运行 GUI 窗口
window.mainloop()