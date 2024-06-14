import json
import os
import uuid  # Import the uuid library
from bs4 import BeautifulSoup

def extract_url(soup):
    # Attempt to extract URL from <meta> tags
    meta_tag = soup.find('meta', property='og:url')
    if meta_tag:
        return meta_tag['content']
    
    # Fallback to <link> tags
    link_tag = soup.find('link', rel='canonical')
    if link_tag:
        return link_tag['href']
    
    # Fallback to the first <a> tag
    a_tag = soup.find('a', href=True)
    if a_tag and a_tag['href'].startswith('http'):
        return a_tag['href']
    
    return None

def extract_content(html_file_path):
    # Load the HTML content from the provided file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Use extract_url function to dynamically find the page URL
    page_url = extract_url(soup)
    
    # Define a minimum word count for all text content
    min_words = 8

    # List to store the content of each targeted element
    content_chunks = []

    # Find all relevant elements including tables
    for tag in ['div', 'h1', 'h2', 'h3', 'p', 'tr']:
        elements = soup.find_all(tag)
        for element in elements:
            text_content = element.get_text(strip=True, separator=' ')
            # Check word count before processing the content
            if len(text_content.split()) < min_words:
                continue  # Skip content that does not meet the word count threshold

            # Use UUID for unique identifier
            unique_id = str(uuid.uuid4())
            content = {
                'id': unique_id,
                'content': text_content,
                'url': page_url
            }
            content_chunks.append(content)
            filename = f'chunks/{html_file_path}_{unique_id}.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(content, json_file, indent=4)

    return {'url': page_url, 'content': f'Content saved in {len(content_chunks)} JSON files in the chunks directory.'}

# Loop over each HTML file in the current directory
directory = '.'  # Current directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        html_file_path = os.path.join(directory, filename)
        extracted_content = extract_content(html_file_path)
        print(f'Processed {html_file_path}: {extracted_content["content"]}')
