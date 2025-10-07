from monitoring.monitoring import display_usage, show_current_status
import psutil

def print_main_menu():
    print("\n--- HUVUDMENY ---")
    print("1. Starta övervakning")
    print("2. Lista aktiv övervakning")
    print("3. Skapa larm")
    print("4. Visa larm")
    print("5. Starta övervakningsläge")
    print("6. Avsluta programmet")


def menu():
    monitoring_active = False
    alarms = []

    while True:
        print_main_menu()
        menu_choice = input("Välj ett alternativ (1-6): ")

        if menu_choice == "1":
            monitoring_active = True
            display_usage()
            print("Övervakning startad.")

        elif menu_choice == "2":
            show_current_status(psutil.cpu_percent(), psutil.virtual_memory().percent, psutil.disk_usage('C:').percent)

        elif menu_choice == "3":
            # Här ska skapas larm
            alarm_type = input("Välj larmtyp (CPU/Minne/Disk): ")
            threshold = input("Ställ in nivå för alarm (1-100): ")
            alarms.append({"type": alarm_type, "threshold": threshold})
            print(f"Larm för {alarm_type} satt till {threshold}%.")

        elif menu_choice == "4":
            # Här ska larm listas, sorterade
            if not alarms:
                print("Inga larm är konfigurerade.")
            else:
                print("Konfigurerade larm:")
                for alarm in alarms:
                    print(f"{alarm['type']} larm {alarm['threshold']}%")

        elif menu_choice == "5":
            # Här ska övervakningsläget
            if monitoring_active:
                print("Övervakningsläge startat. (Tryck tangent för att återgå)")
                # Här ska en loop vara som kontrollerar larm
            else:
                print("Ingen övervakning är aktiv. Starta övervakning först.")

        elif menu_choice == "6":
            print("Avslutar programmet...")
            quit()

        else:
            print("Ogiltigt val. Välj 1-6.")



