import psutil
import platform

#Hämtar aktuell systeminformation och returnerar som dictionary
def get_system_info():
    disk_path = 'C:' if platform.system() == "Windows" else '/'
    
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_info': psutil.virtual_memory(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_info': psutil.disk_usage(disk_path),
        'disk_percent': psutil.disk_usage(disk_path).percent,
        'disk_path': disk_path
    }