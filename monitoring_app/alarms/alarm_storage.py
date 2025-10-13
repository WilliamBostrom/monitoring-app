import json
import os
import threading
from .alarm import Alarm

class AlarmStorage:
    def __init__(self, storage_file="alarms.json"):
        self.storage_file = storage_file
        self.lock = threading.Lock()
        self._ensure_storage_file()
    
    def _ensure_storage_file(self):
        """Säkerställ att storage-filen finns"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"alarms": [], "monitoring_active": False}, f)
    
    def _load_alarms(self):
        """Ladda alarm från fil"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data.get("alarms", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_alarms(self, alarms, monitoring_active=False):
        """Spara alarm till fil"""
        data = {
            "alarms": alarms,
            "monitoring_active": monitoring_active
        }
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_alarm(self, alarm):
        """Lägg till ett nytt alarm"""
        with self.lock:
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
    
    def get_alarms(self):
        """Hämta alla alarm"""
        with self.lock:
            alarms_data = self._load_alarms()
            return [
                {
                    "id": alarm["id"],
                    "type": alarm["type"],
                    "threshold": alarm["threshold"],
                    "str": f"{alarm['type']} larm {alarm['threshold']}%"
                }
                for alarm in alarms_data
            ]
    
    def remove_alarm(self, alarm_id):
        """Ta bort ett alarm"""
        with self.lock:
            alarms_data = self._load_alarms()
            if 0 <= alarm_id < len(alarms_data):
                alarms_data.pop(alarm_id)
                # Uppdatera ID:n för återstående alarm
                for i, alarm in enumerate(alarms_data):
                    alarm["id"] = i
                self._save_alarms(alarms_data)
                return True
            return False
    
    def get_alarm_objects(self):
        """Hämta alarm som Alarm-objekt"""
        with self.lock:
            alarms_data = self._load_alarms()
            return [Alarm(alarm["type"], alarm["threshold"]) for alarm in alarms_data]
    
    def set_monitoring_status(self, active):
        """Sätt monitoring status"""
        with self.lock:
            alarms_data = self._load_alarms()
            self._save_alarms(alarms_data, active)
    
    def get_monitoring_status(self):
        """Hämta monitoring status"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data.get("monitoring_active", False)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

# Global instans
alarm_storage = AlarmStorage()
