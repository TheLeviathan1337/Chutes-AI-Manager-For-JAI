from model_configs import model_configs
import random
from chutes import fetch_chute

class Helper:
    loaded_models = []
    current_index = 0

    def load_model_configs():
        Helper.loaded_models = []
        for model in model_configs:
            if getattr(model, "active"):
                Helper.loaded_models.append(model)

    @staticmethod
    async def read_index():
        store_index = Helper.current_index
        if Helper.current_index >= len(Helper.loaded_models) - 1:
            Helper.current_index = 0
        else:
            Helper.current_index += 1
        return store_index


    @staticmethod
    async def process_request(body, api_key, type):
        stream = body['stream']
        messages = body['messages']
        if type == 'Random':
            model_config = random.choice(Helper.loaded_models)
        elif type == 'Ordered':
            model_config = Helper.loaded_models[await Helper.read_index()]

        print(f"FETCHING RESPONSE FROM MODEL {model_config.model_name}")
        return fetch_chute(api_key, model_config, messages, stream)