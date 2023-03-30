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
    