import time
from utils.system_info import get_system_info
from utils.utils import wait_for_enter
from .alarm_manager import alarm_manager




class Alarm:
    def __init__(self, alarm_type, threshold):
        self.type = alarm_type
        self.threshold = threshold

    def is_triggered(self, current_value):
        return current_value >= self.threshold

    def __str__(self):
        return f"{self.type} larm {self.threshold}%"



def alarm_monitor():
  try:
    while True:
      system_info = get_system_info()
      triggered_alarms = alarm_manager.check_alarms()
      
      # Visa triggade larm
      if triggered_alarms:
          for alarm_data in triggered_alarms:
              alarm_info = alarm_data['alarm']
              current = alarm_data['current_value']
              threshold = alarm_data['threshold']
              print()
              print(f"***VARNING, LARM AKTIVERAT, {alarm_info['type'].upper()} ÖVERSTIGER {threshold}%***")
              print(f"Aktuellt värde: {current:.1f}%")
              print()
      else:
            print(f"CPU: {system_info['cpu_percent']:.1f}%, Minne: {system_info['memory_percent']:.1f}%, Disk: {system_info['disk_percent']:.1f}%")
      
      print(f"Övervakning är aktiv, tryck på Enter för att återgå till menyn.")
      
      # Kolla om användaren tryckt Enter 
      if wait_for_enter():
          print("\nÅtergår till huvudmenyn...")
          break
      
      time.sleep(2) 
                  
  except KeyboardInterrupt:
      print("\nÅtergår till huvudmenyn...")
      time.sleep(1)