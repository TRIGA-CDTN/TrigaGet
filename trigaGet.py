#!/bin/python

import datetime
import socket
import threading
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.windows_main()

    def windows_main(self):
        self.title("TrigaGet")
        self.ip = "localhost"
        self.port = 1234
        self.tax_amo = 1000
        self.filtro = False
        self.cabeçalho_simples = """TrigaGet - Um software para salvar os dados do reator Triga IPR-R1 no seu computador.
Clique nessa mensagem para instrições de uso.
"""

        # Configurando o tema escuro
        self.configure(bg="#333333")
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use o tema clam para uma aparência mais uniforme no modo escuro
        self.style.configure(".", background="#333333", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#666666")])

        # 1° grupo (do cima)
        self.groupInstructions = ttk.Frame(self)
        self.groupInstructions.grid(row=0, column=0, columnspan=3, padx=5, pady=0, sticky="ewn")
        self.groupInstructions.rowconfigure(0, weight=1)
        self.groupInstructions.columnconfigure(0, weight=1)
        self.groupInstructions.columnconfigure(1, weight=1)
        
        self.label1_groupInstructions = ttk.Label(self.groupInstructions, text=self.cabeçalho_simples)
        self.label1_groupInstructions.grid(row=0, column=0, sticky="w")
        
        # 2° grupo (do cima)
        self.groupConnections = ttk.Frame(self)
        self.groupConnections.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky="ew")
        self.groupConnections.rowconfigure(0, weight=1)
        self.groupConnections.columnconfigure(0, weight=1)
        self.groupConnections.columnconfigure(1, weight=1)
        
        self.label1_groupConnections = ttk.Label(self.groupConnections, text="[ Configurações de Conexão ]")
        self.label1_groupConnections.grid(row=0, column=0, sticky="w")
        
        self.label1_groupConnections = ttk.Label(self.groupConnections, text="Tax (ms):")
        self.label1_groupConnections.grid(row=1, column=0, sticky="w")
        self.entry1_groupConnections = tk.Entry(self.groupConnections,width=8,background="#333333",foreground="#ffffff")
        self.entry1_groupConnections.insert(0, "1000")
        self.entry1_groupConnections.grid(row=2, column=0, sticky="w")
        
        self.label2_groupConnections = ttk.Label(self.groupConnections, text="Port (CSV):")
        self.label2_groupConnections.grid(row=1, column=1, sticky="w")
        self.entry2_groupConnections = tk.Entry(self.groupConnections,width=8,background="#333333",foreground="#ffffff")
        self.entry2_groupConnections.insert(0, "1234")
        self.entry2_groupConnections.grid(row=2, column=1, sticky="w")
        
        self.label3_groupConnections = ttk.Label(self.groupConnections, text="Ip:")
        self.label3_groupConnections.grid(row=1, column=2, sticky="w")
        self.entry3_groupConnections = tk.Entry(self.groupConnections,width=15,background="#333333",foreground="#ffffff")
        self.entry3_groupConnections.insert(0, "127.0.0.1")
        self.entry3_groupConnections.grid(row=2, column=2, sticky="w")
        
        # 3° grupo (do meio)
        
        self.groupData = ttk.Frame(self)
        self.groupData.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky="ew")
        self.groupData.rowconfigure(0, weight=1)
        self.groupData.columnconfigure(0, weight=1)
        self.groupData.columnconfigure(1, weight=1)
        
        self.title__groupData = ttk.Label(self.groupData, text="[ Dados ]")
        self.title__groupData.grid(row=0, column=0, sticky="w")
        self.button_groupData = ttk.Button(self.groupData, text="Obter filtro CSV",command=self.button_click_obter_filtro)
        self.button_groupData.grid(row=2, column=0, sticky="w")
        
        # 4° grupo (abaixo)
        self.groupFile = ttk.Frame(self)
        self.groupFile.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky="ews")
        self.groupFile.rowconfigure(0, weight=1)
        self.groupFile.columnconfigure(0, weight=1)
        self.groupFile.columnconfigure(1, weight=1)
        
        self.title__groupFile = ttk.Label(self.groupFile, text="[ Arquivo ]")
        self.title__groupFile.grid(row=0, column=0, sticky="w")
        self.label1_groupFile = ttk.Label(self.groupFile, text="Nome do arquivo:")
        self.label1_groupFile.grid(row=1, column=0, sticky="w")
        self.entry1_groupFile = tk.Entry(self.groupFile,width=40,background="#333333",foreground="#ffffff")
        self.entry1_groupFile.insert(0, self.generate_filename())
        self.entry1_groupFile.grid(row=2, column=0, sticky="we")
        self.button_groupFile = ttk.Button(self.groupFile, text="Get", command=self.button_get_click)
        self.button_groupFile.grid(row=2, column=2, sticky="w")

        # Configurando o redimensionamento
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=33)
        self.rowconfigure(2, weight=33)
        self.rowconfigure(3, weight=33)
        self.columnconfigure((0, 1, 2, 3), weight=1)
        
    def update_label(self, label, value):
        label.config(text="{:.3f}".format(float(value)))
        
    def generate_filename(self):
        now = datetime.datetime.now()
        filename = f"resultados_{now.strftime('%Y-%m-%d-%H-%M-%S')}"
        return filename
    
    def change_instructions(self):
        self.label1_group0.config(text=self.cabeçalho_instrucoes)
        
    def button_get_click(self):
        self.label1_groupFile.config(text="Gravando!")
        self.entry1_groupFile.config(state="disabled")
        self.button_groupFile.config(text="Parar", command=self.button_parar_click)

        try:
            self.tax_amo = int(self.entry1_groupConnections.get())
            if self.tax_amo < 20:
                self.tax_amo = 20
            elif self.tax_amo > 5000:
                self.tax_amo = 5000
        except ValueError:
            self.tax_amo = 1000
            print("Erro entry")
        
        self.get = True
        # Iniciar a thread para recepção de dados
        #self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
        #self.receive_thread.start()
        
    def button_parar_click(self):
        self.label1_groupFile.config(text="Nome do novo arquivo:")
        self.entry1_groupFile.config(state="normal")
        self.entry1_groupFile.delete(0,100)
        self.entry1_groupFile.insert(0, self.generate_filename())
        self.button_groupFile.config(text="Get",command=self.button_get_click)
        # Encerrar a conexão
        self.get = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.entry3_groupConnections.get(), int(self.entry2_groupConnections.get()) ))
        self.sock.sendall(str(self.tax_amo).encode())
        
    def disconnect(self):
        self.sock.close()

    def get_line(self):
        datas = b""  # Use bytes para acumular os dados
        while True:
            data = self.sock.recv(1)  # Recebe 1 byte de cada vez
            if data == b'\n':  # Verifica se o byte recebido é uma nova linha
                break
            datas += data
        return datas.decode('utf-8')  # Converte os bytes acumulados em string no final

    def button_click_obter_filtro(self):
        self.filtro=True
        self.connect()
        header = self.get_line()
        self.disconnect()
        
        header = header.split(';')
        header =               [item for item in header if item]
        self.header_spu_cha  = [item for item in header if item.startswith("SPU_CHA_")]
        self.header_spu_chb  = [item for item in header if item.startswith("SPU_CHB_")]
        self.header_plc_orig = [item for item in header if item.startswith("PLC_ORIG_")]
        self.header_plc_conv = [item for item in header if item.startswith("PLC_CONV_")]
        self.header_restante = [item for item in header if not (item.startswith("SPU_CHA_") 
                                                            or  item.startswith("SPU_CHB_") 
                                                            or  item.startswith("PLC_ORIG_") 
                                                            or  item.startswith("PLC_CONV_"))]
        
        self.create_checkboxes_window()
        self.button_groupData.config(text="Escolher filtro",command=self.show_checkboxes_window())
        

    def populate_checkboxes(self,header,idy):
        self.var=[]
        self.checkbox=[]
        
        # Inicialize as listas aninhadas, se necessário
        while len(self.var) <= idy:
            self.var.append([])
        while len(self.checkbox) <= idy:
            self.checkbox.append([])

        for idx, item in enumerate(header):
            # Adicione os elementos às listas aninhadas na posição específica
            if len(self.var[idy]) <= idx:
                self.var[idy].append(tk.BooleanVar())
            else:
                self.var[idy][idx] = tk.BooleanVar()

            if len(self.checkbox[idy]) <= idx:
                self.checkbox[idy].append(ttk.Checkbutton(self.checkbox_frame, text=item, variable=self.var[idy][idx]))
            else:
                self.checkbox[idy][idx] = ttk.Checkbutton(self.checkbox_frame, text=item, variable=self.var[idy][idx])

            self.checkbox[idy][idx].grid(row=idx+1, column=idy, sticky="w")

    def show_checkboxes_window(self):
        print("teste")
        
    def create_checkboxes_window(self):
        # Cria uma nova janela
        self.checkbox_window = tk.Toplevel(self)
        self.checkbox_window.title("Checkboxes")      

        # Cria um canvas e uma scrollbar na nova janela
        canvas = tk.Canvas(self.checkbox_window)
        scrollbar = ttk.Scrollbar(self.checkbox_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.checkbox_frame = scrollable_frame

        # Chame a função para popular as checkboxes aqui
        self.populate_checkboxes(self.header_spu_cha, 0)
        self.populate_checkboxes(self.header_spu_chb, 1)
        self.populate_checkboxes(self.header_plc_orig,2)
        self.populate_checkboxes(self.header_plc_conv,3)
        self.populate_checkboxes(self.header_restante,4)

if __name__ == "__main__":
    app = App()
    app.mainloop()

#"SPU_CHA_STATE;SPU_CHA_TIME_Y;SPU_CHA_TIME_Mo;SPU_CHA_TIME_D;SPU_CHA_TIME_H;SPU_CHA_TIME_Mi;SPU_CHA_TIME_S;SPU_CHA_TIME_MS;SPU_CHA_N_DATA_FP;SPU_CHA_T_DATA_FP;SPU_CHA_F1_DATA_FP;SPU_CHA_F2_DATA_FP;SPU_CHA_F3_DATA_FP;SPU_CHA_EMR_N_THRESHOLD;SPU_CHA_WRN_N_THRESHOLD;SPU_CHA_EMR_T_THRESHOLD;SPU_CHA_WRN_T_THRESHOLD;SPU_CHA_EMR_N;SPU_CHA_WRN_N;SPU_CHA_EMR_T;SPU_CHA_WRN_T;SPU_CHA_R1;SPU_CHA_R2;SPU_CHA_R3;SPU_CHA_RDY;SPU_CHA_TEST;SPU_CHA_XXXX;SPU_CHB_STATE;SPU_CHB_TIME_Y;SPU_CHB_TIME_Mo;SPU_CHB_TIME_D;SPU_CHB_TIME_H;SPU_CHB_TIME_Mi;SPU_CHB_TIME_S;SPU_CHB_TIME_MS;SPU_CHB_N_DATA_FP;SPU_CHB_T_DATA_FP;SPU_CHB_F1_DATA_FP;SPU_CHB_F2_DATA_FP;SPU_CHB_F3_DATA_FP;SPU_CHB_EMR_N_THRESHOLD;SPU_CHB_WRN_N_THRESHOLD;SPU_CHB_EMR_T_THRESHOLD;SPU_CHB_WRN_T_THRESHOLD;SPU_CHB_EMR_N;SPU_CHB_WRN_N;SPU_CHB_EMR_T;SPU_CHB_WRN_T;SPU_CHB_R1;SPU_CHB_R2;SPU_CHB_R3;SPU_CHB_RDY;SPU_CHB_TEST;SPU_CHB_XXXX;PLC_ORIG_STATE;PLC_ORIG_TIME;PLC_ORIG_TIME_Mo;PLC_ORIG_TIME_D;PLC_ORIG_TIME_H;PLC_ORIG_TIME_Mi;PLC_ORIG_TIME_S;PLC_ORIG_TIME_MS;PLC_ORIG_BarraReg;PLC_ORIG_BarraCon;PLC_ORIG_BarraSeg;PLC_ORIG_CLogALog;PLC_ORIG_CLogALin;PLC_ORIG_CLogAPer;PLC_ORIG_CParALin;PLC_ORIG_CParALog;PLC_ORIG_CParAPer;PLC_ORIG_CLogARea;PLC_ORIG_CLin;PLC_ORIG_CPer;PLC_ORIG_SRadAre;PLC_ORIG_SRadEntPri;PLC_ORIG_SRadPoc;PLC_ORIG_SRadRes;PLC_ORIG_SRadSaiSec;PLC_ORIG_SRadAer;PLC_ORIG_SVasPri;PLC_ORIG_SPt100Poco;PLC_ORIG_SPt100EntPri;PLC_ORIG_SPt100SaiPri;PLC_ORIG_SPt100EntSec;PLC_ORIG_SPt100SaiSec;PLC_ORIG_STpPoc1;PLC_ORIG_STpPoc2;PLC_ORIG_STpLen;PLC_ORIG_SConPoc;PLC_ORIG_SConSaiPri;PLC_CONV_STATE;PLC_CONV_TIME;PLC_CONV_TIME_Mo;PLC_CONV_TIME_D;PLC_CONV_TIME_H;PLC_CONV_TIME_Mi;PLC_CONV_TIME_S;PLC_CONV_TIME_MS;PLC_CONV_BarraReg;PLC_CONV_BarraCon;PLC_CONV_BarraSeg;PLC_CONV_CLogALog;PLC_CONV_CLogALin;PLC_CONV_CLogAPer;PLC_CONV_CParALin;PLC_CONV_CParALog;PLC_CONV_CParAPer;PLC_CONV_CLogARea;PLC_CONV_CLin;PLC_CONV_CPer;PLC_CONV_SRadAre;PLC_CONV_SRadEntPri;PLC_CONV_SRadPoc;PLC_CONV_SRadRes;PLC_CONV_SRadSaiSec;PLC_CONV_SRadAer;PLC_CONV_SVasPri;PLC_CONV_SPt100Poco;PLC_CONV_SPt100EntPri;PLC_CONV_SPt100SaiPri;PLC_CONV_SPt100EntSec;PLC_CONV_SPt100SaiSec;PLC_CONV_STpPoc1;PLC_CONV_STpPoc2;PLC_CONV_STpLen;PLC_CONV_SConPoc;PLC_CONV_SConSaiPri;\n";
