import re
import time
from loaders.web_search import WebSearchTool
from loaders.simple_calculator import SimpleCalculator
from loaders.wolfram_alpha import WolfRamAlpha
from loaders.code_search import CodeSearchTool

from jinja2 import Environment, FileSystemLoader

# For more detail, you can refer to this repo 
# https://github.com/terry3041/pyChatGPT
from pyChatGPT import ChatGPT


class SwissKnife:
    default_tools = [
        {
            "name": "Calculator",
            "description": "Use this to do math, converting units and do calculations that can be evaluated by python. This tool returns an expression that can be calculated using python eval function. If the calculation is too complex for this tool, try to use WolframAlpha tool instead.",
        },
        {
            "name": "WebSearch",
            "description": "Use this to search the web. Use it to search for information that can be found on the web. This tool returns a list of URLs. If you want to search for code, use CodeSearch tool instead.",
        },
        {
            "name": "CodeSearch",
            "description": "Use this to search public code from GitHub, when you need ideas on how to write code.",
        },
        {
            "name": "OwnKnowledge",
            "description": "Use this to answer questions you are 100% sure you already know the answer to. Replace None with null, if you have to write it in the Action Input when using this tool.",
        },
        # {
        #     "name": "OwnKnowledge",
        #     "description": "Use this to ask questions to the agent. It uses the knowledge base of the agent.",
        # },
        {
            "name": "WolframAlpha",
            "description": "Use this to answer questions using WolframAlpha. The context for WolframAlpha is: mathematics, science, engineering, geography, history, linguistics, finance. Examples include solving equations, performing integrations and differentiations, computing statistical properties, identifying chemical compounds, analyzing genomes, providing weather forecasts, converting units, and comparing nutritional information of foods. Additionally, Wolfram Alpha can answer factual questions by providing curated and up-to-date information from its vast knowledge base, including definitions, biographical information, population data, and more. In case of math, use it only if the computation cannot be done using Calculator.",
        },
        {
            "name": "BashShell",
            "description": "Use this to install dependencies, execute commands and run code and tests. Test commands must be in the form of (example for python code): \"python -c 'from foo import hello; print test_hello()'\".",
        }
    ]  
    
    # to get session_token:
    # in chrome devtools, go to application tab, storage, coockies and copy the value of: 
    # __Secure-next-auth.session-token    
    def __init__(self, available_tools=default_tools , session_token=None, conversation_id=None):
        if session_token is None:
            raise Exception("session_token is required")
        if conversation_id is None:
            raise Exception("conversation_id is required")
        
        self.available_tools = available_tools
        
        templateLoader = FileSystemLoader(searchpath="prompt_templates")
        self.templateEnv = Environment(loader=templateLoader)

        self.chatgpt = ChatGPT(session_token, conversation_id=conversation_id)
        # self.chatgpt = ChatGPT(session_token, moderation=False)
        
    # Generate text from prompt using chatGPT web wrapper
    def generate(self, text, retry=0):
        try:
            result = self.chatgpt.send_message(text)
        except IndexError as e:
            if retry > 5:
                raise e
            print(f"Error: {e}")
            time.sleep(2)
            return self.generate(text, retry=retry+1)
        return result['message']
    
    def get_available_tools(self):
        return self.available_tools
    
    def get_available_tool_names(self):
        tool_names = []
        for tool in self.available_tools:
            tool_names.append(tool['name'])
        return tool_names
    
    def get_available_tool_names_str(self):
        tool_names = self.get_available_tool_names()
        return ", ".join(tool_names)

    def calc(self, expression):
        try:
            calc = SimpleCalculator().evaluate(expression)
            return calc
        except:
            res = f"I cannot calculate espression: {expression}. try to rewrite it in a different way, understandable by python"
        return res

    def wolfram(self, expression):
        try:
            calc = WolfRamAlpha().run(expression)
            return calc
        except:
            res = f"I cannot calculate espression: {expression}. try to rewrite it in a different way, understandable by wolfram alpha"
        return res
    
    def code_search(self, query):
        # use the search tool
        search = CodeSearchTool()
        res = search.run(query)
        # if res is long, summarize it
        if len(res) > 400:
            summarize_prompt = self.prompt_summarize_qa(query, res)
            res = self.generate(summarize_prompt)
        return res

    def web_search(self, query):
        # use the search tool
        search = WebSearchTool()
        res = search.run(query)
        # if res is long, summarize it
        if len(res) > 100:
            summarize_prompt = self.prompt_summarize_qa(query, res)
            res = self.generate(summarize_prompt)
        return res

    def prompt_summarize_qa(self, query, res):
        template = self.templateEnv.get_template('summarize_answer.j2')
        outputText = template.render(query=query, res=res)
        return outputText
    
    # unescape a string returned by pyChatGPT (it uses markdownify to format the text)
    def unescape_chatgpt_response(self, markdown_text):
        # Unescape backslashes
        text = re.sub(r'\\([*_`~])', r'\1', markdown_text)
        
        # Remove formatting for bold, italic, and strikethrough
        text = re.sub(r'\*{1,2}|_{1,2}|~~', '', text)
        
        # Remove heading formatting
        text = re.sub(r'^#+\s|\s#+$', '', text, flags=re.MULTILINE)
        
        # Remove blockquote formatting
        text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
        
        # Remove code blocks
        text = re.sub(r'^```.*?```', '', text, flags=re.MULTILINE | re.DOTALL)
        
        # Remove inline code formatting
        text = re.sub(r'`([^`]*)`', r'\1', text)
        
        # Replace link formatting with the link text
        text = re.sub(r'\[([^\]]*)\]\([^\)]+\)', r'\1', text)

        # Replace image formatting with the alt text
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
        
        # Replace None with null (chat GPT uses None instead of null when using OwnKnowledge)
        text = re.sub(r'None,', r'null,', text)
        
        return text    

