# Overview
Below are the improvements I have made to the BFS searching algorithm that searches for a shortest path between a start Wikipedia page and finish Wikipedia page.

## Keyword Heuristic
The keywords are derived from the start and finish pages. A score is assigned to each link based on how many times the keywords appear on the page. The implementation of this heuristic has brought a significant reduction in search time for certain paths.

(The time limit of the original BFS with no heuristic was set to 30s)

Costume -> Prison: 30s to 3s

Microsoft -> Greek Language: 30s to 8s

## Category Matching
The links that are under the same category as the end page are given a higher heuristic score. 

### Benchmarking
Costume -> Prison: 1.68s

## Depth Limiting
The search is limited to a depth of 20. Stops the algorithm from exploring paths that are too long and unlikely to lead to target page.

## Bidrectional Search
The algorithm simultaneously searches from the start page to the finish page and from the finish page to the start page. When a common page is reached, the parents of the finish queue are taken as path from common page to finish page. 

### Benchmarking
Microsoft -> Greek Language: 0.5s

## Caching
A dictionary named "link_cache" stores the results of previous calls to avoid making same requests to fetch the same page multiple times. Reduces redunancy and improves time slightly.


## Tried Libraries
Tried implementing a more robust version of the keyword heuristic and utilizing libraries such as word2vec for similarity. However, once implemented, the search duration shot up significantly and would not start processing until minutes later. Believe too much computational power is needed to load the word2vec library and worsened the search duration overall.

### Benchmarking
Samples: Could not load word2vec and start the search. Reverted to previous heuristic.

## Preprocessing
The algorithm preprocesses the text. Pages are converted to lowercase, punctuation and common words are removed.

## Testing of the combination
The samples I used were:

The time required to search a shortest path from Costume -> Prison
Along with the path from Microsoft -> Greek Language

At the start, both were max time of 30 seconds required
After implementation of keyword heuristic along with bidirectional search:
Costume -> Prison: 0.36s
Microsoft -> Greek Language: 0.5s

## Conclusion
Through multiple methods, I was able to significantly lower the search time used to find the shortest path between various Wikipedia page links. However, there are certainly more optimizations that will be done in the future.