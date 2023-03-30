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
    