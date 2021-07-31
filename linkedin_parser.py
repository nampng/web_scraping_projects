from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

url = "https://www.indeed.com/jobs?q=software%20engineer&l=Texas&vjk=34f268edad80901b"

results = {}
job_count = 0

for page_number in range(2, 6):
    print(f"FINDING RESULTS FOR PAGE {page_number - 1}")
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    job_card_container = soup.find("div", id="mosaic-provider-jobcards")
    job_cards = job_card_container.find_all("a", class_="tapItem")

    job_card_container.findChild()

    for job in job_cards:
        job_count += 1

        job_title = job.find("h2", class_="jobTitle")
        job_title = job_title.findChild("span", recursive=False).string

        company_name = job.find("span", class_="companyName")
        company_name = company_name.a
        if company_name:
            company_name = company_name.string
        else:
            company_name = None

        salary = job.find("span", class_="salary-snippet")

        if salary:
            salary = salary.string
        else:
            salary = None

        print(f"Company: {company_name}\nJob: {job_title}\nSalary: {salary}\n\n")

        if company_name:
            if company_name in results:
                results[company_name].append([f"Job: {job_title}", f"Salary: {salary}"])
            else:
                results[company_name] = [ [f"Job: {job_title}", f"Salary: {salary}"] ]

    
    nav_buttons = soup.find("ul", class_="pagination-list")
    nav_buttons = nav_buttons.find_all("li")
    for btn in nav_buttons:
        anchor = btn.find("a")
        if anchor:
            if anchor["aria-label"] == str(page_number):
                url = f"https://www.indeed.com{anchor['href']}"
                break
    
    time.sleep(5)

print(f"{job_count} jobs found.")
print(results)
    
