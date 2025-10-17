import time
from utils.system_info import get_system_info
from utils.utils import wait_for_enter




class Alarm:
    def __init__(self, alarm_type, threshold):
        self.type = alarm_type
        self.threshold = threshold

    def is_triggered(self, current_value):
        return current_value >= self.threshold

    def __str__(self):
        return f"{self.type} larm {self.threshold}%"



def alarm_monitor(alarms):
  try:
    while True:
      system_info = get_system_info()
      triggered_alarms = []
      
      # Kontrollera varje larm
      for alarm in alarms:
          current_value = None
          
          # Hämta aktuellt värde baserat på larm-typ
          if alarm.type == "CPU användning":
              current_value = system_info['cpu_percent']
          elif alarm.type == "Minnesanvändning":
              current_value = system_info['memory_percent']
          elif alarm.type == "Diskanvändning":
              current_value = system_info['disk_percent']
          
          # Kontrollera om larmet triggas
          if current_value is not None and alarm.is_triggered(current_value):
              triggered_alarms.append({
                  'alarm': alarm,
                  'current_value': current_value,
                  'threshold': alarm.threshold
              })
      
      # Visa triggade larm
      if triggered_alarms:
          for alarm_data in triggered_alarms:
              alarm = alarm_data['alarm']
              current = alarm_data['current_value']
              threshold = alarm_data['threshold']
              print()
              print(f"***VARNING, LARM AKTIVERAT, {alarm.type.upper()} ÖVERSTIGER {threshold}%***")
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