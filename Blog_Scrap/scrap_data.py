import requests
from bs4 import BeautifulSoup
import json
import time as T

# Define the headers with the user agent string for Chrome
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Send an HTTP request to the website with the headers included
url = 'https://dev.to'
response = requests.get(url, headers=headers)

print(response.status_code)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the data
posts = soup.find_all('div', {'class': 'crayons-story__body'})

# create a list of dictionaries to hold the data
data = []

# print(posts)
i = 0
for post in posts:
    i += 1
    title = post.find('h2', {'class': 'crayons-story__title'}).text.strip()
    author_image = post.find('div', {'class' : 'crayons-story__author-pic'}).find('a').find('img').get('src')
    author = post.find('a', {'class': 'crayons-story__secondary'}).text.strip()
    time = post.find('a', {'class' : 'crayons-story__tertiary'}).find('time').get("datetime")
    likes = post.find('a', {'class' : 'crayons-btn'}).text.lower().replace("reactions", "").strip()
    link = url + post.find('h2', {'class': 'crayons-story__title'}).find('a').get('href')
    try:
        response = requests.get(link)
        print(f"{i} -> {response.status_code}")
        soup = BeautifulSoup(response.content, 'html.parser')
        cover_image = soup.find('img', {'class' : 'crayons-article__cover__image'}).get('src')
        body = soup.find('div', {'class': 'crayons-article__body'}).text.strip()
        data.append({'id': i, "title": title, "author": author, "author_image": author_image, "time":time, "likes": likes, "link" : link, "cover_image":cover_image, "body":body})
    except :
        print(f"Error in {i}")
    
    
    #print(f"{i} -> {title[0:10]} by {author[0:10]} - {author_image[0:10]} ~ {time[0:10]} = {likes} > {link}")
    print("waiting for 5 sec.")
    T.sleep(5)

# write the data to a JSON file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f,  ensure_ascii=False)