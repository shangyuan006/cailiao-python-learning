import tkinter as tk
from tkinter import filedialog
import serial
import wmi
import threading

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

        self.usb_device_connected = False

    def connect(self):
        port = self.entry.get()
        baudrate = int(self.baudrate_entry.get())
        ser = serial.Serial(port, baudrate, timeout=1)
        self.text.insert(tk.END, "Connected to " + port + " at " + str(baudrate) + " baud\n")
        self.save_file_dialog(ser)
        packets_received = 0
        while True:
            data = ser.readline().decode('utf-8').strip()
            if data:
                packets_received += 1


    def save_file_dialog(self, ser):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")  # 打开文件对话框，让用户选择保存数据的位置和文件名
        if file_path:  # 如果用户选择了文件
            with open(file_path, 'w') as f:  # 打开文件
                f.write("Packet Loss Tool\n\n")
                f.write("Serial Port: " + self.entry.get() + "\n")
                f.write("Baudrate: " + self.baudrate_entry.get() + "\n\n")
                f.write("Packet Loss Rate\n")
                f.write("-----------------\n")
                packets_received = 0
                packets_lost = 0
                while True:
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        packets_received += 1
                        packets_lost = packets_received - int(data)
                        packet_loss_rate = packets_lost / packets_received * 100
                        f.write(str(packets_received) + "\t" + str(packet_loss_rate) + "%\n")
                        self.text.insert(tk.END, str(packets_received) + "\t" + str(packet_loss_rate) + "%\n")  # 在文本框中显示数据
        else:
            self.text.insert(tk.END, "File not saved\n")  # 在文本框中显示文件未保存的消息


    def read_data(self, ser, file_path):
        with open(file_path, "w") as f:
            packets_received = 0
            packets_lost = 0
            while True:
                data = ser.readline().decode("utf-8")  # 读取串口数据
                if data:
                    f.write(data)  # 将数据写入文件
                    self.text.insert(tk.END, data)  # 在文本框中显示数据
                    packets_received += 1
                else:
                    break
            packets_lost = packets_received - len(data.split())  # 计算丢失的数据包数量
            packet_loss_rate = packets_lost / packets_received  # 计算丢包率
            self.text.insert(tk.END, "Data collection complete\n")  # 在文本框中显示数据采集完成的消息
            self.text.insert(tk.END, "Packet loss rate: {:.2f}%\n".format(packet_loss_rate * 100))  # 在文本框中显示丢包率

    c = wmi.WMI()
    watcher = c.watch_for(notification_type="Creation", wmi_class="Win32_USBControllerDevice")

    while True:
        usb_device = watcher()
        print("USB device connected:", usb_device.Dependent.Caption)
        # Add your code to connect to the USB device and read data here
        break

root = tk.Tk()
app = PacketLossTool(root)
root.mainloop()
