import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter.colorchooser import askcolor
import pypinyin
import requests
import json

def get_constellation_fortune(constellation):
    api_key = ""
    url = f""
    response = requests.get(url)
    return json.loads(response.text) if response.status_code == 200 else None

def show_fortune(event=None):
    constellation = entry.get()
    constellation = fuzzy_search(constellation)
    if constellation is None:
        messagebox.showerror("错误", "无法找到对应的星座，请重新输入。")
    else:
        result = get_constellation_fortune(constellation)
        if result is None:
            messagebox.showerror("错误". "查询星座运势失败，请稍后重试。")
        else:
            result_text = f"{result['name']}今日运势：\n\n综合指数：{result['all']}% \n健康指数：{resulet['health']} \n爱情指数：{result['love']} \n财运指数：{result['money']} \n工作指数：{result['work']} \n幸运颜色：{result['lucky color']}"
            result_label.configure(text=result_text)

def change_font_size():
    def apply_font_size():
        try:
            font_size = int(font_size_var.get())
            result_label.configure(font=("TkDefaultFont", font_size))
            