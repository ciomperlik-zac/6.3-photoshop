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
filter_frame.place(x=10, y=45, width=370, height=210)

tool_frame = ttk.LabelFrame(root, text="Tools")
tool_frame.place(x=10, y=260, width=370, height=150)

loaded_image = None

mode = "Default"

rect = None
start_x, start_y = 0, 0
end_x, end_y = 0, 0
x_offset, y_offset = 0, 0

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
        messagebox.showerror("Error", "File not found!")

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

def on_click(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_drag(event):
    global start_x, start_y, end_x, end_y, x_offset, y_offset, rect
    end_x, end_y = event.x, event.y

    try:
        x_offset = round((600-loaded_image.width)/2)
    except:
        x_offset = 0
    try:
        y_offset = round((400-loaded_image.height)/2)
    except:
        y_offset = 0

    canvas.delete(rect)
    rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline = "white", dash = (5,5))

def toggle_crop():
    global mode
    if loaded_image:
        if mode == "Default":
            mode = "Crop"
            crop_button.config(text="Crop - Active")
            canvas.bind("<Button-1>", on_click)
            canvas.bind("<B1-Motion>", on_drag)
        elif mode == "Blur":
            mode = "Crop"
            crop_button.config(text="Crop - Active")
            blur_button.config(text="Blur")
        else:
            mode = "Default"
            crop_button.config(text="Crop")
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")

        canvas.delete(rect)

def toggle_blur():
    global mode
    if loaded_image:
        if mode == "Default":
            mode = "Blur"
            blur_button.config(text="Blur - Active")
            canvas.bind("<Button-1>", on_click)
            canvas.bind("<B1-Motion>", on_drag)
        elif mode == "Crop":
            mode = "Blur"
            blur_button.config(text="Blur - Active")
            crop_button.config(text="Crop")
        else:
            mode = "Default"
            blur_button.config(text="Blur")
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")

        canvas.delete(rect)

def apply_tool():
    global start_x, start_y, end_x, end_y, mode, loaded_image
    if mode != "Default":
        if start_x < x_offset:
            start_x = 0
        elif start_x > loaded_image.width+x_offset:
            start_x = loaded_image.width
        else:
            start_x = start_x-x_offset
        
        if end_x < x_offset:
            end_x = 0
        elif end_x > loaded_image.width+x_offset:
            end_x = loaded_image.width
        else:
            end_x = end_x-x_offset

        if start_y < y_offset:
            start_y = 0
        elif start_y > loaded_image.height+y_offset:
            start_y = loaded_image.height
        else:
            start_y = start_y-y_offset

        if end_y < y_offset:
            end_y = 0
        elif end_y > loaded_image.height+y_offset:
            end_y = loaded_image.height
        else:
            end_y = end_y-y_offset

        if start_x > end_x:
            temp = start_x
            start_x = end_x
            end_x = temp
        if start_y > end_y:
            temp = start_y
            start_y = end_y
            end_y = temp

        crop_button.config(text="Crop")
        blur_button.config(text="Blur")
        canvas.unbind("<Button-1>")
        canvas.unbind("<B1-Motion>")

        if mode == "Crop":
            loaded_image = loaded_image.crop([start_x, start_y, end_x, end_y])
        elif mode == "Blur":
            pixels = loaded_image.load()

            for y in range(start_y, end_y, 10):
                for x in range(start_x, end_x, 10):
                    r, g, b = pixels[x, y]

                    for yy in range(y, y + min(loaded_image.height-y, 10)):
                        for xx in range(x, x + min(loaded_image.width-x, 10)):
                            pixels[xx, yy] = (r, g, b)

        display_image(loaded_image)
        mode = "Default"
    


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

# Tools
crop_button = Button(tool_frame, text="Crop", command=toggle_crop)
crop_button.place(x=10, y=10, width=255, height=50)

blur_button = Button(tool_frame, text="Blur", command=toggle_blur)
blur_button.place(x=10, y=70, width=255, height=50)

apply_tool_button = Button(tool_frame, text="Apply", command=apply_tool)
apply_tool_button.place(x=275, y=10, width=80, height=110)



''' VIEW - Widgets That Display Visuals'''
title_label = Label(text="Photoshoppe", font=("Arial", 24))
title_label.place(x=10, y=10, width=180, height=30)

canvas = Canvas(root, bg="white")
canvas.place(x=390, y=10, width=600, height=400)

root.mainloop()