import os
import glob
import requests
from dotenv import load_dotenv
import logging
import json
import time
from bs4 import BeautifulSoup

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Configuration settings
CONFIG = {
    "api_base_url": os.getenv('API_BASE_URL', 'https://api.cloud.llamaindex.ai/api/parsing'),
    "api_key": os.getenv('LLAMA_PARSE_KEY'),
    "input_dir": os.getenv('INPUT_DIR', './html_output'),
    "output_dir": os.getenv('OUTPUT_DIR', './md_output'),
}

def extract_source_url(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        meta_source = soup.find('meta', attrs={'name': 'source'})
        if meta_source:
            return meta_source.get('content')
    return None

def upload_file_and_get_job_id(file_path):
    url = f"{CONFIG['api_base_url']}/upload"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {CONFIG['api_key']}",
    }
    files = {'file': (os.path.basename(file_path), open(file_path, 'rb'), 'text/html')}
    response = requests.post(url, headers=headers, files=files)
    print(response.json())
    if response.status_code == 200:
        job_id = response.json().get('id')
        logging.info(f"File uploaded successfully: {file_path}, job_id: {job_id}")
        return job_id
    else:
        logging.error(f"Failed to upload file: {file_path}, HTTP status code: {response.status_code}")
        return None

def check_job_status(job_id):
    url = f"{CONFIG['api_base_url']}/job/{job_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {CONFIG['api_key']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        logging.error(f"Job ID {job_id} not found. HTTP status code: 404")
        return 'NOT FOUND'
    elif response.status_code != 200:
        logging.error(f"Failed to fetch job status for {job_id}. HTTP status code: {response.status_code}")
        return 'FAILED'
    try:
        response_data = response.json()
        status = response_data.get('status')
        logging.info(f"Job status for {job_id}: {status}")
        return status
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON response for job {job_id}. Response text: {response.text}")
        return 'FAILED'

def download_result(job_id, output_path, source_url):
    url = f"{CONFIG['api_base_url']}/job/{job_id}/result/markdown"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {CONFIG['api_key']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        markdown_content = response_json.get('markdown', '')  # Extract markdown content
        if markdown_content:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(markdown_content)
                if source_url:
                    output_file.write(f"\n\nSource: {source_url}\n")
            logging.info(f"Markdown result for job {job_id} written to {output_path}")
        else:
            logging.error(f"No markdown content found for job {job_id}")
    else:
        logging.error(f"Failed to download result for job {job_id}. HTTP status code: {response.status_code}")

def process_files():
    html_files = glob.glob(os.path.join(CONFIG['input_dir'], "*.html"))
    for html_file in html_files:
        logging.debug(f"Processing file {html_file}")
        source_url = extract_source_url(html_file)
        job_id = upload_file_and_get_job_id(html_file)
        if job_id:
            logging.info(f"Submitted job {job_id} for file {html_file}")
            status = check_job_status(job_id)
            while status == 'PENDING':
                logging.info(f"Job {job_id} is still processing. Current status: {status}. Waiting for 5 seconds.")
                time.sleep(10)
                status = check_job_status(job_id)
            if status == 'SUCCESS':
                result_path = os.path.join(CONFIG['output_dir'], os.path.basename(html_file).replace('.html', '.md'))
                download_result(job_id, result_path, source_url)
            elif status in ['FAILED', 'NOT FOUND']:
                logging.error(f"Job {job_id} failed or not found. Status: {status}")
        else:
            logging.error(f"Failed to submit job for file {html_file}")

if __name__ == '__main__':
    process_files()