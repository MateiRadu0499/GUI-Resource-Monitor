import platform
import psutil
import datetime
import time
from datetime import date,datetime

import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")

LARGE_FONT=("Verdana", 12)
style.use("fivethirtyeight")


inc = 0


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def system_info():
    uname = platform.uname()
    systemN = uname.system
    nodeN = uname.node
    releaseN = uname.release
    versionN = uname.version
    machineN = uname.machine
    processorN = uname.processor
    print(f"System: {systemN}")
    print(f"Node Name: {nodeN}")
    print(f"Release: {releaseN}")
    print(f"Version: {versionN}")
    print(f"Machine: {machineN}")
    print(f"Processor: {processorN}")

    # Boot Time
    print("=" * 40, "Boot Time", "=" * 40)
    bootTimeTstmp = psutil.boot_time()
    bt = datetime.fromtimestamp(bootTimeTstmp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


def clean_cache():
    fileCPU = open("SampleDataCPU.txt", "w")
    fileMem = open("SampleDataMemory.txt", "w")
    fileSwap = open("SampleDataSwap.txt", "w")
    fileNet = open("SampleDataNetwork.txt", "w")


def cpu_info():
    # prepare the file with the data
    f = open("SampleDataCPU.txt", "a")
    # number of cores
    cpuCountP = psutil.cpu_count(logical=False) #Physical number of cores
    cpuCountT = psutil.cpu_count(logical=True) #Total number of cores

    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    freqMax = cpufreq.max
    freqMin = cpufreq.min
    freqCurr = cpufreq.current

    # CPU usage
    print("CPU Usage Per Core:")
    cores = {}
    i = inc + 1
    totalCpu = psutil.cpu_percent()
    f.write(str(i)+","+str(int(totalCpu))+"\n")
    # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    #     cores[i] = percentage
    #     print(f"Core {i}: {cores[i]}%")


def memory_info():
    # prepare the file with the data
    fileMem = open("SampleDataMemory.txt", "a")
    i = inc + 1
    # get the memory details
    svmem = psutil.virtual_memory()
    totalMem = get_size(svmem.total)
    availableMem = get_size(svmem.available)
    usedMem = get_size(svmem.used)
    percentageMem = svmem.percent
    fileMem.write(str(i) + "," + str(percentageMem) + "\n")

    # prepare the file with the data
    fileSwap = open("SampleDataSwap.txt", "a")
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    totalSwap = get_size(swap.total)
    freeSwap = get_size(swap.free)
    usedSwap = get_size(swap.used)
    percentageSwap = swap.percent
    fileSwap.write(str(i) + "," + str(percentageSwap) + "\n")

def disk_info():
    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")

    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partitionDevice = partition.device
        partitionMountPoint = partition.mountpoint
        partitionFstype = partition.fstype
        print(f"=== Device: {partitionDevice} ===")
        print(f"  Mountpoint: {partitionMountPoint}")
        print(f"  File system type: {partitionFstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        sizeDiskT = get_size(partition_usage.total)
        sizeDiskU = get_size(partition_usage.used)
        sizeDiskF = get_size(partition_usage.free)
        sizeDiskP = partition_usage.percent
        print(f"  Total Size: {sizeDiskT}")
        print(f"  Used: {sizeDiskU}")
        print(f"  Free: {sizeDiskF}")
        print(f"  Percentage: {sizeDiskP}%")

    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    totalReadDisk = get_size(disk_io.read_bytes)
    totalWriteDisk = get_size(disk_io.write_bytes)
    print(f"Total read: {totalReadDisk}")
    print(f"Total write: {totalWriteDisk}")


def network_info():
    # prepare the file with the data
    fileMem = open("SampleDataNetwork.txt", "a")
    i = inc + 1

    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    totalBytesS = get_size(net_io.bytes_sent)
    totalBytesR = get_size(net_io.bytes_recv)
    fileMem.write(str(i)+","+str(totalBytesS) + "," + str(totalBytesR) + "\n")


f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("SampleDataCPU.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(x)
            yList.append(y)
    a.clear()
    a.plot(xList, yList)


class GuiResourceMonitor(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Start",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

start = datetime.now()

def history():
    end = datetime.now()
    # try to open the history file if not create it
    f = open("history.txt","a")
    print(start)
    print(end)
    #append the data from the start and the end of the execution
    f.write("---------"+ str(start) +"---------\n")
    f.write("---------" + str(end) + "---------\n")

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Resource Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Exit",
                            command=lambda: history())
        button2.pack()


        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand= True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


clean_cache()
system_info()
cpu_info()
memory_info()
disk_info()
network_info()

# while(True):
#     time.sleep(0.9)
#     inc += 1
#     cpu_info()
#     memory_info()
#     network_info()

app = GuiResourceMonitor()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()


