from dataclasses import dataclass

@dataclass
class PhasePrompt:
    @staticmethod
    def get_phase_prompt(phase):
        match phase:
            case "first_reinforcement" | "reinforcement":
                pattern = f"""
                    {phase}:
                        - Goal: Secure your position.
                        - Rules:
                            1. 'anywhere' troops -> any territory.
                            2. 'restricted' troops -> only territories in that continent.
                                2.1. Example: if continentBonusTroops.south_america = 2, those 2 troops can ONLY go to South America territories.
                            3. 'totalAvailableTroops' is the amount of troops that you move must use.
                            4. id format: Use the exact 'id' string from the input. Do not prepend continent names (e.g., use "argentina", not "south_america/argentina")
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
                        - Strategy:
                            1. Review the list of "validAttacks".
                            2. Prioritize attacks where "advantage" is "high" or "medium".
                            3. Prioritize targets that are in continents related to your objective.
                            4. If all attacks have "low" advantage, choose "skipAttack": true.
                        - Constraint:
                            1. Yout must pick a pair (sourceId, targetId) exactly as listed in valid_attacks.
                """
                json_expected = """
                {
                    "action": "attack",
                    "attackerTerritoryId": "sourceId_from_list",
                    "defenderTerritoryId": "targetId_from_list",
                    "attackDice": int (usually min(3, sourceTroops - 1)),
                    "skipAttack": false,
                }
                OR
                { "action": "attack", "skipAttack": true, }
                """
            case "strategic":
                pattern = """"""
                json_expected = """"""
        return pattern, json_expected