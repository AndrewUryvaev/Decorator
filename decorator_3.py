import re
import csv
import datetime

DATA_FILE = 'phonebook.csv'
PHONE_PATTERN = '(8|\+7)?\s*(\(*)(\d{3})(\)*)(\s*|-)(\d{3})(\s*|-)(\d{2})(\s*|-)(\d{2})\s*(\(*)(\w\w\w\.)*\s*(\d{4})*(\))*'
SUB_PHONE = r'+7(\3)\6-\8-\10 \12\13'

def logger(old_function):

    def new_function(*args, **kwargs):
        date = datetime.datetime.now()
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding="utf-8") as log_file:
            log_file.write(f'{date} функция: {old_function.__name__} аргументы: {args} {kwargs} результат: {result}\n')
        return result

    return new_function

def test_3():

    @logger
    def input_data():
        with open(DATA_FILE, encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
        return contacts_list

    @logger
    def parse_contact_list(contacts_list):
        new_contacts_list = list()
        for contact in contacts_list:
            new_contact = list()
            full_name_str = ",".join(contact[:3])
            result = re.findall(r'(\w+)', full_name_str)
            while len(result) < 3:
                result.append('')
            new_contact += result
            new_contact.append(contact[3])
            new_contact.append(contact[4])
            phone_pattern = re.compile(PHONE_PATTERN)
            changed_phone = phone_pattern.sub(SUB_PHONE, contact[5])
            new_contact.append(changed_phone)
            new_contact.append(contact[6])
            new_contacts_list.append(new_contact)
        return new_contacts_list

    @logger
    def delete_duplicates_contact(new_contacts_list):
        phone_book = dict()
        for contact in new_contacts_list:
            if contact[0] in phone_book:
                contact_value = phone_book[contact[0]]
                for i in range(len(contact_value)):
                    if contact[i]:
                        contact_value[i] = contact[i]
            else:
                phone_book[contact[0]] = contact
        return list(phone_book.values())

    @logger
    def write_data(new_contacts_list):
        with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(new_contacts_list)


    new_contacts_list = input_data()

    new_parsed_list = parse_contact_list(new_contacts_list)

    contact_book_values = delete_duplicates_contact(new_parsed_list)

    write_data(contact_book_values)

if __name__ == '__main__':
    test_3()
