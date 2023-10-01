from classes import HeadHunter, DBManager, Add_to_DB

dict_companies = {'KIA Motors': 4500968, 'BAUF': 5672395, 'Fersol': 1124,
                  'FinSTC Software LLC': 3551849, 'Mobile Solutions': 6019759, 'Вахэлп': 9519486,
                  'КМ Лаб': 1272719}
list_companies = []
list_id_companies = []


def main():
    db_name = 'db_headhunter'
    dbase = DBManager()
    dbase.create_database(db_name)
    print(f"БД {db_name} успешно создана")

    for name, id_emp in dict_companies.items():
        hh = HeadHunter(name)
        vacancies = hh.get_vacancies(id_emp)
        list_companies.append(name)
        list_id_companies.append(id_emp)
        dbase.save_vacancies_to_database(vacancies, db_name)

    condb = Add_to_DB(list_companies)
    emp = condb.get_all_employers()
    dbase.save_employers_to_database(emp, db_name)
    # for company in list_id_companies:
    #     var = dbase.get_companies_and_vacancies_count(company)
    #     print(var)


if __name__ == '__main__':
    main()
