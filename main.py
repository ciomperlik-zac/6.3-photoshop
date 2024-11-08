from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageDraw, ImageFilter
import random
import os

root = Tk()
root.title("Photoshoppe")
root.geometry("1000x420")
root.minsize(1000, 420)
root.maxsize(1000, 420)

filter_frame = ttk.LabelFrame(root, text="Filters")
filter_frame.place(x=10, y=50, width=370, height=210)

tool_frame = ttk.LabelFrame(root, text="Tools")
tool_frame.place(x=10, y=265, width=370, height=145)

loaded_image = None

''' MODEL - Functions and Data'''
# Load the image
def load_image():
    global loaded_image

    try:
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Image files", "*.png *.jpg")])
        img = Image.open(file_path)

        width, height = img.size
        if width > height:
            loaded_image = img.resize((600, 400), Image.LANCZOS)
        else: 
            multiplier = 400 / height
            loaded_image = img.resize((int(width * multiplier), 400), Image.LANCZOS)
        display_image(loaded_image)
    except:
        pass

# Display the image
def display_image(image):
    global loaded_image
    loaded_image = image
    root.photo_image = ImageTk.PhotoImage(loaded_image)
    canvas.create_image(300, 200, image=root.photo_image)

# Save the modified image
def save_image():
    if loaded_image:
        try:
            loaded_image.save(filedialog.asksaveasfilename(title="Choose a save location", initialfile=f"image.png", filetypes=[("Image files", "*.png *.jpg")]))
        except:
            pass
# Filters
def apply_black_and_white():
    if loaded_image:
        pixels = loaded_image.load()
        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r,g,b = pixels[x,y]
                avg = int((r+g+b)/3)
                pixels[x,y]=(avg,avg,avg)
        display_image(loaded_image)

def apply_sepia():
    if loaded_image:
        pixels = loaded_image.load()
        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r, g, b = pixels[x, y]
                r_ = r * .393 + g * 0.769 + b * 0.189
                g_ = r * .349 + g * 0.686 + b * 0.168
                b_ = r * .272 + g * 0.534 + b * 0.131
                pixels[x, y] = (int(r_), int(g_), int(b_))
        display_image(loaded_image)

def apply_invert():
    if loaded_image:
        pixels = loaded_image.load()
        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r, g, b = pixels[x, y]
                pixels[x, y]=(255-r, 255-g, 255-b)
        display_image(loaded_image)

def apply_edge():
    global loaded_image
    if loaded_image:
        loaded_image = loaded_image.filter(ImageFilter.EDGE_ENHANCE)
        display_image(loaded_image)

def apply_contrast():
    if loaded_image:
        pixels = loaded_image.load()

        avg_brightness = 0
        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r, g, b = pixels[x, y]
                avg_brightness += r+b+g
        avg_brightness /= loaded_image.height * loaded_image.width

        for y in range(loaded_image.height):
            for x in range(loaded_image.width):
                r, g, b = pixels[x, y]
                if r + g + b > avg_brightness:
                    r += 20
                    g += 20
                    b += 20
                else:
                    r -= 20
                    g -= 20
                    b -= 20
                pixels[x, y] = (r, g, b)
        display_image(loaded_image)

def apply_point():
    global loaded_image
    if loaded_image:
        pixels = loaded_image.load()
        canvas = Image.new("RGB", (loaded_image.width, loaded_image.height+1), "white")
        for run in range(100000):
            x = random.randint(0, loaded_image.width-1)
            y = random.randint(0, loaded_image.height-1)

            size = random.randint(3, 5)
            ellipsebox=[(x, y),(x+size, y+size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox,fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw
        loaded_image = canvas
        display_image(loaded_image)



''' CONTROLLERS - Widgets That Users Interact With'''
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_dropdown = Menu(menu_bar, tearoff=0)
file_dropdown.add_command(label="Open image", command=load_image)
file_dropdown.add_separator()
file_dropdown.add_command(label="Save image", command=save_image)
menu_bar.add_cascade(label="File", menu=file_dropdown)

# Filters
bw_button = Button(filter_frame, text="Black & White", command=apply_black_and_white)
bw_button.place(x=10, y=10, width=167, height=50)

sepia_button = Button(filter_frame, text="Sepia", command=apply_sepia)
sepia_button.place(x=187, y=10, width=168, height=50)

invert_button = Button(filter_frame, text="Invert", command=apply_invert)
invert_button.place(x=10, y=70, width=167, height=50)

edge_button = Button(filter_frame, text="Highlight Edge", command=apply_edge)
edge_button.place(x=187, y=70, width=168, height=50)

contrast_button = Button(filter_frame, text="Increase Contrast", command=apply_contrast)
contrast_button.place(x=10, y=130, width=167, height=50)

point_button = Button(filter_frame, text="Pointillism", command=apply_point)
point_button.place(x=187, y=130, width=168, height=50)



''' VIEW - Widgets That Display Visuals'''
title_label = Label(text="Photoshoppe", font=("Arial", 24))
title_label.place(x=10, y=10, width=180, height=30)

canvas = Canvas(root)
canvas.place(x=390, y=10, width=600, height=400)

root.mainloop()