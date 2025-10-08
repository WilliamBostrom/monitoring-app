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


def menu():
    alarms = []

    while True:
        print_main_menu()
        menu_choice = input("Välj ett alternativ (1-6): ")

        if menu_choice == "1":
            display_usage()
            print("Övervakning startad.")

        elif menu_choice == "2":
            # Visa aktuell systemstatus
            system_info = get_system_info()
            show_current_status(system_info['cpu_percent'], system_info['memory_percent'], system_info['disk_percent'])

        elif menu_choice == "3":
            # Skapar larm via larm-meny
            new_alarm = create_alarm()
            if new_alarm:
                alarms.append(new_alarm)

        elif menu_choice == "4":
            # Här ska larm listas, sorterade på typ
            if not alarms:
                print("Inga larm är konfigurerade.")
            else:
                print("Konfigurerade larm:")
                # Sortera larm på typ (CPU, Diskanvändning, Minnesanvändning)
                sorted_alarms = sorted(alarms, key=lambda x: x.type)
                for alarm in sorted_alarms:
                    print(alarm)  # Använder __str__ metoden
            print("\nTryck valfri tangent för att gå tillbaka till huvudmeny")
            input()
                    
        elif menu_choice == "5":
            # Här körs övervakningsläget
            if not alarms:
                print("Inga larm är konfigurerade. Skapa larm först.")
            else:
                print("Övervakningsläge startat. (Tryck tangent för att återgå)")
                # Här ska en loop vara som kontrollerar larm
                alarm_monitor(alarms)

        elif menu_choice == "6":
            print("Avslutar programmet...")
            quit()

        else:
            print("Ogiltigt val. Välj 1-6.")



