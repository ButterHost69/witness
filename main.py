import customtkinter as ctk
from image_widgets import *
import keyboard
from PIL import ImageGrab, Image, ImageTk
import os
from os.path import isfile

class MyImage():
    def __init__(self, filepath:str):
        self.filepath = filepath
        self.image = Image.open(self.filepath)
        self.image_tk = ImageTk.PhotoImage(image=self.image)
        self.image_width = self.image.size[0]
        self.image_height = self.image.size[1]
        self.image_ratio = self.image_width / self.image_height

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('800x500')
        self.minsize(800,500)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=2, uniform='a')
        self.columnconfigure(index=1, weight=6, uniform='a')

        self.image_canvas_tagname = "imagecanvas#1"
        self.cropbox_tagname = "cropbox#1"
        self.x1 = None
        self.y1 = None
        self.apply_to_all_checkbox = False

        self.select_folder_widget = SelectFolderWindow(parent = self, start_ss_server_func= self.start_ss_server)
        self.bind('<Escape>', lambda _ : self.quit())
        self.attributes('-alpha', 0.8)
        self.mainloop()

    def start_ss_server(self, path:str):
        self.images_folder_path = path
        self.select_folder_widget.grid_forget()
        self.screenshotserver_window = ScreenshotServerWindow(parent=self, record_keys_func= self.record_keys, stop_record_keys_func=self.stop_record_keys)
    
    def record_keys(self):
        global fileno
        fileno = 0
        keyboard.add_hotkey('ctrl+windows+alt+space', self.take_screenshot)
    
    def take_screenshot(self):
        global fileno
        filepath = f"{self.images_folder_path}/{fileno}.png"
        image_grab_instance = ImageGrab.grab()
        image_grab_instance.save(filepath)
        image_grab_instance.close()
        fileno += 1
    
    def getallimages(self, path:str) -> list[str]:
        image_list = []
        for file in os.listdir(path + "/"):
            fullpath = path + "/" + file 
            if isfile(fullpath):
                if file.split(".")[-1] == "png":
                    image_list.append(fullpath)
        return image_list

    def stop_record_keys(self):
        keyboard.remove_all_hotkeys()
        self.attributes("-alpha", 0.9)
        self.screenshotserver_window.grid_forget()
        self.all_images_fullpath = self.getallimages(self.images_folder_path)
        self.curr_image = MyImage(filepath=self.all_images_fullpath[0])
        self.menu_window = Menu(self, image_list=self.all_images_fullpath, change_image_func = self.change_image, confirm_image_size_func = self.confirm_image_size, apply_crop_to_all_func=self.apply_to_all)
        self.image_canvas = ImageCanvas(self, load_image_func=self.load_image, draw_cropbox_func= self.draw_cropbox, reset_draw_cropbox_func= self.reset_draw_cropbox)
    
    def change_image(self, button):
        image_name = button.cget("text")
        fullpath = self.images_folder_path + "/" + image_name
        self.image_canvas.delete(self.image_canvas_tagname)
        self.curr_image = MyImage(filepath=fullpath)
        self.image_canvas = ImageCanvas(self, load_image_func=self.load_image, draw_cropbox_func= self.draw_cropbox, reset_draw_cropbox_func= self.reset_draw_cropbox)        

    def load_image(self, event):
        self.canvas_ratio = event.width / event.height
        # Check if Image Height of Width is Larger
        if self.canvas_ratio > self.curr_image.image_ratio: # Canvas is wider
            image_height = event.height
            image_width = image_height * self.curr_image.image_ratio
        else: # Canvas is Taller
            image_width = event.width
            image_height = image_width/self.curr_image.image_ratio

        self.image_canvas.delete(self.image_canvas_tagname)
        resized_image = self.curr_image.image.resize((int(image_width), int(image_height)))
        self.curr_image.image_tk = ImageTk.PhotoImage(image = resized_image)
        self.image_canvas.create_image(event.width/2, event.height/2, image = self.curr_image.image_tk)

    def draw_cropbox(self, event):
        if self.x1 is None and self.y1 is None:
            self.x1, self.y1 = event.x, event.y
        else:
            self.image_canvas.delete(self.cropbox_tagname)
        self.old_box = self.image_canvas.create_rectangle(self.x1, self.y1, event.x, event.y, tags=self.cropbox_tagname, )

    def reset_draw_cropbox(self, event):
        # self.x1 = None
        # self.y1 = None
        self.x2 = event.x
        self.y2 = event.y   

    def confirm_image_size(self):
        # Resized Image Coordinates -> to -> Image Cordinates
        resized__image_x, resized__image_y = self.curr_image.image_tk.width(), self.curr_image.image_tk.height()
        real_image_x, real_image_y = self.curr_image.image_width, self.curr_image.image_height
        rate_change_x = real_image_x/resized__image_x
        rate_change_y = real_image_y/resized__image_y
        changed_x1, changed_x2 = self.x1 * rate_change_x, self.x2 * rate_change_x
        changed_y1, changed_y2 = self.y1 * rate_change_y - 130, self.y2 * rate_change_y - 130 # There is some offset in 'Y' I dont know Why ??
        
        if self.apply_to_all:
            for img_path in self.all_images_fullpath:
                image = MyImage(img_path)
                crop_image = image.image.crop([changed_x1, changed_y1, changed_x2, changed_y2])
                crop_image.save(img_path)

        else:
            crop_image = self.curr_image.image.crop([changed_x1, changed_y1, changed_x2, changed_y2])
            crop_image.save(self.curr_image.filepath)
        
        self.image_canvas.delete('all')
        self.curr_image = MyImage(self.curr_image.filepath)
        self.image_canvas = ImageCanvas(self, load_image_func=self.load_image, draw_cropbox_func= self.draw_cropbox, reset_draw_cropbox_func= self.reset_draw_cropbox)        
        self.x1 = None
        self.y1 = None
    
    def apply_to_all(self):
        self.apply_to_all_checkbox =  not self.apply_to_all_checkbox
    



App()



# # import tkinter as tk
# import ttkbootstrap as tk
# from ttkbootstrap import ttk
# from tkinter import filedialog
# import keyboard
# from PIL import ImageGrab

# # Start Window Configurations
# window = tk.Window(themename= 'darkly')
# window.geometry("500x300")

# # Global Screenshot Counter
# global ss_count


# # Screenshot Server Window
# def screenshot_server_window(ss_filepath:str):
#     # New Window Configuration
#     window = tk.Window(themename = 'darkly')
#     window.geometry("500x300")

#     # New Window Widgets
#     label_info = ttk.Label(master = window, text = "Press the Button To Start the Screen Shot Server ... ")
#     label_info.pack()
    

#     # Button Functions
#     def take_screenshots():
#         global ss_count
#         ss = ImageGrab.grab()
#         file_path = ss_filepath + "/" + str(ss_count) + ".png" 
#         ss.save(fp=file_path)
#         ss.close()
#         print(f"SS Taken at {file_path}")
#         ss_count += 1

#     def start_server():
#         global ss_count
#         if button_start_server["text"] == "Start":
#             ss_count = 0
#             keyboard.add_hotkey("ctrl+windows+alt+space", lambda: take_screenshots())
#             button_start_server["text"] = "Stop"
        
#         elif button_start_server["text"] == "Stop":
#             keyboard.remove_hotkey('ctrl+windows+alt+space')
#             button_start_server["text"] = "Start"

#     button_start_server = ttk.Button(master = window, text = "Start", command = start_server)
#     button_start_server.pack()

#     # New Window Run Loop
#     window.mainloop()


# # Button Functions
# def on_btn_start_screenshot_server():
#     file_path = filedialog.askdirectory(initialdir="/", title= "Select Folder to Store Your Screenshots")
#     print(file_path)
#     window.destroy()
#     screenshot_server_window(file_path)

# # Start Window Widgets
# label_select_file_path = ttk.Label(master = window, text = "Select File Path To Store Your ScreenShots")
# label_select_file_path.pack()

# buttton_start_screenshot_server = ttk.Button(master = window, text = "Select Folder", command=on_btn_start_screenshot_server)
# buttton_start_screenshot_server.pack()


# # Start Window KeyBinds
# window.bind('<Escape>', lambda _ : window.quit())

# # Run Loop
# window.mainloop()
