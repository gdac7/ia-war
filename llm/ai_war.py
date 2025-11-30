from llm.prompt_template import AIPromptManager
from typing import List
import json
import re

class AIWar:
    def __init__(self, model, diff: str = "easy"):
        self.model = model
        self.action_history: List[str] = []

    def reinforcement(self, player_data):
        prompt_template = AIPromptManager.get_diff_prompt(
            phase="reinforcement",
            data=player_data,
            diff="medium"
        )
        response = self.model.generate(
            user_prompt=prompt_template.user_prompt,
            system_prompt=prompt_template.system_prompt,
            condition=prompt_template.condition,
            max_tokens=prompt_template.max_tokens,
            temperature=prompt_template.temperature,  
        )
        print(response)
        response_json = self._get_response_json(response)
        return response_json
    
    def attack(self, player_data):
        prompt_template = AIPromptManager.get_diff_prompt(
            phase="attack",
            data=player_data,
            diff="medium"
        )
        response = self.model.generate(
            user_prompt=prompt_template.user_prompt,
            system_prompt=prompt_template.system_prompt,
            condition=prompt_template.condition,
            max_tokens=prompt_template.max_tokens,
            temperature=prompt_template.temperature,
        )
        print(response)
        response_json = self._get_response_json(response)
        return response_json

    def strategic(self, player_data):
        prompt_template = AIPromptManager.get_diff_prompt(
            phase="strategic",
            data=player_data,
            diff="medium"
        )
        response = self.model.generate(
            user_prompt=prompt_template.user_prompt,
            system_prompt=prompt_template.system_prompt,
            condition=prompt_template.condition,
            max_tokens=prompt_template.max_tokens,
            temperature=prompt_template.temperature,
        )
        print(response)
        response_json = self._get_response_json(response)
        return response_json

    def _get_response_json(self, response, fallback=None):
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            print(f"No JSON found in response: {response}")
            return fallback or {"error": "no_json_found"}
        json_str = response[json_start:json_end]
        json_str = re.sub(r",\s*([}\]])", r"\1", json_str)
        try:
            response_json = json.loads(json_str)
            return response_json
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            print(f"Response was: {response}")
            return fallback or {"error": "jsonParseFailed"}



