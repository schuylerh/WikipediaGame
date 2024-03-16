# Schuyler Huang
# Project 3: Wikipedia Game Improvement Proposal
# Benchmark
A benchmark would be required and how it is comparable to the original BFS. A simple benchmark I propose is to reduce the search times of at least five different paths by 50%.
## Proposal to Improve WikipediaGame
The current BFS is one without any heuristics nor word embeddings. I propose to add heuristics to the BFS in order to speed up the process even though it may miss the shortest path. The heuristic I am thinking of is associating links with scores based on how close they are related to the given keywords. The keywords would be from the names of the wikipedia pages at this moment but there could be better ways of coming up with keywords. 

## Pseudo Code
```
Function get_links(page_url, start_page, finish_page):
    # Fetch and parse the page at page_url
    # Extract all links on the page

    # Define keywords based on the start and finish pages
    start_keywords = split the last part of start_page URL by '_'
    finish_keywords = split the last part of finish_page URL by '_'
    keywords = concatenate start_keywords and finish_keywords

    # Assign a score to each link based on the number of keywords it contains
    For each link in links:
        score = count the occurrences of keywords in the link
        Add (link, score) to scored_links

    # Sort the links based on their scores in descending order
    Sort scored_links by score in descending order

    # Get the sorted links
    links = extract the link part from each element in scored_links

    Return links
```
