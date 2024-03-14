import time
import requests
from bs4 import BeautifulSoup
import re
from gensim.models import Word2Vec
import numpy as np
from collections import deque
import gensim
import heapq

# Load the Word2Vec model
model_path = "/Users/schuyler/Documents/CPSC_Courses/406/WikipediaGame/GoogleNews-vectors-negative300.bin.gz"
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)

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
    return links, soup.get_text()  # Return the text of the page for preprocessing

def calculate_similarity(page1, page2, model):
    vector1 = np.mean([model[word] for word in page1 if word in model.key_to_index], axis=0)
    vector2 = np.mean([model[word] for word in page2 if word in model.key_to_index], axis=0)
    cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosine_similarity

def precompute_heuristic(start_page, finish_page, model):
    heuristic_dict = {}
    links = get_links(start_page)
    for link in links:
        heuristic_dict[link] = calculate_similarity(link, finish_page, model)
    return heuristic_dict

def find_path(start_page, model, finish_page="https://en.wikipedia.org/wiki/Cultivation"):
    heuristic_dict = precompute_heuristic(start_page, finish_page, model)
    global stop_search
    stop_search = False
    queue = deque()
    queue.append((start_page, [start_page], 0))
    discovered = set()
    logs = []
    link_dict = {}  # Add this line
    similarity_dict = {}  # Add this line

    try:
        # A* search
        start_time = time.time()
        elapsed_time = time.time() - start_time
        queue = [(0, start_page, [start_page], 0)]  # Initialize the queue as a priority queue
        while queue and elapsed_time < TIMEOUT and not stop_search: 
            (priority, vertex, path, depth) = heapq.heappop(queue)  # Use heapq.heappop to get the vertex with the highest priority
            links, text = link_dict.get(vertex, get_links(vertex))  # Get the links and the text of the page
            link_dict[vertex] = (links, text)  # Store the links and the text of the page
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
                    similarity = similarity_dict.get(next, calculate_similarity(next, finish_page, model))
                    if next not in similarity_dict:
                        similarity_dict[next] = similarity
                    heapq.heappush(queue, (1/similarity, next, path + [next], depth + 1))  # Use heapq.heappush to add the vertex to the queue with priority 1/similarity
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

