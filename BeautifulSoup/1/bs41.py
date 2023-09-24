from bs4 import BeautifulSoup
import requests
import string
import json
main_link = 'https://subslikescript.com'
website = f"{main_link}/movies"
res = requests.get(website)

context = res.text
soup = BeautifulSoup(context, 'html.parser')
box = soup.find('article', class_='main-article')
# print(soup.prettify())
# title = box.find('h1').get_text()

# print(title)
# transcript = box.find(
#     'div', class_='full-script').get_text(strip=True, separator=' ')
# print(transcript)

# with open(f'{title}.txt', 'w', encoding='utf-8') as file:
#     file.write(transcript)


#################### FULL WEBSITE #######################
# links = []
# for link in box.find_all('a', href=True):
#     mylink = 'https://subslikescript.com/'+str(link['href'])
#     links.append(mylink)
# # print(links)
# for link in links[:10]:  # remove [:10] for total website
#     res = requests.get(link)
#     context = res.text
#     soup = BeautifulSoup(context, 'html.parser')
#     box = soup.find('article', class_='main-article')
#     title = box.find('h1').get_text()
#     # print(title)
#     transcript = box.find(
#         'div', class_='full-script').get_text(strip=True, separator=' ')
#     with open(f'{title}.txt', 'w', encoding='utf-8') as file:
#         file.write(transcript)


################ MULTIPLE PAGES (PAGINATION) #################
# alphabets = list(string.ascii_uppercase)
# for i in alphabets:
#     search_by_alpha = f'{main_link}/movies_letter-{alphabets[i]}'

#     pagination = soup.find('ul', class_='pagination')
#     pages = pagination.find_all('li', class_='pages-item')
#     last_page = pages[-2].text
search_by_alpha = f'{main_link}/movies_letter-A'

pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
data = []
links = []
for page in range(1, len(pages))[:3]:
    search_by_alpha = f'{main_link}/movies_letter-A?page={page}'
    res = requests.get(search_by_alpha)
    context = res.text
    soup = BeautifulSoup(context, 'html.parser')
    box = soup.find('article', class_='main-article')
    for link in box.find_all('a', href=True):
        mylink = 'https://subslikescript.com/'+str(link['href'])
        links.append(mylink)
    for link in links:
        try:
            res = requests.get(link)
            context = res.text
            soup = BeautifulSoup(context, 'html.parser')
            box = soup.find('article', class_='main-article')
            title = box.find('h1').get_text()
            # print(title)
            transcript = box.find(
                'div', class_='full-script').get_text(strip=True, separator=' ')
            # with open(f'{title}.txt', 'w', encoding='utf-8') as file:
            #     file.write(transcript)
            scraped_data = {
                'link': link,
                'title': title,
                'transcript': transcript,
            }
            data.append(scraped_data)
        except:
            print('link failed')
            print(link)
with open('movie_transcripts.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
