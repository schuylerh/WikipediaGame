import time
import requests
from bs4 import BeautifulSoup
import re
from collections import deque
import heapq
from collections import Counter
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

TIMEOUT = 999999  # time limit in seconds for the search
stop_search = False  # control variable for stopping the search

def stop_searching():
    global stop_search
    stop_search = True

def preprocess_text(text):
    "preprocess the text by converting to lowercase, removing punctuation, and removing common words"
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

def get_links(page_url, start_page, finish_page, category_dict):
    if not page_url or not page_url.startswith('http'):
        print(f"Invalid or empty URL: {page_url}")
        return tuple([]), ""
    try:
        print(f"Fetching page: {page_url}")
        response = requests.get(page_url)
        print(f"Finished fetching page: {page_url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        from urllib.parse import urljoin
        all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
        links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
        # Define your keywords based on the start and finish pages
        start_keywords = start_page.split('/')[-1].split('_')
        finish_keywords = finish_page.split('/')[-1].split('_')
        keywords = start_keywords + finish_keywords
        print(keywords)
        # Assign a score to each link based on the number of keywords it contains
        scored_links = [(link, sum(keyword in link for keyword in keywords) + (link in category_dict[finish_page])) for link in links]
        # Sort the links based on their scores in descending order
        scored_links.sort(key=lambda x: x[1], reverse=True)
        # Get the sorted links
        links = [link for link, score in scored_links]
        print(f"Found {len(links)} links on page: {page_url}")
        text = preprocess_text(soup.get_text())
        categories = [link for link in all_links if 'Category:' in link]
        return tuple(links), text, categories
    except Exception as e:
        print(f"Error occurred while fetching links from {page_url}: {str(e)}")
        return tuple([]), "", []


def find_path(start_page, finish_page="https://en.wikipedia.org/wiki/Cultivation"):
    global stop_search
    stop_search = False
    queue_start = deque()
    queue_finish = deque()
    category_dict = {}
    start_links, start_text, start_categories = get_links(start_page, start_page, finish_page, category_dict)
    finish_links, finish_text, finish_categories = get_links(finish_page, start_page, finish_page, category_dict)
    queue_start.append((start_page, [start_page], 0))
    queue_finish.append((finish_page, [finish_page], 0))
    discovered_start = set()
    discovered_finish = set()
    logs = []
    link_dict = {}  # Add this line
    similarity_dict = {}  # Add this line
    category_dict = {start_page: start_categories, finish_page: finish_categories}

    try:
        # Bidirectional search
        start_time = time.time()
        elapsed_time = 0
        while queue_start and queue_finish and not stop_search:
            vertex_start, path_start, depth_start = queue_start.popleft()
            vertex_finish, path_finish, depth_finish = queue_finish.popleft()
            links_start, text_start, categories_start = get_links(vertex_start, start_page, finish_page, category_dict)
            links_finish, text_finish, categories_finish = get_links(vertex_finish, start_page, finish_page, category_dict)
            category_dict[vertex_start] = categories_start
            category_dict[vertex_finish] = categories_finish
            for next_start in links_start:
                if next_start not in discovered_start and next_start != "https://en.wikipedia.org/wiki/Main_Page":
                    if next_start in discovered_finish:
                        log = f"Found path: {next_start}"
                        print(log)
                        logs.append(log)
                        elapsed_time = time.time() - start_time
                        logs.append(f"Search took {elapsed_time} seconds.")
                        print(f"Search took {elapsed_time} seconds.")
                        logs.append(f"Discovered pages: {len(discovered_start) + len(discovered_finish)}")
                        return path_start + path_finish[::-1], logs, elapsed_time, len(discovered_start) + len(discovered_finish) # return with success
                    else:
                        log = f"Adding link to start queue: {next_start} (depth {depth_start})"
                        print(log)
                        logs.append(log)
                        discovered_start.add(next_start)
                        queue_start.append((next_start, path_start + [next_start], depth_start + 1))
            for next_finish in links_finish:
                if next_finish not in discovered_finish and next_finish != "https://en.wikipedia.org/wiki/Main_Page":
                    if next_finish in discovered_start:
                        log = f"Found path: {next_finish}"
                        print(log)
                        logs.append(log)
                        elapsed_time = time.time() - start_time
                        logs.append(f"Search took {elapsed_time} seconds.")
                        print(f"Search took {elapsed_time} seconds.")
                        logs.append(f"Discovered pages: {len(discovered_start) + len(discovered_finish)}")
                        return path_start + path_finish[::-1], logs, elapsed_time, len(discovered_start) + len(discovered_finish) # return with success
                    else:
                        log = f"Adding link to finish queue: {next_finish} (depth {depth_finish})"
                        print(log)
                        logs.append(log)
                        discovered_finish.add(next_finish)
                        queue_finish.append((next_finish, path_finish + [next_finish], depth_finish + 1))
            if queue_start and queue_finish and not stop_search:
                elapsed_time = time.time() - start_time
        elapsed_time = time.time() - start_time
        logs.append(f"Search took {elapsed_time} seconds.")
        print(f"Search took {elapsed_time} seconds.")
        logs.append(f"Discovered pages: {len(discovered_start) + len(discovered_finish)}")
        if stop_search:
            logs.append("Search was stopped by user.")
            print("Search was stopped by user.")
            return [], logs, elapsed_time, len(discovered_start) + len(discovered_finish)  # return with stop message
        else:
            raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(discovered_start) + len(discovered_finish))
    except Exception as e:
        logs.append(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")
        return [], logs, elapsed_time, len(discovered_start) + len(discovered_finish)  # return with error message

class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered
