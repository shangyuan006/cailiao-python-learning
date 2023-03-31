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
        