import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, font

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
        soup = BeautifulSoup(response.text, 'html.parser')
        extracted_data = {
            'titles': [],
            'paragraphs':[],
            'list_items':[],
        }

        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            elements = soup.find_all(tag)
            extract_data['title'].extend([element.text.strip() for element in elements])

        p_elements = soup.find_all('p')
        extract_data['paragraphs'].extend([p.text.strip() for p in p_elements])

        li_elements = soup.find_all('li')
        extract_data['list_items'].extend([li.text.strip() for li in li_elements])

        display_data(extract_data)
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
        for idx, item in enumerate(items):
            result_text.insert(tk.END, f"{idx + 1}. {item}\n")
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

