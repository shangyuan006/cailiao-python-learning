import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from PIL import Image
import io
import time
from PIL import ImageOps
from aip import AipOcr

APP_ID = ""
API_KEY = ""
SECRET_KEY = ""

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def preprocess_image(image):
    gray_image = image.convert()
    binary_image = ImageOps.autocontrast(gray_image)
    return binary_image

def baidu_ocr(image):
    image_data = io.BytesIO()
    image.save(image_data, format="PNG")
    response = client.basicGeneral(image_data.getvalue())
    text = ""
    if "words_result" in response:
        for item in response["words_result"]:
            text += item["words"] + "\n"
    return text


def scroll_and_capture_screenshots(driver):
    total_height = driver.execute_script("return document.body.scrollHeight;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    scroll_position = 0
    screenshots = []

    while scroll_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))
        scroll_position += viewport_height
        if scroll_position > total_height:
            # Crop overlapping part
            overlapping_height = scroll_position - total_height
            screenshot = screenshots[-1].crop((0, overlapping_height, screenshots[-1].width, screenshots[-1].height))
            screenshots[-1] = screenshot

        # Update total_height, in case of dynamic loading of content
        total_height = driver.execute_script("return document.body.scrollHeight;")

    return screenshots


def stitch_screenshots(screenshots):
    stitched_image = Image.new("RGB", (screenshots[0].width, sum([s.height for s in screenshots])))
    y_offset = 0

    for screenshot in screenshots:
        stitched_image.paste(screenshot, (0, y_offset))
        y_offset += screenshot.height

    return stitched_image

def get_text_from_screenshot(url):
    driver = webdriver.Edge(executable_path=msedgedriver_path)
    driver.get(url)
    screenshots = scroll_and_capture_screenshots(driver)
    stitched_image = stitch_screenshots(screenshots)
    preprocessed_image =preprocess_image(stitched_image)
    text = baidu_ocr(preprocessed_image)
    driver.quit()
    return text

def fetch_text():
    url = url_entry.get()
    if url:
        result_text.delete(1.0, tk.END)
        text = get_text_from_screenshot(url)
        result_text.insert(tk.END, text)
#这里用的是别人的路径，记得修改成自己的路径
msedgedriver_path = "C:/user/Administrator/Desktop/pythonProject2/HuanJingBianLiang/edgedriver_win64/msedgedriver.exe"

root = tk.Tk()
root.title("网站爬取升级版")
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry("+{}+{}".format(position_right, position_down))

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

url_label = ttk.Label(main_frame, text="网址：")
url_label.grid(row=0, column=0, sticky=tk.W)

url_entry = ttk.Entry(main_frame, width=50)
url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

fetch_button = tk.Button(main_frame, text="获取文本", command=fetch_text)
fetch_button.grid(row=0, column=2, padx=(10, 0), sticky=tk.W)

result_label = ttk.Label(main_frame, text="提取的文本：")
result_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
result_text = tk.Text(main_frame, wrap=tk.WORD, width=80, height=20)
result_scrollbar = ttk.ScrollBar(main_frame, orient="vertical", command=result_text.yview)
result_configure(yscrollcommand=result_scrollbar.set)
result_text.grid(row=2, column=0, columnspan=2, pady=(5, 0), sticky=(tk.W, tk.E))
result_scrollbar.grid(row=2, column=2, pady=(5, 0), sticky=(tk.N, tk.S))


root.mainloop()
