from .alarm import Alarm
from .alarm_storage import alarm_storage
import threading
import time
from utils.system_info import get_system_info

class AlarmManager:
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_thread = None
        self.lock = threading.Lock()
    
    def add_alarm(self, alarm: Alarm):
        """Lägg till ett nytt alarm"""
        return alarm_storage.add_alarm(alarm)
    
    def get_alarms(self):
        """Hämta alla alarm"""
        return alarm_storage.get_alarms()
    
    def remove_alarm(self, alarm_id):
        """Ta bort ett alarm"""
        return alarm_storage.remove_alarm(alarm_id)
    
    @property
    def alarms(self):
        """Hämta alarm som Alarm-objekt"""
        return alarm_storage.get_alarm_objects()
    
    def check_alarms(self):
        """Kontrollera alla alarm och returnera triggade"""
        alarms = self.alarms
        if not alarms:
            return []
        
        system_info = get_system_info()
        triggered_alarms = []
        
        for alarm in alarms:
            current_value = None
            
            if alarm.type == "CPU användning":
                current_value = system_info['cpu_percent']
            elif alarm.type == "Minnesanvändning":
                current_value = system_info['memory_percent']
            elif alarm.type == "Diskanvändning":
                current_value = system_info['disk_percent']
            
            if current_value is not None and alarm.is_triggered(current_value):
                triggered_alarms.append({
                    'alarm': {
                        'type': alarm.type,
                        'threshold': alarm.threshold
                    },
                    'current_value': current_value,
                    'threshold': alarm.threshold,
                    'timestamp': time.time()
                })
        
        return triggered_alarms
    
    def start_monitoring(self):
        """Starta bakgrundsmonitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        alarm_storage.set_monitoring_status(True)
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stoppa bakgrundsmonitoring"""
        self.monitoring_active = False
        alarm_storage.set_monitoring_status(False)
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """Bakgrundsloop för alarm monitoring"""
        while self.monitoring_active:
            triggered = self.check_alarms()
            if triggered:
                # Här kan du lägga till notifikationer, loggning, etc.
                print(f"ALARM TRIGGERED: {len(triggered)} alarms")
            time.sleep(2)

# Global instans
alarm_manager = AlarmManager()