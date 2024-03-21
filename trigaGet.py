#!/bin/python

import sys
import socket
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(tk.Tk):
    def __init__(self, ip):
        super().__init__()
        self.title("TrigaGet")
        self.ip = ip
        
        # Configurando o tema escuro
        self.configure(bg="#333333")
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use o tema clam para uma aparência mais uniforme no modo escuro
        self.style.configure(".", background="#333333", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#666666")])
        
        # 1° grupo (superior)
        self.group1 = ttk.Frame(self)
        self.group1.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.group1.rowconfigure(0, weight=1)  # Redimensionamento da linha 0
        self.group1.columnconfigure((0, 1, 2), weight=1)  # Redimensionamento das colunas
        
        titles = ["Barra de Segurança", "Barra de Controle", "Barra de Regulação"]
        for i, title in enumerate(titles):
            #Criação dos Subgrupos
            subgroup                = ttk.Frame(self.group1) #Este subgrupo
            
            label_top__SubSubGroup  = ttk.Frame(subgroup)
            label_down_SubSubGroup  = ttk.Frame(subgroup)
            slider_____SubSubGroup  = ttk.Frame(subgroup)
            
            slider_SubSubSubGroup1 = ttk.Frame(slider_____SubSubGroup)
            slider_SubSubSubGroup2 = ttk.Frame(slider_____SubSubGroup)
            slider_SubSubSubGroup3 = ttk.Frame(slider_____SubSubGroup)
            

            
            #Definição da Grade
            
            subgroup              .grid(row=0, column=i, padx=0, pady=0, sticky="nsew", rowspan=3)
            label_top__SubSubGroup.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            label_down_SubSubGroup.grid(row=2, column=0, padx=0, pady=0, sticky="nsew", columnspan=3)
            slider_____SubSubGroup.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
            slider_SubSubSubGroup1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            slider_SubSubSubGroup2.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
            slider_SubSubSubGroup3.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
            
            
            # Redimensionamento das linhas
            #subgroup              .rowconfigure((0, 1, 2), weight=1) 
            subgroup              .rowconfigure(0, weight=1) 
            subgroup              .rowconfigure(1, weight=98) 
            subgroup              .rowconfigure(2, weight=1) 
            
            
            
            label_top__SubSubGroup.rowconfigure(0, weight=1)
            label_down_SubSubGroup.rowconfigure(0, weight=1)
            slider_____SubSubGroup.rowconfigure(0, weight=1)
            slider_SubSubSubGroup1.rowconfigure(0, weight=1)
            slider_SubSubSubGroup2.rowconfigure(0, weight=1)
            slider_SubSubSubGroup3.rowconfigure(0, weight=1)
            
            
            # Redimensionamento da coluna
            subgroup              .columnconfigure(0, weight=1)
            label_top__SubSubGroup.columnconfigure(0, weight=1)
            label_down_SubSubGroup.columnconfigure(0, weight=1)
            #slider_____SubSubGroup.columnconfigure((0, 1, 2), weight=1)
            slider_____SubSubGroup.columnconfigure(0, weight=45)
            slider_____SubSubGroup.columnconfigure(1, weight=10)
            slider_____SubSubGroup.columnconfigure(2, weight=45)
            slider_SubSubSubGroup1.columnconfigure(0, weight=1)
            slider_SubSubSubGroup2.columnconfigure(0, weight=1)
            slider_SubSubSubGroup3.columnconfigure(0, weight=1)
            
            
            #Criação dos elementos dentro dos subgrupos
            label_top = ttk.Label(label_top__SubSubGroup, text=title)
            label_top.grid(row=0, column=0)#, sticky="ew")
            
            label_bottom = ttk.Label(label_down_SubSubGroup, text="0.000")
            label_bottom.grid(row=0, column=0)#, sticky="we")
            
            slider = ttk.Scale(slider_SubSubSubGroup2, from_=1000, to=0, orient="vertical", command=lambda value, label=label_bottom: self.update_label(label, value))
            slider.grid(row=0, column=0, sticky="ns")
            slider.config(state="disabled")

        
        # 2° grupo (do meio)
        self.group2 = ttk.Frame(self)
        self.group2.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky="ew")
        self.group2.rowconfigure(0, weight=1)
        self.group2.columnconfigure(0, weight=1)
        self.group2.columnconfigure(1, weight=1)
        
        self.label_group2 = ttk.Label(self.group2, text="Insira a taxa de amostragem em milissegundos.\nClique em Get para iniciar a coleta de dados.")
        self.label_group2.grid(row=0, column=0, sticky="w")
        
        self.entry_group2 = tk.Entry(self.group2,width=5,background="#333333",foreground="#ffffff")
        self.entry_group2.insert(0, "20")
        self.entry_group2.grid(row=0, column=1, sticky="e")
        
        self.button_group2 = ttk.Button(self.group2, text="Get", command=self.button_get_click)
        self.button_group2.grid(row=0, column=2, sticky="e")
        
        # 3° grupo (inferior)
        self.group3 = ttk.Frame(self)
        self.group3.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky="nsew")
        self.group3.rowconfigure(0, weight=1)
        self.group3.columnconfigure(0, weight=1)
        
        self.figure, self.ax = plt.subplots(facecolor="#333333")
        self.ax.tick_params(colors="#ffffff")
        self.ax.spines['bottom'].set_color('#ffffff')
        self.ax.spines['top'].set_color('#ffffff')
        self.ax.spines['left'].set_color('#ffffff')
        self.ax.spines['right'].set_color('#ffffff')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.group3)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        self.plot_graph()

        # Configurando o redimensionamento
        self.rowconfigure(0, weight=45)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=45)
        self.columnconfigure((0, 1, 2), weight=1)
        
    def update_label(self, label, value):
        label.config(text="{:.3f}".format(float(value)))
        
    def button_get_click(self):
        self.label_group2.config(text="Gravando!\nAo clicar em parar será oferecido um local para salvar o arquivo JSON.")
        self.entry_group2.config(state="disabled")
        self.button_group2.config(text="Parar", command=self.button_parar_click)

        try:
            self.tax_amo = int(self.entry_group2.get())
            if self.tax_amo < 20:
                self.tax_amo = 20
            elif self.tax_amo > 5000:
                self.tax_amo = 5000
        except ValueError:
            self.tax_amo = 20
            print("Erro entry")
        
        self.get = True
        # Iniciar a thread para recepção de dados
        self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.receive_thread.start()

    def receive_data(self):
        try:
            with open('dados.txt', 'w') as file:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("localhost", 12345))
                    sock.sendall(str(self.tax_amo).encode())
                    while self.get:
                        data = sock.recv(1024)
                        if not data:
                            break
                        file.write(data.decode())
                    sock.close()

        except Exception as e:
            print("Erro ao receber dados:", e)

        
    def button_parar_click(self):
        self.label_group2.config(text="Insita a taxa de amostragem em milissegundos.\nClique em Get para iniciar a coleta de dados.")
        self.entry_group2.config(state="normal")
        self.button_group2.config(text="Get",command=self.button_get_click)
        # Encerrar a conexão
        self.get = False
        
        
    def plot_graph(self):
        t_data = [1, 2, 3, 4, 5]
        p_data = [10, 20, 30, 40, 50]
        self.ax.plot(t_data, p_data, color="#ffffff")
        self.ax.set_facecolor("#333333")
        self.ax.set_xlabel("Tempo", color="#ffffff")
        self.ax.set_ylabel("Potência", color="#ffffff")
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    ip = "localhost"#"192.168.1.100"
    tax_amo = 20
    
    if len(sys.argv) > 3:
        print("Muitos argumentos! Por favor, informe um IP e uma taxa de amostragem em milissegundos como no exemplo abaixo:")
        print("")
        print("    ./trigaGet.py <ip> <tax_amo>")
        print("")
        print("Ou apenas o IP para usar a taxa de amostragem padrão (" + str(tax_amo) + "ms);")
        print("Ou sem parâmetros para IP padrão (" + ip + ") e taxa de amostragem padão (" + str(tax_amo) + ") :")
        sys.exit(1)
        
    if len(sys.argv) == 3:
        try:
            tax_amo = int(sys.argv[2])
            if tax_amo < 20:
                tax_amo = 20
            elif tax_amo > 5000:
                tax_amo = 5000
        except ValueError:
            print("Por favor, insira um número válido para taxa de amostragem.\n")
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
            
    app = App(tax_amo)
    app.mainloop()
