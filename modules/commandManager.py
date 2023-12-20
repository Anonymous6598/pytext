
import customtkinter as ctk
from modules import shortcuts
import re



class CommandManager:
    def __init__(self, root:ctk.CTk()):
        self.root = root


    def setup(self, main_app_instance, main_textarea:ctk.CTkTextbox, bottom_command_output:ctk.CTkTextbox,
              gui_instance):
        self.maintext = main_textarea
        self.bottom_command_output = bottom_command_output
        self.main_app_instance = main_app_instance
        self.gui = gui_instance


    def capture_keybinds(self):
        self.root.bind("<Key>", self.tecla_pressionada)
        self.root.bind("<KeyRelease>", self.atualizar_contador_de_linhas_e_colunas_globais)
        self.root.bind("<Escape>", lambda e: self.trocar_modo(self.main_app_instance.modo))
        # Atualizar as labels para ajustar na resolução
        self.root.bind("<Prior>", lambda e: self.gui.teste(e))
        self.maintext.bind("<MouseWheel>", lambda e: "break")


    def atualizar_contador_de_linhas_e_colunas_globais(self, e = None):
        return self.gui.bottom_output_doc_info.configure(text=self.gui.obter_numero_de_linhas_e_colunas(f=True))


    def trocar_modo(self, modo):
        if modo == "view":
            # caso vc aperte ESC com comando definido na caixa, ele so apaga o comando. Nao troca de modo
            comando = self.bottom_command_output.get("1.0", "end-1c")

            if comando != "":
                self.bottom_command_output.delete("1.0", ctk.END)
                self.maintext.focus_set()
                return 0

            self.main_app_instance.modo = "insert"
            self.maintext.configure(state="normal")
            self.maintext.focus_set()
            self.gui.bottom_output_detail.configure(text="")
        else:
            self.main_app_instance.modo = "view"
            self.maintext.configure(state="disabled")
        
        self.bottom_command_output.delete("1.0", ctk.END)
        #print(self.main_app_instance.modo)
        return self.gui.bottom_output_mode.configure(text=self.main_app_instance.modo)


    def tecla_pressionada(self, event):
        self.gui.realcar_linha_selecionada(self.gui)
        tecla = event.keysym
        #print(event)

        if self.main_app_instance.modo == "view":
            comando = self.bottom_command_output.get("1.0", "end-1c")
            
            # Caso não haja comandos e aperte :
            if comando == "":
                if tecla == "colon":
                    self.bottom_command_output.focus_set()

                else:
                    match tecla:
                        case "i":
                            return self.trocar_modo(self.main_app_instance.modo)
                        
                        case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                            return self.gui.atualizar_contador(tecla)
                        
                        case _:
                            return 0

            # Caso aperte Enter para registrar o comando
            elif tecla == "Return":
                self.catch_command(comando)
                self.maintext.focus_set()
 

        elif self.main_app_instance.modo == "insert":

            match tecla:
                case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                    return self.gui.atualizar_contador(tecla)
                case _:
                    return 0


    def catch_command(self, comando):
        # separando o comando em partes: numero de vezes a rodar e o comando
        def extrair_numeros(texto):
            numeros = re.findall(r'\d+', texto)
            if numeros:
                return int(''.join(numeros))
            else:
                return 0

        comando_sem_numeros = re.sub(r'\d', '', comando)
        numeros = extrair_numeros(comando)

        # tratando o comando de fato
        command_output = shortcuts.search_command(comando_sem_numeros, numeros, self.maintext)

        if command_output == "sair":
            self.root.destroy()
            exit()
        else:
            self.gui.bottom_output_detail.configure(text=command_output)
            self.gui.atualizar_contador()
            self.gui.realcar_linha_selecionada()

            # apagando o comando enviado
            self.bottom_command_output.delete("1.0", ctk.END)
            return 0
