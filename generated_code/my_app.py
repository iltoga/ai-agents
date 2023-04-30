from github import Github

def scrape_github(query):
    g = Github()
    repos = g.search_repositories(query)
    return repos