import os
import time
import subprocess
import tkinter as tk
from aves_to_py import *

class i2c_probe:
    def __init__(
        self,
        i2c_port=1,
    ):
        self.i2c_port = i2c_port
        # add chip addr 2024.02.04
        self.chip_addr = 0x58

    #####   copy write/read reg   #####
    def run_linux_old(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
            return output.strip()
        except subprocess.CalledProcessError as error_run:
            error_message = f"Command '{cmd}' returned non-zero exit status {error_run.returncode}:\n{error_run.output}"
            print(error_message)
            return "error"

    def writeReg(self, addr1, addr2, value):
        # address1->first 8bit address
        # address2->second 8bit address
        # value->value write to addr
        write_cmd = f"/usr/sbin/i2ctransfer -f -y {str(self.i2c_port)} " \
                    f"w3@{hex(self.chip_addr)} " \
                    f"{hex(addr1)} {hex(addr2)} " \
                    f"{hex(value)}"
        self.run_linux_old(write_cmd)
        return

    def readReg(self, addr1, addr2):
        # address1->first 8bit address
        # address2->second 8bit address
        read_cmd = f"/usr/sbin/i2ctransfer -f -y {str(self.i2c_port)} " \
                   f"w2@{hex(self.chip_addr)} " \
                   f"{hex(addr1)} {hex(addr2)} " \
                   f"r1"
        i=0
        while(i<3):
            read_out = self.run_linux_old(read_cmd)
            if (read_out != "error"):
                break
            else:
                i = i + 1
        # hex str -> int
        read_int = int(read_out, 16)
        return read_int
    #####  end copy write / read reg   #####


class i2c_raspberry:
    def __init__(
        self,
        disc_use={},
        i2c_port=1,         # raspberry default i2c_1
        ):
        self.disc_use=disc_use
        self.i2c_port=i2c_port
        # initial clear writebuf
        self.writebuf=[]



    def try_linux(self,cmd):
        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
            #return output.strip()
        except subprocess.CalledProcessError as error_run:
            error_message = f"Command \"{cmd}\":\n\t{error_run.output}"
            print(error_message)
            return None

        #double check if write success
        #print("double check if write success")
        cmd_split=cmd.split(" ")
        write_value=cmd_split[-1]
        cmd_split[-1]="r1"
        read_cmd=" ".join(cmd_split)
        read_cmd=read_cmd.replace("w3@", "w2@")
        read_output=subprocess.check_output(read_cmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        #read_output=hex(int(read_output.strip(),16))
        read_output=read_output.strip()
        if(read_output==write_value.lower()):
            return True
        else:
            #just report
            print(f"i2c write--then->read double check fail.")
            print(f"\twrite_value: {write_value}; read_value: {read_output}")
            #return False
            return True


    def run_linux(self,cmd):
        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
            return True
        except:
            #do not care what error is
            return False

    '''
    #debug run linux
    def run_linux(self, cmd):
        with open("test.cmd", "w") as file:
            file.write(cmd)
    '''

    def buf_clear(self):
        self.writebuf = []

    def addr_to_linuxcmd(self, addr_line):
        #chip_addr=addr_line[0:2]
        chip_int=int(addr_line[0:2],16)>>1
        chip_addr=hex(chip_int)

        page_addr=addr_line[2:4]
        reg_addr=addr_line[4:6]
        value=addr_line[6:8]
        write_cmd = f"/usr/sbin/i2ctransfer -f -y {str(self.i2c_port)} " \
                    f"w3@{chip_addr} " \
                    f"0x{page_addr} 0x{reg_addr} " \
                    f"0x{value}"
        return write_cmd

    def write_buf(self, func_name):
        # send i2c addr value to buffer
        addr_block=self.disc_use[func_name]
        for addr_line in addr_block:
            if("REF;;SUB" in addr_line):
                # recursive use this function
                sub_func=addr_line.split(" ")[1]
                self.write_buf(sub_func)
            elif(len(addr_line)!=8):
                print("i2c addr number not 8, ERROR")
                return
            else:
                cmd=self.addr_to_linuxcmd(addr_line)
                # buffer write
                self.writebuf.append(cmd)
        return

    def write_i2c(self):
        '''
        0 for i2c error
        1 for i2c ok, write ok
        2 for i2c ok, no write
        '''

        total_num=len(self.writebuf)
        if(total_num>0):
            # first check i2c ok
            # use first command for check status
            check_result=self.try_linux(self.writebuf[0])
            if(check_result==True):
                cmd=';'.join(self.writebuf)
                #print(cmd)
                self.run_linux(cmd)
                print(f"total write i2c num={str(total_num)}, clear buffer.")
                self.buf_clear()
                return 1
            else:
                # try not ok
                # error message in try function
                self.buf_clear()
                return 0
        else:
            # len=0, just show log
            # result=true(i2c good)
            self.buf_clear()
            print(f"buffer len=0, do nothing.")
            return 2    #





    '''
    def writeReg(self, addr1, addr2, value):
        #address1->first 8bit address
        #address2->second 8bit address
        #value->value write to addr
        write_cmd=f"/usr/sbin/i2ctransfer -f -y {str(self.i2c_port)} " \
                  f"w3@{hex(self.chip_addr)} " \
                  f"{hex(addr1)} {hex(addr2)} " \
                  f"{hex(value)}"
        self.run_linux(write_cmd)
        return
    '''

#this for log bg class
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass

if __name__ == '__main__':
    #file_path = "./gsu1001_nto_scripts.txt"
    #disc=aves_to_pydisc(file_path)
    disc={}
    i2c_bridge=i2c_raspberry(disc_use=disc)
    #i2c_bridge.write_buf('05_99_retimer_all')
    #i2c_bridge.write_i2c()
    #i2c_bridge.write_buf('05_02_retimer_skp_mode_1')
    #i2c_bridge.write_i2c()

    print(i2c_bridge.readReg(0x05, 0x61))

