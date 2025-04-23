import json
import requests
from bs4 import BeautifulSoup
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

quotes_json = json.dumps(qoutes, indent=2, ensure_ascii=False)
print(quotes_json)

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

authors_json = json.dumps(authors, indent=4, ensure_ascii=False)
print(authors_json)