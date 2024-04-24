#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re 

url = 'https://emploi.educarriere.ci/nos-offres'
page = 'https://emploi.educarriere.ci/nos-offres?page1='

r = requests.get(url)

def get_allpage():
    job_links = []
    number = 1
    for i in range(40):
        i = f"{page}{number}"
        number += 1
        job_links.append(i)
    return job_links

def get_jobs(url):
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    jobs = soup.find_all('div', class_='box row')
    anoucements = []
    for job in jobs:
        try:
            job_links = job.find('h4').a['href'] #ok
        except AttributeError as e:
            job_links = ""
        try:
            title = job.find('h4').find('a').get_text() #ok
        except AttributeError as e:
            title = ""
        try:
            date_edition = job.find_all('strong').find('span').get_text() #a voir
        except AttributeError as e:
            date = ""
        try:
            date_limite = job.find('strong').find('span').get_text() #avoir
        except AttributeError as e:
            date = ""
        try:
            company_name = job.find('a', class_= 'company-name').get_text()
        except AttributeError as e:
            company_name = "" 
        try:
            description = job.find('p', class_='sentry-title').find('a').get_text() #ok
        except AttributeError as e:
            description = ""
        try:
            region = job.find('i', 'fa fa-map-marker').next_elements.get_text()
        except AttributeError as e:
            region = ""

        anoucements.append((job_links,title, date, company_name, description, region))	
            
    chemin = r"/home/oussama/Jobs/educarierreCi.csv"
    with open(chemin, "a") as f:
        for announcement in anoucements:
            f.write(','.join(announcement) + '\n')
        
    return anoucements
    
def get_allJobs():
    pages = get_allpage()
    for page in pages:
        get_jobs(url=page)
        print(f"on scrape {page}")
 
get_allJobs()
