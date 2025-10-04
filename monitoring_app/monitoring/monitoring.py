import psutil
import time
import os


## Test för visa systemanvänding - ska uppdateras med disk/minne gb
def show_usage(cpu_usage, memory_usage, disk_usage, bars=50):
  os.system('cls')  # snyggare termial
  cpu_percent = (cpu_usage / 100.0)
  cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
  memory_percent = (memory_usage / 100.0)
  mem_bar = '█' * int(memory_percent * bars) + '-' * (bars - int(memory_percent * bars))
  disk_percent = (disk_usage / 100.0)
  disk_bar = '█' * int(disk_percent * bars) + '-' * (bars - int(disk_percent * bars))

  print(f"🖥️  CPU Usage:    | {cpu_bar} | {cpu_usage:.1f}%")
  print(f"🧠 Memory Usage: | {mem_bar} | {memory_usage:.1f}%")
  print(f"💾 Disk Usage:   | {disk_bar} | {disk_usage:.1f}%")


def display_usage():
  """Startar monitoring-loopen"""
  while True:
    show_usage(psutil.cpu_percent(), psutil.virtual_memory().percent, psutil.disk_usage('C:').percent)
    time.sleep(1)
  