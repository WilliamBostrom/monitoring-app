def print_larm_menu():
    print("\n--- Konfigera larm ---")
    print("1. CPU användning")
    print("2. Minnesanvändning")
    print("3. Diskanvändning")
    print("4. Tillbaka till huvudmeny")


def get_alarm_threshold():
    """Hämtar och validerar alarm-nivå från användaren"""
    while True:
        try:
            threshold = int(input("Ställ in nivå för alarm mellan 1-100: "))
            if 1 <= threshold <= 100:
                return threshold
            else:
                print("Fel: Välj en siffra mellan 1-100.")
        except ValueError:
            print("Fel: Ange en giltig siffra mellan 1-100.")


from alarms.alarm import Alarm

def create_alarm(alarm_type=None, threshold=None, frontend=False):
    """Huvudfunktion för att skapa larm"""
    if frontend:
        if alarm_type not in ["CPU användning", "Minnesanvändning", "Diskanvändning"]:
            return None
        if not (1 <= threshold <= 100):
            return None
        return Alarm(alarm_type, threshold)

    while True:
        print_larm_menu()
        menu_choice = input("Välj ett alternativ (1-4): ")

        if menu_choice == "1":
            threshold = get_alarm_threshold()
            print(f"Larm för CPU användning satt till {threshold}%.")
            return Alarm("CPU användning", threshold)

        elif menu_choice == "2":
            threshold = get_alarm_threshold()
            print(f"Larm för Minnesanvändning satt till {threshold}%.")
            return Alarm("Minnesanvändning", threshold)

        elif menu_choice == "3":
            threshold = get_alarm_threshold()
            print(f"Larm för Diskanvändning satt till {threshold}%.")
            return Alarm("Diskanvändning", threshold)

        elif menu_choice == "4":
            return None  # Användaren vill gå tillbaka

        else:
            print("Ogiltigt val. Välj 1-4.")