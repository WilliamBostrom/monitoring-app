def print_larm_menu():
    print("\n--- Konfigera larm ---")
    print("1. CPU larm")
    print("2. Minneslarm")
    print("3. Disklarm")
    print("4. Tillbaka till huvudmeny")

# Hämtar och validerar alarm-nivå 
def get_alarm_threshold():
    while True:
        try:
            threshold = int(input("Ställ in nivå för alarm mellan 1-100: "))
            if 1 <= threshold <= 100:
                return threshold
            else:
                print("Fel: Välj en siffra mellan 1-100.")
        except ValueError:
            print("Fel: Ange en giltig siffra mellan 1-100.")


from alarms.alarm_manager import alarm_manager

 # funktion för att skapa larm
def create_alarm():
    while True:
        print_larm_menu()
        menu_choice = input("Välj ett alternativ (1-4): ")

        if menu_choice == "1":
            threshold = get_alarm_threshold()
            print(f"Larm för CPU användning satt till {threshold}%.")
            return {"type": "CPU larm", "threshold": threshold}

        elif menu_choice == "2":
            threshold = get_alarm_threshold()
            print(f"Larm för Minnesanvändning satt till {threshold}%.")
            return {"type": "Minneslarm", "threshold": threshold}

        elif menu_choice == "3":
            threshold = get_alarm_threshold()
            print(f"Larm för Diskanvändning satt till {threshold}%.")
            return {"type": "Disklarm", "threshold": threshold}

        elif menu_choice == "4":
            return None  

        else:
            print("Ogiltigt val. Välj 1-4.")

def edit_larm_menu():
    print("\n--- Editera larm ---")
    print("1. Ta bort larm")
    print("2. Tillbaka till huvudmeny")


# Funktion för att editera/ta bort larm
def edit_alarm():
    while True:
        edit_larm_menu()
        menu_choice = int(input("Välj ett alternativ (1-2): "))

        if menu_choice == 1:
            alarm_id = get_alarm_id()
            if alarm_id is None:
                return "Inga larm att ta bort."
            
            result = alarm_manager.remove_alarm(alarm_id)
            if result:
                return f"\nLarm med id {alarm_id} har tagits bort.\n"
            else:
                return f"Kunde inte ta bort larm med id {alarm_id}. Kontrollera att id:t finns."

        elif menu_choice == 2:
            return None 

        else:
            print("Ogiltigt val. Välj 1-2.")

# Hämtar alarm och tar mot id för eventullt ta bort
def get_alarm_id():
    while True:
        try:
            alarms = alarm_manager.get_alarms()
            if not alarms:
                print("Inga larm finns att ta bort.")
                return None
            
            print("\n--- Tillgängliga larm ---")
            for alarm in alarms:
                print(f"ID {alarm['id']}: {alarm['str']}")
            
            alarm_id = int(input("\nVälj id på larmet du vill ta bort: "))
            if alarm_id >= 0:
                return alarm_id
            else:
                print("Fel: Välj ett giltigt id.")
        except ValueError:
            print("Fel: Ange en giltig siffra.")