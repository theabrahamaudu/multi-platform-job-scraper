from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import math

# Initialize Selenium web driver
wd = webdriver.Chrome(executable_path='../chromedriver.exe')

# Initialize job parameters to be scraped
job_id= []
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
            if n < 5:
                job_title0 = job.find_element(By.XPATH,
                                              f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div[2]/div/div[1]/a/p').get_attribute(
                    'innerText')
                job_title.append(job_title0)

                company_name0 = job.find_element(By.XPATH,
                                                 f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div[2]/div/p[1]').get_attribute(
                    'innerText')
                company_name.append(company_name0)

                location0 = job.find_element(By.XPATH,
                                             f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div[2]/div/div[2]/span[1]').get_attribute(
                    'innerText')
                location.append(location0)

                date0 = job.find_element(By.XPATH,
                                         f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[2]/p').get_attribute(
                    'innerText')
                date.append(date0)

                job_link0 = job.find_element(By.XPATH,
                                             f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div[2]/div/div[1]/a').get_attribute(
                    'href')
                job_link.append(job_link0)

                job_id0 = "Not available on Jobberman"
                job_id.append(job_id0)


            else:
                job_title0 = job.find_element(By.XPATH,
                                              f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div/div/div[1]/a/p').get_attribute(
                    'innerText')
                job_title.append(job_title0)

                company_name0 = job.find_element(By.XPATH,
                                                 f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div/div/p[1]').get_attribute(
                    'innerText')
                company_name.append(company_name0)

                location0 = job.find_element(By.XPATH,
                                             f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div/div/div[2]/span[1]').get_attribute(
                    'innerText')
                location.append(location0)

                date0 = job.find_element(By.XPATH,
                                         f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div/p').get_attribute(
                    'innerText')
                date.append(date0)

                job_link0 = job.find_element(By.XPATH,
                                             f'/html/body/main/section/div[2]/div[2]/div[1]/div[{n}]/div[1]/div/div/div[1]/a').get_attribute(
                    'href')
                job_link.append(job_link0)

                job_id0 = "Not available on Jobberman"
                job_id.append(job_id0)
        except Exception as e:
            continue


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
                job_summary = wd.find_element(By.CSS_SELECTOR,
                                              "#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div:nth-child(4)").get_attribute(
                    'innerText')
                job_req = wd.find_element(By.CSS_SELECTOR,
                                          "#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div:nth-child(5)").get_attribute(
                    'innerText')
                job_description = job_summary + "\n\n" + job_req
                job_desc.append(job_description)
            except:
                job_desc.append('NA')

            try:
                # Seniority level
                seniority_level = wd.find_element(By.CSS_SELECTOR,
                                                  '#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div:nth-child(4) > ul > li:nth-child(2) > span.pb-1.text-gray-500').get_attribute(
                    'innerText')
                seniority.append(seniority_level)
            except:
                seniority.append('NA')

            try:
                # Employment type
                employment_type = wd.find_element(By.CSS_SELECTOR,
                                                  "#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div.flex.flex-wrap.justify-start.pt-5.pb-2.px-4.w-full.border-b.border-gray-300.md\:flex-nowrap.md\:px-5 > div.w-full.text-gray-500 > div.mt-3 > span > a").get_attribute(
                    'innerText')
                emp_type.append(employment_type)
            except:
                emp_type.append('NA')

            try:
                # Job function
                job_function = wd.find_element(By.CSS_SELECTOR,
                                               "#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div.flex.flex-wrap.justify-start.pt-5.pb-2.px-4.w-full.border-b.border-gray-300.md\:flex-nowrap.md\:px-5 > div.w-full.text-gray-500 > h2:nth-child(3) > a").get_attribute(
                    'innerText')
                job_func.append(job_function)
            except:
                job_func.append('NA')

            try:
                # Job industry
                industries = wd.find_element(By.CSS_SELECTOR,
                                             "#tab1 > div.flex.flex-col.rounded-lg.border-gray-300.md\:border.hover\:border-gray-400.md\:mx-0 > article > div.flex.flex-wrap.justify-start.pt-5.pb-2.px-4.w-full.border-b.border-gray-300.md\:flex-nowrap.md\:px-5 > div.w-full.text-gray-500 > div:nth-child(5) > a").get_attribute(
                    'innerText')
                ind.append(industries)
            except:
                ind.append('NA')

        except Exception as e:
            print('There was an error scraping Page ', page, ': ', e)
            job_desc.append("NA")
            seniority.append("NA")
            emp_type.append("NA")
            job_func.append("NA")
            ind.append("NA")


def selenium_scrape(search_url, num_of_jobs):
    num_of_pages = math.ceil(num_of_jobs / 14)

    for i in range(num_of_pages):
        i = i + 1
        page = "?page=" + str(i)
        url = search_url + page

        wd.get(url)
        jobs_lists = wd.find_element(By.XPATH, "/html/body/main/section/div[2]/div[2]/div[1]")
        jobs = jobs_lists.find_elements(By.CLASS_NAME, "mx-5")  # return a list

        extract_job_card_info(jobs)

        if i == 1:
            start_at = 0
        else:
            start_at = 14 * (i - 1)

        extract_job_page_info(job_link, start_at)

    data = [job_id, job_title, company_name, location, date,
            job_link, job_desc, seniority, emp_type, job_func, ind]

    columns = ["job_id", "job_title", "company_name", "location", "date",
               "job_link", "job_desc", "seniority", "emp_type", "job_func", "ind"]

    jobberman_jobs_dataframe = pd.DataFrame(data, columns).transpose()

    return jobberman_jobs_dataframe


if __name__ == "__main__":
    search_url = "https://www.jobberman.com/jobs"
    num_of_jobs = 20

    jobberman = selenium_scrape(search_url, num_of_jobs)

    print(jobberman.head(),
          "\n",
          len(jobberman))