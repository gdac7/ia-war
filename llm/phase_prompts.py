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
                        - Objective: Attack enemy territories to conquer them and achieve your objective;
                        - Attack rules:
                            1. You can only attack from territories in territoriesCanAttackFrom (troops >= 2)
                            2. You can only attack to enemy territories listed in enemyNeighbors
                            3. attackDice must be between 1 and maxDice for that territory
                            4. You can choose to skip attacking by setting "skipAttack": true
                        - Constraints:
                            1. attackerTerritoryId must be in territoriesCanAttackFrom
                            2. defenderTerritoryId must be in that territory's enemyNeighbors
                            3. attackDice must be between 1 and maxDice
                """
                json_expected = """
                {
                    "action": "attack",
                    "attackerTerritoryId": "your_territory_id",
                    "defenderTerritoryId": "enemy_territory_id",
                    "attackDice": number_of_dice (1 to maxDice),
                    "skipAttack": false,
                }
                or {"action": "attack", "skipAttack": true,}
                """
            case "strategic":
                pattern = """"""
                json_expected = """"""
        return pattern, json_expected