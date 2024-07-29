# Import required libraries
from datetime import timedelta, datetime
import random
import os

# Constants for text formatting
orange = "\033[38;2;255;165;0m"  # orange color text
bold = "\033[1m"  # bold text
end = "\033[0m"  # end text formatting

# Constants for file locations
reservation_file = "reservation.txt"
menu_items_file = "menuItems.txt"

# Create a list to store information for all reservations
reservations = []

# Create a reservation dictionary & add it to the list
def create_and_add_reservation(reservations, date, session, name, email, phone, no_of_pax):
    reservation = {
        "date": date,
        "session": session,
        "name": name,
        "email": email,
        "phone": phone,
        "no_of_pax": no_of_pax
    }
    reservations.append(reservation)

# Import reservations from file
def import_reservation():
    reservations.clear()  # clear the existing reservations list

    with open(reservation_file, "r") as file:
        for line in file:
            fields = line.strip().split("|")

            if len(fields) == 6:  # check if the line has all the required fields
                date = fields[0]
                session = fields[1]
                name = fields[2]
                email = fields[3]
                phone = fields[4]

                # Convert the number of pax per reservation to an integer
                try:
                    no_of_pax = int(fields[5])
                except ValueError:
                    print("Invalid number of pax format in the file.")
                    continue

                # Create a reservation dictionary and add it to the list
                create_and_add_reservation(reservations, date, session, name, email, phone, no_of_pax)
            else:
                print("Invalid data format in the file.")

    print("Reservations imported successfully.")

# Validate numeric input
def numeric_validation(prompt):
    while True:
            number = input(prompt)
            if number.isdigit() & int(number) > 0:
                return int(number)
            else:
                print("Invalid input. Please enter a number greater than 0.")

# Validate date input
def date_validation():
    while True:
        input_date = input("Enter the date of the reservation (YYYY-MM-DD): ")
        try:
            # Parse the input date string to a datetime object
            parsed_date = datetime.strptime(input_date, "%Y-%m-%d")
            # Format the date back to a string with zero-padded month and day
            date = parsed_date.strftime("%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

# Validate session input
def session_validation():
    while True:
        session = input("Enter session (1-4): ")
        if session.isdigit() and 0 < int(session) < 5:
            return session
        else:
            print("Invalid session. Please select a session between 1 and 4.")

# Validate email input
def email_validation():
    while True:
        email = input("Enter email: ")
        if email and email.count('@') == 1 and email.endswith('.com'):
            return email
        else:
            print("Invalid email. Please enter a valid email address.")

# Validate phone number input
def phone_validation():
    while True:
        phone = input("Enter phone number: ")
        if phone.isdigit() and (phone.startswith('011') or phone.startswith('015')) and len(phone) == 11:
            return phone
        elif phone.isdigit() and phone.startswith('01') and len(phone) == 10:
            return phone
        else:
            print("Invalid phone number. Please enter a valid phone number.")

# Validate input for number of pax per reservation
def no_of_pax_validation():
    while True:
        try:
            no_of_pax = int(input("Enter number of pax (1-4): "))
            if 0 < no_of_pax < 5:
                return no_of_pax
            else:
                print("Exceeded the maximum number of 4 pax per reservation.")
        except ValueError:
            print("Invalid input. Try again.")

# Print time session for reservation
def print_reservation_session():
    print(orange + "Reservation Session:" + end,
          "[1] 12:00 pm – 02:00 pm",
          "[2] 02:00 pm – 04:00 pm",
          "[3] 06:00 pm – 08:00 pm",
          "[4] 08:00 pm – 10:00 pm", sep="\n")

# Check if the number of reservations for the current session exceeds the limit of 8
def check_reservation_limit(date, session):
    total_reservation_per_session = sum(1 for res in reservations if res["date"] == date and res["session"] == str(session))
    if total_reservation_per_session >= 8:
        print("Reached the limit of 8 reservations for this session.")
        return False
    return True

# Display found reservations
def display_found_res(matching_reservations):
    for i, reservation in enumerate(matching_reservations, 1):
        print(f"{orange + "Reservation " + str(i) + end}")
        print(f"Date: {reservation['date']}")
        print(f"Session: {reservation['session']}")
        print(f"Name: {reservation['name'].title()}")
        print(f"Email: {reservation.get('email')}")
        print(f"Phone: {reservation.get('phone')}")
        print(f"Number of pax: {reservation['no_of_pax']}")
        print()

# Add reservation
def add_reservation():
    # Prompt the user to enter the number of reservations to add
    num_reservations = numeric_validation("Enter the number of reservations to add: ")

    # Loop to add multiple reservations based on the user input
    for _ in range(num_reservations):
        cancel_adding_reservation = False  # flag to cancel adding the reservation
        while True:
            date = date_validation()

            # Check if reservation booked at least 5 days prior
            current_date = datetime.now().date()
            reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
            advance_date = current_date + timedelta(days=5)
            if reservation_date < advance_date:
                print("Reservations must be made at least 5 days in advance.\n")
                continue

            # Prompts the user to enter valid session
            print_reservation_session()
            session = session_validation()

            # Check if the number of reservations for the current session exceeds the limit of 8
            if not check_reservation_limit(date, session):
                print("[1] Enter a different date and session",
                      "[2] Cancel",
                      sep="\n")
                choice = input("Choose an option: ")
                if choice == "1":  # go back to entering a different date and session
                    continue
                elif choice == "2":  # cancel adding the reservation
                    cancel_adding_reservation = True
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                break

        if cancel_adding_reservation:
            continue  # continue to the next reservation iteration if the user cancels adding the reservation

        pass

        # Prompts the user to enter name
        name = input("Enter name: ").upper()

        # Check if there's an existing reservation with the same name & date
        # (If there's an existing reservation) ask if the user wants to update it or proceed adding the reservation
        for reservation in reservations:
            if reservation["date"] == date and reservation["name"].strip() == name.strip():
                print(f"There's an existing reservation in our record on {orange + reservation["date"] + end} in {orange + reservation["session"] + end}.")
                choice = input("Do you want to update the reservation instead? [y/n]: ")
                if choice.lower() == "y":
                    update_reservation()
                    return
                else:
                    continue_add_reservation = input("Do you want to proceed adding this reservation? [y/n]: ")
                    if continue_add_reservation.lower() == "y":
                        continue
                    else:
                        input("Press any key to continue ...")
                        return
        # Prompts the user to enter valid email
        email = email_validation()

        # Prompts the user to enter valid phone number
        phone = phone_validation()

        # Limit the number of pax to maximum of 4 pax in a group for a single reservation
        no_of_pax = no_of_pax_validation()

        create_and_add_reservation(reservations, date, session, name, email, phone, no_of_pax)
        print("\nReservation added successfully.\n")

    input("Press any key to continue ...")

# Cancel reservation
def cancel_reservation():
    del_reservation = numeric_validation("Enter the number of reservations to cancel: ")

    for _ in range(del_reservation):
        while True:
            date = date_validation()
            # Check if the reservation date has passed
            current_date = datetime.now().date()
            reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
            if reservation_date < current_date:
                end_program = input("Reservation date has passed. Do you want to end the program? [y/n]: ")
                if end_program == "y":
                    return
                elif end_program == "n":
                    continue
                else:
                    print("Invalid input. Try again.")
            else:
                break

        print()
        print_reservation_session()
        session = session_validation()
        print()

        matching_reservations = []
        for i, res in enumerate(reservations, 1):
            if res["date"] == date and res["session"] == session:
                matching_reservations.append(res)

        # Check if there are no matching reservations
        if not matching_reservations:
            print(f"No reservations found for {orange + date + end}, Session {orange + session + end}.\n")
            input("Press any key to continue ...")
            return  # Exit the function

        display_found_res(matching_reservations)

        # Ask the user to choose which reservation to remove
        while True:
            choice = input("Enter the reservation number to remove or 'NA' to end the process: ").lower()
            if choice == "na":
                break
            try:
                choice = int(choice)
                if 1 <= choice <= len(matching_reservations):
                    # Remove the selected reservation
                    reservations.remove(matching_reservations[choice - 1])
                    print("Reservation removed successfully.")
                    break
                else:
                    print("Invalid choice. Please enter a valid reservation number.")
            except ValueError:
                print("Invalid input.")

    input("Press any key to continue ...")

# Update reservation
def update_reservation():
    # Prompts user to input name and number of a reservation to update a reservation
    print("[1] Search by date & session")
    print("[2] Search by name")
    while True:
        search_type = input("Enter [1] or [2]: ")
        if search_type == "1":
            date = date_validation()
            print()
            print_reservation_session()
            session = session_validation()
            break

        elif search_type == "2":
            name = input("Enter the name of the reservation: ").upper()
            break
        else:
            print("Error. Enter either 1 or 2.")

    matching_reservations = []

    for i, res in enumerate(reservations, 1):
        if (search_type == "1" and res["date"] == date and res["session"] == session) or (search_type == "2" and res["name"].strip() == name.strip()):
            matching_reservations.append(res)

    if not matching_reservations:
        if (search_type == "1"):
            print(f"\nNo reservations found for {orange + date + end}, Session {orange + session + end}.\n")
        else:
            print(f"\nNo matching reservation found for {orange + name + end}.\n")
        print("[1] Add a new reservation", "[2] Search again", "[3] End", sep="\n")
        not_found_choice = input("Enter your choice (1-3): ").lower()
        if not_found_choice == '1':
            add_reservation()
            return
        elif not_found_choice == '2':  # return to ask for enter either date & session or name again
            update_reservation()
            return
        elif not_found_choice == '3':
            return
        else:
            print("Not a valid input. Try again.")

    print()

    display_found_res(matching_reservations)

    # Ask the user to choose which reservation to update
    while True:
        try:
            choice = int(input("Enter the index of the reservation to update (eg: 1, 2, 3): "))
            if 0 < choice <= len(matching_reservations):
                chosen_reservation = matching_reservations[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid index.")
        except ValueError:
            print("Invalid choice. Please enter a valid index.")

    while True:
        print("\n[1] Date")
        print("[2] Session")
        print("[3] Name")
        print("[4] Email")
        print("[5] Phone")
        print("[6] Number of pax")
        print("[7] End")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            print(f"The initial date is {orange + chosen_reservation['date'] + end}")
            while True:
                new_date = date_validation()
                current_date = datetime.now().date()
                reservation_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                if reservation_date < current_date:
                    print("Reservation date has passed.")
                else:
                    # Count reservations for the specified date and session to satisfy the session limit
                    session = chosen_reservation['session']

                    # Check if the number of reservations for the current session exceeds the limit of 8
                    if not check_reservation_limit(new_date, session):
                        continue
                    else:
                        chosen_reservation['date'] = new_date
                        print("Date updated successfully.")
                        break

        elif choice == "2":
            print_reservation_session()
            print(f"\nThe initial session is {orange + chosen_reservation['session'] + end}")
            date = chosen_reservation['date']
            while True:
                new_session = session_validation()
                # Check if the number of reservations for the current session exceeds the limit of 8
                if not check_reservation_limit(date, new_session):
                    continue
                else:
                    chosen_reservation['session'] = str(new_session)
                    print("Session updated successfully.")
                    break

        elif choice == "3":
            print(f"The initial name is {orange + chosen_reservation['name'] + end}")
            new_name = input("Enter new name: ")
            if new_name:
                chosen_reservation['name'] = new_name.upper()
                print("Name updated successfully.")

        elif choice == "4":
            print(f"The initial email is {orange + chosen_reservation['email'] + end}")
            new_email = email_validation()
            chosen_reservation['email'] = new_email
            print("Email updated successfully.")

        elif choice == "5":
            print(f"The initial phone number is {orange + chosen_reservation['phone'] + end}")
            new_phone = phone_validation()
            chosen_reservation['phone'] = new_phone
            print("Phone number updated successfully.")

        elif choice == "6":
            print(f"The initial number of pax is {orange + str(chosen_reservation['no_of_pax']) + end}")
            new_no_of_pax = no_of_pax_validation()
            chosen_reservation['no_of_pax'] = new_no_of_pax
            print("Number of pax updated successfully.")

        elif choice == "7":
            # Find the index of the chosen reservation in the reservations list
            index = None
            for i, res in enumerate(reservations):
                if res == chosen_reservation:
                    index = i
                    break

            # Update the reservation in the reservations list
            if index is not None:
                reservations[index] = chosen_reservation
                # Write the updated reservations back to the file
                export()
                print("Reservation updated successfully.\n")
                input("Press any key to continue ...")
            else:
                print("Reservation not found in the list.")
            return

        else:
            print("Invalid choice. Please try again.")

# Sort the reservations by date and session
def sort(data):
    sorted_data = sorted(data, key=lambda x: (x["date"], x["session"]))
    return sorted_data

# Display reservation
def display_reservations():
    headers = ["Date", "Session", "Name", "Email", "Phone", "Number of pax"]
    column_width = [len(header) for header in headers]
    fields = ["date", "session", "name", "email", "phone"]

    # Adjust the column width based on the length of the longest value in each field
    for reservation in reservations:
        for i, field in enumerate(fields):
            if len(reservation[field]) > column_width[i]:
                column_width[i] = len(reservation[field])

    # Print headers
    for header in headers:
        index = headers.index(header)
        print(f'{bold}{orange}{header:<{column_width[index]}}{end}', end=" ")
    print()

    # Print the reservations
    for reservation in sort(reservations):
        for i, field in enumerate(["date", "session", "name", "email", "phone", "no_of_pax"]):
            print(f'{reservation[field]:<{column_width[i]}}', end=" ")
        print()

    input("Press any key to continue ...")

# Meal recommendation
def meal_recommendation():
    menu = {}  # hold menu items by category
    categories = []  # hold menu categories
    menu_items = []  # hold all menu items

    with open(menu_items_file, 'r') as file:
        item_numbering = 1  # initialize item numbering
        for line in file:
            line = line.strip()
            if line:
                if line.endswith(":"):
                    category = line.capitalize().rstrip(":")
                    menu[category] = []  # append category to the list of categories
                    categories.append(category)  # append category to the list of categories
                    item_numbering = 1  # reset item numbering for each category
                else:
                    menu[category].append(line)  # add menu item to the category's list
                    menu_items.append(line)  # add menu item to the menu_items list
                    item_numbering += 1

    # Display the categories
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")
    # Display the option to select all categories
    print(f"{len(categories)+1}. Need surprise? Get a full course.")

    while True:
        try:
            user_menu_choice = int(input("Enter your choice (1-7): "))
            break
        except ValueError:
            print("\nNot a number. Please try again.\n")

    # Get a random item from the selected category
    if 1 <= user_menu_choice <= len(categories):
        category = categories[user_menu_choice - 1]
        if category in menu:
            random_item = random.choice(menu[category])
            print("\nHere's a random", orange + category + end, "recommendation for you:", orange + random_item + end)
        else:
            print(category, "category does not exist in the menu.")
    # Suggest a full course
    elif user_menu_choice == len(categories)+1:
        print("\nHere's a full course recommendation for you:")

        # Suggest one item from either 'pizza', 'pasta', or 'antipasta'
        main_course_categories = ['Pizza', 'Pasta', 'Antipasta']
        main_course_category = random.choice(main_course_categories)
        if main_course_category in menu:
            random_item = random.choice(menu[main_course_category])
            print(f"{main_course_category.ljust(10)}: {orange+random_item+end}")

        # Suggest one item each from 'zuppa', 'dolci', and 'drink'
        additional_categories = ['Zuppa', 'Dolci', 'Drink']
        for category in additional_categories:
            if category in menu:
                random_item = random.choice(menu[category])
                print(f"{category.ljust(10)}: {orange+random_item+end}")

    print()
    input("Press any key to continue ...")

# Export reservations to file
def export():
    with open(reservation_file, "w") as file:
        # Write each reservation in the designated format
        for res in reservations:
            session = str(res["session"])
            line = "|".join([
                str(res["date"]),
                str(res["session"]),
                str(res["name"]),
                str(res["email"]),
                str(res["phone"]),
                str(res["no_of_pax"])
            ])
            file.write(line + "\n")

# Display reservation menu
def print_menu():
    os.system('cls')  # clear the console screen
    print(f"{orange+bold+"Charming Thyme Trarroria's"+end}",
          f"{bold+"Reservation System Menu:"+end}")
    print("1. Add Reservation(s)")
    print("2. Cancel Reservation(s)")
    print("3. Update/Edit Reservation(s)")
    print("4. Display All Reservations")
    print("5. Meal recommendation")
    print("6. Exit")

# Import reservations from file
import_reservation()

# Execute the main program loop
while True:
    print_menu()
    choice = input("Enter your choice (1-6): ")
    print()

    if choice == "1":
        # Add reservation
        add_reservation()
        export()

    elif choice == "2":
        # Cancel reservation
        cancel_reservation()
        export()

    elif choice == "3":
        # Update reservation
        update_reservation()
        export()

    elif choice == "4":
        # Display all reservations
        display_reservations()

    elif choice == "5":
        # Meal recommendation
        meal_recommendation()

    elif choice == "6":
        # Exit the program
        print("Exiting...")
        export()
        break

    else:
        # Invalid choice
        print("Invalid choice. Please enter a number between 1 and 6.")
