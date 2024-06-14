import os
import json
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_logical_chunks(soup):
    
    sections = []
    current_section = ""

    for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
        text = element.get_text(separator=' ', strip=True)
        if element.name in ['h1', 'h2', 'h3']:
            if current_section:
                sections.append(current_section.strip())
            current_section = text + "\n"
        else:
            if element.name == 'p' and not text.strip():
                continue 
            current_section += text + " "
    
    if current_section:
        sections.append(current_section.strip())
    
    return sections

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

chunk_size = 900
chunk_overlap = 100

text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

output_directory = 'chunks_json_smaller'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

global_id_counter = 1

for file_name in os.listdir('.'):
    if file_name.endswith('.html'):
        with open(file_name, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        for script in soup(['script', 'style']):
            script.extract()
        url = extract_url(soup)
        if not url:
            url = f"https://www.erasmushogeschool.be/notfound" 

        # Extract logical chunks
        logical_chunks = extract_logical_chunks(soup)

        # Split logical chunks
        final_chunks = []
        for chunk in logical_chunks:
            split_chunks = text_splitter.split_text(chunk)
            final_chunks.extend(split_chunks)

        # Filter out unnecessary small or empty chunks
        filtered_chunks = [chunk for chunk in final_chunks if len(chunk.strip()) > 50]

        # Save each chunk as a separate JSON file
        for chunk in filtered_chunks:
            chunk_data = {
                "id": global_id_counter,
                "url": url,
                "content": chunk
            }
            json_filename = os.path.join(output_directory, f'{file_name}_chunk_{global_id_counter}.json')
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(chunk_data, json_file, indent=2, ensure_ascii=False)
            print(f"Saved chunk {global_id_counter} from file {file_name} to {json_filename}")
            global_id_counter += 1

print(f"Chunks saved to directory: {output_directory}")
