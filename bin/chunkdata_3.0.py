import json
import os
from bs4 import BeautifulSoup
import uuid 

def extract_url(soup):

    meta_tag = soup.find('meta', property='og:url')
    if meta_tag:
        return meta_tag['content']
    
    link_tag = soup.find('link', rel='canonical')
    if link_tag:
        return link_tag['href']
    
    a_tag = soup.find('a', href=True)
    if a_tag and a_tag['href'].startswith('http'):
        return a_tag['href']
    
    return None

def extract_content(html_file_path):
    
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    page_url = extract_url(soup)
    min_words = 8
    content_chunks = []

    for tag in ['div', 'h1', 'h2', 'h3', 'p', 'tr']:
        elements = soup.find_all(tag)
        for element in elements:
            text_content = element.get_text(strip=True, separator=' ')
            if len(text_content.split()) < min_words:
                continue  

            if tag == 'tr':
                tds = element.find_all('td')
                combined_text = ' '.join(td.get_text(strip=True, separator=' ') for td in tds)
                if combined_text:
                    content = {
                        'id': str(uuid.uuid4()), 
                        'content': combined_text,
                        'url': page_url
                    }
                    content_chunks.append(content)
                    filename = f'chunks/{html_file_path}_{content["id"]}.json'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(content, json_file, indent=4)
            elif (tag == 'div' and element.get('id') and 
                (element['id'].startswith('accordion') or element['id'].startswith('collapse'))) or tag in ['h1', 'h2', 'h3', 'p']:
                content = {
                    'id': str(uuid.uuid4()),  
                    'content': text_content,
                    'url': page_url
                }
                content_chunks.append(content)
                filename = f'chunks/{html_file_path}_{content["id"]}.json'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump(content, json_file, indent=4)

    return {'url': page_url, 'content': f'Content saved in {len(content_chunks)} JSON files in the chunks directory.'}

html_file_path = 'opleidingen_toegepaste-informatica.html'
extracted_content = extract_content(html_file_path)
print(extracted_content['content'])
