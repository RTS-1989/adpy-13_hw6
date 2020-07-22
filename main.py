import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
##pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
def get_positions(contacts_list):
    
    position_list = []
    new_position_list = []
    
    for item in contacts_list:
        if item[4] == '' or item[4] == 'position':
            pass
        else:
            position_list.append(item[4])

    new_position_list = []
    for item in position_list:
        new_position_list.append(item.split())

    return new_position_list
    
def make_correct_names(contacts_list):
    formated_name_list = []
    pattern = r'^([А-я]+)[\s|,]([А-я]+)[\s|,]([А-я]+|)'
    replace_names = r'\1, \2, \3'
    for people in contacts_list:
        people = ''.join(people)
        result = [re.sub(pattern, replace_names, people)]
        formated_name_list.append(result)
    return formated_name_list

def make_correct_phone_numbers(contacts_list):
    formated_phone_list = []
    pattern = r'(\+7|8)\s*?\(?(\d{3})\)?(\s|-)?(\d{3})\-?(\d{2})\-?(\d{2})\s*((\(?)(доб\.)\s*(\d+)(\)?))?'
    replace_phone_numbers = r'+7(\2)\4-\5-\6 \9\10'
    for people in contacts_list:
        people = ''.join(people)
        result = re.sub(pattern, replace_phone_numbers, people)
        formated_phone_list.append(result)
    return formated_phone_list

def delete_extra_comma(contacts_list):

    formated_phone_list = []
    pattern = r'[,]+'
    replace_with = r', '
    for info in contacts_list:
        info = ",".join(info)
        result = [re.sub(pattern, replace_with, info)]
        formated_phone_list.append(result)
    return formated_phone_list

def main():
    formated_phone_book = make_correct_phone_numbers(make_correct_names(delete_extra_comma(contacts_list)))
    headers = formated_phone_book[0].split()
    some_info_list = []

    for item in formated_phone_book[1:]:
        some_info_list.append(item.split())

    new_list = []

    for item in some_info_list:
            new_dict = {'Фамилия': item[0], 'Имя': item[1], 'Отчество': '',
                        'Учреждение': '', 'Должность': '', 'Телефон': '', 'e-mail': ''}
            position = []
            set_of_work = set()
            if len(item) > 3:
                set_of_work.add(item[3])
            for i in item[2:]:
                pos = ''
                if i.endswith('вна,') or i.endswith('вич,'):
                    new_dict['Отчество'] = i
                elif i.startswith('+7'):
                    new_dict['Телефон'] = i
                elif '@' in i and i.endswith('.ru'):
                    new_dict['e-mail'] = i
                elif i in set_of_work:
                    new_dict['Учреждение'] = i
            for i in item[4:]:
                for item in get_positions(contacts_list):
                    if i in item:
                        new_dict['Должность'] = ' '.join(item)
            new_list.append(new_dict)

    for contact in new_list:
        for i in range(len(new_list)):
            if contact['Фамилия'] == new_list[i]['Фамилия']:
                if contact['Отчество'] == '' and (new_list[i]['Отчество'].endswith('вна,')
                                                  or new_list[i]['Отчество'].endswith('вич,')):
                    contact['Отчество'] = new_list[i]['Отчество']
                elif contact['Телефон'] == '' and new_list[i]['Телефон'].startswith('+7'):
                    contact['Телефон'] = new_list[i]['Телефон']
                elif contact['e-mail'] == '' and ('@' in new_list[i]['e-mail']
                                                  and new_list[i]['e-mail'].endswith('.ru')):
                    contact['e-mail'] = new_list[i]['e-mail']
                if contact['Учреждение'] == '':
                    contact['Учреждение'] = new_list[i]['Учреждение']
               
    new_dict = {i['Фамилия']: i for i in new_list}
    new_info_list = list(new_dict.values())

    some_new_list = []
    some_new_list.append(headers)

    for contacts in new_info_list:
        some_new_list.append(list(contacts.values()))

    print(some_new_list)
    
    return some_new_list
              
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
if __name__ == '__main__':
    with open("phonebook.csv", "w", encoding='utf8') as f:
        datawriter = csv.writer(f, delimiter=',')
      # Вместо contacts_list подставьте свой список
        datawriter.writerows(main())