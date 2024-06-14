import json
import os
from bs4 import BeautifulSoup

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

    content_chunks = []
    unique_id = 1  
    min_words = 3

    for tag in ['div', 'h1', 'h2', 'h3', 'p']:
        elements = soup.find_all(tag)
        for element in elements:
            if (tag == 'div' and element.get('id') and 
                (element['id'].startswith('accordion') or element['id'].startswith('collapse'))) or tag in ['h1', 'h2', 'p']:
                text_content = element.get_text(strip=True, separator=' ')
                if text_content:
                    content = {
                        'id': unique_id,
                        'content': text_content,
                        'url': page_url
                    }
                    content_chunks.append(content)
                
                    filename = f'chunks/chunk_{unique_id}.json'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(content, json_file, indent=4)
                    unique_id += 1  
            elif tag == 'h3':
                text_content = element.get_text(strip=True, separator=' ')
                if text_content and len(text_content.split()) > min_words:
                    content = {
                        'id': unique_id,
                        'text_content': text_content,
                        'url': page_url
                    }
                    content_chunks.append(content)

                    filename = f'chunks/chunk_{unique_id}.json'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(content, json_file, indent=4)
                    unique_id += 1

    return {'url': page_url, 'content': f'Content saved in {len(content_chunks)} JSON files in the chunks directory.'}

html_file_path = 'opleidingen_toegepaste-informatica.html'
extracted_content = extract_content(html_file_path)
print(extracted_content['content'])
