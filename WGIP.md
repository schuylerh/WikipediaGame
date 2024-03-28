# Schuyler Huang
# Project 3: Wikipedia Game Improvement Proposal
## Overview
Currently, WikipediaGame runs on a simple Breath First Search that could use a wide range of improvements. 
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
## Progress
I've implemented the heuristic described above, a heuristic that prioritizes links based on the number of keywords they contain. The keywords are derived from the start and finish pages. A score is assigned to each link based on how many times the keywords appear on the page. The implementation of this heuristic has brought a significant reduction in search time for certain paths.

Here are some examples: (The time limit was set to 30s)

Costume -> Prison: 30s to 3s

Microsoft -> Greek Language: 30s to 8s

## Milestones
### Milestone 1
Implement category matching, where categories of the start and finish pages are also part of the heuristic. Higher scores are given to pages that are the same category as the finish page.
**Deadline**: April 4, 2024
### Milestone 2
Find an improvement, a more sophiscated approach of obtaining relevant keywords rather than just taking them from the title page. 
**Deadline**: April 11, 2024
### Milestone 3
Error handling such as exceptions and testing of the system to ensure that the prototype works as intended.
**Deadline**: April 18, 2024