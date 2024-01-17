import customtkinter as ctk
import tkinter as tk
from tklinenums import TkLineNumbers

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.token import Token


from modules.UserConfig import UserConfig


class MainApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.__load_user_config__()
		self.__create_gui__()

	
	def __load_user_config__(self):
		self.config = UserConfig.get_user_config()

	def __create_gui__(self):
		self.__create_window__()
		self.__configure_grids__()
		self.__create_frames__()

		self.main_frame.__create_textbox__()
		self.main_frame.textbox.__create_line_counter__(self.left_frame)
	
	def __create_window__(self):
		self.title("The Pytext Editor Refactored")
		self.geometry("1100x749")
		self.resizable(True, True)

	def __configure_grids__(self):
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=0)

		self.grid_columnconfigure(0, weight=0, minsize=60)
		self.grid_columnconfigure(1, weight=1)

	def __create_frames__(self):
		self.bottom_frame = BottomFrame(self)
		self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=2, rowspan=2)

		self.main_frame = MainFrame(self)
		self.main_frame.grid(row=0, column=1, sticky="nsew")

		self.left_frame = LeftFrame(self)
		self.left_frame.grid(row=0, column=0, sticky="nsew")




class LeftFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
	

class BottomFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.mode = ctk.CTkLabel(self, text="Insert", justify="center")
		self.mode.grid(row=1, column=0)

		self.output = ctk.CTkLabel(self, text="Welcome to Pytext refactored")
		self.output.grid(row=2, column=0)


class MainFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)


	def __create_textbox__(self):
		self.update()
		self.textbox = Texto(self, font=ctk.CTkFont("Consolas", 30))
		self.textbox.grid(row=0, column=0, sticky="nsew")

	def set_textbox_height(self, height:int):
		"""set the main textbox height in lines."""
		return self.textbox._textbox.configure(height=height)


class Texto(ctk.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._lexer = pygments.lexers.PythonLexer

    def __create_line_counter__(self, master):
        self.update()
        self.line_counter = TkLineNumbers(master, self, justify="right", colors=("#DCE4EE", "#1D1E1E"), bd=0)
        self.line_counter.grid(row=0, column=0, sticky="nsew", pady=(6,0))
        self.__enable_auto_redraw__()

    def __enable_auto_redraw__(self):
        self.bind("<Key>", lambda e: self.after_idle(self.line_counter.redraw), add=True)
        self.bind("<KeyRelease>", lambda e: self.highlight_line())
	
    
    def highlight_line(self, lexer="python"):
		
        for tag in self.tag_names(index=None):
            if tag.startswith("Token"):
                self.tag_remove(tag, "1.0", "end")
				
        lexer = get_lexer_by_name(lexer)
        content = self.get("1.0", "end")
        tokens = list(pygments.lex(content, lexer))
		
        start_col = 0
        for i, (token, text) in enumerate(tokens):
            token = str(token)
			
            end_col = start_col + len(text)
            if token not in ["Token.Text.Whitespace", "Token.Text"]:
                print(token)
                print(self.tag_names())
                self.tag_add(token, f"{i+1}.{start_col}", f"{i+1}.{end_col}")
                #self.tag_config(token, foreground="#1c92ba")
            start_col = end_col
            self._setup_tags()
		
    def _setup_tags(self):
        for key in self.tag_names():
            self.tag_config(f"{key}", foreground="#1c92ba")

    
if __name__ == "__main__":
	app = MainApp()
	app.mainloop()
