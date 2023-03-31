import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, font
import chardet


def center_window(window, width=None, height=None):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    if width is None:
        width = window.winfo_screenwidth()
    if height is None:
        height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def change_font(font_family):
    result_text.config(font=(font_family, 10))


def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # 使用 chardet 检测编码
        encoding = chardet.detect(response.content)['encoding']

        # 使用检测到的编码解码网页内容
        content = response.content.detect(encoding)
        soup = BeautifulSoup(content, 'html.parser')
        extracted_data = {
            'text':[]
        }

        # 查找所有的文本元素并提取其中的文本
        text_elements = soup.find_all(text=True)
        extracted_data['text'].extend([text.strip() for text in text_elements])

        display_data(extracted_data)
    else:
        print(f"请求失败，状态码：{response.status_code}")


def display_data(data):
    result_window = tk.Toplevel(root)
    result_window.title("爬取结果")
    center_window(result_window, 800, 600)

    global result_text
    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=30, font=("微软雅黑", 10))
    result_text.pack(expand=True, fill='both')

    for category, items in data.items():
        result_text.insert(tk.END, category.capitalize() + ":\n")
        for item in items:
            result_text.insert(tk.END, f"{item}\n")
        result_text.insert(tk.END, "\n")



    result_text.config(status='disabled')

def start_scraping(event=None):
    url = url_entry.get()
    extract_data(url)

root = tk.Tk()
root.title("网页爬取工具")
root.geometry("600x200")
center_window(root)

url_label = ttk.Label(root, text="请输入网址", font=("微软雅黑", 12))
url_label.pack()

url_entry = ttk.Entry(root, width=50, font=("微软雅黑", 12))
url_entry.pack()
url_entry.bind('<Return>', start_scraping)

start_button = ttk.Button(root, text="开始爬取", command=start_scraping)
start_button.pack(pady=5)

font_label = ttk.Label(root, text="选择字体", font=("微软雅黑", 12))
font_label.pack()

font_var = tk.StringVar()
font_var.set("微软雅黑")
font_optionmenu = ttk.OptionMenu(root, font_var, "微软雅黑", "宋体", "黑体", "楷体", "仿宋", command=change_font)
font_optionmenu.pack()

root.mainloop()

