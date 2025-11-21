from dataclasses import dataclass

@dataclass
class PhasePrompt:
    @staticmethod
    def get_phase_prompt(phase):
        match phase:
            case "first_reinforcement" | "reinforcement":
                pattern = f"""
                    {phase}:
                        - Goal: Secure your position;
                        - Rules:
                            1. 'anywhere' troops -> any territory
                            2. 'restricted' troops -> only territories in that continent
                                2.1. Example: if continentBonusTroops.south_america = 2, those 2 troops can ONLY go to South America territories
                            3. 'totalAvailableTroops' is the amount of troops that you move must use
                        - Strategy:
                            1. Prioritize territories marked "is_border": true (they face enemies).
                            2. Do not reinforce "safe" territories (is_border: false) unless necessary.
                            3. Try to secure a role continent if you're close
                """
                json_expected = f"""
                {{
                    "action": "{phase}",
                    "placements": [
                        {{"territoryId": "id of the territory that will be reinforced", "troops": number_of_troops}},
                        {{"territoryId": "another_territory_id", "troops": number_of_troops}},
                    ]
                }}
                """

           
            case "attack":
                pattern = """
                    attack:
                        - Goal: Conquer territories to fullfill objective.
                        - Rules:
                            1. You need > 1 troops to attack
                            2. Max dice = troops - 1 (capped at 3).
                            3. You can only attack to enemy territories listed in enemyNeighbors                        
                        - Strategy:
                            1. Attack where you have more troops than the enemy (e.g., 5 vs 2 is good).
                            2. Avoid attacking 2 vs 2 or 3 vs 3 (high risk).
                            3. If you want stop attacking, send "skipAttack": true.
                """
                json_expected = """
                {
                    "action": "attack",
                    "attackerTerritoryId": "your territory id",
                    "defenderTerritoryId": "enemy territory id",
                    "attackDice": int,
                    "skipAttack": false,
                }
                OR
                { "action": "attack", "skipAttack": true, }
                """
            case "strategic":
                pattern = """"""
                json_expected = """"""
        return pattern, json_expected