import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TrigaCalib - Aquisição de dados")
        
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
        
        # 2° grupo (do meio)
        self.group2 = ttk.Frame(self)
        self.group2.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky="ew")
        self.group2.rowconfigure(0, weight=1)
        self.group2.columnconfigure(0, weight=1)
        self.group2.columnconfigure(1, weight=1)
        
        self.label_group2 = ttk.Label(self.group2, text="Coloque o reator crítico e clique em gravar.\nMova 1 barra em caso calibração ou as deixem paradas para tirar valores médios.")
        self.label_group2.grid(row=0, column=0, sticky="w")
        
        self.button_group2 = ttk.Button(self.group2, text="Gravar", command=self.button_click)
        self.button_group2.grid(row=0, column=1, sticky="e")
        
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
        
    def button_click(self):
        self.label_group2.config(text="Gravando!\nClique em parar quando a quantidade de dados for suficiente.")
        
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
    app = App()
    app.mainloop()
