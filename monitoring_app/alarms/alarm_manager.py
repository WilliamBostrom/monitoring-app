from .alarm import Alarm
import json
import os
import time
from utils.system_info import get_system_info

class AlarmManager:
    def __init__(self, storage_file="alarms.json"):
        self.storage_file = storage_file
        self._ensure_storage_file()
    

    # Hämta alarm som Alarm-objekt
    @property
    def alarms(self):
        return self.get_alarm_objects()
    
    # Kontrollera alla alarm och returnera triggade
    def check_alarms(self):
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
    
    # Säkerställ att storage-filen finns
    def _ensure_storage_file(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"alarms": []}, f)
    
    # Ladda alarm från fil
    def _load_alarms(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data.get("alarms", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    # Spara alarm till fil
    def _save_alarms(self, alarms):
        data = {"alarms": alarms}
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Lägg till ett nytt alarm
    def add_alarm(self, alarm):
        alarms_data = self._load_alarms()
        alarm_data = {
            "type": alarm.type,
            "threshold": alarm.threshold,
            "id": len(alarms_data)
        }
        alarms_data.append(alarm_data)
        self._save_alarms(alarms_data)
        
        return {
            "message": f"Larm '{alarm.type}' skapat.",
            "threshold": alarm.threshold,
            "type": alarm.type,
            "id": alarm_data["id"]
        }
    
    # Hämta alla alarm
    def get_alarms(self):
        alarms_data = self._load_alarms()
        return [f'{alarm["id"] + 1}. {alarm["type"]} larm {alarm["threshold"]}%'
                for alarm in alarms_data]
    
    # Ta bort ett alarm
    def remove_alarm(self, alarm_id):
        alarms_data = self._load_alarms()
        if 0 <= alarm_id < len(alarms_data):
            alarms_data.pop(alarm_id)
            # Uppdatera ID:n för återstående alarm
            for i, alarm in enumerate(alarms_data):
                alarm["id"] = i
            self._save_alarms(alarms_data)
            return True
        return False
    
    # Hämta alarm som Alarm-objekt
    def get_alarm_objects(self):
        alarms_data = self._load_alarms()
        return [Alarm(alarm["type"], alarm["threshold"]) for alarm in alarms_data]
    

alarm_manager = AlarmManager()