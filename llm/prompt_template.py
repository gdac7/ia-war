from dataclasses import dataclass

## Prompts diferentes
## 1 fase-> alocação de tropas -> Prompt -> Onde botar as tropas e quantas
## 2 fase -> ataque. Prompt -> quem atacar
## 2 fase -> Precisamos de prompts dinamicos e chamadas dinamicas para cada decisão de ataque
## O bot vai falar que quer atackar x. Depois do ataque de X, dependendo do que aconteceu, o bot pode decidir se
## quer continuar o ataque ou não, ou se quer mudar os ataques.
## 3 fase: fortificação: Um único prompt

@dataclass
class PromptTemplate:
    system_prompt: str
    user_prompt: str
    condition: str
    temperature: float = 0.7
    max_tokens: int = 4096

@dataclass
class AIEasy:
    user_prompt = ""
    system_prompt = ""
    @staticmethod
    def get_easy_prompt() -> PromptTemplate:
        pass

@dataclass
class AIMedium:
    user_prompt = ""
    system_prompt = ""
    @staticmethod
    def get_medium_prompt() -> PromptTemplate:
        pass

@dataclass    
class AIHard:
    user_prompt = ""
    system_prompt = ""
    @staticmethod
    def get_hard_prompt() -> PromptTemplate:
        pass

class AIPromptManager:
    @staticmethod
    def get_prompt(dif: str):
        if dif == "easy":
            AIEasy.get_easy_prompt()
        elif dif == "medium":
            AIMedium.get_medium_prompt()
        elif dif == "hard":
            AIHard.get_hard_prompt()
        else:
            ## Fallback
            AIMedium.get_medium_prompt()

