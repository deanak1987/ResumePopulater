from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import re


def fetch_job_posting(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    print("Loading webpage.")
    driver.get(url)

    if "indeed" in url:
        print("Waiting for security verification.")
        time.sleep(10)  # Wait for the page to load fully
    else:
        time.sleep(3)  # Wait for the page to load fully

    html = driver.page_source
    driver.quit()

    return html


def parse_job_details(html, url):
    soup = BeautifulSoup(html, "html.parser")
    domain = urlparse(url).netloc

    job_details = {
        "Job Title": None,
        "Company Name": None,
        "Location": None,
        "Job Type": None,
        "Job Description": None,
        "Responsibilities": None,
        "Requirements": None,
        "Preferred Qualifications": None,
        "Technologies": None,
        "Soft Skills": None,
        "Salary Range": None,
        "Application Deadline": None,
        "Application URL": url,
        "Posting Date": None,
        "Job ID": None,
        "Hiring Manager": None,
        "Hiring Address": None,
    }
    print("Scraping details...")
    if "indeed.com" in domain:
        job_details["Job Title"] = (
            soup.find("h1", class_="jobsearch-JobInfoHeader-title").text
            if soup.find("h1", class_="jobsearch-JobInfoHeader-title")
            else None
        )
        job_details["Company Name"] = (
            soup.find("div", class_="jobsearch-CompanyInfoContainer").text
            if soup.find("div", class_="jobsearch-CompanyInfoContainer")
            else None
        )
        job_details["Job Description"] = (
            soup.find("div", class_="jobsearch-JobComponent-description").text
            if soup.find("div", class_="jobsearch-JobComponent-description")
            else None
        )

    elif "governmentjobs.com" in url:
        job_details["Job Title"] = (
            soup.find("h2", class_="entity-title").text.strip()
            if soup.find("h2", class_="entity-title")
            else None
        )
        job_details["Location"] = (
            soup.find("p", class_="job-location").text.strip()
            if soup.find("p", class_="job-location")
            else None
        )
        job_details["Company Name"] = (
            soup.find("div", class_="agency-info agency-name").find("dd").text.strip()
            if soup.find("div", class_="agency-info agency-name")
            else None
        )

        dt_elements = soup.find_all("dt")
        for dt in dt_elements:
            if "Position Description" in dt.get_text():
                dd = dt.find_next_sibling("dd")
                if dd:

                    details = [
                        line.strip()
                        for line in dd.get_text("\n").split("\n")
                        if line.strip()
                    ]  # dd.get_text(strip=False)
                    if "Responsibilities Include:" in details:
                        index = details.index("Responsibilities Include:")
                        job_details["Job Description"] = details[:index]
                        job_details["Responsibilities"] = details[index + 1 :]
                    elif any("with any of the following:" in itm for itm in details):
                        index = next(
                            i
                            for i, itm in enumerate(details)
                            if "with any of the following:" in itm
                        )
                        job_details["Job Description"] = details[:index]
                        job_details["Responsibilities"] = details[index + 1 :]
                    else:
                        job_details["Job Description"] = details
            if "Qualifications" in dt.get_text():
                dd = dt.find_next_sibling("dd")
                if dd:
                    job_details["Requirements"] = [
                        line.strip()
                        for line in dd.get_text("\n").split("\n")
                        if line.strip()
                    ]  # dd.get_text(strip=False)
            if "Selection Process & Supplemental Information" in dt.get_text():
                dd = dt.find_next_sibling("dd")
                if dd:
                    if "This recruitment is being managed by" in dd.get_text():
                        match = re.search(
                            r"This recruitment is being managed by (\w+ \w+)",
                            dd.get_text(strip=True),
                        )
                        if match:
                            job_details["Hiring Manager"] = match.group(1)
            if "Address" in dt.get_text():
                dd = dt.find_next_sibling("dd")
                if dd:
                    job_details["Hiring Address"] = [
                        line.strip()
                        for line in dd.get_text("\n").split("\n")
                        if line.strip()
                    ]
            if "Knowledge & Skills" in dt.get_text():
                dd = dt.find_next_sibling("dd")
                if dd:
                    job_details["Soft Skills"] = [
                        line.strip()
                        for line in dd.get_text("\n").split("\n")
                        if line.strip()
                    ]

        # job_details["Job Description"] = soup.find("div", id="details-info", class_="tab-pane active fr-view").find(
        #     "dd").text.strip() if soup.find("div", id="details-info", class_="tab-pane active fr-view") else None

        job_type_p = soup.find(string=lambda text: text and "Job Type" in text)
        if job_type_p:
            job_details["Job Type"] = job_type_p.text.strip()
            # Navigate to the parent's sibling div that contains the <p>
            job_type_container = job_type_p.find_parent(
                "div", class_="span4"
            ).find_next_sibling("div", class_="span8")
            job_details["Job Type"] = (
                job_type_container.find("p").text.strip()
                if job_type_container and job_type_container.find("p")
                else None
            )
        else:
            job_details["Job Type"] = None

        job_num_p = soup.find(string=lambda text: text and "Job Number" in text)
        if job_num_p:
            job_details["Job ID"] = job_num_p.text.strip()
            # Navigate to the parent's sibling div that contains the <p>
            job_num_container = job_num_p.find_parent(
                "div", class_="span4"
            ).find_next_sibling("div", class_="span8")
            job_details["Job ID"] = (
                job_num_container.find("p").text.strip()
                if job_num_container and job_num_container.find("p")
                else None
            )
        else:
            job_details["Job ID"] = None

        deadline_p = soup.find(string=lambda text: text and "Closing Date" in text)
        if deadline_p:
            job_details["Application Deadline"] = deadline_p.text.strip()
            # Navigate to the parent's sibling div that contains the <p>
            deadline_type_container = deadline_p.find_parent(
                "div", class_="span4"
            ).find_next_sibling("div", class_="span8")
            job_details["Application Deadline"] = (
                deadline_type_container.find("p").text.strip()
                if deadline_type_container and deadline_type_container.find("p")
                else None
            )
        else:
            job_details["Application Deadline"] = None

        salary_div = soup.find("div", id="salary-label-id", class_="term-description")
        if salary_div:
            # Navigate to the parent's sibling div that contains the <p>
            salary_container = salary_div.find_parent(
                "div", class_="span4"
            ).find_next_sibling("div", class_="span8")
            job_details["Salary Range"] = (
                salary_container.find("p").text.strip()
                if salary_container and salary_container.find("p")
                else None
            )
        else:
            job_details["Salary Range"] = None
    return job_details


def scrape_job(url):
    html = fetch_job_posting(url)
    if not html:
        return None

    job_data = parse_job_details(html, url)
    return job_data


# # Example usage
# if __name__ == "__main__":
#     job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"  # Replace with actual job URL
#     job_info = scrape_job(job_url)
#
# for item in job_info:
#     print(f"{item}: {job_info[item]}")