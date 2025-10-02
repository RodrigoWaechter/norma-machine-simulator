# app.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from typing import List
from norma import Registrador, ler_programas, executar_com_logs

class NormaApp(tk.Tk):
    # ============================
    # Inicializa a aplicação e seus componentes
    # ============================
    def __init__(self):
        super().__init__()
        self.title("Simulador de Máquina Norma")
        self.geometry("1200x750") 

        self.registradores_widgets: List[tk.Entry] = []
        self.macros_dir = "macros"
        self.current_file_path = ""

        self.create_widgets()
        self.update_register_entries()
        self.populate_and_load_initial_file()

    # ============================
    # Cria e posiciona todos os elementos visuais da interface
    # ============================
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        controls_frame = ttk.LabelFrame(left_frame, text="Configuração", padding="10")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controls_frame, text="Nº de Registradores:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.num_regs_spinbox = ttk.Spinbox(controls_frame, from_=1, to=26, width=5, command=self.update_register_entries)
        self.num_regs_spinbox.set(3)
        self.num_regs_spinbox.grid(row=0, column=1, sticky="w")
        
        regs_container = ttk.LabelFrame(left_frame, text="Valores Iniciais dos Registradores", padding="10")
        regs_container.pack(fill=tk.X, pady=(0, 10))
        self.canvas = tk.Canvas(regs_container, height=50)
        scrollbar = ttk.Scrollbar(regs_container, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill="x")
        self.canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.canvas.configure(xscrollcommand=scrollbar.set)
        self.regs_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.regs_frame, anchor="nw")
        self.regs_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.code_frame = ttk.LabelFrame(left_frame, text="Editor de Código", padding="10")
        self.code_frame.pack(fill=tk.BOTH, expand=True)
        selector_frame = ttk.Frame(self.code_frame)
        selector_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(selector_frame, text="Arquivo:").pack(side=tk.LEFT, padx=(0, 5))
        self.macro_selector = ttk.Combobox(selector_frame, state="readonly", width=30)
        self.macro_selector.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.macro_selector.bind("<<ComboboxSelected>>", self.on_file_select)
        self.code_text = scrolledtext.ScrolledText(self.code_frame, wrap=tk.WORD, width=40, height=10, font=("Courier New", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        log_frame = ttk.LabelFrame(right_frame, text="Computação Completa", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.log_output = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled", font=("Courier New", 10))
        self.log_output.pack(fill=tk.BOTH, expand=True)
        self.log_output.tag_configure("STATE", foreground="black")
        self.log_output.tag_configure("INFO", foreground="#555555")
        self.log_output.tag_configure("MACRO", foreground="blue", font=("Courier New", 10, "italic"))
        self.log_output.tag_configure("ERROR", foreground="red", font=("Courier New", 10, "bold"))
        final_state_frame = ttk.LabelFrame(right_frame, text="Estado Final dos Registradores", padding="10")
        final_state_frame.pack(fill=tk.X)
        self.final_state_label = ttk.Label(final_state_frame, text="Aguardando execução...", font=("Courier New", 10))
        self.final_state_label.pack()

        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)
        self.execute_button = ttk.Button(action_frame, text="Executar Programa (main.txt)", command=self.run_main_simulation)
        self.execute_button.pack(side=tk.LEFT, padx=5)
        
        self.execute_current_button = ttk.Button(action_frame, text="Executar Arquivo Aberto", command=self.run_current_file_simulation)
        self.execute_current_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(action_frame, text="Limpar", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    # ============================
    # Contém a lógica central para executar a simulação
    # ============================
    def _execute_logic(self, start_file: str):
        self.save_editor_to_file()
        
        self.log_output.config(state="normal")
        self.log_output.delete("1.0", tk.END)
        self.final_state_label.config(text="Executando...")

        if not start_file:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado para executar.")
            return

        regs = []
        try:
            for i, entry in enumerate(self.registradores_widgets):
                nome = chr(ord('a') + i)
                valor = int(entry.get())
                regs.append(Registrador(nome, valor))
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Valores dos registradores devem ser inteiros.")
            return
            
        try:
            programas = ler_programas(self.macros_dir)
            final_regs, log_completo = executar_com_logs(programas, regs, start_file)               
            for linha in log_completo:
                partes = linha.split("|", 1)
                tag = "STATE"
                if len(partes) == 2:
                    tag, texto = partes;
                    if not texto.strip(): continue
                    self.log_output.insert(tk.END, texto + "\n", tag)
                else:
                    self.log_output.insert(tk.END, linha + "\n", tag)

            self.final_state_label.config(text=str(final_regs))
        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro inesperado: {e}")
            self.final_state_label.config(text="Erro durante a execução.")
        finally:
            self.log_output.config(state="disabled")

    # ============================
    # Executa a simulação a partir do arquivo main.txt
    # ============================
    def run_main_simulation(self):
        self._execute_logic("main.txt")

    # ============================
    # Executa a simulação a partir do arquivo aberto no editor
    # ============================
    def run_current_file_simulation(self):
        selected_file = self.macro_selector.get()
        self._execute_logic(selected_file)

    # ============================
    # Carrega a lista de macros e abre o arquivo inicial
    # ============================
    def populate_and_load_initial_file(self):
        if not os.path.exists(self.macros_dir): os.makedirs(self.macros_dir)
        main_path = os.path.join(self.macros_dir, "main.txt")
        if not os.path.exists(main_path):
            with open(main_path, "w", encoding="utf-8") as f:
                f.write("1: ")
        macro_files = [f for f in os.listdir(self.macros_dir) if f.endswith(".txt")]
        self.macro_selector['values'] = sorted(macro_files)
        if "main.txt" in macro_files:
            self.macro_selector.set("main.txt")
            self.load_file_to_editor("main.txt")
        elif macro_files:
            first_file = macro_files[0]
            self.macro_selector.set(first_file)
            self.load_file_to_editor(first_file)

    # ============================
    # Carrega o conteúdo de um arquivo para o editor de texto
    # ============================
    def load_file_to_editor(self, filename):
        self.current_file_path = os.path.join(self.macros_dir, filename)
        self.code_frame.config(text=f"Editor de Código ({filename})")
        try:
            with open(self.current_file_path, 'r', encoding='utf-8') as f: content = f.read()
            self.code_text.delete('1.0', tk.END)
            self.code_text.insert('1.0', content)
        except Exception as e:
            messagebox.showerror("Erro de Leitura", f"Não foi possível ler o arquivo '{filename}':\n{e}")

    # ============================
    # Salva o conteúdo do editor no arquivo atual
    # ============================
    def save_editor_to_file(self):
        if not self.current_file_path: return
        try:
            content = self.code_text.get('1.0', tk.END)
            with open(self.current_file_path, 'w', encoding='utf-8') as f: f.write(content)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo '{self.current_file_path}':\n{e}")

    # ============================
    # Gerencia a troca de arquivos no seletor
    # ============================
    def on_file_select(self, event=None):
        self.save_editor_to_file()
        new_file = self.macro_selector.get()
        self.load_file_to_editor(new_file)

    # ============================
    # Limpa os resultados da tela e reseta os registradores
    # ============================
    def clear_results(self):
        self.log_output.config(state="normal")
        self.log_output.delete("1.0", tk.END)
        self.log_output.config(state="disabled")
        self.final_state_label.config(text="Aguardando execução...")
        for widget in self.registradores_widgets:
            widget.delete(0, tk.END)
            widget.insert(0, "0")
            
    # ============================
    # Atualiza os campos de entrada dos registradores
    # ============================
    def update_register_entries(self):
        for widget in self.regs_frame.winfo_children(): widget.destroy()
        self.registradores_widgets.clear()
        try: num_regs = int(self.num_regs_spinbox.get())
        except ValueError: num_regs = 0
        for i in range(num_regs):
            reg_name = chr(ord('a') + i)
            ttk.Label(self.regs_frame, text=f"{reg_name}:").grid(row=0, column=i*2, padx=(0, 2), pady=5)
            entry = ttk.Entry(self.regs_frame, width=7)
            entry.insert(0, "0")
            entry.grid(row=0, column=i*2 + 1, padx=(0, 15), pady=5)
            self.registradores_widgets.append(entry)

if __name__ == "__main__":
    app = NormaApp()
    app.mainloop()