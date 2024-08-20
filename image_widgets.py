import customtkinter as ctk
from tkinter import filedialog, ttk



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
