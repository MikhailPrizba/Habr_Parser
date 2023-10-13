from parser_1 import VacanciesService


def main():
    vacancies_service = VacanciesService()
    vacancies_service.get_vacancies("https://career.habr.com/vacancies")
    vacancies_service.save_vacancies()


if __name__ == "__main__":
    main()