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
        self.screenshotserver_window.grid_forget()
        images_fullpath = self.getallimages(self.images_folder_path)
        self.curr_image = MyImage(filepath=images_fullpath[0])
        self.menu_window = Menu(self, image_list=images_fullpath, change_image_func = self.change_image)
        self.image_canvas = ImageCanvas(self, load_image_func=self.load_image)
    
    def change_image(self, button):
        image_name = button.cget("text")
        fullpath = self.images_folder_path + "/" + image_name
        print(fullpath)
        self.image_canvas.delete(self.image_canvas_tagname)
        self.curr_image = MyImage(filepath=fullpath)
        self.image_canvas.create_image(0,0,image = self.curr_image.image_tk, tags = self.image_canvas_tagname)

        

    def load_image(self, event):
        self.image_canvas.delete(self.image_canvas_tagname)
        self.image_canvas.create_image(0,0,image = self.curr_image.image_tk, tags = self.image_canvas_tagname)

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
