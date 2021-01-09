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


TURN = 0

def increment():
    global TURN
    TURN = TURN+1

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
    # Boot Time
    bootTimeTstmp = psutil.boot_time()
    bt = datetime.fromtimestamp(bootTimeTstmp)


def clean_cache():
    fileCPU = open("SampleDataCPU.txt", "w")
    fileMem = open("SampleDataMemory.txt", "w")
    fileSwap = open("SampleDataSwap.txt", "w")
    fileNet = open("SampleDataNetwork.txt", "w")


cores_init={}
core_percentage_init = psutil.cpu_percent()
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
    i = TURN + 1
    totalCpup= psutil.cpu_percent()
    f.write(str(i)+","+str(totalCpup)+"\n")
    if TURN == 0:
        cores_init = cores
    for j, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores[j] = percentage
        print(f"Core {j}: {cores[j]}%")


mem_init = psutil.virtual_memory()
swap_init = psutil.swap_memory()
def memory_info():
    # prepare the file with the data
    fileMem = open("SampleDataMemory.txt", "a")
    i = TURN + 1
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

partitions_init = psutil.disk_partitions()
def disk_info():
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partitionDevice = partition.device
        partitionMountPoint = partition.mountpoint
        partitionFstype = partition.fstype
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

    # get IO statistics sTURNe boot
    disk_io = psutil.disk_io_counters()
    totalReadDisk = get_size(disk_io.read_bytes)
    totalWriteDisk = get_size(disk_io.write_bytes)

net_io_init = psutil.net_io_counters()
def network_info():
    # prepare the file with the data
    fileMem = open("SampleDataNetwork.txt", "a")
    i = TURN + 1

    # get IO statistics sTURNe boot
    net_io = psutil.net_io_counters()
    totalBytesS = get_size(net_io.bytes_sent)
    totalBytesR = get_size(net_io.bytes_recv)
    fileMem.write(str(i)+","+str(totalBytesS) + "," + str(totalBytesR) + "\n")

clean_cache()
system_info()
cpu_info()
memory_info()
disk_info()
network_info()


f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    increment()
    cpu_info()
    memory_info()
    network_info()
    pullData = open("SampleDataCPU.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(float(y))
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

        button1 = ttk.Button(self, text="Start", command=lambda: controller.show_frame(PageOne))
        button1.pack()


def write_start():
    print("The start")


def write_final():
    print("The end")


start = datetime.now()


def history(controller):
    end = datetime.now()
    # try to open the history file if not create it
    f = open("history.txt","a")
    # -----------------System-----------------
    uname = platform.uname()
    bootTimeTstmp = psutil.boot_time()
    bt = datetime.fromtimestamp(bootTimeTstmp)
    f.write("---------System Info---------\n")
    f.write(f"System:" + str(uname.system) + "\n")
    f.write(f"Node Name: {uname.node}\n")
    f.write(f"Release: {uname.release}\n")
    f.write(f"Version: {uname.version}\n")
    f.write(f"Machine: {uname.machine}\n")
    f.write(f"Processor: {uname.processor}\n")
    f.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")
    # -----------------System-----------------
    # ----------------- CPU -----------------
    cpuCountP = psutil.cpu_count(logical=False)  # Physical number of cores
    cpuCountT = psutil.cpu_count(logical=True)  # Total number of cores
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    freqMax = cpufreq.max
    freqMin = cpufreq.min
    freqCurr = cpufreq.current
    f.write("---------CPU Info---------\n")
    f.write(f"Number of physical cores: {cpuCountP}\n")
    f.write(f"Total number of cores: {cpuCountT}\n")
    f.write(f"Maximum frequency: {freqMax}\n")
    f.write(f"Minimum frequency: {freqMin}\n")
    f.write(f"Current frequency: {freqCurr}\n")
    # ----------------- CPU -----------------
    # append the data from the start and the end of the execution
    f.write("\n")
    f.write(f"--------- {start.year}/{start.month}/{start.day} {start.hour}:{start.minute}:{start.second} ---------\n")

    # -------CPU--------
    f.write("\n")
    f.write(f"####CPU####\n")
    for j, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores_init[j] = percentage
        f.write(f"Core {j}: {cores_init[j]}%\n")
    f.write(f"Total core percentage start: {core_percentage_init}%\n")
    # -------CPU--------

    # -------Memory-------
    f.write("\n")
    f.write(f"####MEMORY####\n")
    totalMem= get_size(mem_init.total)
    availableMem= get_size(mem_init.available)
    usedMem= get_size(mem_init.used)
    percentageMem= mem_init.percent
    f.write(f"Total memory: {totalMem}\n")
    f.write(f"Available memory: {availableMem}\n")
    f.write(f"Used memory: {usedMem}\n")
    f.write(f"Percentage used memory start:{percentageMem}\n")
    f.write(f"####SWAP MEMORY####\n")
    totalSwap = get_size(swap_init.total)
    freeSwap = get_size(swap_init.free)
    usedSwap = get_size(swap_init.used)
    f.write(f"Total swap memory: {totalSwap}\n")
    f.write(f"Available swap memory: {freeSwap}\n")
    f.write(f"Used swap memory: {usedSwap}\n")
    f.write(f"Percentage used swap memory: {swap_init.percent}\n")
    # -------Memory-------

    # -------Disk-------
    f.write("\n")
    f.write(f"####DISK SPACE####\n")
    f.write(f"Partitions and Usage:\n")
    partitions_init = psutil.disk_partitions()
    for partition in partitions_init:
        partitionDevice = partition.device
        partitionMountPoint = partition.mountpoint
        partitionFstype = partition.fstype
        f.write(f"=== Device: {partitionDevice} ===\n")
        f.write(f"  Mountpoint: {partitionMountPoint}\n")
        f.write(f"  File system type: {partitionFstype}\n")
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
        f.write(f"  Total Size: {sizeDiskT}\n")
        f.write(f"  Used: {sizeDiskU}\n")
        f.write(f"  Free: {sizeDiskF}\n")
        f.write(f"  Percentage: {sizeDiskP}%\n")
    disk_io = psutil.disk_io_counters()
    totalReadDisk = get_size(disk_io.read_bytes)
    totalWriteDisk = get_size(disk_io.write_bytes)
    f.write(f"Total read: {totalReadDisk}\n")
    f.write(f"Total write: {totalWriteDisk}\n")
    # -------Disk-------

    # -------Network-------
    f.write("\n")
    f.write(f"####NETWORK USAGE####\n")
    totalBytesS = get_size(net_io_init.bytes_sent)
    totalBytesR = get_size(net_io_init.bytes_recv)
    f.write(f"Total bytes sent: {totalBytesS}\n")
    f.write(f"Total bytes received: {totalBytesR}\n")
    # -------Network-------
    f.write("\n")

    # ------------------------------------------------------------------------------------------------------------------
    f.write(f"--------- {end.year}/{end.month}/{end.day} {end.hour}:{end.minute}:{end.second} ---------\n")
    # -------CPU--------
    f.write("\n")
    f.write(f"####CPU####\n")
    cores = {}
    totalCpup = psutil.cpu_percent()
    for j, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores[j] = percentage
        f.write(f"Core {j}: {cores[j]}%\n")
    f.write(f"Total core percentage start: {totalCpup}%\n")
    # -------CPU--------

    # -------Memory-------
    f.write("\n")
    f.write(f"####MEMORY####\n")
    svmem = psutil.virtual_memory()
    totalMem = get_size(svmem.total)
    availableMem = get_size(svmem.available)
    usedMem = get_size(svmem.used)
    percentageMem = svmem.percent
    f.write(f"Total memory: {totalMem}\n")
    f.write(f"Available memory: {availableMem}\n")
    f.write(f"Used memory: {usedMem}\n")
    f.write(f"Percentage used memory start:{percentageMem}\n")
    f.write(f"####SWAP MEMORY####\n")
    swap = psutil.swap_memory()
    totalSwap = get_size(swap.total)
    freeSwap = get_size(swap.free)
    usedSwap = get_size(swap.used)
    f.write(f"Total swap memory: {totalSwap}\n")
    f.write(f"Available swap memory: {freeSwap}\n")
    f.write(f"Used swap memory: {usedSwap}\n")
    f.write(f"Percentage used swap memory: {swap.percent}\n")
    # -------Memory-------

    # -------Disk-------
    f.write("\n")
    f.write(f"####DISK SPACE####\n")
    f.write(f"Partitions and Usage:\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partitionDevice = partition.device
        partitionMountPoint = partition.mountpoint
        partitionFstype = partition.fstype
        f.write(f"=== Device: {partitionDevice} ===\n")
        f.write(f"  Mountpoint: {partitionMountPoint}\n")
        f.write(f"  File system type: {partitionFstype}\n")
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
        f.write(f"  Total Size: {sizeDiskT}\n")
        f.write(f"  Used: {sizeDiskU}\n")
        f.write(f"  Free: {sizeDiskF}\n")
        f.write(f"  Percentage: {sizeDiskP}%\n")
    disk_io = psutil.disk_io_counters()
    totalReadDisk = get_size(disk_io.read_bytes)
    totalWriteDisk = get_size(disk_io.write_bytes)
    f.write(f"Total read: {totalReadDisk}\n")
    f.write(f"Total write: {totalWriteDisk}\n")
    # -------Disk-------

    # -------Network-------
    f.write("\n")
    f.write(f"####NETWORK USAGE####\n")
    net_io=psutil.net_io_counters()
    totalBytesS = get_size(net_io.bytes_sent)
    totalBytesR = get_size(net_io.bytes_recv)
    f.write(f"Total bytes sent: {totalBytesS}\n")
    f.write(f"Total bytes received: {totalBytesR}\n")
    # -------Network-------

    f.write(f"######################################################################################################")
    f.write("\n\n\n")
    controller.show_frame(StartPage)


class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Resource Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Exit", command=lambda: history(controller))
        button2.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand= True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GuiResourceMonitor()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()