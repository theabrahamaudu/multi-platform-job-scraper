from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import time as t
import random as rand
from utils.html_cleaner import linkedin_bs4_clean as clean

# Initial page url
url = "https://www.linkedin.com/jobs/search?" \
      "keywords=&location=Nigeria&geoId=" \
      "105365761&trk=public_jobs_jobs-search-bar_search-submit" \
      "&position=1&pageNum=0"


def selenium_scrape(url, no_of_jobs):
    """
    This function scrapes jobs from LinkedIn url
    :param url:
    :param no_of_jobs:
    :return:
    """

    # Initialize selenium web driver
    wd = webdriver.Chrome(executable_path='../chromedriver.exe')
    wd.get(url)

    # Retrieve jobs on page
    i = 2
    while i <= int(no_of_jobs / 25) + 1:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        try:
            wd.find_element("xpath", '/html/body/main/div/section/button').click()
            time.sleep(5)
        except:
            pass
            time.sleep(5)

    # Extract job details with Selenium
    jobs_lists = wd.find_element(By.CLASS_NAME, "jobs-search__results-list")
    jobs = jobs_lists.find_elements(By.TAG_NAME, "li")  # return a list

    return jobs


def selenium_job_details(jobs):
    """
    This function parses through scraped jobs using CSS selectors to get
    job details

    :param jobs:
    :return:
    """

    job_id = []
    job_title = []
    company_name = []
    location = []
    date = []
    job_link = []

    for job in jobs:
        job_id0 = job.get_attribute('data-id')
        job_id.append(job_id0)

        job_title0 = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
        job_title.append(job_title0)

        company_name0 = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
        company_name.append(company_name0)

        location0 = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__location"]').get_attribute('innerText')
        location.append(location0)

        date0 = job.find_element(By.CSS_SELECTOR, "div>div>time").get_attribute('datetime')
        date.append(date0)

        job_link0 = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        job_link.append(job_link0)

    return job_id, job_title, company_name, location, date, job_link


def bs4_job_details(job_link):
    """
    This function parses through scraped jobs using BeautifulSoup html parser

    :param job_link:
    :return:
    """

    job_desc = []
    seniority = []
    emp_type = []
    job_func = []
    ind = []

    page = 0
    for link in job_link:
        page += 1
        try:
            # Parse job page
            response = uReq(link)
            job_page = response.read()
            job_page_html = bs(job_page, "html.parser")

            # Get job description
            job_description = job_page_html.findAll("div", {"class": "show-more-less-html__markup"})
            job_description = bs(job_description[0].text).text
            job_description = clean(job_description)
            job_desc.append(job_description)

            # Get job details
            job_details = job_page_html.findAll("span", {
                "class": "description__job-criteria-text description__job-criteria-text--criteria"})

            # Seniority level
            seniority_level = bs(job_details[0].text).text
            seniority_level = clean(seniority_level)
            seniority.append(seniority_level)

            # Employment type
            employment_type = bs(job_details[1].text).text
            employment_type = clean(employment_type)
            emp_type.append(employment_type)

            # Job function
            job_function = bs(job_details[2].text).text
            job_function = clean(job_function)
            job_func.append(job_function)

            # Job industry
            industries = bs(job_details[3].text).text
            industries = clean(industries)
            ind.append(industries)

            # Wait a bit...
            t.sleep(rand.uniform(0.5, 1))
            print("Job ", page, " page scraped successfully")

        except Exception as e:
            print('There was an error scraping Page ', page, ': ', e)
            job_desc.append("NA")
            seniority.append("NA")
            emp_type.append("NA")
            job_func.append("NA")
            ind.append("NA")

    return job_desc, seniority, emp_type, job_func, ind


def jobs_dataframe(selenium_job_details, bs4_job_details):
    job_id = selenium_job_details[0]
    job_title = selenium_job_details[1]
    company_name = selenium_job_details[2]
    location = selenium_job_details[3]
    date = selenium_job_details[4]
    job_link = selenium_job_details[5]

    job_desc = bs4_job_details[0]
    seniority = bs4_job_details[1]
    emp_type = bs4_job_details[2]
    job_func = bs4_job_details[3]
    ind = bs4_job_details[4]

    data = [job_id, job_title, company_name, location, date,
            job_link, job_desc, seniority, emp_type, job_func, ind]

    columns = ["job_id", "job_title", "company_name", "location", "date",
               "job_link", "job_desc", "seniority", "emp_type", "job_func", "ind"]

    linkedin_jobs = pd.DataFrame(data, columns).transpose()

    return linkedin_jobs


if __name__ == "__main__":
    url = "https://www.linkedin.com/jobs/search?keywords=&location=Nigeria&geoId=" \
          "105365761&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

    number_of_jobs = 50

    jobs = selenium_scrape(url=url, no_of_jobs=number_of_jobs)
    selenium_job_details = selenium_job_details(jobs=jobs)
    bs4_job_details = bs4_job_details(job_link=selenium_job_details[5])
    jobs_dataframe = jobs_dataframe(selenium_job_details=selenium_job_details,
                                    bs4_job_details=bs4_job_details)
    print("Operation Complete: \n", jobs_dataframe.head())