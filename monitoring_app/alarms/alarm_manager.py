import json
from utils.system_info import get_system_info

class AlarmManager:
    def __init__(self, storage_file="alarms.json"):
        self.storage_file = storage_file

    # Publika metoder
    def add_alarm(self, alarm):
        alarms_data = self._load_alarms()
        alarm_data = {
            "type": alarm.type,
            "threshold": alarm.threshold,
            "id": len(alarms_data)
        }
        alarms_data.append(alarm_data)
        self._save_alarms(alarms_data)
        
        return None
    
    def get_alarms(self):
        alarms_data = self._load_alarms()
        return [
            {
                "id": alarm["id"],
                "type": alarm["type"],
                "threshold": alarm["threshold"],
                "str": f"{alarm['id']}. {alarm['type']} {alarm['threshold']}%"
            }
            for alarm in alarms_data
        ]
    
    def remove_alarm(self, alarm_id):
        alarms_data = self._load_alarms()
        if 0 <= alarm_id < len(alarms_data):
            alarms_data.pop(alarm_id)
            for i, alarm in enumerate(alarms_data):
                alarm["id"] = i
            self._save_alarms(alarms_data)
            return True
        return False
    
    def check_alarms(self):
        alarms_data = self._load_alarms()
        if not alarms_data:
            return []

        system_info = get_system_info()
        triggered_alarms = []

        for alarm in alarms_data:
            current_value = None

            if alarm["type"] == "CPU larm":
                current_value = system_info['cpu_percent']
            elif alarm["type"] == "Minneslarm":
                current_value = system_info['memory_percent']
            elif alarm["type"] == "Disklarm":
                current_value = system_info['disk_percent']

            if current_value is not None and current_value >= alarm["threshold"]:
                triggered_alarms.append({
                    'alarm': {
                        'type': alarm["type"],
                        'threshold': alarm["threshold"]
                    },
                    'current_value': current_value,
                    'threshold': alarm["threshold"]
                })

        return triggered_alarms

    # Hjälpmetoder
    def _load_alarms(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data.get("alarms", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_alarms(self, alarms):
        data = {"alarms": alarms}
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    

alarm_manager = AlarmManager()