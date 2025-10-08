import os
import platform
from .system_info import get_system_info

# Visar systemstatus med progress bars och GB-information
def display_system_status(cpu_usage, memory_usage, disk_usage, bars=50, msg="Aktuell status"):
    # Rensa skärm baserat på operativsystem
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')
    
    # Hämta systeminfo för GB-information
    system_info = get_system_info()
    
    # CPU bar
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
    
    # Memory bar och GB info
    memory_percent = (memory_usage / 100.0)
    mem_bar = '█' * int(memory_percent * bars) + '-' * (bars - int(memory_percent * bars))
    memory_used_gb = system_info['memory_info'].used / (1024**3)
    memory_total_gb = system_info['memory_info'].total / (1024**3)
    
    # Disk bar och GB info
    disk_percent = (disk_usage / 100.0)
    disk_bar = '█' * int(disk_percent * bars) + '-' * (bars - int(disk_percent * bars))
    disk_used_gb = system_info['disk_info'].used / (1024**3)
    disk_total_gb = system_info['disk_info'].total / (1024**3)

    print(f"🔄 {msg}\n")
    print(f"🖥️  CPU-användning:    | {cpu_bar} | {cpu_usage:.1f}%")
    print(f"🧠 Minnesanvändning: | {mem_bar} | {memory_usage:.1f}% ({memory_used_gb:.1f} GB av {memory_total_gb:.1f} GB använt)")
    print(f"💾 Diskutrymme:      | {disk_bar} | {disk_usage:.1f}% ({disk_used_gb:.1f} GB av {disk_total_gb:.1f} GB använt)")
    