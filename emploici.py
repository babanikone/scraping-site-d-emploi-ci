#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re 

url = 'https://www.emploi.ci/recherche-jobs-cote-ivoire'
page = 'https://www.emploi.ci/recherche-jobs-cote-ivoire?page=' #pages url
page_number = 6 #number of pages
r = requests.get(url)

# function to get all pages of the website
def get_allpage():
    job_links = []
    number = 1
    for i in range(page_number):
        i = f"{page}{number}"
        number += 1
        job_links.append(i)
    return job_links

# function to get the informations that we need
def get_jobs(url):
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    jobs = soup.find_all('div', class_='job-description-wrapper')
    anoucements = []
    for job in jobs:
        try:
            job_links = job['data-href']
        except AttributeError as e:
            job_links = ""
        try:
            title = job.find('h5').find('a').get_text()
        except AttributeError as e:
            title = ""
        try:
            date = job.find('p', class_='job-recruiter').get_text()
        except AttributeError as e:
            date = ""
        try:
            company_name = job.find('a', class_= 'company-name').get_text()
        except AttributeError as e:
            company_name = ""
        try:
            description = job.find('div', class_='search-description').get_text()
        except AttributeError as e:
            description = ""
        try:
            region = job.find('p').get_text()
        except AttributeError as e:
            region = ""

        anoucements.append((job_links,title, date, company_name, description, region))	

     # write the informations in a csv file       
    chemin = r"/home/oussama/Jobs/emploiCi.csv"
    with open(chemin, "a") as f:
        for announcement in anoucements:
            f.write(','.join(announcement) + '\n')
        
    return anoucements
    
# function to get all jobs
def get_allJobs():
    pages = get_allpage()
    for page in pages:
        get_jobs(url=page)
        print(f"on scrape {page}")
 
get_allJobs()
