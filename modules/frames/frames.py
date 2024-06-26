from tkinter import Frame, font, Label, Scrollbar, ttk

import os
from modules.widgets.text import Lefttext, Maintext
from modules.ImageManager import ImageManager
from modules.Application import Application

DEFAULT_SIZE_OF_EXPLORER_TEXT_WIDGET = 20


class PytextFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bg_color      = ''
        self.fg_color      = ''
        self.mode_color    = ''
        self.command_color = ''
        self.output_color  = ''
        self.branch_color  = ''
        self.sys_theme      = master.sys_theme
        self.theme          = master.theme
        self.dark = "_dark" if self.sys_theme == "dark" else ""

    def load_frame_theme(self, frame):
        self.bg_color       = self.theme["frames"][frame][f"bg{self.dark}"]
        self.fg_color       = self.theme["frames"][frame][f"fg{self.dark}"]

    def load_bottom_widget_theme(self):
        self.mode_color     = self.theme["widgets"]["bottom"][f"mode{self.dark}"]
        self.command_color  = self.theme["widgets"]["bottom"][f"command{self.dark}"]
        self.output_color   = self.theme["widgets"]["bottom"][f"output{self.dark}"]
        self.branch_color   = self.theme["widgets"]["bottom"][f"branch{self.dark}"]


class LeftFrame(PytextFrame):
    """ Contains the file explorer. """
    def __init__(self, master, obj_font: font):
        super().__init__(master)
        self.textbox = None
        self.font = obj_font
        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.terminal_dir = master.terminal_dir
        self.file_name = master.file_name
        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.mode = master.mode

        self.__grid_setup__()
        super().load_frame_theme("left")
        self.__scrollbar_setup__()

    def __scrollbar_setup__(self):
        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.__scroll_x__)
        self.scrollbar_x.grid(row=0, column=0, sticky="we")

    def __scroll_x__(self, *args):
        self.textbox.xview(*args)

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_textbox(self, row: int = 0, column: int = 0):
        self.textbox = Lefttext(self, font=self.font, width=DEFAULT_SIZE_OF_EXPLORER_TEXT_WIDGET, wrap='none')
        self.textbox.configure(bg=self.bg_color)
        self.textbox.config(xscrollcommand=self.scrollbar_x.set)
    
    def show_textbox(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.textbox.grid(row=0, column=0, sticky="nsew")
        file_abs_path = os.path.dirname(os.path.join(self.terminal_dir, self.file_name))
        isdir = os.path.isdir(file_abs_path)
        path = file_abs_path if isdir else self.terminal_dir
        self.textbox.open_directory(path)
        self.textbox.focus_set()

    def switch_view(self, e=None):
        if self.winfo_ismapped():
            if "leftframe" in str(self.focus_get()):
                self.grid_forget()
                Application.mainapp.main_frame.textbox.focus_set()
            else:
                self.textbox.focus_set()
        else:
            self.show_textbox()

    def open_file_or_directory(self):
        if "leftframe" not in str(self.focus_get()):
            return False

        side_bar_selected_file_name = self.textbox.get_current_line_content().strip()
        if side_bar_selected_file_name[0] == "▼":
            self.textbox.updir()
            return

        elif side_bar_selected_file_name[0] == "/":
            side_bar_selected_file_name = side_bar_selected_file_name[1:]

        content = os.path.join(self.textbox.path, side_bar_selected_file_name)

        if os.path.isdir(content):
            self.textbox.open_directory(content)
            return
        else:
            # contar quantos diretorios tem antes e ir salvando a posicao do cursor pra retomar
            if Application.mainapp.main_frame.textbox.open_file(content):
                Application.mainapp.main_frame.textbox.focus_set()


# class LineCounterFrame(PytextFrame):
#     def __init__(self, master):
#         super().__init__(master)
#
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=0)
#
#         self.sys_theme = master.sys_theme
#         self.theme = master.theme
#         super().load_frame_theme("line_counter")
#         self.configure(bg="red")


class BottomFrame(PytextFrame):
    """Contains the outputs labels."""
    def __init__(self, master):
        super().__init__(master)
        self.output       = None
        self.command      = None
        self.branch       = None

        self.sys_theme = master.sys_theme
        self.theme     = master.theme
        self.mode      = master.mode
        self.gui_font  = master.gui_font

        super().load_frame_theme("bottom")
        super().load_bottom_widget_theme()
        self.configure(bg=self.bg_color)

    def create_widgets(self, output: str):
        self.mode = Label(
            self, text=self.mode, justify="center",
            bg=self.bg_color, foreground=self.mode_color,
            font=self.master.gui_font
        )
        self.mode.grid(row=1, column=0, columnspan=2)

        self.command = Label(
            self, text="", justify="left",
            bg=self.bg_color, foreground=self.command_color,
            font=self.master.gui_font
        )
        self.command.grid(row=2, column=1, sticky="e")

        self.output = Label(
            self, text=output.replace("\\", "/"), justify="left",
            bg=self.bg_color, foreground=self.output_color,
            padx=10,
            font=self.master.gui_font
        )
        self.output.grid(row=2, column=0)
        self.grid_columnconfigure(1, weight=1)

    def clear_command_output(self):
        self.command.configure(text='')


class MainFrame(PytextFrame):
    """It is the main frame that contains the Maintext instance."""
    def __init__(self, master, obj_font: font):
        super().__init__(master)
        self.tabs = None
        self.textbox = None
        self.font = obj_font

        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.mode = master.mode

        self.__grid_setup__()
        self.__load_theme__()

    def create_textbox(self, row: int = 1, column: int = 2):
        self.tabs = ttk.Notebook(self, width=10)
        self.tabs.grid(row=0, column=2, sticky="ew")
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text="teste")

        self.textbox = Maintext(self, font=self.font)
        self.textbox.grid(row=row, column=column, sticky="nsew")
        self.master.update()
        self.textbox.focus_set()





            # text_widget = tk.Text(frame)
            # text_widget.pack(expand=1, fill="both")
            #
            # self.file_contents[title] = text_widget

    def __load_theme__(self):
        dark = "_dark" if self.sys_theme == "dark" else ""
        self.bg_color = self.theme["frames"]["left"][f"bg{dark}"]
        self.fg_color = self.theme["frames"]["left"][f"fg{dark}"]

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


class TopFrame(PytextFrame):
    def __init__(self, master):
        super().__init__(master)

        self.tabs = ttk.Notebook(self, width=10)
        self.tabs.grid(row=0, column=0, sticky="we")
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text="teste")
