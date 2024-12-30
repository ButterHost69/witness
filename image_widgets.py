import random
import customtkinter as ctk
from tkinter import filedialog, ttk, Canvas
import tkinter as tk
import os
import shutil


class SelectFolderWindow(ctk.CTkFrame):
    def __init__(self, parent, start_ss_server_func, delete_ss_folder_later_func):
        super().__init__(master = parent, fg_color="#242424")
        self.start_ss_server_func = start_ss_server_func
        self.delete_ss_folder_later_func = delete_ss_folder_later_func
        # self.delete_ss_folder_later = delete_ss_folder_later
        self.grid(row = 0, columnspan=2,column = 0 , stick = 'nsew')
        
        expand_frame = ctk.CTkFrame(master = self, fg_color='#242424')
        label = ctk.CTkLabel(master = expand_frame, text = "Select Path to Store Screenshots")
        label.pack()
        select_folder_btn = ctk.CTkButton(master = expand_frame, text="Open Explorer", command=self.select_path)
        select_folder_btn.pack()

        continue_without_folder_btn = ctk.CTkButton(master = expand_frame, text="Continue Without Selecting Destination Folder", command=self.select_temp_path, )
        continue_without_folder_btn.configure(fg_color="transparent")
        continue_without_folder_btn.configure(border_width=2)
        continue_without_folder_btn.configure(border_color="#ADD8E6")
        continue_without_folder_btn.pack(pady=10)

        expand_frame.pack(expand = True)

    def select_temp_path(self):
        self.delete_ss_folder_later_func(True)
        # path = os.path.abspath(r"temp")
        path = "C:\\Users\\palas\\Documents\\witness_temp\\"
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        self.start_ss_server_func(path)

    def select_path(self):
        path = filedialog.askdirectory()
        self.start_ss_server_func(path)


class ScreenshotCounterWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color=self.generate_random_color())
        # super().__init__(fg_color="#242424")
        self.geometry("20x20+0+0")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.counter_int = tk.IntVar()
        self.counter_int.set(0)
        self.counter = ctk.CTkLabel(master = self, textvariable = self.counter_int)
        self.counter.pack()
    
    def generate_random_color(self):
        # Generate a random RGB color
        r = random.randint(0, 200)
        g = random.randint(0, 200)
        b = random.randint(0, 200)
        return f'#{r:02x}{g:02x}{b:02x}'

    def increament_counter(self):
        self.counter_int.set(self.counter_int.get() + 1)
        self.configure(fg_color = self.generate_random_color())

class ScreenshotServerWindow(ctk.CTkFrame):
    def __init__(self, parent, record_keys_func, stop_record_keys_func):
        super().__init__(master = parent, fg_color="#242424")
        self.record_keys_func = record_keys_func
        self.stop_record_keys_func = stop_record_keys_func

        self.grid(row = 0, columnspan = 2, column = 0, sticky = 'nsew')
        expand_frame = ctk.CTkFrame(master = self, fg_color="#242424")
        expand_frame.pack(expand = True)
        instruction_label = ctk.CTkLabel(master = expand_frame, text = "Press <Ctrl-WinL+Alt+Space> To Take Screenshot !!")
        instruction_label.pack()
        miniss_label = ctk.CTkLabel(master = expand_frame, text = "Press <Ctrl-WinL+Z> To Open Mini SS Edit Window !!")
        miniss_label.pack()

        self.button_state = tk.StringVar()
        self.button_state.set("Start...")
        self.record_button = ctk.CTkButton(master = expand_frame, textvariable=self.button_state, command=self.start_server)
        self.record_button.pack()

        self.image_taken_var = tk.StringVar()
        self.images_taken_label = ctk.CTkLabel(master = expand_frame, textvariable = self.image_taken_var)

    def start_server(self):
        if self.button_state.get() == "Start...":
            self.button_state.set("Stop !!")
            self.record_button.configure(fg_color="#b1101e")
            self.record_button.configure(hover_color="red")
            self.image_taken_var.set("Screenshots Taken: 0")
            self.images_taken_label.pack()
            self.record_keys_func()
        else:
            self.record_button.configure(fg_color="#144367")
            self.button_state.set("Start...")
            self.stop_record_keys_func()


class ImageCanvas(Canvas):
    def __init__(self, parent, load_image_func, draw_cropbox_func, reset_draw_cropbox_func):
        super().__init__(master = parent, background='#242424', bd=0, highlightthickness = 0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew')
        # self.bind('<Motion>',  lambda event: print(f'Image Cnavas: x1: {event.x} | y1: {event.y}'))
        self.bind('<B1-Motion>', draw_cropbox_func)
        self.bind('<ButtonRelease-1>', reset_draw_cropbox_func) # IDK What this does
        self.bind('<Configure>', load_image_func)


class Menu(ctk.CTkFrame):
    def __init__(self, parent, image_list, change_image_func, confirm_image_size_func, apply_crop_to_all_func, load_all_images_to_clipboardserver_func):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')
        if len(image_list) == 0:
            noimages = ctk.CTkLabel(master=self, text="No Images Found")
            noimages.pack()
        
        else:
            self.change_image_func = change_image_func
            self.scrollabe_images_frame = ctk.CTkScrollableFrame(master = self)
            self.image_buttons_list = []
            for file in image_list:
                image_name = file.split("/")[-1]
                button = ctk.CTkButton(master = self.scrollabe_images_frame, text = image_name, bg_color = 'transparent', fg_color='transparent', text_color='white')
                button.configure(command = lambda button = button: change_image_func(button))
                button.pack(pady=1)
                self.image_buttons_list.append(button)

        
            self.scrollabe_images_frame.pack()
            confirm_ss_btn = ctk.CTkButton(master = self, text = "Confirm Crop", command= confirm_image_size_func)
            confirm_ss_btn.pack(pady=5)

            apply_to_all_btn = ctk.CTkCheckBox(master = self, text = "Apply Crop to All", command= apply_crop_to_all_func)
            apply_to_all_btn.pack(pady = 10)

            load_images_to_clipboard_btn = ctk.CTkButton(master = self, text = "Load Images to Clipboard", command=load_all_images_to_clipboardserver_func)
            load_images_to_clipboard_btn.pack(pady = 30)

class ClipboardWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.grid(row = 0, columnspan = 2, column = 0, sticky = 'nsew')
        
        self.image_preview_canvas = Canvas(master = self, background='#242424', bd=0, highlightthickness = 0, relief='ridge')
        self.image_preview_canvas.pack()

        self.image_label_content_str = tk.StringVar()
        self.image_label_content_str.set("current/no_of_images")
        self.image_no_label = ctk.CTkLabel(master = self, textvariable = self.image_label_content_str)
        self.image_no_label.pack()

        self.instruction_label = ctk.CTkLabel(master = self, text = "Press <ctrl+windows+shift+'>' To cycle Images")
        self.instruction_label.pack()


class MiniSSEditWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x280+100+0")
        self.attributes("-topmost", True)
        
        # FIXME: [ ] Fix ME
        # self.grid(row = 0, columnspan = 2, column = 0, sticky = 'nsew')
        
        self.image_preview_canvas = Canvas(master = self, background='#242424', bd=0, highlightthickness = 0, relief='ridge')
        self.image_preview_canvas.pack()

        self.image_label_content_str = tk.StringVar()
        
        self.image_label_content_str.set("current/no_of_images")
        # self.instruction_label_str.set("Press <ctrl+windows+shift+:>' To Remove Image")
        self.image_no_label = ctk.CTkLabel(master = self, textvariable = self.image_label_content_str)
        self.image_no_label.pack()


        self.instruction_label_str = tk.StringVar()
        self.instruction_label = ctk.CTkLabel(master = self, text = "Press <ctrl+windows+shift+'>' To cycle Images")

        self.instruction_label_str.set("Press <ctrl+windows+shift+:' To Remove Image")
        self.delete_label = ctk.CTkLabel(master = self, textvariable = self.instruction_label_str)
        # self.instruction_label = ctk.CTkLabel(master = self, text = "Press <ctrl+windows+shift+'>' To cycle Images")
        self.instruction_label.pack()
        self.delete_label.pack()
    

