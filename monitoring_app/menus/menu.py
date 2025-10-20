from monitoring.monitoring import display_usage, show_current_status
from .larm_menu import create_alarm, edit_alarm
from utils.system_info import get_system_info
from alarms.alarm import alarm_monitor
from alarms.alarm_manager import alarm_manager

def print_main_menu():
    print("\n--- HUVUDMENY ---")
    print("1. Starta systemövervakning")
    print("2. Lista systemövervakning")
    print("3. Skapa larm")
    print("4. Visa larm")
    print("5. Editera larm")
    print("6. Starta övervakningsläge")
    print("7. Avsluta programmet")


def handle_menu_choice(choice):
    if choice == 1:
        display_usage()
        return "Övervakning startad."
    elif choice == 2:
        system_info = get_system_info()
        show_current_status(
                system_info['cpu_percent'],
                system_info['memory_percent'],
                system_info['disk_percent']
            )
        return "Aktuell status visad."
    elif choice == 3:
        new_alarm = create_alarm()
        if new_alarm:
            alarm_manager.add_alarm(new_alarm)
            return None
        return "Inget larm skapat."
    elif choice == 4:
        alarms = alarm_manager.get_alarms()
        if not alarms:
            return "Inga larm är konfigurerade."
        return "\n".join([alarm["str"] for alarm in alarms])
    elif choice == 5:
        result = edit_alarm()
        if result:
            return result
        return "Inget larm editerat."
    elif choice == 6:
        alarms = alarm_manager.get_alarms()
        if not alarms:
            return "Inga larm är konfigurerade. Skapa larm först."
        alarm_monitor()
        return None
    elif choice == 7:
        return "Avslutar programmet.."
    
    else:
        return "Ogiltigt val, välj 1-7."


def menu():
    while True:
        print_main_menu()
        try:
            choice = int(input("\nVälj ett alternativ (1-7): "))
        except ValueError:
            print("\nOgiltigt val, ange en siffra 1–7.")
            continue
        result = handle_menu_choice(choice)
        if result:
            print(result)
        if choice == 7:
            break


