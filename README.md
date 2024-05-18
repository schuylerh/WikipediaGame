# WikipediaGame


## Description

Implemented a keyword heuristic including category matching. The more a word appears in a wikipedia page, the better the score attached. Pages that are in the same category as the destination page also increases score. 

Implemented Bidirectional search. One queue from the start page and one queue from the finish page until they both find a common page. When a common page is found, the parents of the finish queue are taken as path from common page to finish page. Significantly decreases search time for the shortest path. 

- **Responsive:** A Stop button feature has been added in the case where some paths may take too long to find the shortest path for. This could lead to timing out in normal cases. A stop button has been added to prevent this. 
## Installation

(these instructions should work under GNU/Linux and Macos and WSL)

Prerequisites: Python
**Install Python:**
Download and install it from [python.org](https://www.python.org/downloads/)
**(Optional) Set Up a Virtual Environment:**
Use a virtual environment to manage the Python packages for this project:
```bash
# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS and Linux:
source myenv/bin/activate
```
**Install Required Packages:**
```bash
pip install requests beautifulsoup4 
```

```
git clone https://github.com/schuylerh/WikipediaGame
cd WikipediaGame/server
source setup.sh
```

Starting the server:

```
python server.py
```

(For development one may want to use `watchmedo auto-restart -d . -p '*.py' -- python server.py`.)


Play the game on [`localhost:5000`](http://127.0.0.1:5000/) (this link will only work after you started the server on your machine (watch the console in case the port number changed to eg `5001`)).

## Testing

Run the code using this script:
```bash
python3 server.py
```
Click on the HTTP link provided and enter the link of a start Wikipedia page and a final Wikipedia page. 

## Limitations

1. **True shortest path**: 
    - Due to it being a a heuristic, it may limit its ability to find the actual shortest path. After all, it is a heuristic, so the actual shortest path may not be found as not all possible paths are searched.
2. **Dependency on Wikipedia**:
    - The algorithm relies on external services such as Wikipedia being online as it uses http requests.

- The UI works as expected only for chrome-based browsers (Chrome, Brave, ...).
- Only works for wikipedia pages.
- Implemented via HTTP requests (no websocket connection between client and server).
- Users are identified by IP address (no cookies or sessions).
- ...

## Future Work
1. **Multithreading**
    - Implementing multithreading or parallel processing could speed up the process by a slight margin.
2. **Error Handling**
    - Better error handling in the case of network failures and other unexpected errors.
3. **Semantic Model**
    - The current heuristic, while decent, uses a simple heuristic method to find the shortest path. While this lowers the search duration significantly, it may not be the most accurate compared to robust libraries.

## Parameters

- `RATELIMIT` in `server.py`.
- `TIMEOUT` in `crawler.py`.




