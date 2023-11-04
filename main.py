from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None | str:
        if len(new_value) == 10 and new_value.isdigit():
            self._value = new_value
        else:
            raise ValueError('Phone must have 10 digits')


class Birthday(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @property
    def value(self: str) -> None | str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = datetime.strptime(new_value, '%Y-%m-%d')

    def __str__(self) -> str:
        return self._value.strftime('%Y-%m-%d')
    

class Record:
    def __init__(self, name: str, birthday: Birthday = None) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone_number: str) -> None | str:
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break
        else:
            raise ValueError(f'phone {phone_number} not found in the record')
        
    def edit_phone(self, old_phone: str, new_phone: str) -> None | str:
        for id, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[id] = Phone(new_phone)
                break
        else:
            raise ValueError(f'phone {old_phone} not found in the record')        
        
    def find_phone(self, phone_number: str) -> Phone | str:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        # else:
        #     raise ValueError(f'phone {phone_number} not found in the record')          

    def days_to_birthday(self) -> int:
        if self.birthday:
            today = datetime.now()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = self.birthday.value.replace(year=today.year + 1)
            days_remaining = (next_birthday - today).days
            return f'days to next birthday: {days_remaining}'
        return 'no bd info'

    def __str__(self) -> str:
        name = self.name.value
        phones = '; '.join(p.value for p in self.phones)
        days_to_bd = self.days_to_birthday()
        bd = self.birthday
        return f"Contact name: {name}, phones: {phones}, bd: {bd}, days to bd: {days_to_bd}"    


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
        
    def find(self, name: str) -> str:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if self.find(name):
            self.data.pop(name)

    def iterator(self, n=2):
        records = list(self.data.values())
        num_records = len(records)
        current_index = 0
        while current_index < num_records:
            yield records[current_index:current_index + n]
            current_index += n

    def search(self, search_str):
        results = []
        for record in self.data.values():
            if search_str in record.name.value:
                results.append(record)
            else:
                for phone in record.phones:
                    if search_str in phone.value:
                        results.append(record)
                        break
        return results
    

def serialeze(obj, filename):
    with open(filename, 'wb') as fh:
        pickle.dump(obj, fh)

def unpack(filename):
    with open(filename, 'rb') as fh:
        obj = pickle.load(fh)
    return obj
    

if __name__ == '__main__':
    book = AddressBook()    

    bd = Birthday('1990-01-15')
    john_record = Record('John', bd)   
    john_record.add_phone('1234567890')
    john_record.add_phone('2222222222')
    book.add_record(john_record)
  
    kevin_record = Record('Kevin', bd)
    kevin_record.add_phone('2222222221')
    book.add_record(kevin_record)
    mike_record = Record('Mike', bd) 
    book.add_record(mike_record)

    jane_record = Record('Jane')
    jane_record.add_phone('1233333333')
    jane_record.add_phone('4444444444')
    book.add_record(jane_record)


    filename = 'adress_book.bin'
    serialeze(book, filename)
    result = unpack(filename)
    print (result)
    

    search_result = book.search('J')
    for record in search_result:
        print(record)    