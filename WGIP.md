# Project 3: Wikipedia Game Improvement Proposal
## Proposal to Improve WikipediaGame
Currently, the code fetches and processes pages one at a time. My proposal is speeding this up by fetching and processing multiple pages in parallel. 
## Parallelization
Parallelization in computing is the process of carrying out multiple operations or tasks simultaneously. It's a way of speeding up computation by dividing a problem into sub-problems and solving these sub-problems at the same time.
## Implementation
To implement this, we can use Python's built-in multiprocessing library. A pool would be created, where worker processes are created. They are pre-initialized and ready to execute tasks. Each process in the pool picks up a task from the shared queue or pool of tasks and executes it. 
## Synchronization
To ensure synchronization and share data between processes, a pool manager can be used. Pool manager is a class that controls a process. It oversees the distribution of tasks and ensures that processes are utilized efficiently. It also manages any communication or synchronization between processes if necessary. map() would be called, applying get_links() to every item in the queue of links, distributing the work to the processes in the pool.

## Pseudo Code
```
1. Import necessary libraries for parallel processing (like multiprocessing or concurrent.futures in Python).

2. Define a worker function `process_url`:
   - Input: URL
   - Output: Tuple of (URL, links, text)
   - This function calls `get_links` for the given URL and returns a tuple of the URL and the result.

3. Modify `find_path` function:
   - Initialize an empty set `discovered` for discovered URLs.
   - Initialize an empty list `logs` for logging.
   - Initialize a list `urls_to_process` and add the start page to it.
   - Initialize a `ThreadPoolExecutor` for parallel processing.
   - While `urls_to_process` is not empty and the search is not stopped and the timeout is not exceeded:
     - Use the `map()` function of the executor to process all URLs in `urls_to_process` in parallel using the `process_url` function. This returns an iterator of results.
     - Clear `urls_to_process`.
     - Iterate over the results:
       - For each result (URL, links, text):
         - If the URL is the finish page, stop the search and return the path.
         - Otherwise, for each link in `links`, if the link is not in `discovered`, add it to `discovered` and `urls_to_process`.
   - If the search is stopped or the timeout is exceeded, stop the executor and return the appropriate message.
```