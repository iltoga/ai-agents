from my_app import scrape_github

def test_scrape_github():
    result = scrape_github("python requests")
    assert result.totalCount > 0
    