from customtkinter import CTkFrame, CTkFont, CTkLabel, CTkScrollableFrame
import os
from modules.widgets.text import Lefttext, Maintext
from modules.ImageManager import ImageManager


class LeftFrame(CTkFrame):
    """ Contains the line counter. """
    def __init__(self, master, font:CTkFont):
        super().__init__(master)

        self.__grid_setup__()
        self.font = font
        
        self.terminal_dir = master.terminal_dir
        self.file_name = master.file_name
        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.mode = master.mode

        self.__load_theme__()
        self.configure(bg_color=self.bg_color, fg_color=self.fg_color)

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __load_theme__(self):
        dark = "_dark" if self.master.sys_theme == "dark" else ""
        self.bg_color = self.master.theme["frames"]["left"][f"bg{dark}"]
        self.fg_color = self.master.theme["frames"]["left"][f"fg{dark}"]

    def create_textbox(self, row:int = 0, column:int = 0):
        self.textbox = Lefttext(self, font=self.font)
        # self.textbox.configure(bg_color=self.bg_color, fg_color=self.fg_color)
    
    def hide_textbox(self):
        if self.textbox.winfo_ismapped():
            self.textbox.grid_forget()
    
    def show_textbox(self):
        if not self.textbox.winfo_ismapped():
            self.textbox.grid(row=0, column=0, sticky="nsew")
            file_abs_path = os.path.dirname(os.path.join(self.terminal_dir, self.file_name))
            isdir = os.path.isdir(file_abs_path)
            path = file_abs_path if isdir else self.terminal_dir
            print("abrindo ", path)
            self.textbox.open_directory(path)


class BottomFrame(CTkFrame):
    """Contains the outputs labels."""
    def __init__(self, master):
        super().__init__(master)
        self.output       = None
        self.command      = None
        self.branch_image = None
        self.branch       = None

        self.sys_theme = master.sys_theme
        self.theme     = master.theme
        self.mode      = master.mode

        self.__load_theme__()
        self.configure(bg_color=self.bg_color, fg_color=self.fg_color)

    def __load_theme__(self):
        dark = "_dark" if self.sys_theme == "dark" else ""
        self.bg_color       = self.theme["frames"]["bottom"][f"bg{dark}"]
        self.fg_color       = self.theme["frames"]["bottom"][f"fg{dark}"]

        self.mode_color     = self.theme["widgets"]["bottom"][f"mode{dark}"]
        self.command_color  = self.theme["widgets"]["bottom"][f"command{dark}"]
        self.output_color   = self.theme["widgets"]["bottom"][f"output{dark}"]
        self.branch_color   = self.theme["widgets"]["bottom"][f"branch{dark}"]

    def create_widgets(self, output: str):
        self.mode = CTkLabel(self, text=self.mode, justify="center", text_color=self.mode_color, bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.mode.grid(row=1, column=0, columnspan=2)

        self.command = CTkLabel(self, text="", justify="left", text_color=self.command_color, bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.command.grid(row=2, column=1, sticky="e")

        self.output = CTkLabel(self, text=output.replace("\\", "/"), text_color=self.output_color, bg_color=self.bg_color, fg_color=self.fg_color, padx=10, justify="left", font=self.master.gui_font)
        self.output.grid(row=2, column=0)

        self.grid_columnconfigure(1, weight=1)

    def load_icons(self):
        self.branch_image = ImageManager.get_image("branch", (20, 22))
    
    def create_branch_icon(self, branch: str):
        if "\n" in branch:
            branch = branch.replace("\n", "")

        self.branch = CTkLabel(self, image=self.branch_image, text=branch, text_color=self.branch_color, justify="left", compound="left", font=self.master.gui_font, padx=10)
        self.branch.grid(row=2, column=2, sticky="e")

    
    def destroy_branch_icon(self):
        print("Destruindo")
        try:
            self.branch.destroy()
        except AttributeError:
            pass

    def clear_command_output(self):
        self.command.configure(text='')


class MainFrame(CTkFrame):
    """It is the main frame that contains the Maintext instance."""
    def __init__(self, master, font:CTkFont):
        super().__init__(master)
        self.font = font

        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.mode = master.mode


        self.__grid_setup__()
        self.__load_theme__()


    def __load_theme__(self):
        dark = "_dark" if self.sys_theme == "dark" else ""
        self.bg_color = self.theme["frames"]["left"][f"bg{dark}"]
        self.fg_color = self.theme["frames"]["left"][f"fg{dark}"]
        

    def create_textbox(self, row:int = 0, column:int = 0):
        self.textbox = Maintext(self, font=self.font)
        self.textbox.grid(row=row, column=column, sticky="nsew")
        #self.textbox.configure(bg_color=self.bg_color, fg_color=self.bg_color)
        self.master.update()
        self.textbox.focus_set()

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
