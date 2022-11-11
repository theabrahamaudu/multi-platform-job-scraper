from multiprocessing import Process
import concurrent.futures
import glassdoor_scraper
import indeed_scraper
import jobberman_scraper
import linkedin_scraper
import pandas as pd

with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__=="__main__":

        # LinkedIn Jobs
        # linkedin_url = "https://www.linkedin.com/jobs/search?keywords=&location=Nigeria&geoId=" \
        #       "105365761&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
        #
        # linkedin_number_of_jobs = 25
        #
        # jobs = linkedin_scraper.selenium_scrape(url=linkedin_url, no_of_jobs=linkedin_number_of_jobs)
        # selenium_job_details = linkedin_scraper.selenium_job_details(jobs=jobs)
        # bs4_job_details = linkedin_scraper.bs4_job_details(job_link=selenium_job_details[5])
        # linkedin_jobs = linkedin_scraper.jobs_dataframe(selenium_job_details=selenium_job_details,
        #                                 bs4_job_details=bs4_job_details)

        # Indeed Jobs
        indeed_url = "https://ng.indeed.com/jobs?q=&l=Nigeria&from=searchOnHP&vjk=701c24acfea16b1d"
        indeed_num_of_jobs = 25
        # indeed_jobs = indeed_scraper.selenium_scrape(search_url=indeed_url,
        #                                              num_of_jobs=indeed_num_of_jobs)

        # Glassdoor Jobs
        glassdoor_url = "https://www.glassdoor.com/Job"
        glassdoor_num_of_jobs = 25
        # glassdoor_jobs = glassdoor_scraper.selenuim_scrape(url=glassdoor_url,
        #                                  num_of_jobs=glassdoor_num_of_jobs)

        # Jobberman Jobs
        jobberman_url = "https://www.jobberman.com/jobs"
        jobberman_num_of_jobs = 20
        #
        # jobberman = jobberman_scraper.selenium_scrape(jobberman_url, jobberman_num_of_jobs)

        jobberman = executor.submit(jobberman_scraper.selenium_scrape, jobberman_url, jobberman_num_of_jobs)
        indeed = executor.submit(indeed_scraper.selenium_scrape, indeed_url, indeed_num_of_jobs)

        jobberman_jobs = jobberman.result()
        indeed_jobs = indeed.result()

        print(jobberman_jobs.head(),
              "\n",
              len(jobberman_jobs))
        print(indeed_jobs.head(),
              "\n",
              len(indeed_jobs))




