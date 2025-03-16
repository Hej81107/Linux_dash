import tkinter as tk
from tkinter import messagebox
import requests
import time
import threading

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Global lists to hold historical data
cpu_data = []
mem_data = []
disk_data = []
io_data = []
net_data = []

#How many data points to keep in history
MAX_POINTS = 30

METRICS_URL = "http://34.136.205.1:3939/metrics"

#Create the main Tkinter window
root = tk.Tk()
root.title("System Monitoring Dashboard")

cpu_threshold_var = tk.StringVar(value="80")
mem_threshold_var = tk.StringVar(value="80")

cpu_label = tk.Label(root, text="CPU Usage: --%", font=("Arial", 14))
cpu_label.pack()

mem_label = tk.Label(root, text="Memory Usage: --%", font=("Arial", 14))
mem_label.pack()

disk_label = tk.Label(root, text="Disk Usage: --%", font=("Arial", 14))
disk_label.pack()

io_label = tk.Label(root, text="Disk I/O: -- bytes", font=("Arial", 14))
io_label.pack()

net_label = tk.Label(root, text="Network Traffic: -- bytes", font=("Arial", 14))
net_label.pack()

threshold_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
threshold_frame.pack(pady=10)

tk.Label(threshold_frame, text="CPU Threshold:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
cpu_threshold_entry = tk.Entry(threshold_frame, textvariable=cpu_threshold_var, width=5)
cpu_threshold_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(threshold_frame, text="Memory Threshold:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
mem_threshold_entry = tk.Entry(threshold_frame, textvariable=mem_threshold_var, width=5)
mem_threshold_entry.grid(row=0, column=3, padx=5, pady=5)

#Create frame to arrange graphs
charts_frame = tk.Frame(root)
charts_frame.pack(padx=10, pady=10)

#CPU Figure
fig_cpu = Figure(figsize=(4, 2))
ax_cpu = fig_cpu.add_subplot()
line_cpu, = ax_cpu.plot([], [])
ax_cpu.set_title("CPU Usage (%)")
ax_cpu.set_xlabel("Time (last N samples)")
ax_cpu.set_ylabel("CPU %")

canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=charts_frame)
canvas_cpu_widget = canvas_cpu.get_tk_widget()
canvas_cpu_widget.grid(row=0, column=0, padx=5, pady=5)


#Memory Figure
fig_mem = Figure(figsize=(4, 2))
ax_mem = fig_mem.add_subplot()
line_mem, = ax_mem.plot([], [])
ax_mem.set_title("Memory Usage (%)")
ax_mem.set_xlabel("Time (last N samples)")
ax_mem.set_ylabel("Memory %")

canvas_mem = FigureCanvasTkAgg(fig_mem, master=charts_frame)
canvas_mem_widget = canvas_mem.get_tk_widget()
canvas_mem_widget.grid(row=0, column=1, padx=5, pady=5)

#Disk Usage Figure
fig_disk = Figure(figsize=(4, 2))
ax_disk = fig_disk.add_subplot()
line_disk, = ax_disk.plot([], [])
ax_disk.set_title("Disk Usage (%)")
ax_disk.set_xlabel("Time (last N samples)")
ax_disk.set_ylabel("Disk %")

canvas_disk = FigureCanvasTkAgg(fig_disk, master=charts_frame)
canvas_disk_widget = canvas_disk.get_tk_widget()
canvas_disk_widget.grid(row=0, column=2, padx=5, pady=5) 

#I/O Figure
fig_io = Figure(figsize=(4, 2))
ax_io = fig_io.add_subplot()
line_io, = ax_io.plot([], [])
ax_io.set_title("Disk I/O (bytes)")
ax_io.set_xlabel("Time (last N samples)")
ax_io.set_ylabel("Bytes")

canvas_io = FigureCanvasTkAgg(fig_io, master=charts_frame)
canvas_io_widget = canvas_io.get_tk_widget()
canvas_io_widget.grid(row=1, column=0, padx=5, pady=5)

#Network Figure
fig_net = Figure(figsize=(4, 2))
ax_net = fig_net.add_subplot()
line_net, = ax_net.plot([], [])
ax_net.set_title("Network Traffic (bytes)")
ax_net.set_xlabel("Time (last N samples)")
ax_net.set_ylabel("Bytes")

canvas_net = FigureCanvasTkAgg(fig_net, master=charts_frame)
canvas_net_widget = canvas_net.get_tk_widget()
canvas_net_widget.grid(row=1, column=1, padx=5, pady=5) 

def update_plots():
    #CPU Plot
    line_cpu.set_xdata(range(len(cpu_data)))
    line_cpu.set_ydata(cpu_data)
    ax_cpu.set_xlim(0, len(cpu_data) if cpu_data else 1)
    #Adjust y-limits dynamically
    if cpu_data:
        ax_cpu.set_ylim(0, max(cpu_data) + 10)
    canvas_cpu.draw()

    #Memory Plot
    line_mem.set_xdata(range(len(mem_data)))
    line_mem.set_ydata(mem_data)
    ax_mem.set_xlim(0, len(mem_data) if mem_data else 1)
    if mem_data:
        ax_mem.set_ylim(0, max(mem_data) + 10)
    canvas_mem.draw()

    #Disk Plot
    line_disk.set_xdata(range(len(disk_data)))
    line_disk.set_ydata(disk_data)
    ax_disk.set_xlim(0, len(disk_data) if disk_data else 1)
    if disk_data:
        ax_disk.set_ylim(0, max(disk_data) + 10)
    canvas_disk.draw()

    #I/O Plot
    line_io.set_xdata(range(len(io_data)))
    line_io.set_ydata(io_data)
    ax_io.set_xlim(0, len(io_data) if io_data else 1)
    if io_data:
        ax_io.set_ylim(0, max(io_data) * 1.1)
    canvas_io.draw()

    #Network Plot
    line_net.set_xdata(range(len(net_data)))
    line_net.set_ydata(net_data)
    ax_net.set_xlim(0, len(net_data) if net_data else 1)
    if net_data:
        ax_net.set_ylim(0, max(net_data) * 1.1)
    canvas_net.draw()


def fetch_metrics():
    try:
        response = requests.get(METRICS_URL, timeout=5)
        data = response.json()

        #Update labels
        cpu_usage = data['cpu_usage']
        mem_usage = data['memory_usage']
        dsk_usage = data['disk_usage']
        dsk_io = data['io_counters']
        net_io = data['network_io']

        cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        mem_label.config(text=f"Memory Usage: {mem_usage}%")
        disk_label.config(text=f"Disk Usage: {dsk_usage}%")
        io_label.config(text=f"Disk I/O: {dsk_io} bytes")
        net_label.config(text=f"Network Traffic: {net_io} bytes")

        #Color alerts based on thresholds
        current_cpu_threshold = float(cpu_threshold_var.get())
        current_mem_threshold = float(mem_threshold_var.get())

        if cpu_usage > current_cpu_threshold:
            cpu_label.config(bg='red')
        else:
            cpu_label.config(bg='white')

        if mem_usage > current_mem_threshold:
            mem_label.config(bg='red')
        else:
            mem_label.config(bg='white')

        #Update historical data
        cpu_data.append(cpu_usage)
        mem_data.append(mem_usage)
        disk_data.append(dsk_usage)
        io_data.append(dsk_io)
        net_data.append(net_io)

        #Keep only MAX_POINTS in each
        if len(cpu_data) > MAX_POINTS:
            cpu_data.pop(0)
        if len(mem_data) > MAX_POINTS:
            mem_data.pop(0)
        if len(disk_data) > MAX_POINTS:
            disk_data.pop(0)
        if len(io_data) > MAX_POINTS:
            io_data.pop(0)
        if len(net_data) > MAX_POINTS:
            net_data.pop(0)

        #Update the charts
        update_plots()

    except Exception as e:
        cpu_label.config(text="Error fetching data", bg='red')
        print("Error fetching metrics:", e)

    #Time between data updates
    root.after(1000, fetch_metrics)

#Begin fetching data
fetch_metrics()


root.mainloop()
