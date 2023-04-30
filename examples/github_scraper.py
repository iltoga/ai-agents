from github import Github

def search_github(input_string):
    # Authentication
    g = Github("access_token")
    
    # Search repositories for code related to input string
    query = input_string + " in:file language:python"
    result = g.search_code(query=query)
    
    # Return a list of URLs of the code files found
    urls = [file.download_url for file in result]
    return urls

def test_search_github():
    urls = search_github("web scraping")
    assert type(urls) == list
    assert len(urls) > 0
    for url in urls:
        assert url.endswith(".py")
