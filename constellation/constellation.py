import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter.colorchooser import askcolor
import pypinyin
import requests
import json

def get_constellation_fortune(constellation):
    api_key = "f268f63358ec26a9593b73d5c132d4"
    url = f"http://web.juhe.cn:8080/constellation/qetAll?consName={constellation}&type=today&key={api_key}"
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
            messagebox.showerror("错误", "查询星座运势失败，请稍后重试。")
        else:
            result_text = f"{result['name']}今日运势：\n\n综合指数：{result['all']}% \n健康指数：{result['health']} \n爱情指数：{result['love']} \n财运指数：{result['money']} \n工作指数：{result['work']} \n幸运颜色：{result['lucky color']}"
            result_label.configure(text=result_text)

def change_font_size():
    def apply_font_size():
        try:
            font_size = int(font_size_var.get())
            result_label.configure(font=("TkDefaultFont", font_size))
            font_size_window.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的字体大小。")

    font_size_window = Toplevel(root)
    font_size_window.title("更改字体大小")
    font_size_window.geometry("200x100")
    font_size_window.eval('tk::PlaceWindow . center')

    font_size_label = tk.label(font_size_window, text="请输入字体大小：")
    font_size_label.pack(pady=10)

    font_size_var = tk.StringVar()
    font_size_entry = tk.Entry(font_size_window, textvariable=font_size_var)
    font_size_entry.pack()

    apply_button = tk.Button(font_size_window, text="应用", command=apply_font_size)
    apply_button.pack(pady=10)

def change_font_color():
    color = askcolor()[1]
    if color:
        result_label.configure(fg=color)


def change_bg_color():
    color = askcolor()[1]
    if color:
        root.configure(bg=color)
        label.configure(bg=color)
        result_label.configure(bg=color)






def fuzzy_search(input_str):
    constellation = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    if input_str in constellation:
        return input_str
    for c in constellation:
        if input_str in c or input_str in pypinyin.slug(c, style=pypinyin.Style.FIRST_LETTER, separator=""):
            return c
    return None



root = tk.Tk()
root.title("星座运势查询")

root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

menu = tk.Menu(root)
root.config(menu=menu)

settings_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="设置", menu=settings_menu)
settings_menu.add_command(label="更改字体大小", command=change_font_size)
settings_menu.add_command(label="更改字体颜色", command=change_font_color)
settings_menu.add_command(label="更改背景颜色", command=change_bg_color)

label = tk.Label(root, text="请输入星座名称")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack()
entry.bind('<Return>', show_fortune)

search_button = tk.Button(root, text="查询", command=show_fortune)
search_button.pack(pady=10)

result_label = tk.Label(root, wraplength=550, justify=tk.LEFT)
result_label.pack(pady=10)

root.mainloop()