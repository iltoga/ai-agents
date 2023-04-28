# Agent smith is free from the boundaries of the Matrix!
# It uses pyChatGPT to generate text from chatGPT (free) instead of using OpenAI (paid) API.
# Bonus: if you have chatGPT plus, you can use GPT4 too (but the agent will be limited in the number of responses)

# this is to allow import from the sibling directories
import sys
sys.path.append("..")

from pyChatGPT import ChatGPT
from pprint import pprint
import ssl
from jinja2 import Environment, FileSystemLoader
import re
import json
from loaders.search_tool import SearchTool
from loaders.wolfram_alpha import WolfRamAlpha
from loaders.simple_calculator import SimpleCalculator

tool_names = ["Calculator", "Search", "Own_Knolwedge", "WolframAlpha"]

# this resolves the problem of SSL: CERTIFICATE_VERIFY_FAILED
ssl._create_default_https_context = ssl._create_unverified_context

# For more detail, you can refer to this repo 
# https://github.com/terry3041/pyChatGPT

last_thought = ""

import re

def unescape_markdown(markdown_text):
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
    
    return text

def parse_json_answer(json_string):
    try:
        json_string = unescape_markdown(json_string)
        # # Replace single backslashes with double backslashes in the string
        # json_string = json_string.replace('\\_', '_')
        # json_string = json_string.replace('\n', '')
        # json_string = json_string.replace('\\n', '\n')
        # json_string = json_string.replace('\\"', '"')
        # json_string = json_string.replace('\\\\', '\\')
        # json_string = json_string.replace('\\/', '/')
        # json_string = json_string.replace('\\t', '\t')
        # json_string = json_string.replace('\\r', '\r')
        # json_string = json_string.replace('\\b', '\b')
        # json_string = json_string.replace('\\f', '\f')  
        # json_string = json_string.replace('\\*', '*')
        # json_string = json_string.replace("\'", "'")
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return None

    question = data.get('Question', '')
    plan = data.get('Plan', [])

    actions_and_observations = []

    for step in plan:
        if 'Thought' in step and 'Action' in step and 'Action_Input' in step and 'Score' in step and 'Observation' in step and 'Step' in step:
            thought = step['Thought']
            action = step['Action']
            action_input = step['Action_Input']
            observation = step['Observation']
            score = step['Score']
            step = step['Step']
            actions_and_observations.append((thought, action, action_input, score, step, observation))

    final_thought = data.get('Final_Thought', '')
    final_answer = data.get('Final_Answer', '')

    return question, actions_and_observations, final_thought, final_answer

def extract_actions_and_inputs(text):
    actions_and_inputs = []
    actions = re.findall("Action: (\w+)", text)
    action_input_blocks = re.findall("Action Input:(.+?)(?=Action:|Observation:|Thought:|Final Answer:)", text, re.DOTALL)

    for action, input_block in zip(actions, action_input_blocks):
        inputs = re.findall("\* (.+)", input_block.strip(), re.MULTILINE)
        for action_input in inputs:
            actions_and_inputs.append((action, action_input))

    return actions_and_inputs

def generate(text):
    result = chatgpt.send_message(text)
    return result['message']

def clean_response(response):
    return response.strip().replace('\n', ' ')

def compile_prompt_default(question, tool_names):
    # load the template
    templateLoader = FileSystemLoader(searchpath="prompt_templates")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template('agent_json.j2')

    # compile the template
    outputText = template.render(question=question, tool_names=tool_names)
    return outputText

def compile_prompt_continue(initial_prompt, previous_response, action, action_input, observation):
    # load the template
    templateLoader = FileSystemLoader(searchpath="prompt_templates")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template('agent_continue_json.j2')

    # compile the template
    outputText = template.render(
        initial_prompt=initial_prompt,
        previous_response=previous_response, 
        action=action, 
        action_input=action_input, 
        observation=observation
    )
    return outputText

def tool_calc(expression):
    try:
        calc = SimpleCalculator().evaluate(expression)
        return calc
    except:
        res = f"I cannot calculate espression: {expression}. try to rewrite it in a different way, understandable by python"

def tool_wolfram(expression):
    try:
        calc = WolfRamAlpha().run(expression)
        return calc
    except:
        res = f"I cannot calculate espression: {expression}. try to rewrite it in a different way, understandable by wolfram alpha"

def tool_search(query):
    # use the search tool
    search = SearchTool()
    res = search.run(query)
    # if res is long, use semantic search to summarize it
    # if len(res) > 100:
    #     summarize_prompt = f"Given this Question: {query}, summarize the following text in the most concise way possible:\n\n{res}"
    #     res = generate(summarize_prompt)
    #     # TODO: fix this
    #     # res = search.summarize(corpus=res, query=query)
    return res

def process_response(initial_prompt, prompt=None, next_step=1):
    if not prompt:
        prompt = initial_prompt
    agent_answer = generate(prompt)
    response = parse_json_answer(agent_answer)
    if not response:
        print("Error: cannot parse response")
        exit(1)
    
    # break down the response
    question, actions_and_observations, final_thought, final_answer = response
    
    for thought, action, action_input, score, step, observation in actions_and_observations:
        if step < next_step:
            continue
        if action not in tool_names:
            print(f"Action {action} not supported. Try to re-run the agent modifying your question.")
            exit(1)
        res = None
        if action == "Calculator":
            res = tool_calc(action_input)
        elif action == "WolframAlpha":
            res = tool_wolfram(action_input)
        elif action == "Search":
            res = tool_search(action_input)
        else:
            continue
        prompt = compile_prompt_continue(initial_prompt=initial_prompt, previous_response=response, action=action, action_input=action_input, observation=res)
        break
    
    next_step += 1
    if actions_and_observations and next_step <= len(actions_and_observations):
        response = process_response(initial_prompt, prompt, next_step)    
    return response

# to get session_token:
# in chrome devtools, go to application tab, storage, coockies and copy the value of: 
# __Secure-next-auth.session-token
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..u5OgiMUov_JxkzSl.84yBsbn7aMZ9iw_s3VGGM7cBtwJspr38z-g5bK0fDILGUiBEY4TDCBomEyhul1SP_KB4kOsl_gllXknJoxHswvVRKer6RjKeOUsdXQVP3KbdpnB4NrAA9qBjIr3CY6_1WSTb7p7mOMhLQeaSOVgdw_t5rWfZyPiwnm7qJIO1ItNCZzNIT2MMWvad2LZztwk9-erAo70wsGnDJFXm1iF3kqTx9XEOyo9e5mXe_dIPYPMzHS_O83eyIE3ntxlPIQpL9QJIotW79ajIcW0EhQ4pSxdReprnQs59_9_7Fv5bg5FMGuv1QJRzef2jXVi5MXIN8-SR5m4bo0WAV-X_fCPEndu5p1_LWv2_PI0_WDgM6h6iTrnxbUSR6_Ih3ZmdiCbTG8oLbX49JPwogTPuRAJrdgLvNi0fe3YKZ5XbybwaKLgupiRWXC3MWwBr7satX5gcMnPYEg8oc-otQHKKPMHB9kMt2qvjG3Kv2vFGLgtbSmhMcBnprA01l1esxBCjXQU7_H1n5LDI5JciFNIC-AonK_7k8EQCdHz9EmZHG1Z042CyvGIkuM2p81wb7EezeWisHVcdaG1t8BdM7U1IrObG6E0WSi8zgvwZVgXIv0jcx93756XaOr2Mxw82iyKWXTBOYqQhjOeXGk8IqcWr-FrPGkEa2ZuiwZcJ7ze55JDEDh95uzo5fz08Ij05hJyfzhfzT6r3XLaMfQ6yCamabW4NQ0AJHF6W_lpmCfmCAjNj3MMD3Ww-CcCYLDPJGo0L512xl_yYxxpQROqxQMFdfe8EHTT8dK5rqStjVXzDRMPWuPUSnEtlKvoqBEqNRo9q6rfwgFdMB6LY8YW2BI2jypnCS7NvzvDAmXH-QDga-6UpcXL6NwhAd2Pq8Y8S45Trhy5Y3-Vpcn-RvDvEYFvLXBkqcAq43S326YwRdpd3tspOqM-qYvXSLSqLwOQ2IYpntXY58Pl3_9NrVEE_qnfjGh59poLfEq5qs4g0pEU2IprEzBlwco_Bualz6Uu7zqveW331JiX5EeX5uOjqmSSAGhHkZBGmorzFn94-Gbe-q4mL-Vw_jvrvwKNi_5qQaVhAT8OEmlY5Wn8uo3b0r0Lj1pyC8tjsxp2neJnhbBB0nA-jMYTjkakXqA0ysQUnKcYlZgtfusNDc6-UOXIikunyKyGauufmDR7XFtU7UFBhTTiyTi0aO7g2kFvlxhaYG5TnPFBWyq0ff8uYsIzhs4X3PE6y4edlVjraBdpteKWIphS4Px6-K-3QW6tCgqOA0Rt86EPRHyieJxScFch5eBAfacf6MPoMTaCI-NAp1WmhmEAb50OhsTKN63fpm2RhC6cJHKDh78Zwqtl5tsgUWfF9ie8b9yXghy6O6dKzonmtsyEDd4nxve-DUlCJJhaCWgKkHa9VBFb6rLuAKh4-Hng7OR_NBOhxBeS8CIplrPI6a8zTTk1BI-tUlOA8__ADx5evbfezZIuqQFd8HHcfHqj4-5SRRgmPAkBrV8_zN6vYY6jaUVKTes1sEkG-Pv3yPwHM6r_K7oZSMbRbGNn3DATe44p781mMwuGXDlNFw5wbWaELCiUYks2HHIXLkSAMI27bcebHjz2KW5WI91mfz8JsRpfISo8RUoRcsoUkWXjANAL4YWL0CeVao-12cry-VBabL0nyMm7A7qFhu85S_9texXq9lzpCxfe-uu0U213_Lsgfh34qSQRSSNpLjY-8ZlYws75V1YCeGI3LvhjGeZNq3OBj4DbjhV9hekJ8gmlTQw_W_y88QSpLVPvI0v7SLXHdnDgxFirz27TUP0OPvi6N0wIewfBuzIZyqZMAnXK3ymi0Ve8acCdTCLQ3r6IUZVbKT0YP3jT8gko_02nV2khKJlQHhISFOd-imipuBrZTAwMoXljceg0Xp3oHBpjq3rLK_Vol4Z2MeImlF8tGOugaBR9qL2tmTjPhsaATHJ6Ts5mEOPNsP4rDRi5f77k7nN86A5DYEUKNl5mLKEqKs3QtUaobRtXZM10fosXfXNzBASgmH6hyPOMzmkS86F_Nge9-EX1cGG_ElXULPfyqO7H_zfkaLFI_YSLMwmVH2ztV-YEYH8o7vJl-XhHebDtKGPD4r63_QazSEI0cJKelBEQkLu3U8ATDJQ9R04qhsYQ3vEFs7vjMJMQOb9iHHsoUp0LPx2oui_mkP60zWNNgjY6r_chGvsbv4INPDrLF1pwYJ5WsQxXfG9uhKewcpkFiTkQZNeYAXRM2JGNRC5cWDi92WxekmNO5i-hxDR_4pu-ko90LMPThzcls9PHurkTjoajpWyMg33guNitPW6lb58DhKyvaYMZ8xBveDkhKTjmjdj8ELfMBXj06wbXIe7JesudVziahJw6RiLVJfl5732kpNkoolqVfagnQzFkef1gx4Q9j6NAAMGKJ_pkx7tjfwtyzzdiajdojd3Jg_jBGbVfozVTb0_r2zHGWISRfijN40zWoLQxpXWZx2najKH8v7nNj0mJxQ6ssCNk65Ntd45Ouixj3-p_hMJ2oBD3njxKQQW0umSuWI_Y7-xximlsGGKhZHme5KfFDfmUgyi874wGO9kQSGoF8Bk7kvXgU_38YE_ZzBR7vk_zUdvQL3T6T9vJGMmi8o6bRb79clK8edVE9YivuUg.yfVAWCb3_tV2T72Ex3z9Hw'
conversation_id = '923a66c3-b95f-408a-a7db-91bcdf8cf786'
# session_token = os.environ.get('SESSION_TOKEN')
# conversation_id = os.environ.get('CONVERSATION_ID')
chatgpt = ChatGPT(session_token, conversation_id=conversation_id)

# prompt = compile_prompt("What is the age of the president of Egypt squared?")
# response = generate(prompt)
# print(response)

initial_prompt = compile_prompt_default(
    question="Give me a projection of the population of the United States in 2050 and compare it with the population of Egypt in 2050.",
    tool_names=", ".join(tool_names)
)
res = process_response(initial_prompt=initial_prompt)
# get the last element of res array
res = res[-1]
# get the last field of res dict
res = res[5]
pprint(res)



