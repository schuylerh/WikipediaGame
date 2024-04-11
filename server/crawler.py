import time
import requests
from bs4 import BeautifulSoup
import re
from collections import deque
import heapq
from collections import Counter
import string
import concurrent.futures
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

def get_links(page_url):
    if not page_url or not page_url.startswith('http'):
        print(f"Invalid or empty URL: {page_url}")
        return tuple([]), "", []
    try:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        from urllib.parse import urljoin
        all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
        links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
        text = preprocess_text(soup.get_text())
        categories = [link for link in all_links if 'Category:' in link]
        return tuple(links), text, categories
    except Exception as e:
        print(f"Error occurred while fetching links from {page_url}: {str(e)}")
        return tuple([]), "", []


def find_path(start_page, finish_page="https://en.wikipedia.org/wiki/Cultivation"):
    global stop_search
    stop_search = False
    queue = deque()
    category_dict = {}
    start_links, start_text, start_categories = get_links(start_page)
    finish_links, finish_text, finish_categories = get_links(finish_page)
    links = start_links
    queue.append((start_page, [start_page], 0))
    discovered = set()
    logs = []
    link_dict = {}  # Add this line
    similarity_dict = {}  # Add this line
    category_dict = {start_page: start_categories, finish_page: finish_categories}

    try:
        # A* search
        start_time = time.time()
        elapsed_time = time.time() - start_time
        queue = deque()
        queue.append((start_page, [start_page], 0))
        while queue and elapsed_time < TIMEOUT and not stop_search:
            vertex, path, depth = queue.popleft()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                try:
                    future_to_url = {executor.submit(get_links, url): url for url in links}
                    for future in concurrent.futures.as_completed(future_to_url):
                        url = future_to_url[future]
                        links, text, categories = future.result()
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                    else:
                        category_dict[vertex] = categories
                        for next in links:
                            if next not in discovered:
                                if next == finish_page:
                                    log = f"Found finish page: {next}"
                                    print(log)
                                    logs.append(log)
                                    logs.append(f"Search took {elapsed_time} seconds.")
                                    print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
                                    logs.append(f"Discovered pages: {len(discovered)}")
                                    return path + [next], logs, elapsed_time, len(discovered) # return with success
                                else:
                                    log = f"Adding link to queue: {next} (depth {depth})"
                                    # print(log)
                                    logs.append(log)
                                    discovered.add(next)
                                    queue.append((next, path + [next], depth + 1))
            elapsed_time = time.time() - start_time
        logs.append(f"Search took {elapsed_time} seconds.")
        print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
        logs.append(f"Discovered pages: {len(discovered)}")
        if stop_search:
            logs.append("Search was stopped by user.")
            print("Search was stopped by user.")
            return [], logs, elapsed_time, len(discovered)  # return with stop message
        else:
            raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(discovered))
    except Exception as e:
        logs.append(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")
        return [], logs, elapsed_time, len(discovered)  # return with error message

class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered
