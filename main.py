from datetime import datetime
from sys import argv
import platform
import psutil

NAME= argv[0]

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

def cpu_info():
    # let's print CPU information
    print("=" * 40, "CPU Info", "=" * 40)

    # number of cores
    cpuCountP = psutil.cpu_count(logical=False) #Physical number of cores
    cpuCountT = psutil.cpu_count(logical=True) #Total number of cores
    print("Physical cores:", cpuCountP)
    print("Total cores:", cpuCountT)

    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    freqMax = cpufreq.max
    freqMin = cpufreq.min
    freqCurr = cpufreq.current
    print(f"Max Frequency: {freqMax}Mhz")
    print(f"Min Frequency: {freqMin}Mhz")
    print(f"Current Frequency: {freqCurr}Mhz")

    # CPU usage
    print("CPU Usage Per Core:")
    cores = {}
    totalCpu = psutil.cpu_percent()
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores[i] = percentage
        print(f"Core {i}: {cores[i]}%")
    print(f"Total CPU Usage: {totalCpu}%")

def memory_info():
    # Memory Information
    print("=" * 40, "Memory Information", "=" * 40)

    # get the memory details
    svmem = psutil.virtual_memory()
    totalMem = get_size(svmem.total)
    availableMem = get_size(svmem.available)
    usedMem = get_size(svmem.used)
    percentageMem = svmem.percent
    print(f"Total: {totalMem}")
    print(f"Available: {availableMem}")
    print(f"Used: {usedMem}")
    print(f"Percentage: {percentageMem}%")
    print("=" * 20, "SWAP", "=" * 20)

    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    totalSwap = get_size(swap.total)
    freeSwap = get_size(swap.free)
    usedSwap = get_size(swap.used)
    percentageSwap = swap.percent
    print(f"Total: {totalSwap}")
    print(f"Free: {freeSwap}")
    print(f"Used: {usedSwap}")
    print(f"Percentage: {percentageSwap}%")

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
    # Network information
    print("=" * 40, "Network Information", "=" * 40)

    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    totalBytesS = get_size(net_io.bytes_sent)
    totalBytesR = get_size(net_io.bytes_recv)
    print(f"Total Bytes Sent: {totalBytesS}")
    print(f"Total Bytes Received: {totalBytesR}")


system_info()
cpu_info()
memory_info()
disk_info()
network_info()