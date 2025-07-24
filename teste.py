import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import sys 
from PIL import Image, ImageTk 

# --- Funções Auxiliares ---

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, para ser compatível com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
        print(f"DEBUG: Modo PyInstaller detectado. Base path: {base_path}") 
    else:
        base_path = os.path.abspath(".")
        print(f"DEBUG: Modo de script normal detectado. Base path: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"DEBUG: Caminho completo do recurso: {full_path}") 
    return full_path

def show_message(title, message, type='info'):
    """Exibe uma caixa de mensagem personalizada."""
    if type == 'error':
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)

def save_start_date(date_str):
    """Salva a data de início em um arquivo."""
    try:
        with open(resource_path("start_date.txt"), "w") as f:
            f.write(date_str)
        return True
    except IOError:
        show_message("Erro", "Não foi possível salvar a data.", 'error')
        return False

def load_start_date():
    data_file_path = resource_path("start_date.txt")
    if os.path.exists(data_file_path):
        try:
            with open(data_file_path, "r") as f:
                return f.read().strip()
        except IOError:
            show_message("Erro", "Não foi possível carregar a data.", 'error')
    return None

def calculate_days(start_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        today = datetime.now()
        
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        diff = today - start_date
        return diff.days
    except ValueError:
        return -1

# --- Lógica Principal do Aplicativo ---

class RelationshipCounterApp:
    def __init__(self, master):
        self.master = master
        master.title("Eu te amo")
        master.geometry("400x550") 
        master.resizable(False, False) 
        master.configure(bg="#ffe4e6") 

        self.font_title = ("Inter", 18, "bold")
        self.font_days = ("Inter", 30, "bold")
        self.font_label = ("Inter", 10)
        self.font_button = ("Inter", 12, "bold")
        self.pink_dark = "#d81b60"
        self.pink_light = "#fbcfe8"
        self.white = "#fff"

        # Frame principal para centralizar o conteúdo
        self.main_frame = tk.Frame(master, bg=self.white, bd=0, relief="flat")
        self.main_frame.pack(pady=30, padx=20, fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Container para o conteúdo central
        self.content_frame = tk.Frame(self.main_frame, bg=self.white, padx=20, pady=20, bd=0, relief="flat")
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=0) 
        self.content_frame.grid_rowconfigure(1, weight=0) 
        self.content_frame.grid_rowconfigure(2, weight=1) 
        self.content_frame.grid_rowconfigure(3, weight=0) 
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.gif_image_path = resource_path("cat_animated.gif")
        self.frames = []
        self.current_frame_index = 0
        self.animation_id = None 
        
        print(f"DEBUG: Tentando carregar GIF de: {self.gif_image_path}") 
        try:
            if os.path.exists(self.gif_image_path):
                print(f"DEBUG: Arquivo GIF encontrado em: {self.gif_image_path}") 
                self.gif_img = Image.open(self.gif_image_path)
                
                
                try:
                    while True:
                        
                        frame = self.gif_img.copy()
                        frame = frame.resize((100, 100), Image.LANCZOS)
                        self.frames.append(ImageTk.PhotoImage(frame))
                        self.gif_img.seek(len(self.frames)) 
                except EOFError:
                    pass 

                if self.frames:
                    self.cat_label = tk.Label(self.content_frame, image=self.frames[0], bg=self.white)
                    self.cat_label.grid(row=0, column=0, pady=(0, 15))
                    self.animate_gif() 
                    print(f"DEBUG: GIF carregado com {len(self.frames)} quadros.") 
                else:
                    self.cat_label = tk.Label(self.content_frame, text="[GIF de Gatinho (vazio)]", font=("Inter", 10), fg="#888", bg=self.white)
                    self.cat_label.grid(row=0, column=0, pady=(0, 15))
                    show_message("Aviso", "O arquivo GIF está vazio ou corrompido. Usando placeholder de texto.", 'info')
                    print(f"DEBUG: O GIF '{self.gif_image_path}' não contém quadros válidos ou está vazio.")
            else:
                self.cat_label = tk.Label(self.content_frame, text="[GIF de Gatinho Fofo]", font=("Inter", 10), fg="#888", bg=self.white)
                self.cat_label.grid(row=0, column=0, pady=(0, 15))
                show_message("Aviso", f"Arquivo '{self.gif_image_path}' não encontrado. Usando placeholder de texto para o gatinho.\nCertifique-se de que o GIF está na mesma pasta do script e o nome está correto.", 'info')
                print(f"DEBUG: Arquivo GIF NÃO encontrado em: {self.gif_image_path}")
        except Exception as e:
            self.cat_label = tk.Label(self.content_frame, text="[Erro ao carregar GIF]", font=("Inter", 10), fg="#888", bg=self.white)
            self.cat_label.grid(row=0, column=0, pady=(0, 15))
            show_message("Erro", f"Não foi possível carregar o GIF do gatinho: {e}. Usando placeholder de texto.", 'error')
            print(f"DEBUG: Erro inesperado ao carregar GIF: {e}")


        # Título
        self.title_label = tk.Label(self.content_frame, text="eu te amo há...", font=self.font_title, fg="#333", bg=self.white)
        self.title_label.grid(row=1, column=0, pady=(0, 10))

        # Contador de dias
        self.days_display = tk.Label(self.content_frame, text="0 dias", font=self.font_days, fg=self.pink_dark, bg=self.white)
        self.days_display.grid(row=2, column=0, pady=(10, 20))

        # Seção de entrada de data
        self.date_input_frame = tk.Frame(self.content_frame, bg=self.white)
        self.date_input_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.date_input_frame.grid_columnconfigure(0, weight=1) 

        self.date_label = tk.Label(self.date_input_frame, text="Quando tudo começou? (AAAA-MM-DD)", font=self.font_label, fg="#555", bg=self.white)
        self.date_label.pack(pady=(0, 5))

        self.start_date_entry = tk.Entry(self.date_input_frame, width=20, font=self.font_label, bd=2, relief="solid", highlightbackground=self.pink_light, highlightthickness=2, justify="center")
        self.start_date_entry.pack(pady=(0, 10), ipady=5, fill="x")

        self.save_button = tk.Button(self.date_input_frame, text="Salvar Data", command=self.save_date, bg=self.pink_dark, fg=self.white, font=self.font_button, relief="flat", padx=15, pady=8, cursor="hand2")
        self.save_button.pack(fill="x")

        # Carrega a data inicial e atualiza a exibição
        self.initial_load()

    def animate_gif(self):
        """Atualiza o quadro do GIF para criar a animação."""
        if self.frames:
            self.cat_label.config(image=self.frames[self.current_frame_index])
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            
            delay = self.gif_img.info['duration'] if hasattr(self, 'gif_img') and 'duration' in self.gif_img.info else 100
            self.animation_id = self.master.after(delay, self.animate_gif)
        
    def initial_load(self):
        """Carrega a data salva e atualiza a exibição ao iniciar."""
        saved_date = load_start_date()
        if saved_date:
            self.start_date_entry.insert(0, saved_date)
            self.update_display()
        else:
            self.days_display.config(text="Defina a data de início!")

    def save_date(self):
        """Salva a data inserida pelo usuário."""
        date_str = self.start_date_entry.get()
        if not date_str:
            show_message("Erro", "Por favor, insira uma data.", 'error')
            return

        # Valida o formato da data
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            show_message("Erro", "Formato de data inválido. Use AAAA-MM-DD.", 'error')
            return

        if save_start_date(date_str):
            self.update_display()
            show_message("Sucesso", "Data salva com sucesso!")

    def update_display(self):
        """Atualiza o contador de dias na interface."""
        date_str = self.start_date_entry.get()
        if date_str:
            days = calculate_days(date_str)
            if days != -1:
                self.days_display.config(text=f"{days} dias")
            else:
                self.days_display.config(text="Erro na data!")
        else:
            self.days_display.config(text="Defina a data de início!")

# --- Execução do Aplicativo ---

if __name__ == "__main__":
    root = tk.Tk()
    app = RelationshipCounterApp(root)
    root.mainloop()