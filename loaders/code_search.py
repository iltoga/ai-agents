from pprint import pprint
from github import Github

class CodeSearchTool:
    def __init__(self):
        # initialize PyGithub
        self.g = Github(jwt="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")
        
    def run(self, input_string, language="python", max_results=1):
        # search for repositories
        query = input_string + f" in:file language:{language}"
        result = self.g.search_code(query)
        
        # TODO: for now return the first result, but in future we should use a similarity metric to return the most similar result
        # get file contents
        file_contents = ""
        i = 0
        for file in result:
            file_contents += file.decoded_content.decode()
            i += 1
            if i > max_results:
                break
        
        # return scraped code
        return file_contents

if __name__ == "__main__":
    input_string = "python web scraping"
    expected_output = "import requests\nfrom bs4 import BeautifulSoup\n\nurl = 'https://example.com'\nresponse = requests.get(url)\nhtml = response.content\nsoup = BeautifulSoup(html, 'html.parser')\n"
    test_g = CodeSearchTool()
    scraped_code = test_g.run(input_string)
    pprint(scraped_code)
