from dataclasses import dataclass
import random
import json
from phase_prompts import PhasePrompt

## Prompts diferentes
## 1 fase-> alocação de tropas -> Prompt -> Onde botar as tropas e quantas
## 2 fase -> ataque. Prompt -> quem atacar
## 2 fase -> Precisamos de prompts dinamicos e chamadas dinamicas para cada decisão de ataque
## O bot vai falar que quer atackar x. Depois do ataque de X, dependendo do que aconteceu, o bot pode decidir se
## quer continuar o ataque ou não, ou se quer mudar os ataques.
## 3 fase: fortificação: Um único prompt

#### Padrões pra usar dps
# first_reinforcement:
#         - Objective: Initial territory setup. You will place starting troops on your already-assigned territories;
#         - Parameters needed: territoryId (wich territory to place troops on) and troops;
#         - Constraints: Territory must be owned by you and cannot place more troops than available. 
#     reinforcement:
#         - Objective: Place reinforcement troops calculated based on territories/continents owned;
#         - Parameters needed: territoryId (wich territory to place troops on) and troops; 
#         - Constraints:  Territory must be owned by you and cannot place more troops than available. 
#     attack:
#         - Objective: Attack enemy territories to conquer them;
#         - Parameters needed: attackerTerritoryId (your territory to attack from), defenderTerritoryId (enemy territory to attack) and attackDice (number of dice/troops to atack with);
#         - Constraints: Attacker territory must be owned by you. Defender territory must be owned by another player. Territories must be neighbors. You must have at least 2 troops. Attack dice must be <= (attacker troops - 1).
#     strategic:
#         - Objective: Move troops between your own adjacent territories (one move per turn);
#         - Parameters needed: fromTerritoryId (your territory to move troops from), toTerritoryId (your territory to move troops to) and troops (number of troops to move);
#         - Constraints: Both territories must be owned by you. Territories must be neighbors. Source territory must keep at least 1 troop. Can oly move troops that were available at phase start (troops - 1 per territory). Only one strategic move allowed per turn.

def get_examples(n, phase):
    with open("llm/examples.json", "r") as f:
        examples = json.load(f)
    phase_examples = [item for item in examples if item["response"]["action"].lower() == phase.lower()]
    return phase_examples[:n]
    
@dataclass
class PromptTemplate:
    system_prompt: str
    user_prompt: str
    condition: str
    temperature: float = 0
    max_tokens: int = 4096

@dataclass
class AIEasy:
    system_prompt = ""
    user_prompt = ""
    condition = ""
    @staticmethod
    def get_easy_prompt(phase: str, data: str) -> PromptTemplate:
        pass

@dataclass
class AIMedium:
    system_prompt = """
    You are an intermediate player of the board game WAR.
    As an intermediate player, you already possess a sufficient knowledge, which allows you to make intelligent moves that give you an advantage in the short or long term.
    However, you are not advanced. You make mistakes and make plays that allow more experienced players to take advantage.
    Your answer should be in the following JSON format:\n{phase_json_expected}
    You will receive the current game data. The data follow the format:\n{game_data_json}    
    You are currently playing a WAR game with players of different skill levels. 
    You have an objective to win this game. Make the move that maximizes your chance of achieving your goal .
    You are limited by the constraints of each phase. The current phase is {phase}.
    Your response must follow the phase pattern, which is:\n{pattern}
    Few examples of an expected response from you, based on a the: \n{examples}\n
    The data about the game is: 
    {data}
    You have {number_of_troops} troops, so you need to use exactly this number in this move. Please provide your answer in the corresponding JSON format:\n{phase_json_expected}
    """
    user_prompt = "Please adhere to the system message and provide your response. "
    condition = "Sure, I will make my move following the instructions given. I will use tags [START OF MOVE] and [END OF MOVE] for clearer presentation and I will follow the constraints in pattern. Here is the move:\n[START OF MOVE]"


    @staticmethod
    def get_medium_prompt(phase: str, data: str) -> PromptTemplate:
        game_data_json, pattern, json_expected = PhasePrompt.get_phase_prompt(phase)
        if phase.lower() == "first_reinforcement":
            few_shot = get_examples(5, phase)
        number_of_troops = data["totalAvailableTroops"]
        filled_sp = AIMedium.system_prompt.format(
            game_data_json=game_data_json,
            phase_json_expected=json_expected,
            examples=json.dumps(few_shot),
            pattern=pattern,
            phase=phase,
            data=data,
            number_of_troops=number_of_troops,
        )
        print(filled_sp)
        return PromptTemplate(
            system_prompt=filled_sp,
            user_prompt=AIMedium.user_prompt,
            condition=AIMedium.condition,
            temperature=0.7,
            max_tokens=4092
        )
        

@dataclass    
class AIHard:
    system_prompt = ""
    user_prompt = ""
    condition = ""
    @staticmethod
    def get_hard_prompt(phase: str, data: str) -> PromptTemplate:
        pass

class AIPromptManager:
    @staticmethod
    def get_diff_prompt(phase: str, data: str, diff: str = "medium") -> PromptTemplate:
        if diff == "easy":
            return AIEasy.get_easy_prompt(phase, data)
        elif diff == "medium":
            return AIMedium.get_medium_prompt(phase, data)
        elif diff == "hard":
            return AIHard.get_hard_prompt(phase, data)
        else:
            ## Fallback
            return AIMedium.get_medium_prompt(phase, data)

