from random import (randint)
from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import pickle
import pandas as pd
import re


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get(url, headers, params, proxies, output_name):
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    path = f"{output_name}.rsp"
    save_pickle(r, path)
    r = load_pickle(path)
    return r


def superjob(vacancies_container):
    sj_r = get(sj_url, headers, sj_params, proxies, 'sj')
    soup = bs(sj_r.text, 'html.parser')
    vacancy_head = soup.find_all(attrs={"class": "jNMYr GPKTZ _1tH7S"})
    for v in vacancy_head:
        vacancy = {}
        job_name = v.find(attrs={"class": ["_3mfro PlM3e _2JVkc _3LJqf"]})
        link = 'https://superjob.ru' + job_name.find('a')['href']
        name = job_name.text
        salary = v.find(attrs={"class": ["_3mfro _2Wp8I PlM3e _2JVkc _2VHxz"]}).text
        money = salary.split(u'\xa0')
        salary_min = ''
        salary_max = ''
        salary_curr = ''
        if money[0] == 'от':
            for m in money:
                if m.isdigit():
                    salary_min += m
                    salary_curr = money[-1]
        elif money[0] == 'до':
            for m in money:
                if m.isdigit():
                    salary_max += m
                    salary_curr = money[-1]
        elif money.count('—') != 0:
            dash = money.index('—')
            i = 1
            while money[dash - i].isdigit():
                salary_min = money[dash - i] + salary_min
                i += 1
            i = 1
            while money[dash + i].isdigit():
                salary_max = salary_max + money[dash + i]
                i += 1
            salary_curr = money[-1]
        vacancy['site'] = 'https://russia.superjob.ru'
        vacancy['name'] = name
        vacancy['link'] = link
        vacancy['salary_min'] = salary_min
        vacancy['salary_max'] = salary_max
        vacancy['salary_curr'] = salary_curr
        vacancies_container.append(vacancy)
    is_next = soup.find_all('span', attrs={"class": "_1BOkc"})
    for n in is_next:
        if n.text == 'Дальше':
            sj_params['page'] = str(int(sj_params.get('page')) + 1)
            sleep(randint(100, 200)/50)
            superjob(vacancies_container)


def hh(vacancies_container):
    hh_r = get(hh_url, headers, hh_params, proxies, 'hh')
    hh_path = "hh.rsp"
    save_pickle(hh_r, hh_path)
    hh_r = load_pickle(hh_path)
    soup = bs(hh_r.text, 'html.parser')
    container = soup.findAll(attrs={"class": "vacancy-serp-item"})
    for v in container:
        vacancy = {}
        vacancy['site'] = 'https://hh.ru'
        name = v.find(attrs={"class": "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"}).text
        link = v.find(attrs={"class": "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"}, href=True)
        vacancy['name'] = name
        vacancy['link'] = link['href']
        salary_min = ''
        salary_max = ''
        salary_curr = ''
        try:
            salary = v.find(attrs={"class": "bloko-section-header-3 bloko-section-header-3_lite",
                                      "data-qa": "vacancy-serp__vacancy-compensation"}).text
            money = salary.replace(u'\xa0', u'')
            sal = re.split(' |-', money)
            if sal[0].isdigit():
                salary_min = float(sal[0])
                salary_max = float(sal[1])
                salary_curr = sal[2]
            elif sal[0] == 'от':
                salary_min = float(sal[1])
                salary_curr = sal[2]
            elif sal[0] == 'до':
                salary_max = float(sal[1])
                salary_curr = sal[2]
        except:
            pass
        vacancy['salary_min'] = salary_min
        vacancy['salary_max'] = salary_max
        vacancy['salary_curr'] = salary_curr
        vacancies_container.append(vacancy)
    is_next = soup.find_all(attrs={"data-qa": "pager-next"})
    if len(is_next) != 0 and hh_params['page'] != 3:
        hh_params['page'] = str(int(hh_params.get('page')) + 1)
        sleep(randint(100, 200) / 50)
        hh(vacancies_container)


sj_url = "https://russia.superjob.ru/vacancy/search/"
sj_params = {
    'keywords': 'python',
    'page': '1'
}

hh_url = "https://spb.hh.ru/search/vacancy"
hh_params = {
    'clusters': 'true',
    'enable_snippets': 'true',
    'text': 'python',
    'L_save_area': 'true',
    'area': '2',
    'from': 'cluster_area',
    'showClusters': 'true',
    'page': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}
proxies = {
    'http': 'https://146.66.172.217:8080',
}

vacancies = []
superjob(vacancies)
hh(vacancies)

with open('out.csv', 'w') as f:
    df = pd.DataFrame(vacancies)
    df.to_csv('out.csv', index=False)
