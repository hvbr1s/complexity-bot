import hashlib
import json
import os
import re
from pathlib import Path
from tqdm.auto import tqdm
from collections import Counter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import tiktoken
from dotenv import load_dotenv

load_dotenv()

openai_key = os.environ['OPENAI_API_KEY']

################### HC CHUNKER ######################
class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata
        
    def to_dict(self):
        return {
            'page_content': self.page_content,
            'metadata': self.metadata
        }

def load_md_file(file_path):
    file_name = Path(file_path).stem
    print(f'File name: {file_name}')
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the source URL from the last line
    lines = content.split('\n')
    source_url = 'https://github.com/tpiliposian/Immunefi_bugfixes/blob/main/README.md'  # Default source
    if lines and lines[-2].startswith('Source:'):
        source_url = lines[-2].strip()[7:]  # Remove 'Source:' prefix
        # Add '/tree/master/docs/' to the source URL
        if 'github.com/Certora/Documentation/' in source_url:
            parts = source_url.split('github.com/Certora/Documentation/')
            source_url = f"{parts[0]}github.com/Certora/Documentation/tree/master/docs/{parts[1]}"
        content = '\n'.join(lines[:-2])  # Remove the source line from content

    title = file_name.upper()
    metadata = {
        'title': f'#TITLE: {title}.#',
        'source': source_url,
        'source-type': 'documentation'
    }

    text_without_tags = content
    text_with_collapsed_whitespace = re.sub(r'\s+', ' ', text_without_tags)
    return Document(page_content=text_with_collapsed_whitespace, metadata=metadata)

def load_files(directory_path):
    docs = []
    for file_name in os.listdir(directory_path):
        if not file_name.lower().endswith('.md'):
            continue  # Skip non-markdown files
        file_path = os.path.join(directory_path, file_name)
        doc = load_md_file(file_path)
        docs.append(doc)
    return docs

text_splitter = SemanticChunker(
    OpenAIEmbeddings(
        openai_api_key=openai_key,
        model='text-embedding-3-large',
        chunk_size=1024,
    )
)

# Define the length function
def tiktoken_len(text):
    # Initialize the tokenizer
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

def count_chars_in_json(file_name):
    # Read the json file
    with open(file_name, 'r') as f:
        data = json.load(f)

    # Initialize a counter
    char_counts = Counter()

    # Check if data is a list
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Get the text
                text = item.get('text', '')

                # Count the characters and update the overall counter
                char_counts.update(Counter(text))

    return char_counts

def run_chunker(output_directory_path: str = None, chunk_size: int = 1024, chunk_overlap: int = 0, minimum_chunk_size: int = 50):
    # Initialize the loader and load documents
    if not output_directory_path:
        pinecone_pipeline_root_directory = os.path.dirname(os.path.dirname(__file__))
        output_directory_path = os.path.join(pinecone_pipeline_root_directory, 'update_scripts')
    scraped_articles_folder = os.path.join(output_directory_path, 'md_output')
    output_json_file_path = os.path.join(output_directory_path, 'output.json')
    chunk_list = []  # list of chunks to be written to the json file

    # Process each document
    with open(output_json_file_path, 'w+', encoding='utf-8') as f:
        for file_name in tqdm(os.listdir(scraped_articles_folder)):
            if not file_name.lower().endswith('.md'):
                continue  # Skip non-markdown files
            file_path = os.path.join(scraped_articles_folder, file_name)
            doc = load_md_file(file_path)
            
            # Check if the document content is empty or invalid
            if not doc.page_content.strip():
                print(f"Skipping empty or invalid content in file: {file_name}")
                continue
            
            # Generate a unique ID for the document
            uid = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()[:12]

            try:
                chunks = text_splitter.create_documents([doc.page_content])
                for i, chunk in enumerate(chunks):
                    chunk_text = chunk.page_content  # Extract text from the Document object
                    entry = {
                        'source': doc.metadata['source'],
                        'source-type': doc.metadata['source-type'],
                        'title': doc.metadata['title'],
                        'id': f'{uid}-{i}',
                        'chunk-uid': uid,
                        'chunk-page-index': i,
                        'text': chunk_text,
                    }
                    chunk_list.append(entry)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
                continue
            
        json.dump(chunk_list, f, ensure_ascii=False)  # write the list of chunks to the json file

    # Character count
    counts = count_chars_in_json(output_json_file_path)

    # Compute total number of characters
    total_chars = sum(counts.values())
    print(f'Total characters: {total_chars}')
    return output_json_file_path

if __name__ == "__main__":
    run_chunker(chunk_size=1024)