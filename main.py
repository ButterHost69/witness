import customtkinter as ctk
from image_widgets import *
import keyboard
from PIL import ImageGrab, Image, ImageTk
import os
from os.path import isfile
import io
import win32clipboard
import shutil

# Bugs:
# [X] Have to Run EXE as Admin to create temp dir (Sol: Shit the temp fol to docs fol)
# [ ] App freezeses and unable to close during and error (Sol: better error handl)

# TODO: [ ] Discard a taken screenshot
# TODO: [ ] Reorder Screenshots in the Editing Menu
# TODO: [ ] Use a better color for crop border

#TODO: [ ] Continue Taking More Screenshots in SS Edit Window and be displayed
#TODO: [ ] See a better way of loading Images/Something like lazy loading ?? Have a Global Place to store images, from where they can be accessed by others

# FIXME: [ ] When No Images blank screen appears, fix and display no image or something

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
        super().__init__(fg_color='#242424')
        ctk.set_appearance_mode('dark')
        self.geometry('800x500')
        self.minsize(800,500)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing_window)
        self.title("Witness")
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=2, uniform='a')
        self.columnconfigure(index=1, weight=6, uniform='a')

        self.image_canvas_tagname = "imagecanvas#1"
        self.cropbox_tagname = "cropbox#1"
        self.x1 = None
        self.y1 = None
        self.apply_to_all_checkbox = False

        self.screenshot_counter_window = None

        self.delete_ss_folder_later = False
        self.select_folder_widget = SelectFolderWindow(parent = self, start_ss_server_func= self.start_ss_server, delete_ss_folder_later_func= self.update_delete_ss_folder_later)

        # self.bind('<Escape>', lambda _ : self.quit())
        self.attributes('-alpha', 0.8)
        # self.attributes('-alpha', 1)
        png_path = os.path.abspath("32x32logo.png")
        ico_path = os.path.abspath(r"assets/logo.ico")
        # icon = PhotoImage(file=png_path)
        self.wm_iconbitmap(bitmap=ico_path, default=ico_path)
        self.mainloop()

    def on_closing_window(self):
        if self.delete_ss_folder_later:
            # print("LOG: Deleting Temp Dirr")
            shutil.rmtree(self.images_folder_path)

        if self.screenshot_counter_window != None:
            self.screenshot_counter_window.destroy()
            self.screenshot_counter_window = None

        # print("LOG: Window is closing. Executing cleanup function.")
        self.destroy() 
        os._exit(0)

    def update_delete_ss_folder_later(self, value: bool):
        # print(f"log : Update Called: {value}")
        self.delete_ss_folder_later = value

    def start_ss_server(self, path:str):
        self.images_folder_path = path
        self.select_folder_widget.grid_forget()
        self.screenshotserver_window = ScreenshotServerWindow(parent=self, record_keys_func= self.record_keys, stop_record_keys_func=self.stop_record_keys)
    
    def record_keys(self):
        global fileno
        fileno = 0
        self.if_miniss_edit_window = False
        keyboard.add_hotkey('ctrl+windows+alt+space', self.take_screenshot)
        keyboard.add_hotkey('ctrl+windows+z', self.open_ss_edit_window)
        self.screenshot_counter_window = ScreenshotCounterWindow()
        # print(f"LOG : Screen Shot Counter Set : {self.screenshot_counter_window}")
    
    # TODO: [ ] Unable to Load Separate Window, atm same start, stop window is overriden
    def open_ss_edit_window(self):
        # If Window Already Opened, Close
        if self.if_miniss_edit_window:
            self.mini_ss_edit_window.destroy()
            self.if_miniss_edit_window = False
            # keyboard.remove_hotkey('ctrl+windows+shift+>')
            # keyboard.remove_hotkey('ctrl+windows+shift+D')
            return

        # Or Open Window
        self.if_miniss_edit_window = True
        self.all_images_fullpath = self.getallimages(self.images_folder_path)
        self.mini_ss_edit_window = MiniSSEditWindow()
        keyboard.add_hotkey('ctrl+windows+shift+>', self.cycle_preview_miniss_images)
        keyboard.add_hotkey('ctrl+windows+shift+:', self.delete_screenshot_confirm)

        self.update_preview_page_stack()
        
        global preview_image_index
        preview_image_index = 0
        total_images = len(self.all_images_fullpath)
        image_counter_str = f'{preview_image_index + 1}/{total_images}'
        self.mini_ss_edit_window.image_label_content_str.set(image_counter_str)
        self.mini_ss_edit_window.image_preview_canvas.create_image(150, 150, image = self.preview_image_stack[0].image_tk)
    
    def exit_delete_option(self):
        try:
            keyboard.remove_hotkey('enter')
            self.mini_ss_edit_window.instruction_label_str.set("Press <ctrl+windows+shift+:' To Remove Image")    
        except:
            print("Already Escaped")

    def delete_screenshot_confirm(self):
        keyboard.add_hotkey('enter', self.delete_screenshot_function)
        keyboard.add_hotkey('escape', self.exit_delete_option)
        # print("Confirm Delete Screenshot Button...")
        self.mini_ss_edit_window.instruction_label_str.set("Press `enter` To Confirm Delete")

    def update_preview_page_stack(self):
        self.preview_image_stack = []
        for image_path in self.all_images_fullpath:
            myimage = MyImage(image_path)
            image_width = 300
            image_height = image_width/myimage.image_ratio
            resized_image = myimage.image.resize((int(image_width), int(image_height)))
            myimage.image_tk = ImageTk.PhotoImage(image = resized_image)
            self.preview_image_stack.append(myimage)
        

    # [X] Change File Location Name to match sequence ??? maybe
    # [X] Esc Doesnt Work, display Esc as Presesed and delete menu is closed
    # [X] Check is Keybind there is not dont error use try Cath
    # [X] Next Image in SSEDIT MENU NOT working after deletion
    # [X] Index out of range error if deleting last ss
    # [X] If No image Display, No Image rather than crashing
    # [X] Path error in final Menu 

    # [ ] Counter display is not proper becomes 0 for some reason
    # [X] Deleted Image and Previewing Images is not the same
    def delete_screenshot_function(self):
        global preview_image_index
        print(f"Preview Image Index: {preview_image_index}")
        print(f"Image Deleting: {self.all_images_fullpath[preview_image_index]}")
        
        # Dont Change this --- This is correct
        os.remove(self.all_images_fullpath[preview_image_index])
        del self.all_images_fullpath[preview_image_index]
        # preview_image_index = (preview_image_index + 1)%len(self.all_images_fullpath)
        self.update_preview_page_stack()

        if len(self.all_images_fullpath) >= preview_image_index:
            preview_image_index -= 1
        elif preview_image_index < 0:
            preview_image_index = 0
        elif preview_image_index == 0:
            preview_image_index = 0
        # if len(self.all_images_fullpath) <= 1:
        #     preview_image_index = 0
        if len(self.all_images_fullpath) == 0:
            self.mini_ss_edit_window.image_preview_canvas.delete('all')
            self.mini_ss_edit_window.image_label_content_str.set("No More Screenshots")    
        else:
            self.mini_ss_edit_window.image_preview_canvas.delete('all')
            self.mini_ss_edit_window.image_preview_canvas.create_image(150, 150, image = self.preview_image_stack[preview_image_index].image_tk)
            image_counter_str = f'{preview_image_index + 1}/{len(self.all_images_fullpath)}'
            self.mini_ss_edit_window.image_label_content_str.set(image_counter_str)
        self.exit_delete_option()
        # self.all_images_fullpath[preview_image_index]
        # pass
        

    def take_screenshot(self):
        global fileno
        # filepath = f"{fileno}.png"
        filepath = f"{self.images_folder_path}/{fileno}.png"
        image_grab_instance = ImageGrab.grab()
        image_grab_instance.save(filepath)
        image_grab_instance.close()
        self.screenshotserver_window.image_taken_var.set(f"Screenshots Taken: {fileno + 1}")
        fileno += 1
        self.screenshot_counter_window.increament_counter()
    
    def getallimages(self, path:str) -> list[str]:
        image_list = []
        for file in os.listdir(path + "/"):
            fullpath = path + "/" + file 
            if isfile(fullpath):
                if file.split(".")[-1] == "png":
                    image_list.append(file)

        
        images_sort_list = [int(image.split(".")[0]) for image in image_list]
        images_sort_list.sort()
        # path = str(rf"{path}\{str(image)}.png")
        print("Pre-add",images_sort_list)
        # images_sort_list = [os.path.join(path, f"{image}.png") for image in images_sort_list]
        images_sort_list = [f"{path}/{image}.png" for image in images_sort_list]
        print("Post-add", images_sort_list)
        # images_sort_list = [str(path + r"\\" + str(image) + ".png") for image in images_sort_list]
        return images_sort_list

    def stop_record_keys(self):
        keyboard.remove_all_hotkeys()
        self.attributes("-alpha", 0.9)
        self.screenshotserver_window.grid_forget()
        
        if self.screenshot_counter_window != None:
            self.screenshot_counter_window.destroy()
            self.screenshot_counter_window = None

        self.all_images_fullpath = self.getallimages(self.images_folder_path)
        self.curr_image = MyImage(filepath=self.all_images_fullpath[0])

        self.update_preview_page_stack()
        self.menu_window = Menu(self, image_list=self.all_images_fullpath, change_image_func = self.change_image, confirm_image_size_func = self.confirm_image_size, apply_crop_to_all_func=self.apply_to_all, load_all_images_to_clipboardserver_func = self.load_all_images_to_clipboard)
        self.image_canvas = ImageCanvas(self, load_image_func=self.load_image, draw_cropbox_func= self.draw_cropbox, reset_draw_cropbox_func= self.reset_draw_cropbox)
    
    def change_image(self, button:ctk.CTkButton):
        for cbutton in self.menu_window.image_buttons_list:
            cbutton.configure(bg_color = 'transparent', fg_color='transparent')

        button.configure(fg_color="blue")
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
        # print(f"Load Image: X: {self.curr_image.image_tk.width()} ; Y: {self.curr_image.image_tk.height()}")
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
        extra_yspace = (self.image_canvas.winfo_height() / 2) - (self.curr_image.image_tk.height() / 2)
        extra_xspace = (self.image_canvas.winfo_width() / 2) - (self.curr_image.image_tk.width() / 2)
        self.x2 = event.x
        self.y2 = event.y 
        self.newy1 = self.y1 - extra_yspace
        self.newy2 = self.y2 - extra_yspace
        self.newx1 = self.x1 - extra_xspace
        self.newx2 = self.x2 - extra_xspace

    def confirm_image_size(self):
        # Resized Image Coordinates -> to -> Image Cordinates
        resized__image_x, resized__image_y = self.curr_image.image_tk.width(), self.curr_image.image_tk.height()
        real_image_x, real_image_y = self.curr_image.image_width, self.curr_image.image_height
        rate_change_x = real_image_x/resized__image_x
        rate_change_y = real_image_y/resized__image_y
        changed_x1, changed_x2 = self.newx1 * rate_change_x, self.newx2 * rate_change_x
        changed_y1, changed_y2 = self.newy1 * rate_change_y, self.newy2 * rate_change_y # There is some offset in 'Y' I dont know Why ??
        # print(f"Confirm Image: X: {self.curr_image.image_tk.width()} ; Y: {self.curr_image.image_tk.height()}")
        if self.apply_to_all_checkbox:
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
    
    def load_all_images_to_clipboard(self):
        self.image_canvas.grid_forget()
        self.menu_window.grid_forget()
        
        self.clipboard_window = ClipboardWindow(parent = self)
        self.minsize(0,0)
        self.geometry("300x280")
        self.attributes("-topmost", True)
        keyboard.add_hotkey('ctrl+windows+shift+>', self.cycle_preview_images)

        self.update_preview_page_stack()

        global preview_image_index
        preview_image_index = 0
        total_images = len(self.all_images_fullpath)
        image_counter_str = f'{preview_image_index + 1}/{total_images}'
        self.clipboard_window.image_label_content_str.set(image_counter_str)
        self.load_image_to_clipboard(image = self.preview_image_stack[preview_image_index].image)
        clipboardcanvas_height = self.clipboard_window.image_preview_canvas.winfo_height()
        clipboardcanvas_width = self.clipboard_window.image_preview_canvas.winfo_width()
        self.clipboard_window.image_preview_canvas.create_image(150, 150, image = self.preview_image_stack[0].image_tk)

    # TODO: [ ] Merge Both load image code for miniss and clipboard
    def cycle_preview_miniss_images(self):
        global preview_image_index
        preview_image_index += 1
        total_images = len(self.all_images_fullpath)
        if preview_image_index == total_images:
            preview_image_index = 0

        self.mini_ss_edit_window.image_preview_canvas.delete('all')
        self.mini_ss_edit_window.image_preview_canvas.create_image(150, 150, image = self.preview_image_stack[preview_image_index].image_tk)
        image_counter_str = f'{preview_image_index + 1}/{total_images}'
        self.mini_ss_edit_window.image_label_content_str.set(image_counter_str)

    def cycle_preview_images(self):
        global preview_image_index
        preview_image_index += 1
        total_images = len(self.all_images_fullpath)
        if preview_image_index == total_images:
            preview_image_index = 0
        
        self.load_image_to_clipboard(image = self.preview_image_stack[preview_image_index].image)
        self.clipboard_window.image_preview_canvas.delete('all')
        self.clipboard_window.image_preview_canvas.create_image(150, 150, image = self.preview_image_stack[preview_image_index].image_tk)
        image_counter_str = f'{preview_image_index + 1}/{total_images}'
        self.clipboard_window.image_label_content_str.set(image_counter_str)

    def load_image_to_clipboard(self, image:Image):
        output = io.BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        # Copy the image to the clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

App()


