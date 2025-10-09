from monitoring.monitoring import display_usage, show_current_status
from .larm_menu import create_alarm
from utils.system_info import get_system_info
from alarms.alarm import alarm_monitor

def print_main_menu():
    print("\n--- HUVUDMENY ---")
    print("1. Starta övervakning")
    print("2. Lista aktiv övervakning")
    print("3. Skapa larm")
    print("4. Visa larm")
    print("5. Starta övervakningsläge")
    print("6. Avsluta programmet")

alarms = []

def get_main_menu():
    return [
        {"id": 1, "text": "Starta övervakning"},
        {"id": 2, "text": "Lista aktiv övervakning"},
        {"id": 3, "text": "Skapa larm"},
        {"id": 4, "text": "Visa larm"},
        {"id": 5, "text": "Starta övervakningsläge"},
        {"id": 6, "text": "Avsluta programmet"},
    ]

def handle_menu_choice(choice: int, frontend = False):
    if choice == 1:
        if frontend:
            return display_usage(live=False)
        else:
            display_usage()
            return "Övervakning startad."

    elif choice == 2:
        system_info = get_system_info()

        if frontend:
            return {
            "cpu_percent": system_info["cpu_percent"],
            "memory_percent": system_info["memory_percent"],
            "disk_percent": system_info["disk_percent"]
            }
        else:
            show_current_status(
                system_info['cpu_percent'],
                system_info['memory_percent'],
                system_info['disk_percent']
            )
            return system_info

    elif choice == 3:
        new_alarm = create_alarm()
        if new_alarm:
            alarms.append(new_alarm)
            return f"Larm '{new_alarm}' skapat."
        return "Inget larm skapat."

    elif choice == 4:
        if not alarms:
            return "Inga larm är konfigurerade."
        sorted_alarms = sorted(alarms, key=lambda x: x.type)
        return [str(a) for a in sorted_alarms]

    elif choice == 5:
        if not alarms:
            return "Inga larm är konfigurerade. Skapa larm först."
        alarm_monitor(alarms)
        return "Övervakningsläge startat."
    
    elif choice == 6:
        return "Avslutar programmet.."
    
    else:
        return "Ogiltigt val, välj 1-6."

def menu():
    while True:
        print_main_menu()
        try:
            choice = int(input("Välj ett alternativ (1-6): "))
        except ValueError:
            print("Ogiltigt val, ange en siffra 1–6.")
            continue

        result = handle_menu_choice(choice)
        print(result)

        if choice == 6:
            break
