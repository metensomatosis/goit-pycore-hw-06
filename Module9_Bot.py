from collections import UserDict


class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        phone: Phone | None = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            print("Phone not found")

    def edit_phone(self, old_number: str, new_number: str) -> None:
        phone: Phone | None = self.find_phone(old_number)
        if phone:
            self.phones.remove(phone)
            self.phones.append(Phone(new_number))
        else:
            print("Old phone not found")

    def find_phone(self, phone_number: str) -> Phone | None:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        phones_str: str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            print("Contact not found")


def main() -> None:
    book: AddressBook = AddressBook()

    while True:
        command: str = input(
            "\nEnter command (add, show, show all, edit, delete phone, delete contact, find, exit): "
        ).strip().lower()

        if command == "add":
            name: str = input("Enter name: ").strip()
            phone: str = input("Enter phone (10 digits): ").strip()

            try:
                record: Record | None = book.find(name)
                if record is None:
                    record = Record(name)
                    record.add_phone(phone)
                    book.add_record(record)
                else:
                    record.add_phone(phone)
                print("Contact added successfully")
            except ValueError as error:
                print(error)

        elif command == "show":
            name = input("Enter name: ").strip()
            record = book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found")

        elif command == "show all":
            if not book.data:
                print("Address book is empty")
            else:
                for record in book.data.values():
                    print(record)

        elif command == "edit":
            name = input("Enter name: ").strip()
            old_phone = input("Enter old phone: ").strip()
            new_phone = input("Enter new phone: ").strip()

            record = book.find(name)
            if record:
                try:
                    record.edit_phone(old_phone, new_phone)
                    print("Phone updated successfully")
                except ValueError as error:
                    print(error)
            else:
                print("Contact not found")

        elif command == "delete phone":
            name = input("Enter name: ").strip()
            phone = input("Enter phone to delete: ").strip()

            record = book.find(name)
            if record:
                record.remove_phone(phone)
            else:
                print("Contact not found")

        elif command == "delete contact":
            name = input("Enter name: ").strip()
            if book.find(name):
                book.delete(name)
                print("Contact deleted")
            else:
                print("Contact not found")

        elif command == "find":
            name = input("Enter name: ").strip()
            record = book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found")

        elif command == "exit":
            print("Good bye!")
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
