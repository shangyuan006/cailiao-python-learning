import tkinter as tk
from tkinter import filedialog
import serial

class PacketLossTool:
    def __init__(self, master):
        self.master = master
        master.title("Packet Loss Tool")  # 设置窗口标题

        self.label = tk.Label(master, text="Enter the serial port:")  # 创建标签
        self.label.pack()  # 将标签添加到窗口中

        self.entry = tk.Entry(master)  # 创建文本框
        self.entry.pack()  # 将文本框添加到窗口中

        self.baudrate_label = tk.Label(master, text="Enter the baudrate:")
        self.baudrate_label.pack()

        self.baudrate_entry = tk.Entry(master)
        self.baudrate_entry.pack()

        self.button = tk.Button(master, text="Connect", command=self.connect)  # 创建按钮
        self.button.pack()  # 将按钮添加到窗口中

        self.text = tk.Text(master)  # 创建文本框
        self.text.pack()  # 将文本框添加到窗口中

    def connect(self):
        port = self.entry.get()  # 获取用户输入的串口号
        baudrate = int(self.baudrate_entry.get())  # 获取用户输入的波特率
        try:
            ser = serial.Serial(port, 9600, timeout=1)  # 连接到串口
            self.text.insert(tk.END, "Connected to " + port + " at " + str(baudrate) + " baud\n")  # 在文本框中显示连接成功的消息
            self.save_file_dialog(ser)  # 打开文件对话框，让用户选择保存数据的位置和文件名
            self.read_data(ser)  # 读取串口数据
        except serial.SerialException:
            self.text.insert(tk.END, "Could not connect to " + port + "\n")  # 在文本框中显示连接失败的消息

    def save_file_dialog(self, ser):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")  # 打开文件对话框，让用户选择保存数据的位置和文件名
        if file_path:
            with open(file_path, "w") as f:
                f.write("Serial port: " + self.entry.get() + "\n")  # 在文件中写入一些元数据
                self.text.insert(tk.END, "Data will be saved to " + file_path + "\n")

    def read_data(self, ser):
        total_packets = 0
        lost_packets = 0
        prev_data = None
        while True:
            data = ser.readline().decode().strip()
            if data:
                total_packets += 1
                self.text.insert(tk.END, data + "\n")
                # Add your packet loss calculation code here
                if prev_data is not None:
                    prev_seq_num, prev_data_len = prev_data.split()
                    curr_seq_num, curr_data_len = data.split()
                    if int(curr_seq_num) != int(prev_seq_num) + 1 or int(curr_data_len) != int(prev_data_len):
                        lost_packets += int(curr_seq_num) - int(prev_seq_num) - 1
                prev_data = data
                packet_loss_rate = lost_packets / total_packets * 100
                self.text.insert(tk.END, "Packet loss rate: {:.2f}%\n".format(packet_loss_rate))



root = tk.Tk()
app = PacketLossTool(root)
root.mainloop()







