from dataclasses import dataclass
import random
import json
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

@dataclass
class PhasePrompt:
    @staticmethod
    def get_phase_prompt(phase):
        if phase == "first_reinforcement":
            pattern = """
                first_reinforcement:
                    - Objective: Initial territory setup. You will place starting troops on your already-assigned territories;
                    - Parameters needed: territoryId (wich territory to place troops on) and troops;
                    - Constraints: Territory must be owned by you and cannot place more troops than available. 
                """
            json_expected = """
            {
                "action": "first_reinforcement",
                "placements": [
                    {"territoryId": id of the territory that will be reinforced, "troops": amount of troops},
                    {same if you will reinforce some more territory}
                ],
            }
            """
            
            return pattern, json_expected
    

@dataclass
class PromptTemplate:
    system_prompt: str
    user_prompt: str
    condition: str
    temperature: float = 0.7
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
    The mistakes you made is determined by a number. If the number is less than or equal to 6 you will make a intelligent play. Else you will make a bad play. 
    Your answer should be in the following JSON format: \n{phase_json_expected}
    Your objective is to make a play according to the current phase, which follows this pattern: {pattern}
    You will receive the data about how you are doing in the game. The data follow the format:
    {{
        currentPlayer: the data about you. You will use data from here to make your move.
        allPlayers: data about the others players,
        allTerritories: data about of other player's territories.
        phase: current phase,
    }}
    You are currently playing a WAR game with players of different skill levels.
    The number that determines your level of play: {quality_number}
    You are limited by the constraints of each phase. The current phase is {phase}.
    The data about the game is: 
    {data}
    Please provide you in the corresponding JSON format: \n{phase_json_expected}
    """
    user_prompt = "Please adhere to the system message and provide your response."
    condition = "Sure, I will make my move following the instructions given. I will use tags [START OF MOVE] and [END OF MOVE] for clearer presentation. Here is the move:\n[START OF MOVE]"
    @staticmethod
    def get_medium_prompt(phase: str, data: str) -> PromptTemplate:
        n = random.randint(1, 9)
        print(n)
        pattern, json_expected = PhasePrompt.get_phase_prompt("first_reinforcement")
        filled_sp = AIMedium.system_prompt.format(
            phase_json_expected=json_expected,
            pattern=pattern,
            quality_number=n,
            phase=phase,
            data=data
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

