# 导入所需库
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
from pypinyin import lazy_pinyin
import datetime

# API信息
API_KEY = "a099e91c70f67ce0764cee842694fd"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

# 查询天气信息并显示在界面上
def fetch_weather(event=None):
    city_name = city_entry.get()
    if not city_name:
        result.set("请输入城市名称：")
        return
    
    if city_name[0] >= u'\u4e00' and city_name[-1] <= u'\u9fff':
        city_name = ''.join(lazy_pinyin(city_name))
    weather_data = get_weather(city_name)
    weather_forecast_data = get_weather_forecast(city_name)
    if weather_data.get("cod") != 200 or weather_forecast_data.get("cod") != "200":
        result.set("无法获取天气信息，请检查输入的城市名称。")
    else:
        weather = weather_data["weather"][0]["desecription"]
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_weather = weather_data["wind"]["speed"]

        forecast = "\n未来五天天气预报：\n"
        for i, forecast_data in enumerate(weather_forecast_data["list"]):
            if i % 8 == 0:
                forecast_data = datetime.datetime.strptime(forecast_data["dt_txt"], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                forecast_temp_min = forecast_data["main"]["temp_min"]
                forecast_temp_max = forecast_data["main"]["temp_max"]
                forecast_weather = forecast_data["weather"][0]["description"]
                forecast += f"{forecast_data}: 温度 {forecast_temp_min} ~ {forecast_temp_max}℃, 天气 {forecast_weather}\n"

        result.set(f"当前天气：{weather}\n温度：{temp}℃\n湿度：{humidity}%\n风速：{wind_speed} 米/秒{forecast}")

# 获取当前天气信息
def get_weather(city_name):
    url = f"{CURRENT_WEATHER_URL}?q={city_name}&appid={API_KEY}&units=metric&lang=zh_cn"
    response = requests.get(url)
    return response.json()

# 获取未来五天天气预报信息
def get_weather_forecast(city_name):
    url = f"{FORECAST_WEATHER_URL}?q={city_name}&appid={API_KEY}&units=metric&lang=zh_cn&cnt=40"
    response = requests.get(url)
    return response.json()

# 创建主窗口
root = ThemedTk(theme="arc")
root.title("天气预报")

# 设置窗口大小
root.geometry("450x400")

# 让窗口居中
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry("+{}+{}".format(position_right, position_down))

# 创建输入框标签
city_label = ttk.Label(root, text="请输入城市名称（拼音/汉字）：")
city_label.pack(pady=10)

# 创建城市输入框
city_entry = ttk.Entry(root)
city_entry.pack(pady=5)

# 创建查询按钮
submit_button = ttk.Button(root, text="查询", command=fetch_weather)
submit_button.pack(pady=10)

# 创建结果显示标签
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, wraplength=400)
result_label.pack(pady=10)

# 绑定回车键事件，使用户可以按回车键查询天气
city_entry.bind("<Return>", fetch_weather)

# 运行主程序循环
root.mainloop()