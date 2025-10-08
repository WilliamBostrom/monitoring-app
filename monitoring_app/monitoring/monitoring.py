import time
from utils.monitoring_display import display_system_status
from utils.system_info import get_system_info

# Visar live systemövervakning med live uppdatering (1 sek mellanrum)
def show_usage(cpu_usage, memory_usage, disk_usage, bars=50, msg="Live-övervakning"):
  display_system_status(cpu_usage, memory_usage, disk_usage, bars, msg)
  print("\nTryck Ctrl+C för att gå tillbaka till menyn")

# Visar snapshot av aktuell systemstatus
def show_current_status(cpu_usage, memory_usage, disk_usage):
  display_system_status(cpu_usage, memory_usage, disk_usage)
  print("\nTryck Enter för att gå tillbaka till huvudmenyn")
  input()

# Startar live systemövervakning
def display_usage():
  try:
    while True:
      system_info = get_system_info()
      show_usage(system_info['cpu_percent'], system_info['memory_percent'], system_info['disk_percent'])
      time.sleep(1)
  except KeyboardInterrupt:
    print("\nÅtergår till huvudmenyn...")
    time.sleep(1)
