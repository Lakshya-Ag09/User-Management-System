import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class UserEntry:
    def __init__(self, srno, name, age, gender, occupation):
        self.srno = srno
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation

    def to_dict(self):
        return {
            'srno': self.srno,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'occupation': self.occupation
        }

    def display(self):
        print(f"SRNO: {self.srno}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Occupation: {self.occupation}\n")


class UserManager:
    def __init__(self):
        self.entries = []

    def get_next_srno(self):
        return len(self.entries) + 1

    def reassign_serial_numbers(self):
        for i, entry in enumerate(self.entries):
            entry.srno = i + 1

    def is_duplicate(self, new_entry):
        for entry in self.entries:
            if (entry.name == new_entry['name'] and
                entry.age == new_entry['age'] and
                entry.gender == new_entry['gender'] and
                entry.occupation == new_entry['occupation']):
                return True
        return False

    def add_entry(self, entry_data):
        if self.is_duplicate(entry_data):
            print("Duplicate entry. Not added.")
            return
        srno = self.get_next_srno()
        entry = UserEntry(srno, entry_data['name'], entry_data['age'], entry_data['gender'], entry_data['occupation'])
        self.entries.append(entry)
        print("Entry successfully added.")

    def search_entries(self, field, value):
        return [entry for entry in self.entries if getattr(entry, field) == value]

    def update_entry(self, srno, updated_data):
        for entry in self.entries:
            if entry.srno == srno:
                entry.name = updated_data['name']
                entry.age = updated_data['age']
                entry.gender = updated_data['gender']
                entry.occupation = updated_data['occupation']
                self.reassign_serial_numbers()
                print("Entry successfully updated.")
                return True
        print("No matching SRNO found.")
        return False

    def delete_entry(self, srno):
        for i, entry in enumerate(self.entries):
            if entry.srno == srno:
                confirm = input(f"Are you sure you want to delete SRNO {srno}? (y/n): ").lower()
                if confirm == 'y':
                    del self.entries[i]
                    self.reassign_serial_numbers()
                    print("Entry successfully deleted.")
                else:
                    print("Deletion cancelled.")
                return
        print("No matching SRNO found.")

    def display_all_entries(self):
        sorted_entries = sorted(self.entries, key=lambda x: x.srno)
        if not sorted_entries:
            print("No entries to display.")
            return

        page_size = 3
        current_page = 0
        while True:
            clear_screen()
            start = current_page * page_size
            end = start + page_size
            print(f"Showing entries {start + 1} to {min(end, len(sorted_entries))} of {len(sorted_entries)}\n")
            for entry in sorted_entries[start:end]:
                entry.display()
            if len(sorted_entries) <= page_size:
                break
            print("n - next page | p - previous page | q - quit")
            choice = input("Choice: ").lower()
            if choice == 'n' and end < len(sorted_entries):
                current_page += 1
            elif choice == 'p' and current_page > 0:
                current_page -= 1
            elif choice == 'q':
                break
            else:
                print("Invalid choice.")

    def display_entries(self, entries):
        for entry in entries:
            entry.display()


def get_valid_input(prompt, validate_func):
    while True:
        value = input(prompt)
        if validate_func(value):
            return value
        print("Invalid input. Please try again.")

def get_entry_details():
    name = get_valid_input("Enter name: ", lambda x: len(x.strip()) > 0)
    age = get_valid_input("Enter age: ", lambda x: x.isdigit() and 0 < int(x) <= 150)
    gender = get_valid_input("Enter gender (M/F/O): ", lambda x: x.upper() in ['M', 'F', 'O']).upper()
    occupation = get_valid_input("Enter occupation: ", lambda x: len(x.strip()) > 0)
    return {'name': name, 'age': age, 'gender': gender, 'occupation': occupation}


def main():
    manager = UserManager()
    while True:
        print("\n===== User Management System =====")
        print("1. Add entry")
        print("2. Update entry")
        print("3. Delete entry")
        print("4. Search entry")
        print("5. Display all entries")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            entry_data = get_entry_details()
            manager.add_entry(entry_data)

        elif choice == '2':
            srno = get_valid_input("Enter SRNO to update: ", lambda x: x.isdigit())
            srno = int(srno)
            updated_data = get_entry_details()
            manager.update_entry(srno, updated_data)

        elif choice == '3':
            srno = get_valid_input("Enter SRNO to delete: ", lambda x: x.isdigit())
            srno = int(srno)
            manager.delete_entry(srno)

        elif choice == '4':
            field_map = {
                '1': 'srno',
                '2': 'name',
                '3': 'age',
                '4': 'gender',
                '5': 'occupation'
            }
            print("\nSearch by:\n1. SRNO\n2. Name\n3. Age\n4. Gender\n5. Occupation")
            field_choice = input("Enter your choice: ")
            if field_choice not in field_map:
                print("Invalid choice.")
                continue
            search_value = input("Enter search value: ")
            field = field_map[field_choice]
            if field == 'srno' and not search_value.isdigit():
                print("SRNO must be a number.")
                continue
            if field == 'srno':
                search_value = int(search_value)
            results = manager.search_entries(field, search_value)
            if results:
                print(f"\nFound {len(results)} matching entries:\n")
                manager.display_entries(results)
            else:
                print("No matching entries found.")

        elif choice == '5':
            manager.display_all_entries()

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
