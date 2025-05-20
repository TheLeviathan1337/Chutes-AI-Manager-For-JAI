# THIS IS JUST AN EXAMPLE CONFIG, DON'T USE THIS CONFIG
# Copy/paste this config with actual data to create LLM configs
class EXAMPLE_CONFIG:
    model_name = "chutes/model/name" # String that defines model name
    max_tokens = 0 # Pick an integer value for max_tokens
    temperature = 1.1 # Pick a number for your preferred temperature
    start_reasoning_token = None # Either None or a String or a list of Strings that should indicate that the reasoning process has began for the LLM
    end_reasoning_token = None # Either None or a String that ends the reasoning process for the LLM
    active = True # Boolean that determines if this config will be actively used or ignored, set to True or False


class Chimera:
    model_name = "tngtech/DeepSeek-R1T-Chimera"
    max_tokens = 0
    temperature = 0.7
    start_reasoning_token = ["Okay", "Alright"]
    end_reasoning_token ="</think>"
    active = True

class V30324:
    model_name = "deepseek-ai/DeepSeek-V3-0324"
    max_tokens = 0
    temperature = 0.7
    start_reasoning_token = None
    end_reasoning_token = None
    active = True

class R1:
    model_name = "deepseek-ai/DeepSeek-R1"
    max_tokens = 0
    temperature = 0.7
    start_reasoning_token = "<think>"
    end_reasoning_token = "</think>"
    active = True


# Add all your configs to this list to have them actually in use
# You do not have to remove models to de-activate them, just keep them here and set the "active" boolean to false in their class definition
model_configs = [Chimera, V30324, R1]


