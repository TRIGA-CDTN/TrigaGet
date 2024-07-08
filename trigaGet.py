#!/bin/python

import socket
import threading
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    
    
    def __init__(self):
        cabeçalho_simples = """TrigaGet - Um software para salvar os dados do reator Triga IPR-R1 no seu computador.
Clique nessa mensagem para instrições de uso.
"""
        super().__init__()
        self.title("TrigaGet")
        self.ip = "localhost"
        self.port = 12345
        self.tax_amo = 20
        
        # Configurando o tema escuro
        self.configure(bg="#333333")
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use o tema clam para uma aparência mais uniforme no modo escuro
        self.style.configure(".", background="#333333", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#666666")])

        # 0° grupo (do cima)
        self.groupInstructions = ttk.Frame(self)
        self.groupInstructions.grid(row=0, column=0, columnspan=3, padx=5, pady=0, sticky="ewn")
        self.groupInstructions.rowconfigure(0, weight=1)
        self.groupInstructions.columnconfigure(0, weight=1)
        self.groupInstructions.columnconfigure(1, weight=1)
        
        self.label1_group0 = ttk.Label(self.groupInstructions, text=cabeçalho_simples)
        self.label1_group0.grid(row=0, column=0, sticky="w")
        
        # 1° grupo (do cima)
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
        self.entry1_groupConnections.insert(0, "20")
        self.entry1_groupConnections.grid(row=2, column=0, sticky="w")
        
        self.label2_groupConnections = ttk.Label(self.groupConnections, text="Port:")
        self.label2_groupConnections.grid(row=1, column=1, sticky="w")
        self.entry2_groupConnections = tk.Entry(self.groupConnections,width=8,background="#333333",foreground="#ffffff")
        self.entry2_groupConnections.insert(0, "123")
        self.entry2_groupConnections.grid(row=2, column=1, sticky="w")
        
        self.label3_groupConnections = ttk.Label(self.groupConnections, text="Ip:")
        self.label3_groupConnections.grid(row=1, column=2, sticky="w")
        self.entry3_groupConnections = tk.Entry(self.groupConnections,width=15,background="#333333",foreground="#ffffff")
        self.entry3_groupConnections.insert(0, "127.0.0.1")
        self.entry3_groupConnections.grid(row=2, column=2, sticky="w")
        
        # 2° grupo (do meio)
        
        self.groupData = ttk.Frame(self)
        self.groupData.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky="ew")
        self.groupData.rowconfigure(0, weight=1)
        self.groupData.columnconfigure(0, weight=1)
        self.groupData.columnconfigure(1, weight=1)
        
        self.title__groupData = ttk.Label(self.groupData, text="[ Dados ]")
        self.title__groupData.grid(row=0, column=0, sticky="w")
        self.button_groupData = ttk.Button(self.groupData, text="Obter cabeçalho")
        self.button_groupData.grid(row=2, column=0, sticky="w")
        
        # 3° grupo (abaixo)
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
        self.entry1_groupFile.insert(0, "resultados_")
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
        
    def button_get_click(self):
        self.label1_groupFile.config(text="Gravando!\nAo clicar em parar será salvo o arquivo.")
        self.entry1_groupFile.config(state="disabled")
        self.button_groupFile.config(text="Parar", command=self.button_parar_click)

        try:
            self.tax_amo = int(self.entry_groupData.get())
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
        self.label_groupData.config(text="Insita a taxa de amostragem em milissegundos.\nClique em Get para iniciar a coleta de dados.")
        self.entry_groupData.config(state="normal")
        self.button_groupData.config(text="Get",command=self.button_get_click)
        # Encerrar a conexão
        self.get = False

if __name__ == "__main__":
    app = App()
    app.mainloop()

#"SPU_CHA_STATE;SPU_CHA_TIME_Y;SPU_CHA_TIME_Mo;SPU_CHA_TIME_D;SPU_CHA_TIME_H;SPU_CHA_TIME_Mi;SPU_CHA_TIME_S;SPU_CHA_TIME_MS;SPU_CHA_N_DATA_FP;SPU_CHA_T_DATA_FP;SPU_CHA_F1_DATA_FP;SPU_CHA_F2_DATA_FP;SPU_CHA_F3_DATA_FP;SPU_CHA_EMR_N_THRESHOLD;SPU_CHA_WRN_N_THRESHOLD;SPU_CHA_EMR_T_THRESHOLD;SPU_CHA_WRN_T_THRESHOLD;SPU_CHA_EMR_N;SPU_CHA_WRN_N;SPU_CHA_EMR_T;SPU_CHA_WRN_T;SPU_CHA_R1;SPU_CHA_R2;SPU_CHA_R3;SPU_CHA_RDY;SPU_CHA_TEST;SPU_CHA_XXXX;SPU_CHB_STATE;SPU_CHB_TIME_Y;SPU_CHB_TIME_Mo;SPU_CHB_TIME_D;SPU_CHB_TIME_H;SPU_CHB_TIME_Mi;SPU_CHB_TIME_S;SPU_CHB_TIME_MS;SPU_CHB_N_DATA_FP;SPU_CHB_T_DATA_FP;SPU_CHB_F1_DATA_FP;SPU_CHB_F2_DATA_FP;SPU_CHB_F3_DATA_FP;SPU_CHB_EMR_N_THRESHOLD;SPU_CHB_WRN_N_THRESHOLD;SPU_CHB_EMR_T_THRESHOLD;SPU_CHB_WRN_T_THRESHOLD;SPU_CHB_EMR_N;SPU_CHB_WRN_N;SPU_CHB_EMR_T;SPU_CHB_WRN_T;SPU_CHB_R1;SPU_CHB_R2;SPU_CHB_R3;SPU_CHB_RDY;SPU_CHB_TEST;SPU_CHB_XXXX;PLC_ORIG_STATE;PLC_ORIG_TIME;PLC_ORIG_TIME_Mo;PLC_ORIG_TIME_D;PLC_ORIG_TIME_H;PLC_ORIG_TIME_Mi;PLC_ORIG_TIME_S;PLC_ORIG_TIME_MS;PLC_ORIG_BarraReg;PLC_ORIG_BarraCon;PLC_ORIG_BarraSeg;PLC_ORIG_CLogALog;PLC_ORIG_CLogALin;PLC_ORIG_CLogAPer;PLC_ORIG_CParALin;PLC_ORIG_CParALog;PLC_ORIG_CParAPer;PLC_ORIG_CLogARea;PLC_ORIG_CLin;PLC_ORIG_CPer;PLC_ORIG_SRadAre;PLC_ORIG_SRadEntPri;PLC_ORIG_SRadPoc;PLC_ORIG_SRadRes;PLC_ORIG_SRadSaiSec;PLC_ORIG_SRadAer;PLC_ORIG_SVasPri;PLC_ORIG_SPt100Poco;PLC_ORIG_SPt100EntPri;PLC_ORIG_SPt100SaiPri;PLC_ORIG_SPt100EntSec;PLC_ORIG_SPt100SaiSec;PLC_ORIG_STpPoc1;PLC_ORIG_STpPoc2;PLC_ORIG_STpLen;PLC_ORIG_SConPoc;PLC_ORIG_SConSaiPri;PLC_CONV_STATE;PLC_CONV_TIME;PLC_CONV_TIME_Mo;PLC_CONV_TIME_D;PLC_CONV_TIME_H;PLC_CONV_TIME_Mi;PLC_CONV_TIME_S;PLC_CONV_TIME_MS;PLC_CONV_BarraReg;PLC_CONV_BarraCon;PLC_CONV_BarraSeg;PLC_CONV_CLogALog;PLC_CONV_CLogALin;PLC_CONV_CLogAPer;PLC_CONV_CParALin;PLC_CONV_CParALog;PLC_CONV_CParAPer;PLC_CONV_CLogARea;PLC_CONV_CLin;PLC_CONV_CPer;PLC_CONV_SRadAre;PLC_CONV_SRadEntPri;PLC_CONV_SRadPoc;PLC_CONV_SRadRes;PLC_CONV_SRadSaiSec;PLC_CONV_SRadAer;PLC_CONV_SVasPri;PLC_CONV_SPt100Poco;PLC_CONV_SPt100EntPri;PLC_CONV_SPt100SaiPri;PLC_CONV_SPt100EntSec;PLC_CONV_SPt100SaiSec;PLC_CONV_STpPoc1;PLC_CONV_STpPoc2;PLC_CONV_STpLen;PLC_CONV_SConPoc;PLC_CONV_SConSaiPri;\n";
