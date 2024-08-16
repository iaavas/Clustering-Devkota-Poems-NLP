import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://wikisource.org/wiki/Author:%E0%A4%B2%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A5%8D%E0%A4%AE%E0%A5%80%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%A6%E0%A5%87%E0%A4%B5%E0%A4%95%E0%A5%8B%E0%A4%9F%E0%A4%BE'  
base_url = "https://wikisource.org/"


response = requests.get(url)
html_content = response.text


soup = BeautifulSoup(html_content, 'html.parser')


li_elements = soup.find_all('li')


results = []
for li in li_elements:
    
    title = li.get_text(strip=True)
    
    
    if title == "Authors":
        break
    if title != "Muna Madan":
        
        a_tag = li.find('a')
        if a_tag and a_tag.get('href'):
            link = a_tag['href']
            
            results.append({'title': title, 'link': base_url+link})

            

results = results[2:]

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {url}")
        return None

def extract_poem_content(link):
    poem_html = fetch_html(link)
    soup = BeautifulSoup(poem_html, 'html.parser')
    poem_div = soup.find('div', class_='poem')
    
    if poem_div:
        return "\n".join([p.get_text(strip=True) for p in poem_div.find_all('p')])
    return ""

poems_data = []

for poem in results:
    title = poem['title']  
    content = extract_poem_content(poem['link'])
    poems_data.append({'Title': title, 'Content': content})

df = pd.DataFrame(poems_data)
df.to_csv('nepali_poems.csv', index=False)

print("Poems scraped and saved to nepali_poems.csv")



