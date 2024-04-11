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
        # Get the main content of the page
        content = soup.find('div', {'id': 'mw-content-text'})
        from urllib.parse import urljoin
        # Only extract links from the main content
        all_links = [urljoin(page_url, a['href']) for a in content.find_all('a', href=True) if '#' not in a['href']]
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
    start_queue = deque()
    start_queue.append(start_page)
    start_discovered = {start_page: [start_page]}

    finish_queue = deque()
    finish_queue.append(finish_page)
    finish_discovered = {finish_page: [finish_page]}

    logs = []
    link_dict = {}  # Add this line
    similarity_dict = {}  # Add this line
    start_links, start_text, start_categories = get_links(start_page, start_page, finish_page, {})
    finish_links, finish_text, finish_categories = get_links(finish_page, start_page, finish_page, {})
    category_dict = {start_page: start_categories, finish_page: finish_categories}

    try:
        # A* search
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while start_queue and finish_queue and elapsed_time < TIMEOUT and not stop_search:
            start_vertex, start_path, start_depth = start_queue.popleft()
            finish_vertex, finish_path, finish_depth = finish_queue.popleft()

            start_links, start_text, start_categories = get_links(start_vertex, start_page, finish_page, category_dict)
            finish_links, finish_text, finish_categories = get_links(finish_vertex, start_page, finish_page, category_dict)

            category_dict[start_vertex] = start_categories
            category_dict[finish_vertex] = finish_categories

            for next in start_links:
                if next not in start_discovered:
                    if next in finish_discovered:
                        log = f"Found finish page: {next}"
                        print(log)
                        logs.append(log)
                        logs.append(f"Search took {elapsed_time} seconds.")
                        print(f"Search took {elapsed_time} seconds.")
                        logs.append(f"Discovered pages: {len(start_discovered) + len(finish_discovered)}")
                        return start_path + [next] + finish_path[::-1], logs, elapsed_time, len(start_discovered) + len(finish_discovered)
                    else:
                        log = f"Adding link to start queue: {next} (depth {start_depth})"
                        print(log)
                        logs.append(log)
                        start_discovered.add(next)
                        start_queue.append((next, start_path + [next], start_depth + 1))

            for next in finish_links:
                if next not in finish_discovered:
                    if next in start_discovered:
                        log = f"Found start page: {next}"
                        print(log)
                        logs.append(log)
                        logs.append(f"Search took {elapsed_time} seconds.")
                        print(f"Search took {elapsed_time} seconds.")
                        logs.append(f"Discovered pages: {len(start_discovered) + len(finish_discovered)}")
                        return start_path + [next] + finish_path[::-1], logs, elapsed_time, len(start_discovered) + len(finish_discovered)
                    else:
                        log = f"Adding link to finish queue: {next} (depth {finish_depth})"
                        print(log)
                        logs.append(log)
                        finish_discovered.add(next)
                        finish_queue.append((next, finish_path + [next], finish_depth + 1))

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
