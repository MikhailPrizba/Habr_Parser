import requests
from bs4 import BeautifulSoup
import json
import os


class Vacancy:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.description = None
        self.publication_date = None
        self.location = None
        self.employment_type = None

    def get_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")
        scripts = soup.find("script", {"type": "application/ld+json"})
        json_data = json.loads(scripts.text)

        try:
            self.title = json_data["title"]
        except Exception:
            pass

        try:
            self.description = json_data["description"]
        except Exception:
            pass

        try:
            self.publication_date = json_data["datePosted"]
        except Exception:
            pass

        try:
            self.location = json_data["jobLocation"][0]["address"]
        except Exception:
            pass

        try:
            self.employment_type = json_data["jobLocationType"]
        except Exception:
            pass

    def to_json(self):
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "publication_date": self.publication_date,
            "location": self.location,
            "employment_type": self.employment_type,
        }


class VacanciesService:
    def __init__(self):
        self.vacancies = []
        self.headers = os.environ.get('HEADERS')
        self.params ={
            "page" : None,
            "q" : None,
            "qid" : None,
            "type" : "all"
            
        }

    def get_vacancies(self, url):
        self.params["q"] = input("Введите запрос: ")
        self.params["qid"] = input(
            "Квалификация: \n all     : enter \n intern : 1 \n junior : 3 \n middle : 4 \n senior : 5 \n lead   : 6\n Выберете квалификацию: ")
        page = 1

        while True:
            self.params["page"] = page
            r = requests.get(url=url, headers=self.headers, params=self.params)
            soup = BeautifulSoup(r.text, "lxml")
            articles = soup.find_all(class_="vacancy-card__icon-link")

            if not articles:
                break
            print(page)
            for item in articles:
                item_url = item.get("href")
                vacancy = Vacancy(f"https://career.habr.com{item_url}")
                try:
                    vacancy.get_data()
                    self.vacancies.append(vacancy)
                except Exception:
                    pass

            page += 1

    def save_vacancies(self):
        with open("vacancies.json", "w", encoding="utf-8") as vacancy:
            json.dump([vacancy.to_json() for vacancy in self.vacancies],
                      vacancy, indent=4, ensure_ascii=False)