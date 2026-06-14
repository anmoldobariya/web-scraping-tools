import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", {"id": "ResultsContainer"})

job_elements = results.find_all("div", {"class":"card-content"})
list=[]
for job_element in job_elements:
    title_element = job_element.find("h2", {"class":"title"})
    company_element = job_element.find("h3", {"class":"company"})
    location_element = job_element.find("p", {"class":"location"})

    if 'python' in title_element.text.lower():
        list.append({title_element.text.strip(),company_element.text.strip(),location_element.text.strip()})
        # print(title_element.text.strip())
        # print(company_element.text.strip())
        # print(location_element.text.strip())
        # print()

print(len(list))
print(list)
