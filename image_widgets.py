import customtkinter as ctk
from tkinter import filedialog, ttk, Canvas



class SelectFolderWindow(ctk.CTkFrame):
    def __init__(self, parent, start_ss_server_func):
        super().__init__(master = parent)
        self.start_ss_server_func = start_ss_server_func
        self.grid(row = 0, columnspan=2,column = 0 , stick = 'nsew')

        expand_frame = ctk.CTkFrame(master = self)
        label = ctk.CTkLabel(master = expand_frame, text = "Select Path to Store Screenshots")
        label.pack()
        select_folder_btn = ctk.CTkButton(master = expand_frame, text="Open Explorer", command=self.select_path)
        select_folder_btn.pack()
        expand_frame.pack(expand = True)
    
    def select_path(self):
        path = filedialog.askdirectory()
        self.start_ss_server_func(path)


class ScreenshotServerWindow(ctk.CTkFrame):
    def __init__(self, parent, record_keys_func, stop_record_keys_func):
        super().__init__(master = parent)
        self.record_keys_func = record_keys_func
        self.stop_record_keys_func = stop_record_keys_func

        self.grid(row = 0, columnspan = 2, column = 0, sticky = 'nsew')
        expand_frame = ctk.CTkFrame(master = self)
        expand_frame.pack(expand = True)
        instruction_label = ctk.CTkLabel(master = expand_frame, text = "Press <Ctrl-WinL+Alt+Space> To Take Screenshot !!")
        instruction_label.pack()
        
        self.record_button = ttk.Button(master = expand_frame, text="Start...", command=self.start_server)
        # self.record_button["background"] = "blue"
        self.record_button.pack()

    def start_server(self):
        if self.record_button["text"] == "Start...":
            # self.record_button["background"] = "Red"
            self.record_button["text"] = "Stop !!"
            self.record_keys_func()
        else:
            # self.record_button["background"] = "Blue"
            self.record_button["text"] = "Start..."
            self.stop_record_keys_func()


class ImageCanvas(Canvas):
    def __init__(self, parent, load_image_func):
        super().__init__(master = parent, background='#242424', bd=0, highlightthickness = 0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew')
        self.bind('<Configure>', load_image_func)


class Menu(ctk.CTkFrame):
    def __init__(self, parent, image_list, change_image_func):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')
        for file in image_list:
            image_name = file.split("/")[-1]
            button = ctk.CTkButton(master = self, text = image_name, bg_color = 'transparent', fg_color='transparent', text_color='white')
            button.configure(command = lambda button = button: change_image_func(button))
            button.pack()
            