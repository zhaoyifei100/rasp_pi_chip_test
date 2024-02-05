import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#aves to py lib
from aves_to_py import *
#i2c class
from i2c_raspberry import i2c_raspberry
from i2c_raspberry import i2c_probe
from i2c_raspberry import TextRedirector

class Page1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.i2c_bridge=None
        self.disc_use={}

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.content_frame, text="Select AVES Script...")
        self.button = tk.Button(self.content_frame, text="AVES", command=self.on_button_click)
        self.scrollbar = None
        self.func_listbox = None
        self.label.pack()
        self.button.pack()

        self.build_listbox()

        #status label
        self.status_label = tk.Label(self.content_frame, text="STATUS: idle", bg="Yellow")
        self.status_label.pack()

    def reset_status_label(self,event):
        self.status_label.config(text=f"STATUS: idle")
        self.status_label.config(bg="Yellow")
        self.content_frame.update_idletasks()

    def on_list_double_click(self,event):
        selection = self.function_listbox.curselection()
        if selection:
            function_name = self.function_listbox.get(selection[0])
            #label set to busy
            self.status_label.config(text=f"   ---busy---   ")
            self.content_frame.update_idletasks()
            # run_function(function_name)
            self.i2c_bridge.write_buf(function_name)
            i2c_status = self.i2c_bridge.write_i2c()
            #status refresh
            if (i2c_status==0):
                self.status_label.config(text=f"STATUS: i2c error")
                self.status_label.config(bg="LightCoral")
            elif (i2c_status==1):
                self.status_label.config(text=f"STATUS: \"{function_name}\" write")
                self.status_label.config(bg="DarkSeaGreen1")
            elif (i2c_status==2):
                self.status_label.config(text=f"STATUS: idle")
                self.status_label.config(bg="Yellow")
            self.content_frame.update_idletasks()
            return

    def build_listbox(self):
        self.scrollbar = tk.Scrollbar(self.content_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.function_listbox = tk.Listbox(self.content_frame, height=30, width=100,\
                                      yscrollcommand=self.scrollbar.set)
        self.function_listbox.pack()
        self.scrollbar.config(command=self.function_listbox.yview)

        self.function_listbox.bind("<Double-Button-1>", self.on_list_double_click)
        self.function_listbox.bind("<Button-1>", self.reset_status_label)
        return

    def refresh_listbox(self):
        func_list=self.disc_use.keys()
        #clear old
        self.function_listbox.delete(0, tk.END)
        #insert
        for name in func_list:
            self.function_listbox.insert(tk.END, name)
        return

    def on_button_click(self):
        #get aves script
        file_path = filedialog.askopenfilename()

        #error protect
        if (file_path==''):
            return

        #get disc from script
        self.disc_use = aves_to_pydisc(file_path)
        #build bridge class
        self.i2c_bridge = i2c_raspberry(disc_use=self.disc_use)
        self.refresh_listbox()

        self.label["text"] = file_path

class Page2(tk.Frame):
    ### Probe Use ###
    def __init__(self, parent):
        super().__init__(parent)
        self.i2c_probe_use = i2c_probe()
        self.label = tk.Label(self, text="This is content for Window 2.")
        # 创建一个按钮，点击按钮时添加一个新的 Frame 容器
        self.button_probe = tk.Button(self, text="Add Probe", command=self.add_frame)
        self.button_probe.pack()
        #use canvas->main_frame->probe_frame hier for scroll probe
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.scrollbar.config(command=self.canvas.yview)

    def add_frame(self):
        def read_func():
            addr = txt_box1.get()
            val = txt_box2.get()
            try:
                if addr != '':
                    addr_s = str(addr).zfill(4)
                    addr1_dec = int(addr_s[:2], 16)
                    addr2_dec = int(addr_s[2:4], 16)
                else:
                    addr_s = 0
                    addr1_dec = 0
                    addr2_dec = 0
                if val != '':
                    val_dec = int(str(val), 16)
                else:
                    val_dec = 0
            except:
                txt_box3.delete('0', tk.END)
                txt_box3.insert(0, 'input error!')
                print("input error!")
                return None
            try:
                read_results = hex(self.i2c_probe_use.readReg(addr1_dec, addr2_dec))
                txt_box3.delete('0', tk.END)
                txt_box3.insert(0, read_results)
                #print("选择了rb")
            except:
                txt_box3.delete('0', tk.END)
                txt_box3.insert(0, 'i2c error!')
                print("i2c error!")
                #print(self.i2c_probe_use.readReg(addr1_dec, addr2_dec))

        def write_func():
            addr = txt_box1.get()
            val = txt_box2.get()
            try:
                if addr != '':
                    addr_s = str(addr).zfill(4)
                    addr1_dec = int(addr_s[:2], 16)
                    addr2_dec = int(addr_s[2:4], 16)
                else:
                    addr_s = 0
                    addr1_dec = 0
                    addr2_dec = 0
                if val != '':
                    val_dec = int(str(val), 16)
                else:
                    val_dec = 0
            except:
                txt_box3.delete('0', tk.END)
                txt_box3.insert(0, 'input error!')
                print("input error!")
                return None
            try:
                self.i2c_probe_use.writeReg(addr1_dec, addr2_dec, val_dec)
                #print("选择了wr")
            except:
                txt_box3.delete('0', tk.END)
                txt_box3.insert(0, 'i2c error!')
                print("i2c error!")

        def del_pack():
            probe_frame.pack_forget()
        # 创建一个新的 Frame 容器
        # 创建一个 Frame 容器
        #probe_frame = tk.Frame(self)
        probe_frame = tk.Frame(self.main_frame)
        ##### ADD Probe  ####
        rb1 = tk.Button(probe_frame, text="read", command=read_func)
        rb2 = tk.Button(probe_frame, text="write", command=write_func)

        # add del button 2024.02.05
        rb3 = tk.Button(probe_frame, text="X", command=del_pack)
        #####end add######

        label1 = tk.Label(probe_frame, text="input address:")
        txt_box1 = tk.Entry(probe_frame)

        label2 = tk.Label(probe_frame, text="input value:")
        txt_box2 = tk.Entry(probe_frame)

        label3 = tk.Label(probe_frame, text="result:")
        txt_box3 = tk.Entry(probe_frame)
        txt_box3.insert(0, '输出结果')


        ###end probe###
        ## pack * ##

        # add del button 2024.02.05
        rb3.pack(side="left", anchor="w")
        #####end add######

        label1.pack(side="left", anchor="w")
        txt_box1.pack(side="left", anchor="w")

        label2.pack(side="left", anchor="w")
        txt_box2.pack(side="left", anchor="w")

        rb1.pack(side="left", anchor="w")
        rb2.pack(side="left", anchor="w")

        label3.pack(side="left", anchor="w")
        txt_box3.pack(side="left", anchor="w")

        probe_frame.pack()
        ###end pack ###

        #add refresh
        self.main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    ## End Probe use ##



class Page_log(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(self.content_frame)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        sys.stdout = TextRedirector(self.text)

class i2c_pi_gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("I2C Raspberry Pi GUI")


        self.notebook = ttk.Notebook(self.window)

        self.page1 = Page1(self.notebook)
        self.page2 = Page2(self.notebook)
        self.page3 = Page_log(self.notebook)

        self.notebook.add(self.page1, text="Script")
        self.notebook.add(self.page2, text="Probe")
        self.notebook.add(self.page3, text="Log")

        self.notebook.pack()



    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = i2c_pi_gui()
    gui.run()