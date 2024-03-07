import time
import requests
from bs4 import BeautifulSoup
import re
from gensim.models import Word2Vec
import numpy as np
from queue import PriorityQueue

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
    # Extract words from the URLs
    words1 = page1.split('/')[-1].split('_')
    words2 = page2.split('/')[-1].split('_')

    # Load the Word2Vec model
    model = Word2Vec.load('actual_path_to_your_model')

    # Get the word embeddings
    embeddings1 = [model[word] for word in words1 if word in model]
    embeddings2 = [model[word] for word in words2 if word in model]

    # Calculate the cosine similarity
    similarity = np.dot(np.mean(embeddings1, axis=0), np.mean(embeddings2, axis=0)) / (np.linalg.norm(np.mean(embeddings1, axis=0)) * np.linalg.norm(np.mean(embeddings2, axis=0)))

    return similarity

def find_path(start_page, finish_page="https://en.wikipedia.org/wiki/Cultivation"):
    global stop_search
    stop_search = False
    queue = PriorityQueue()
    queue.put((1, (start_page, [start_page], 0)))
    discovered = set()
    logs = []

    try:
        # breadth first search
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while queue and elapsed_time < TIMEOUT and not stop_search: 
            (_, (vertex, path, depth)) = queue.get()
            for next in set(get_links(vertex)) - discovered:
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
                    similarity = calculate_similarity(next, finish_page)
                    queue.put((1 - similarity, (next, path + [next], depth + 1)))  # Use 1 - similarity because PriorityQueue returns the smallest items first
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

