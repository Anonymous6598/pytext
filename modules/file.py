import os
import customtkinter as ctk
from time import sleep

class File():
    def __init__(self, file_name, terminal_directory):
        self.current_directory = self.get_current_directory()
        self.file_name = file_name
        self.terminal_directory = terminal_directory


    def get_current_directory(self):
        return os.getcwd()
    

    def open_local_directory_or_file(self, dir_name:str, textbox, mainapp, gui, updir = False):
        """Runs when user try to open a file or directory inside the Open LocalDir"""
        fulldir = os.path.join(self.terminal_directory, dir_name)
        fulldir_path_format = os.path.join(self.terminal_directory, dir_name[2:-1])

        # if user is trying to open a up directory (..)
        if updir:
            if os.path.isdir(fulldir):
                return self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir)
            # else: print("Root directory not found: ", fulldir)

        # if user is trying to open a directory
        if os.path.isdir(fulldir_path_format):
            return self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir_path_format)

        # if user is trying to open a file
        elif os.path.isfile(fulldir):
            with open(fulldir, "r", encoding="utf8") as file:
                content = file.read()
            return gui.write_another_file_content(content, file_name=dir_name, auto_insert=True)
        #else: print("Path is not a file or a directory. ", fulldir, fulldir_path_format)
        

    def load_local_files_to_open(self, textbox, mainapp, path_to_open:str = ""):
        """Runs when user Opens the current directory"""
        try:
            # path_to_open is used to open a custom path
            current_terminal_directory = self.current_directory if path_to_open == "" else path_to_open
            files_in_current_dir = os.listdir(current_terminal_directory)
            
            textbox.configure(state="normal")
            textbox.delete("1.0", "end")
            all_tags = []
        
            for i, file in enumerate(files_in_current_dir):
                cur_line = int(textbox.index(ctk.INSERT).split(".")[0])

                # check if its the last element. True if i = len(files_in_current_dir) - 1
                is_last_element = i == len(files_in_current_dir) - 1

                # check if it is a directory
                is_dir = os.path.isdir(os.path.join(current_terminal_directory, file))

                file_type_prefix = "▼ " if is_dir else ""
                file_type_sufix = "/" if is_dir else ""

                textbox.insert(f"{i + 1}.0", f"{file_type_prefix}{file}{file_type_sufix}" + ("" if is_last_element else "\n"))
                
                tag_name = f"dir_color{i}" if is_dir else f"file_color{i}"
                textbox.tag_add(tag_name, f"{cur_line}.0", f"{cur_line}.end")
                all_tags.append(tag_name)

            for tag in all_tags:
                color = "red" if "file" in tag else "blue"
                textbox.tag_config(tag, foreground=color)

            # insert the current terminal directory in the first line
            textbox.insert(f"1.0", f"{current_terminal_directory}\n")
            textbox.tag_add("curdir", "1.0", "1.end")
            textbox.tag_config("curdir", foreground="green")

            textbox.configure(state="disabled")
            mainapp.File.file_name = "__pytextLocaldir__"
            # Saving the current terminal directory after it sucessfully opens
            self.terminal_directory = current_terminal_directory
            textbox.mark_set(ctk.INSERT, "2.0")
            mainapp.GUI.realcar_linha_selecionada()

        except PermissionError:
            print("Pytext doesn't have permission to open this file: ", path_to_open)


    def get_up_directory(self):
        return os.path.dirname(self.terminal_directory)


    def create_new_file(self, gui):
        self.file_name = None
        return gui.write_another_file_content("", file_name=None, auto_insert=True)


    def create_new_directory(self, dir_name:str, textbox, mainapp):
        full_path = os.path.join(self.terminal_directory, dir_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        self.load_local_files_to_open(textbox, mainapp, path_to_open=self.terminal_directory)
    

    def insert_new_dir_title(self, gui):
        newDirTitlepreset = os.path.join(os.getcwd(), ".temp", "__pytextNewDirTitle__.txt")

        with open(newDirTitlepreset, "r", encoding="utf8") as file:
            content = file.read()
            gui.write_another_file_content(content, True)
            self.file_name = "__pytextNewDirTitle__"
