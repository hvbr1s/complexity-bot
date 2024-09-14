import os
from pathlib import Path
import markdown2
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def markdown_to_html(md_content):
    """Convert markdown content to HTML using markdown2."""
    return markdown2.markdown(md_content)

def extract_title(md_content):
    """Extract the first heading as title, considering different heading levels."""
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith(('#', '##', '###', '####', '#####', '######')):
            return line.lstrip('#').strip()
    return "No Title Found"

def embed_metadata(html_content, url, title, text):
    """Embed metadata into HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.html is None:
        html_tag = soup.new_tag('html')
        body_tag = soup.new_tag('body')
        html_tag.append(body_tag)
        soup.append(html_tag)
        body_tag.append(BeautifulSoup(html_content, 'html.parser'))

    head = soup.new_tag('head')
    soup.html.insert(0, head)
    
    # Add metadata tags
    meta_url = soup.new_tag('meta', attrs={"name": "url", "content": url})
    meta_title = soup.new_tag('meta', attrs={"name": "title", "content": title})
    meta_text = soup.new_tag('meta', attrs={"name": "text", "content": text})
    meta_source = soup.new_tag('meta', attrs={"name": "source", "content": url})
    
    soup.head.append(meta_source)  # Add source URL first
    soup.head.append(meta_url)
    soup.head.append(meta_title)
    soup.head.append(meta_text)
    
    # Add visible source information at the top of the body
    source_info = soup.new_tag('div')
    source_info['style'] = 'background-color: #f0f0f0; padding: 10px; margin-bottom: 20px;'
    source_info.string = f"Source: {url}"
    soup.body.insert(0, source_info)
    
    return str(soup)

def process_file(file_path, base_path, output_dir):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = markdown_to_html(md_content)
        title = extract_title(md_content)
        url = f"https://github.com/tpiliposian/Immunefi_bugfixes/blob/main/{file_path.relative_to(base_path).as_posix()}" # update this to the correct url
        text = BeautifulSoup(html_content, 'html.parser').get_text()[:200]

        final_html = embed_metadata(html_content, url, title, text)
        
        # Generate a unique filename based on the original path
        unique_filename = '_'.join(file_path.relative_to(base_path).parts).replace('.md', '.html')
        output_file_path = output_dir / unique_filename
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(final_html)

        return f"Processed {file_path} to {output_file_path}"
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def process_markdown_files(base_path, output_dir):
    """Process all markdown files found in the directory tree rooted at base_path."""
    base_path = Path(base_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_files = list(base_path.rglob('*.md'))
    
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, file, base_path, output_dir) for file in markdown_files]
        
        for future in tqdm(as_completed(futures), total=len(markdown_files), desc="Processing files"):
            print(future.result())

def main():
    base_path = Path('./raw_docs')
    output_dir = Path('html_output')
    process_markdown_files(base_path, output_dir)

if __name__ == "__main__":
    main()