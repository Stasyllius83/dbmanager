from classes import HeadHunter, DBManager, Add_to_DB

# from config import config

# dict_companies = {'yandex': 1740, 'vk': 15478, 'mailru': 17181, 'tinkoff': 78638, 'mts': 3776,
#                   'megafon': 3127, 'tele2': 4219, 'kaspersky': 1057, 'sberbank': 3529, 'rosneft': 6596}
dict_companies = {'yandex': 1740, 'KIA Motors': 15565, 'BAUF': 5672395, 'Fersol': 1124,
                  'FinSTC Software LLC': 3551849, 'Mobile Solutions': 5728706, 'Вахэлп': 9519486, 'КМ Лаб': 1272719}
list_companies = []


def main():
    db_name = 'db_headhunter'
    dbase = DBManager()
    dbase.create_database(db_name)
    print(f"БД {db_name} успешно создана")

    for name, id_emp in dict_companies.items():
        hh = HeadHunter(name)
        vacancies = hh.get_vacancies(id_emp)
        list_companies.append(name)
        dbase.save_vacancies_to_database(vacancies, db_name)

    condb = Add_to_DB(list_companies)
    emp = condb.get_all_employers()
    dbase.save_employers_to_database(emp, db_name)
    # var = dbase.get_companies_and_vacancies_count()
    print(emp)


if __name__ == '__main__':
    main()
