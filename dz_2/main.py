import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi


url_main = 'https://quotes.toscrape.com'
is_next = True
qoutes = []
links_about = set()
url_next = url_main
while is_next:
    response = requests.get(url_next)
    soup = BeautifulSoup(response.text, 'lxml')

    el_quotes = soup.find_all('div', class_='quote')
    for el_quote in el_quotes:
        el_text = el_quote.find('span', class_='text')
        el_author = el_quote.find('small', class_='author')
        el_about_link = el_quote.find('a', href=True)
        about_link = url_main + el_about_link['href']
        links_about.add(about_link)
        el_tags = el_quote.find_all('a', class_='tag')
        list_tags = []
        for el_tag in el_tags:
            list_tags.append(el_tag.text)
        qoutes.append(
            {
                "tags": list_tags,
                "author": el_author.text,
                "quote": el_text.text,
            }
        )
        
    li_next = soup.find('li', class_='next')
    if li_next:
        a_next = li_next.find("a")
        href = a_next["href"]
        url_next = f"https://quotes.toscrape.com{href}"
        print(url_next)
    else:
        is_next = False

with open('./dz_2/quotes.json', 'w', encoding='utf-8') as file:
    json.dump(qoutes, file, ensure_ascii=False, indent=2)

authors = []
for link_about in links_about:
    response = requests.get(link_about)
    soup = BeautifulSoup(response.text, 'lxml')
    el_author_title = soup.find('h3', class_='author-title')
    el_author_born_date = soup.find("span", class_="author-born-date")
    el_author_born_location = soup.find("span", class_="author-born-location")
    el_author_description = soup.find("div", class_="author-description")
    authors.append(
        {
            "fullname": el_author_title.text, 
            "born_date": el_author_born_date.text, 
            "born_location": el_author_born_location.text, 
            "description": el_author_description.text.strip()
        }
    )

with open('./dz_2/authors.json', 'w', encoding='utf-8') as file:
    json.dump(authors, file, ensure_ascii=False, indent=2)

client = MongoClient(
    "mongodb+srv://vitalii:12051987@tormalin.nrp1r.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.goit_ds_hw_03_dz2

with open('./dz_2/quotes.json', 'r', encoding='utf-8') as file:
    data_quotes = json.load(file)
    coll_quotes = db.quotes
    coll_quotes.insert_many(data_quotes)

    # result = coll_quotes.find({})
    # for el in result:
    #     print(el)

with open('./dz_2/authors.json', 'r', encoding='utf-8') as file:
    data_authors = json.load(file)
    coll_authors = db.authors
    coll_authors.insert_many(data_authors)