import socket
import tkinter as tk

def get_all_ip_addresses():
    ip_list = []
    # 获取所有网络接口
    interfaces = socket.socket(socket.AF_INET, socket.SOCK_DGRAM).getsockname()[1]
    for interface in interfaces:
        # 获取接口的IP地址
        ip = socket.gethostbyname(socket.gethostname())
        ip_list.append(f"网卡: {interface}, IP地址: {ip}")
    return "\n".join(ip_list)

def show_all_ip_addresses():
    ip_list = get_all_ip_addresses()
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, ip_list)

root = tk.Tk()
root.title("所有网卡的IP地址信息")

text_area = tk.Text(root)
text_area.pack(fill=tk.BOTH, expand=True)

button = tk.Button(root, text="获取所有网卡的IP地址", command=show_all_ip_addresses)
button.pack()

root.mainloop()