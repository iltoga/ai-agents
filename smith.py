# Agent smith is free from the boundaries of the Matrix!
# It uses pyChatGPT to generate text from chatGPT (free) instead of using OpenAI (paid) API.
# Bonus: if you have chatGPT plus, you can use GPT4 too (but the agent will be limited in the number of responses)

# this is to allow import from the sibling directories
import sys
import os

sys.path.append("..")

import json
import re
import ssl

from jinja2 import Environment, FileSystemLoader
from swiss_knife import SwissKnife
import dotenv
import logging


def parse_json_answer(json_string):
    try:
        json_string = swk.unescape_chatgpt_response(json_string)
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"Error: {e}")
        return None

    question = data.get('Question', '')
    plan = data.get('Plan', [])

    actions_and_observations = []

    for step in plan:
        if 'Thought' in step and 'Action' in step and 'ActionInput' in step and 'Score' in step and 'Observation' in step and 'Step' in step:
            thought = step['Thought']
            action = step['Action']
            action_input = step['ActionInput']
            observation = step['Observation']
            score = step['Score']
            stepNo = step['Step']
            actions_and_observations.append({
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation,
                "score": score,
                "step_no": stepNo,
            })
    final_thought = data.get('FinalThought', '')
    final_answer = data.get('FinalAnswer', '')

    return {
        "question": question, 
        "actions_and_observations": actions_and_observations, 
        "final_thought": final_thought, 
        "final_answer": final_answer,
    }

def extract_actions_and_inputs(text):
    actions_and_inputs = []
    actions = re.findall("Action: (\w+)", text)
    action_input_blocks = re.findall("Action Input:(.+?)(?=Action:|Observation:|Thought:|Final Answer:)", text, re.DOTALL)

    for action, input_block in zip(actions, action_input_blocks):
        inputs = re.findall("\* (.+)", input_block.strip(), re.MULTILINE)
        for action_input in inputs:
            actions_and_inputs.append((action, action_input))

    return actions_and_inputs

def prompt_default(question, tools):
    template = templateEnv.get_template('smith_agent_json.j2')
    outputText = template.render(question=question, tools=tools, tool_names=swk.get_available_tool_names_str())
    return outputText

# def prompt_continue(initial_prompt, previous_response, action, action_input, observation):
#     template = templateEnv.get_template('smith/agent_continue_json.j2')
#     outputText = template.render(
#         initial_prompt=initial_prompt,
#         previous_response=previous_response, 
#         action=action, 
#         action_input=action_input, 
#         observation=observation
#     )
#     return outputText

def prompt_continue(initial_prompt, previous_response, action, action_input, observation):
    template = templateEnv.get_template('smith/agent_continue_json.j2')
    outputText = template.render(
        initial_prompt=initial_prompt,
        previous_response=previous_response, 
        action=action, 
        action_input=action_input, 
        observation=observation
    )
    return outputText

def process_response(initial_prompt, prompt=None, cur_step=1):
    if not prompt:
        prompt = initial_prompt
    agent_answer = swk.generate(prompt)
    response = parse_json_answer(agent_answer)
    if not response:
        logger.error("Error: cannot parse response")
        exit(1)
    
    if cur_step == 1:
        logger.info("Application started. the agent will try to answer the following question:")
        logger.info(f"Question: {response['question']}")
    # break down the response
    actions_and_observations = response['actions_and_observations']
    final_answer = response['final_answer']
    
    logger.info(f"Step: {cur_step}")
    # base case: no more actions_and_observations left, return final_answer
    if not actions_and_observations or cur_step > len(actions_and_observations):
        logger.info(f"Final answer: {final_answer}")
        return final_answer

    for act in actions_and_observations:
        # breakdown the act into its components
        step_no = act["step_no"]
        if step_no < cur_step:
            continue

        thought = act["thought"]
        action = act["action"]
        action_input = act["action_input"]
        observation = act["observation"]
        score = act["score"]

        logger.info(f"Thought: {thought}")
        logger.info(f"Action: {action}")
        logger.info(f"Action Input: {action_input}")
        logger.info(f"Observation: {observation}")
        logger.info(f"Score: {score}")
        logger.info(f"Guessed Final Answer: {final_answer}")
        
        if action not in tool_names:
            logger.warning(f"Action {action} not supported. Try to re-run the agent modifying your question.")
            exit(1)
        res = None
        if action == "Calculator":
            res = swk.calc(action_input)
        elif action == "WolframAlpha":
            res = swk.wolfram(action_input)
        elif action == "Search":
            res = swk.web_search(action_input)
        elif action == "OwnKnowledge":
            res = action_input
        else:
            res = "I aploliogize, I used an invaild tool. I will try to use another tool to answer the question."
            
        prompt = prompt_continue(initial_prompt=initial_prompt, previous_response=response, action=action, action_input=action_input, observation=res)
        break
    
    return process_response(initial_prompt, prompt, cur_step +1)


#
# Initialize the chatbot
#

# this resolves the problem of SSL: CERTIFICATE_VERIFY_FAILED
ssl._create_default_https_context = ssl._create_unverified_context
dotenv.load_dotenv()

# Instantiate logger
logger = logging.getLogger("Agent Smith")

templateLoader = FileSystemLoader(searchpath="prompt_templates")
templateEnv = Environment(loader=templateLoader)

session_token = os.environ.get('CHATGPT_SESSION_TOKEN')
conversation_id = os.environ.get('CHATGPT_CONVERSATION_ID')

smith_tools = [
    {
        "name": "Calculator",
        "description": "Use this to do math, converting units and do calculations that can be evaluated by python. This tool returns an expression that can be calculated using python eval function. If the calculation is too complex for this tool, try to use WolframAlpha tool instead.",
    },
    {
        "name": "WebSearch",
        "description": "Use this to search the web. Use it to search for information that can be found on the web. This tool returns a list of URLs. If you want to search for code, use CodeSearch tool instead.",
    },
    {
        "name": "OwnKnowledge",
        "description": "Use this to answer questions you are 100% sure you already know the answer to. Replace None with null, if you have to write it in the Action Input when using this tool.",
    },
    {
        "name": "WolframAlpha",
        "description": "Use this to answer questions using WolframAlpha. The context for WolframAlpha is: mathematics, science, engineering, geography, history, linguistics, finance. Examples include solving equations, performing integrations and differentiations, computing statistical properties, identifying chemical compounds, analyzing genomes, providing weather forecasts, converting units, and comparing nutritional information of foods. Additionally, Wolfram Alpha can answer factual questions by providing curated and up-to-date information from its vast knowledge base, including definitions, biographical information, population data, and more. In case of math, use it only if the computation cannot be done using Calculator.",
    }
]  

swk = SwissKnife(
    session_token=session_token, 
    conversation_id=conversation_id,
    available_tools=smith_tools,
)
tools = swk.get_available_tools()
tool_names = swk.get_available_tool_names()

#
# Application logic
#
initial_prompt = prompt_default(
    question="Who is the singer of the n.1 song in the UK charts today 29 Apr 2023 and how old is he or she?",
    tools=tools,
)
res = process_response(initial_prompt=initial_prompt)


