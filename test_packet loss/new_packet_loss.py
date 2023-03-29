from tkinter import *
import serial.tools.list_ports
import threading
import time

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.port_label = Label(self, text="Port:")
        self.port_label.grid(row=0, column=0)
        self.port_var = StringVar()
        self.port_menu = OptionMenu(self, self.port_var, "")
        self.port_menu.grid(row=0, column=1)

        self.baudrate_label = Label(self, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0)
        self.baudrate_var = StringVar()
        self.baudrate_entry = Entry(self, textvariable=self.baudrate_var)
        self.baudrate_entry.grid(row=1, column=1)

        self.start_button = Button(self, text="Start", command=self.start_test)
        self.start_button.grid(row=2, column=0)

        self.stop_button = Button(self, text="Stop", command=self.stop_test, state=DISABLED)
        self.stop_button.grid(row=2, column=1)

        self.result_label = Label(self, text="Result:")
        self.result_label.grid(row=3, column=0)
        self.result_var = StringVar()
        self.result_entry = Entry(self, textvariable=self.result_var, state=DISABLED)
        self.result_entry.grid(row=3, column=1)

    def start_test(self):
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.result_var.set("")
        self.thread = threading.Thread(target=self.test_thread)
        self.thread.start()

    def stop_test(self):
        self.stop_button.config(state=DISABLED)

    def test_thread(self):
        port = self.port_var.get()
        baudrate = int(self.baudrate_var.get())
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.flushInput()
        ser.flushOutput()
        total_count = 0
        error_count = 0
        while self.stop_button["state"] == NORMAL:
            data = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a" * 10
            ser.write(data)
            recv_data = ser.read(len(data))
            if recv_data != data:
                error_count += 1
            total_count += 1
            self.result_var.set(f"Total: {total_count}, Error: {error_count}")

            time.sleep(0.1)
        

