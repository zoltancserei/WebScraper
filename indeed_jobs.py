# Web scraping job postings from indeed.co.uk

import os
import pandas as pd
from bs4 import BeautifulSoup
import urllib
import requests


def load_indeed_jobs(job_title, location):
    # Extract the HTML and parse it 
    var = {'q': job_title, 'l': location, 'fromage': 'last', 'sort': 'date'}
    url = (r'https://uk.indeed.com/jobs?' + urllib.parse.urlencode(var))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_soup = soup.find(id='resultsCol')
    return job_soup


# Extract the job details (job title, company name, link, date)

def extract_job_title(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    title = title.split('\n')[0]
    return title


def extract_company(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text
    return company


def extract_link(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.indeed.co.uk/' + link
    return link


def extract_date(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date


# Ask the user for the desired job title and location.
job_title = input('Please enter the desired job title: ')
location = input('Please enter the desired location: ')

# Create the 'soup' of HTML containing all the job listings 
job_soup = load_indeed_jobs(job_title, location)

# Iterating over the job listings
job_elems = job_soup.find_all('div', class_='jobsearch-SerpJobCard')

# Create the table
data = pd.DataFrame()
data['Titles'] = [extract_job_title(title) for title in job_elems]
data['Companies'] = [extract_company(company) for company in job_elems]
data['Link'] = [extract_link(link) for link in job_elems]
data['Date'] = [extract_date(date) for date in job_elems]

# Save the table as an Excel file
data.to_excel(f'{job_title}_jobs_{location}.xlsx')

print(f'Excel file successfully saved here: {os.getcwd()}')
