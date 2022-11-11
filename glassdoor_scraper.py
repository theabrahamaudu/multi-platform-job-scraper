from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time as t
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
            job_id0 = job.find_element(By.XPATH, f'//*[@id="MainCol"]/div[1]/ul/li[{n}]').get_attribute('data-id')
            job_id.append(job_id0)

            job_title0 = job.find_element(By.XPATH, f'//*[@id="MainCol"]/div[1]/ul/li[{n}]/div[2]/a').get_attribute(
                'innerText')
            job_title.append(job_title0)

            company_name0 = job.find_element(By.XPATH,
                                             f'//*[@id="MainCol"]/div[1]/ul/li[{n}]/div[2]/div[1]/a').get_attribute(
                'innerText')
            company_name.append(company_name0)

            location0 = job.find_element(By.XPATH, f'//*[@id="MainCol"]/div[1]/ul/li[{n}]/div[2]/div[2]/span').text
            location.append(location0)

            date0 = job.find_element(By.XPATH,
                                     f'//*[@id="MainCol"]/div[1]/ul/li[{n}]/div[2]/div[2]/div/div[2]').get_attribute(
                'innerText')
            date.append(date0)

            job_link0 = job.find_element(By.XPATH,
                                         f'//*[@id="MainCol"]/div[1]/ul/li[{n}]/div[2]/div[1]/a').get_attribute('href')
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
            wd.get(link)  # half page
            wd.find_element(By.CSS_SELECTOR, '#JobDescriptionContainer > div.css-1rzz8ht.ecgq1xb2').click()  # full page

            job_types_list = ["Full-time", "Part-time", "Contract", "Internship", "Temporary", "Apprentice/Trainee",
                              "Entry Level"]

            try:
                # Get job description
                job_description = wd.find_element(By.CLASS_NAME, "desc").get_attribute('innerText')
                job_desc.append(job_description)
            except:
                job_desc.append('NA')

            # Seniority level
            seniority_level = 'Unavailable on Glassdoor'
            seniority.append(seniority_level)

            try:
                # Employment type
                for jt in job_types_list:
                    if f"Job Type: {jt}" in job_description:
                        emp_type.append(jt)
                        break
                    elif f"Job Types: {jt}" in job_description:
                        emp_type.append(jt)
                        break
            except:
                emp_type.append('NA')

            # Job function
            job_function = 'Unavailable on Glassdoor'
            job_func.append(job_function)

            # Job industry
            industries = 'Unavailable on Glassdoor'
            ind.append(industries)

        except Exception as e:
            print('There was an error scraping Page ', page, ': ', e)
            job_desc.append("NA")
            seniority.append("NA")
            emp_type.append("NA")
            job_func.append("NA")
            ind.append("NA")


def selenuim_scrape(url, num_of_jobs):
    states = ["Lagos", "Federal Capital Territory"]
    #     states = ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River",
    #               "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina",
    #               "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    #               "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "Federal Capital Territory"]
    i = 0
    for state in states:
        try:
            wd.get(url)

            land_page_search_box = wd.find_element(By.CSS_SELECTOR, "#sc\.location")
            land_page_search_box.send_keys(f"{state} (Nigeria)")
            land_page_search_box.send_keys(Keys.RETURN)
            t.sleep(3)
            wd.find_element(By.XPATH, '//*[@id="Discover"]/div/div/div[1]/div[1]/div[3]/a').click()  # load first page
            t.sleep(3)

            # Collect job cards
            jobs_lists = wd.find_element(By.CSS_SELECTOR, "#MainCol > div:nth-child(1) > ul")
            jobs = jobs_lists.find_elements(By.TAG_NAME, "li")  # return a list
            extract_job_card_info(jobs)
        except Exception as e:
            print(f"Error scraping {state} state jobs:\n", e)
            continue

        if num_of_jobs == "all":
            num_of_pages = wd.find_element(By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[2]').get_attribute('innerText')
            num_of_pages = num_of_pages.split()[-1]
        else:
            num_of_pages = math.ceil(num_of_jobs / 30)

        if num_of_pages == 0:
            num_of_pages = 1
        else:
            pass

        loaded_pages = 1
        while loaded_pages < num_of_pages:
            try:
                # Load next page
                ActionChains(wd).send_keys(Keys.ESCAPE).perform()
                wd.find_element(By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[1]/button[7]/span').click()  # next_page
                t.sleep(3)

                # Collect job cards
                jobs_lists = wd.find_element(By.CSS_SELECTOR, "#MainCol > div:nth-child(1) > ul")
                jobs = jobs_lists.find_elements(By.TAG_NAME, "li")  # return a list
                extract_job_card_info(jobs)
                loaded_pages += 1
                i += 1
            except:
                continue

    if len(job_link) == 0:
        start_at = 0
    else:
        start_at = 30 * i

    extract_job_page_info(job_link, start_at)

    data = [job_id, job_title, company_name, location, date,
            job_link, job_desc, seniority, emp_type, job_func, ind]

    columns = ["job_id", "job_title", "company_name", "location", "date",
               "job_link", "job_desc", "seniority", "emp_type", "job_func", "ind"]

    glassdoor_jobs_dataframe = pd.DataFrame(data, columns).transpose()

    return glassdoor_jobs_dataframe


if __name__ == "__main__":
    search_url = "https://www.glassdoor.com/Job"
    num_of_jobs = 25
    glassdoor_jobs = selenuim_scrape(url=search_url,
                                     num_of_jobs=num_of_jobs)

    print(glassdoor_jobs.head(),
          "\n",
          len(glassdoor_jobs))