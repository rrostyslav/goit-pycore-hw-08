import pickle
from datetime import datetime
from typing import List, Optional


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    @staticmethod
    def validate(value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            return date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")  # Форматування дати для виводу


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_phones(self):
        return [phone.value for phone in self.phones]

    def __str__(self):
        phone_numbers = ', '.join(self.show_phones())
        birthday_str = str(self.birthday) if self.birthday else "No birthday"
        return f"{self.name}: {phone_numbers}, Birthday: {birthday_str}"  # Вивід дня народження


class AddressBook:
    def __init__(self):
        self.records: List[Record] = []

    def add_record(self, record: Record):
        self.records.append(record)

    def find(self, name: str) -> Optional[Record]:
        for record in self.records:
            if record.name.value == name:
                return record
        return None

    def __str__(self):
        return "\n".join(str(record) for record in self.records)

    def save_to_file(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)

    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday}."
    return "Birthday not found."


@input_error
def birthdays(book: AddressBook):
    upcoming = []
    today = datetime.now()
    for record in book.records:
        if record.birthday:
            birthday_this_year = record.birthday.value.replace(year=today.year)
            if 0 <= (birthday_this_year - today).days <= 7:
                upcoming.append(record.name.value)
    if upcoming:
        return "Upcoming birthdays: " + ", ".join(upcoming)
    return "No upcoming birthdays."


def main():
    book = AddressBook.load_from_file()
    print("Welcome to the address book!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        match command:
            case "close" | "exit":
                book.save_to_file()
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(book))
            case "all":
                print(book)
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
