from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import math

# Initialize web driver
wd = webdriver.Chrome(executable_path='../chromedriver.exe')

# Initialize job details to be scraped
job_id = []
job_title = []
company_name = []
location = []
date = []
job_link = []
job_desc = []
seniority = []
emp_type = []
job_func = []
ind = []


def extract_job_card_info(jobs):
    n = 0
    for job in jobs:
        n += 1
        try:
            job_id0 = job.find_element(By.XPATH,
                                       f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                       f'"cardOutline")]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div['
                                       f'1]/h2/a/span').get_attribute('id')
            job_id.append(job_id0)

            job_title0 = job.find_element(By.XPATH,
                                          f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                          f'"cardOutline")]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div['
                                          f'1]/h2').get_attribute('innerText')
            job_title.append(job_title0)

            company_name0 = job.find_element(By.XPATH,
                                             f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                             f'"cardOutline")]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div['
                                             f'2]/span').get_attribute('innerText')
            company_name.append(company_name0)

            location0 = job.find_element(By.XPATH,
                                         f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                         f'"cardOutline")]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div['
                                         f'2]/div').get_attribute('innerText')
            location.append(location0)

            date0 = job.find_element(By.XPATH,
                                     f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                     f'"cardOutline")]/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div[1]/span['
                                     f'1]').text
            date.append(date0)

            job_link0 = job.find_element(By.XPATH,
                                         f'//*[@id="mosaic-provider-jobcards"]/ul/li[{n}]/div[contains(@class,'
                                         f'"cardOutline")]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div['
                                         f'1]/h2/a').get_attribute('href')
            job_link.append(job_link0)
        except Exception as e:
            pass


def extract_job_page_info(job_link, start_at):

    if start_at == 0:
        pass
    else:
        job_link = job_link[start_at:]

    page = 0
    for link in job_link:
        page += 1
        try:
            # Load job page
            wd.get(link)

            try:
                # Get job description
                job_description = wd.find_element(By.CLASS_NAME, "jobsearch-jobDescriptionText").get_attribute(
                    'innerText')
                job_desc.append(job_description)
            except:
                job_desc.append('NA')

            # Seniority level
            seniority_level = 'Unavailable on Indeed'
            seniority.append(seniority_level)

            try:
                # Employment type
                employment_type = wd.find_element(By.CSS_SELECTOR,
                                                  "#jobDetailsSection > div:nth-child(3) > div:nth-child(2)").get_attribute(
                    'innerText')
                emp_type.append(employment_type)
            except:
                emp_type.append('NA')

            # Job function
            job_function = 'Unavailable on Indeed'
            job_func.append(job_function)

            # Job industry
            industries = 'Unavailable on Indeed'
            ind.append(industries)

        except Exception as e:
            print('There was an error scraping Page ', page, ': ', e)
            job_desc.append("NA")
            seniority.append("NA")
            emp_type.append("NA")
            job_func.append("NA")
            ind.append("NA")


def selenium_scrape(search_url, num_of_jobs):
    num_of_pages = math.ceil(num_of_jobs / 15)

    if num_of_pages == 0:
        num_of_pages = 1
    else:
        pass

    for i in range(0, num_of_pages):
        extension = ""
        if i is not 0:
            extension = "&start=" + str(i * 10)

        url = search_url + extension
        wd.get(url)
        jobs_lists = wd.find_element(By.CSS_SELECTOR, "#mosaic-provider-jobcards")
        jobs = jobs_lists.find_elements(By.TAG_NAME, "li")  # return a list

        extract_job_card_info(jobs)

        if len(job_link) == 0:
            start_at = 0
        else:
            start_at = 15 * i

        extract_job_page_info(job_link, start_at)

    data = [job_id, job_title, company_name, location, date,
            job_link, job_desc, seniority, emp_type, job_func, ind]

    columns = ["job_id", "job_title", "company_name", "location", "date",
               "job_link", "job_desc", "seniority", "emp_type", "job_func", "ind"]

    indeed_jobs_dataframe = pd.DataFrame(data, columns).transpose()

    return indeed_jobs_dataframe


if __name__ == "__main__":
    search_url = "https://ng.indeed.com/jobs?q=&l=Nigeria&from=searchOnHP&vjk=701c24acfea16b1d"
    num_of_jobs = 25
    indeed_jobs = selenium_scrape(search_url=search_url,
                                  num_of_jobs=num_of_jobs)

    print(indeed_jobs.head(),
          "\n",
          len(indeed_jobs))

