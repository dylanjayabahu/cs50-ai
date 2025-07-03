import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probabilities = {}

    # any link in corpus
    all_links = corpus.keys()
    for link in all_links:
        probabilities[link] = (1-damping_factor)/len(all_links)

    # links from the page
    page_links = corpus[page] if corpus[page] else all_links
    for page_link in page_links:
        probabilities[page_link] += damping_factor/len(page_links)

    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {page: 0 for page in corpus.keys()}
    
    page = random.choice(list(page_rank.keys()))

    for _ in range(n):
        page_rank[page] += 1

        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

    for page in page_rank:
        page_rank[page] /= n 
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    convergance_threshold = 0.001
    d = damping_factor

    pages = corpus.keys()
    N = len(pages)

    page_rank = {page: 1/N for page in pages}

    keep_iterating = True
    while keep_iterating:
        keep_iterating = False

        new_page_rank = {}
        for p in pages:
            rank = (1-d)/N 

            # get all the pages that link to p
            parent_pages = [page for page in pages if p in corpus[page] or len(corpus[page])==0] 

            for page in parent_pages:
                numlinks = len(corpus[page]) if len(corpus[page]) > 0 else len(pages)
                rank += d * page_rank[page]/numlinks
        
            new_page_rank[p] = rank

            if abs(page_rank[p] - rank) > convergance_threshold:
                keep_iterating = True
        
        page_rank = new_page_rank

    return page_rank


if __name__ == "__main__":
    main()