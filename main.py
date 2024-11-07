from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageDraw, ImageFilter
import random
import os

root = Tk()
root.title("Photoshoppe")
root.geometry("1000x420")
root.minsize(1000, 420)
root.maxsize(1000, 420)
root.config(bg="teal")

''' MODEL - Functions and Data'''
def load_image():
    global loaded_image
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Image files", "*.png *.jpg")])
    file_path_tk.set(file_path)
    try:
        img = Image.open(file_path)
        width, height = img.size
        if width > height:
            loaded_image = img.resize((600, 400), Image.LANCZOS)
        else: 
            multiplier = 400 / height
            loaded_image = img.resize((int(width * multiplier), 400), Image.LANCZOS)
        display_image(loaded_image)
    except FileNotFoundError:
        messagebox.showerror("Error", "Invalid image!")

def display_image(image):
    global loaded_image
    loaded_image = image
    root.photo_image = ImageTk.PhotoImage(loaded_image)
    canvas.create_image(300, 200, image=root.photo_image)

def apply_black_and_white():
    if loaded_image:
        pixels = loaded_image.load()
        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r,g,b = pixels[x,y]
                avg = int((r+g+b)/3)
                pixels[x,y]=(avg,avg,avg)
        display_image(loaded_image)

# Save the modified image
def save_image():
    if loaded_image:
        loaded_image.save(filedialog.asksaveasfilename(title="Choose a save location", initialfile=f"image.png", filetypes=[("Image files", "*.png *.jpg")]))

''' CONTROLLERS - Widgets That Users Interact With'''
load_image_button = Button(text="Open Image", command = load_image)
load_image_button.place(x=300, y=50, width=80, height=25)


''' VIEW - Widgets That Display Visuals'''
title_label = Label(text="Photoshoppe", font=("Arial", 24))
title_label.place(x=10, y=10, width=370, height=30)

file_path_tk = StringVar()
path_display = Entry(textvariable=file_path_tk, state="readonly")
path_display.place(x=10, y=50, width=280, height=25)

canvas = Canvas(root)
canvas.place(x=390, y=10, width=600, height=400)

root.mainloop()