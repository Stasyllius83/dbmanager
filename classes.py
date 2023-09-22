from typing import Any
import psycopg2
import psycopg2.errors
import requests
import json
# from utils import get_currencies_hh
from exceptions import ParsingError


class HeadHunter:
    """
        Класс для доступа к api HeadHunter
        """
    employers_dict = {}
    employers_data = []
    vacancies_data = []

    def __init__(self, employer):
        self.employer = employer

    def get_employer(self):
        """
        Функция для получения данных по работодателю
        """
        url_employers = "https://api.hh.ru/employers"
        params = {
            "text": {self.employer},
            "areas": 113,
            "per_page": 20
        }
        response = requests.get(url_employers, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных по работодателю! Статус: {response.status_code}")
        employer = response.json()
        if employer is None:
            return "Данные не получены"
        elif 'items' not in employer:
            return "Нет указанных работодателей"
        else:
            self.employers_dict = {'id': employer['items'][0]['id'], 'name': employer['items'][0]['name'],
                                   'url': employer['items'][0]['alternate_url']}
            self.employers_data.append(self.employers_dict)
            return self.employers_dict

    def get_page_vacancies(self, employer_id, page):
        """
        Функция для получения вакансий по id работодателя
        """
        self.employer_id = employer_id
        url_vacancies = "https://api.hh.ru/vacancies"
        params = {
            "employers_id": {self.employer_id},
            "areas": 113,
            "per_page": 100,
            "page": page
        }
        response = requests.get(url_vacancies, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        data = response.content.decode()
        response.close()
        return data

    def get_vacancies(self, employer_id):
        """
        Функция обработки данных по вакансиям
        """
        vacancies_employer_dicts = []
        for page in range(10):
            vacancies_data = json.loads(self.get_page_vacancies(employer_id, page))
            if 'errors' in vacancies_data:
                return vacancies_data['errors'][0]['value']
            for vacancy_data in vacancies_data['items']:
                if vacancy_data["salary"] is None:
                    vacancy_data["salary"] = {}
                    vacancy_data["salary"]["from"] = None
                    vacancy_data["salary"]["to"] = None

                vacancy_dict = {'id': vacancy_data['id'], 'vacancy': vacancy_data['name'],
                                'url': vacancy_data['apply_alternate_url'],
                                'salary_from': vacancy_data['salary']['from'],
                                'salary_to': vacancy_data['salary']['to'],
                                'employer_id': vacancy_data['employer']["id"]}
                if vacancy_dict['salary_to'] is None:
                    vacancy_dict['salary_to'] = vacancy_dict['salary_from']
                vacancies_employer_dicts.append(vacancy_dict)
        return vacancies_employer_dicts


class Connector_DB(HeadHunter):
    """
    Класс для взаимодействия с базой данных
    """
    __employers_name = []

    def __init__(self, employers_list: list):
        """

        :param employers_list:
        """
        self.employers_list = employers_list
        for employer in self.employers_list:
            super().__init__(employer)
            self.__employers_name.append(self.employer)

    @classmethod
    def __get_all_employers(cls):
        """

        :return:
        """
        for employer in cls.__employers_name:
            employer_info = HeadHunter(employer)
            employer_info.get_employer()
        return super().employers_data


class DBManager:
    """
    Класс для работы с данными БД
    """

    def __init__(self):
        # self.params = params
        self.conn = None
        self.cur = None

    def create_database(self, database_name: str):
        """
        Создание базы данных и таблиц для сохранения данных о .
        """

        conn = psycopg2.connect(
            # dbname='postgres', **self.params)
            database="postgres",
            user="postgres",
            password="12345",
            port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"CREATE DATABASE {database_name}")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ОШИБКА: база данных {database_name} уже существует")
        conn.close()

        conn = psycopg2.connect(database=database_name,
                                user="postgres",
                                password="12345",
                                port="5432")

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    employer VARCHAR(255),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    vacancy_url TEXT
                )
            """)
        conn.commit()
        conn.close()

        conn = psycopg2.connect(database=database_name,
                                user="postgres",
                                password="12345",
                                port="5432")

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employers (
                            employer_id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            emp_id INTEGER,
                            employer_url TEXT
                        )
                    """)
        conn.commit()
        conn.close()

    def save_data_to_database(self, data: list[dict[str, Any]], database_name: str):
        """
        Сохранение данных о вакансиях в базу данных.
        """

        conn = psycopg2.connect(dbname=database_name,
                                user="postgres",
                                password="12345",
                                port="5432")

        with conn.cursor() as cur:
            for vacancy in data:
                cur.execute(
                    """
                    INSERT INTO vacancies (name, employer, salary_from, salary_to, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING vacancy_id
                    """,
                    (vacancy['vacancy'], vacancy['employer_name'], vacancy['salary_from'],
                     vacancy['salary_to'], vacancy['url'])
                )
                # vacancy_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """

    def get_all_vacancies(self):
        """
        Получает список всех вакансий
        :return:
        """
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        pass

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий в названии которых содержатся переданные в метод слова
        :return:
        """
        pass


hh = HeadHunter("skyeng")
# print(hh)
var1 = hh.get_employer()
print(var1)
var2 = hh.get_vacancies("1122462")
print(var2)
# condb = Connector_DB(var2)
