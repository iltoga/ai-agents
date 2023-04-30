# Coder ai
import re

import re

def parse_text_file(file_path):
    data = {}
    step = 0
    
    with open(file_path, "r") as f:
        content = f.read()
        
        thought_matches = re.finditer(r"Thought: (.+)", content)
        action_matches = re.finditer(r"Action: (.+)", content)
        action_inputs = re.finditer(r"Action Input: (.+)", content)
        scores = re.finditer(r"Score: (.+)", content)
        observations = re.finditer(r"Observation: (.+)", content)
        
        for thought in thought_matches:
            step += 1
            data[step] = {"thought": thought.group(1)}

            if (action := next(action_matches, None)):
                data[step]["action"] = action.group(1)
                
            if (action_input := next(action_inputs, None)):
                data[step]["action_input"] = action_input.group(1)
                
            if (score := next(scores, None)):
                data[step]["score"] = float(score.group(1))
                
            if (observation := next(observations, None)):
                data[step]["observation"] = observation.group(1)
                
        final_thought_match = re.search(r"Final Thought: (.+)", content)
        if final_thought_match:
            data["final_thought"] = final_thought_match.group(1)

    return data

# Use the parse_text_file function
file_path = "test_data/coder_test_01.txt"
parsed_data = parse_text_file(file_path)
print(parsed_data)
