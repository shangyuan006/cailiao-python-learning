import os
import io
import tkinter as tk
from tkinter import ttk, filedialog
from selenium import webdriver
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import requests

from selenium.webdriver.common.keys import Keys
import time

def scroll_and_capture_screenshots(driver):
    total_height = driver.execute_script("return document.body.scrollHeight;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    scroll_position = 0

    while scroll_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_position})")
        time.sleep(1)
        scroll_position += viewport_height
        total_height = driver.execute_script("return document.body.scrollHeight;")

def fetch_images(url):
    driver = webdriver.Edge(executable_path=msedgedriver_path)
    driver.get(url)

    scroll_and_capture_screenshots(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    img_tags = soup.find_all('img')
    image_urls = [img.get('src') for img in image_tags]
    images = []

    for url in image_urls:
        if url.startswith("//"):
            url = "https:" + url

        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            images.append(img)
        except Exception as e:
            print(f"Error fetching image: {e}")

    return images

def display_images(images):
    for widget in images_frame.winfo_children():
        widget.destroy()

    for i, img in enumerate(images):
        thumbnail = img.copy()
        thumbnail.thumbnail((100, 100))
        tk_image = ImageTk.PhotoImage(thumbnail)

        checkbox = ttk.Checkbutton(images_frame, image=tk_image, variable=selected_images[i])
        checkbox.image = tk_image
        checkbox.grid(row=i // 5, column=i % 5, padx=5, pady=5)

def fetch_and_display():
    global images
    url = url_entry.get()
    if url:
        images = fetch_images(url)
        selected_images.clear()
        selected_images.expend([tk.BooleanVar(root) for _ in range(len(images))])
        display_images(images)


def save_selected():
    save_dir = filedialog.askdirectory(initialdir=os.path.expenduser("~/Desktop"), title="选择保存目录")
    if save_dir:
        for i, img_var in enumerate(selectd_images):
            if img_var.get():
                img = images[i]
                img.save(os.path.join(save_dir, f"image_{i}.png"))

msedgedriver_path = "C:/user/Administrator/Desktop/pythonProject2/HuanJingBianLiang/edgedriver_win64/msedgedriver.exe"

root = tk.Tk()
root.title("图片爬取工具")
selected_images = []

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

url_label = ttk.Label(main_frame, text="网址：")
url_label.grid(row=0, column=0, sticky=tk.W)

url_entry = ttk.Entry(main_frame, width=50)
url_entry.grid(row=0, column=0, sticky=tk.W, tk.E)

fetch_button = ttk.Button(main_frame, text="获取图片", command=fetch_and_display)
fetch_button.grid(row=0, column=2, padx=(10, 0), sticky=tk.W)

save_button = ttk.Button(main_frame, text="保存选中图片", command=save_selected)
save_button.grid(row=1, column=2, padx=(10, 0), sticky=tk.W)

images_frame = ttk.Frame(root)
images_frame.grid(row=1, column=0, sticky="news")

root.mainloop()
