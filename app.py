import requests
from bs4 import BeautifulSoup
import json

HOST = 'https://hh.ru/search/vacancy?text=python+django+flask&area=1&area=2&only_with_salary=true'

headers ={
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" ,
    "bx-ajax": "true"
    }

if __name__ == '__main__':

    response = requests.get(HOST, headers=headers)
    hh_main = response.text
    soup = BeautifulSoup(hh_main, features='lxml')

    dictionary = {'vacancies': []}
    vacancies_list = soup.find_all('div', class_='vacancy-serp-item-body__main-info')
    for vacancy in vacancies_list:
        link = vacancy.find('a').get('href')
        fork = vacancy.find('span', class_='bloko-header-section-3').text.replace(u'\u202F', '')
        title = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace(u'\u202F', '').replace(u'\xa0', ' ')
        city = vacancy.find('div', class_='bloko-text', attrs={'data-qa' : 'vacancy-serp__vacancy-address'}).text.replace(u'\u202F', '').replace(u'\xa0', ' ')
        element = {'link': link, 'fork': fork, 'title': title, 'city': city}
        dictionary['vacancies'].append(element)

    with open('jobs.json', 'w', encoding='UTF-8') as write_file:
        json.dump(dictionary, write_file, ensure_ascii=False)