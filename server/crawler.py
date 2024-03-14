import time
import requests
from bs4 import BeautifulSoup
import re
from gensim.models import Word2Vec
import numpy as np
from collections import deque

TIMEOUT = 999999  # time limit in seconds for the search
stop_search = False  # control variable for stopping the search

def stop_searching():
    global stop_search
    stop_search = True

def get_links(page_url):
    print(f"Fetching page: {page_url}")
    response = requests.get(page_url)
    print(f"Finished fetching page: {page_url}")
    soup = BeautifulSoup(response.text, 'html.parser')
    from urllib.parse import urljoin
    all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
    # print(f"All links found: {all_links}")
    links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
    print(f"Found {len(links)} links on page: {page_url}")
    return links

def calculate_similarity(page1, page2):
    model = gensim.models.KeyedVectors.load_word2vec_format('/Users/schuyler/Documents/CPSC_Courses/406/WikipediaGame/GoogleNews-vectors-negative300.bin.gz', binary=True)
    vector1 = np.mean([model[word] for word in page1 if word in model.vocab], axis=0)
    vector2 = np.mean([model[word] for word in page2 if word in model.vocab], axis=0)
    cosine = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosine

def find_path(start_page, finish_page="https://en.wikipedia.org/wiki/Cultivation"):
    global stop_search
    stop_search = False
    queue = deque()
    queue.append((start_page, [start_page], 0))
    discovered = set()
    logs = []
    link_dict = {}  # Add this line

    try:
        # breadth first search
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while queue and elapsed_time < TIMEOUT and not stop_search: 
            (vertex, path, depth) = queue.popleft()
            links = link_dict.get(vertex, get_links(vertex))
            link_dict[vertex] = links
            for next in set(links) - discovered:
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
                    print(log)
                    logs.append(log)
                    discovered.add(next)
                    similarity = similarity_dict.get(next, calculate_similarity(next, finish_page))
                    similarity_dict[next] = similarity
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

