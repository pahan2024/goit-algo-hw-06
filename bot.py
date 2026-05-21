from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Обов'язкове поле, логіка базового класу Field повністю підходить
    pass


class Phone(Field):
    def __init__(self, value):
        # Валідація: рядок, що складається рівно з 10 цифр
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        # Створення Phone автоматично запустить валідацію номера
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        # Знаходимо об'єкт Phone та видаляємо його зі списку
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_number, new_number):
        # Пошук старого номера
        phone_to_edit = self.find_phone(old_number)
        if not phone_to_edit:
            raise ValueError(f"Phone number {old_number} not found.")

        # Перевірка нового номера через створення тимчасового об'єкта Phone
        new_phone = Phone(new_number)
        phone_to_edit.value = new_phone.value

    def find_phone(self, phone_number):
        # Пошук об'єкта Phone за його текстовим значенням
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Зберігаємо запис, використовуючи ім'я контакту як ключ
        self.data[record.name.value] = record

    def find(self, name):
        # Повертає об'єкт Record або None, якщо не знайдено
        return self.data.get(name)

    def delete(self, name):
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())


# Перевірочний сценарій із завдання
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
