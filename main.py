from classes import HeadHunter, DBManager, Add_to_DB

dict_companies = {'KIA Motors': 4500968, 'BAUF': 5672395, 'Fersol': 1124,
                  'FinSTC Software LLC': 3551849, 'Вахэлп': 9519486}
list_companies = []


def main():
    # Создание экземпляра класса DBManager и создание БД db_headhunter.
    db_name = 'db_headhunter'
    dbase = DBManager()
    dbase.create_database(db_name)
    print(f"БД {db_name} успешно создана")

    # Получение списка наименований компаний
    for name, id_emp in dict_companies.items():
        list_companies.append(name)

    # Создание экземпляра класса Add_to_DB для добавления данных в БД и само добавление данных в БД
    condb = Add_to_DB(list_companies)
    emp = condb.get_all_employers()
    dbase.save_employers_to_database(emp, db_name)

    # Создание экземпляра класса HeadHunter и добавление вакансий в БД
    for name, id_emp in dict_companies.items():
        hh = HeadHunter(name)
        vacancies = hh.get_vacancies(id_emp)
        dbase.save_vacancies_to_database(vacancies, db_name)

    # Бесконечный цикл программы и выбор вывода данных из БД
    while True:
        command = input(
            "1 - Вывести список всех компаний и количество вакансий у каждой компании; \n"
            "2 - Вывести список всех вакансий; \n"
            "3 - Вывести среднюю зарплату по вакансиям; \n"
            "4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям; \n"
            "5 - Вывести список всех вакансий в названии которых содержатся переданные в метод слова; \n"
            "exit - для выхода. \n"
        )
        if command.lower() == "exit":
            break

        elif command == "1":
            companies_and_vacancies_count = dbase.get_companies_and_vacancies_count(db_name)
            for company_count in companies_and_vacancies_count:
                print(company_count)

        elif command == "2":
            all_vacancies = dbase.get_all_vacancies(db_name)
            for companies_vacancy in all_vacancies:
                print(companies_vacancy)

        elif command == "3":
            avg_salary = dbase.get_avg_salary(db_name)
            print(avg_salary)

        elif command == "4":
            higher_salary = dbase.get_vacancies_with_higher_salary(db_name)
            for higher_vacancy in higher_salary:
                print(higher_vacancy)

        elif command == "5":
            input_keyword = input(f"Введите компанию из списка {list_companies} ")
            keyword_data = dbase.get_vacancies_with_keyword(db_name, input_keyword)
            for keyword_vacancy in keyword_data:
                print(keyword_vacancy)

if __name__ == '__main__':
    main()
