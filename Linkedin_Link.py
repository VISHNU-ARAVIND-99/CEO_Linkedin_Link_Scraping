from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd


def craft_scraping(company_name, ceo_name, k):
    driver.get("https://www.google.com/")
    time.sleep(2)
    search1 = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    if "University" not in company_name and "College" not in company_name:
        search1.send_keys(f'{company_name} + {ceo_name} + CEO + LinkedIn + Profile')
    else:
        search1.send_keys(f'{company_name} + {ceo_name} + President + LinkedIn + Profile')
    search1.send_keys()
    time.sleep(2)
    search1.send_keys(Keys.RETURN)
    if k == 0:
        time.sleep(60)
    else:
        time.sleep(3)

    source = BeautifulSoup(driver.page_source, "html.parser")

    links = [company_name, ceo_name]
    count = 0
    # yuRUbf

    info = source.find_all('div', class_='yuRUbf')
    for div in info:
        a_tags = div.find_all('a')
        links.extend([a.get('href') for a in a_tags if a.get('href')])
        count += 1
        if count >= 5:
            break
    return links


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

list_of_list = []
with open('company.txt', 'r') as file:
    links = file.readlines()
name_list = [x.strip() for x in links]

with open('CEO_name.txt', 'r') as file:
    name = file.readlines()
CEO_name = [x.strip() for x in name]


out = 0
for k in range(len(name_list)):
    list_of_list.append(craft_scraping(company_name=name_list[k], ceo_name=CEO_name[k], k=k))
    out += 1
    print(out)

df = pd.DataFrame(list_of_list)
df.to_excel('CEO_LinkedIn_Link_Scraping_out.xlsx', index=False)