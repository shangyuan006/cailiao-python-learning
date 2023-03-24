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
    