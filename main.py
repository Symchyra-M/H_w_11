from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Name(Field):
    @Field.value.setter
    def value(self, name):
        self._value = name


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError('Enter correct phone')
        self._value = phone


class Birthday(Field):  # Тут birthday це об'єкт datetime
    @Field.value.setter
    def value(self, birthday):
        if isinstance(birthday, datetime):
            self._value = birthday
        else:
            raise ValueError('Enter correct birthday')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday  # Тут birthday це екземпляр класу Birthday

    def add_phone(self, phone):
        valid_phone = Phone(phone)
        if valid_phone.value is not None:
            self.phones.append(valid_phone)
        else:
            return 'Phone is not valid'

    def remove_phone(self, phone):
        valid_phone = Phone(phone)
        phone_to_remove = None
        for ph in self.phones:
            if ph.value == valid_phone.value:
                phone_to_remove = ph
                break
        if phone_to_remove is not None:
            self.phones.remove(phone_to_remove)
        else:
            return 'This contact don`t have this phone'

    def edit_phone(self, old_phone_value, new_phone_value):
        old_phone_index = None
        for i, ph in enumerate(self.phones):
            if ph.value == old_phone_value:
                old_phone_index = i
                break
        if old_phone_index is not None:
            new_phone = Phone(new_phone_value)
            if new_phone.value is not None:
                self.phones[old_phone_index] = new_phone
            else:
                return 'New phone is not valid'
        else:
            raise ValueError('Phone not found')

    def find_phone(self, phone):
        valid_phone = Phone(phone)
        for ph in self.phones:
            if ph.value == valid_phone.value:
                return ph
        return None

    def days_to_birthday(self):
        if self.birthday:
            today_day = datetime.today()
            current_year = today_day.year
            contact_birthday = self.birthday.value
            contact_birthday = contact_birthday.replace(year=current_year)
            if contact_birthday < today_day:
                contact_birthday = contact_birthday.replace(year=current_year + 1)
            result = contact_birthday - today_day
            return result.days
        else:
            return 'No birthday info for this contact'

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record
        else:
            raise ValueError("Here you can add only records")

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            print(f"This contact don`t exist")

    def iterator(self, n):
        index = 0
        not_fitting = len(self.data) % n
        while index < len(self.data):
            try:
                yield dict(list(self.data.items())[index:index + n])
                index += n
            except IndexError:
                yield dict(list(self.data.items())[index:index + not_fitting])