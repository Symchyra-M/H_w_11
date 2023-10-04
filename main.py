from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def is_valid(self, value):
        pass

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid(value):
            raise ValueError('Error, the number must have 10 digits.')

    def is_valid(self, value):
        return len(value) == 10 and self.value.isdigit()


class Birthday(Field):
    def is_valid(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            print('Invalid birthday format. Try DD-MM-YYYY.')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        for ph in self.phones:
            if phone == ph:
                self.phones.remove(phone)
                return self.phones
        raise ValueError('Invalid number.')

    def edit_phone(self, old_phone, edit_phone):
        for ph in self.phones:
            if ph.value == old_phone:
                ph.value = edit_phone
                return ph.value
        raise ValueError('Invalid number.')

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}."

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.now()
        birthday_date = datetime(self.birthday.value.day, self.birthday.value.month, self.birthday.value.year)

        if today > birthday_date:
            next_birthday = datetime(self.birthday.value.day, self.birthday.value.month, self.birthday.value.year + 1)
        else:
            next_birthday = birthday_date

        days_left = (next_birthday - today).days
        return days_left


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, num_of_records=5):
        records = list(self.data.values())
        for i in range(0, len(records), num_of_records):
            yield records[i:i + num_of_records]