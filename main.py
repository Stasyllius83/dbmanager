from classes import HeadHunter, DBManager
from config import config

dict_companies = {'yandex': 1740, 'vk': 15478, 'mailru': 17181, 'tinkoff': 78638, 'mts': 3776,
                  'megafon': 3127, 'tele2': 4219, 'kaspersky': 1057, 'sberbank': 3529, 'rosneft': 6596}


def main():

    vacancies_json = []
    companies_json = []

    db_name = 'db_headhunter'
    # params = config()

    dbase = DBManager()
    dbase.create_database(db_name)
    print(f"БД {db_name} успешно создана")
    hh = HeadHunter("Яндекс")
    vacancies = hh.get_vacancies("1740")
    dbase.save_data_to_database(vacancies, db_name)


if __name__ == '__main__':
    main()
