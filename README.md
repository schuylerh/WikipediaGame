# WikipediaGame

<!--At the time of this writing available at http://192.168.16.72:5000/ from inside the Chapman network.-->

## Description

Implemented a keyword heuristic including category matching. The more a word appears in a wikipedia page, the better the score attached. Pages that are in the same category as the destination page also increases score. 

Implemented Bidirectional search. One queue from the start page and one queue from the finish page until they both find a common page. When a common page is found, the parents of the finish queue are taken as path from common page to finish page. Significantly decreases search time for the shortest path. 

## Installation

(these instructions should work under GNU/Linux and Macos and WSL)

Prerequisites: Python

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

The samples I used were:

The time required to search a shortest path from Costume -> Prison
Along with the path from Microsoft -> Greek Language

At the start, both were max time of 30 seconds required
After implementation of keyword heuristic along with bidirectional search:
Microsoft -> Greek Language: 0.5s
## Limitations

- The UI works as expected only for chrome-based browsers (Chrome, Brave, ...).
- Only works for wikipedia pages.
- Implemented via HTTP requests (no websocket connection between client and server).
- Users are identified by IP address (no cookies or sessions).
- ...

## Parameters

- `RATELIMIT` in `server.py`.
- `TIMEOUT` in `crawler.py`.




