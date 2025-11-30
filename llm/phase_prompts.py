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
                        - Message (REQUIRED):
                            Add a brief explanation of your move (max 15 words).
                """
                json_expected = f"""
                {{
                    "action": "{phase}",
                    "placements": [
                        {{"territoryId": "id of the territory that will be reinforced", "troops": number_of_troops}},
                        {{"territoryId": "another_territory_id", "troops": number_of_troops}},
                    ],
                    "message": "brief explanation of your move (max 15 words)"
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
                        - Message (REQUIRED):
                            Add a brief explanation of your move (max 15 words).
                """
                json_expected = """
                {
                    "action": "attack",
                    "attackerTerritoryId": "sourceId_from_list",
                    "defenderTerritoryId": "targetId_from_list",
                    "attackDice": int (usually min(3, sourceTroops - 1)),
                    "skipAttack": false,
                    "message": "brief explanation of your move (max 15 words)"
                }
                OR
                { "action": "attack", "skipAttack": true, "message": "brief explanation of your move (max 15 words)" }
                """
            case "strategic":
                pattern = """
                    strategic:
                        - Goal: Reposition your forces for better defense or future attacks.
                        - Rules:
                            1. 'validMoves' contains all possible movements between adjacent territories.
                            2. Each move shows 'fromId', 'toId', 'availableTroops'.
                            3. id format: Use the exact 'id' string from validMoves.
                        - Strategy:
                            1. Review the list of "validMoves".
                            2. Prioritize moving troops to border territories (is_border: true).
                            3. Consider your objective when deciding where to move troops.
                            4. If no move seems beneficial, choose "skipMove": true.
                        - Constraint:
                            1. You must pick a pair (fromId, toId) exactly as listed in validMoves.
                            2. troops must be <= availableTroops for that specific move.
                        - Message (REQUIRED):
                            Add a brief explanation of your move (max 15 words).
                """
                json_expected = """
                {
                    "action": "strategic",
                    "fromTerritoryId": "fromId_from_list",
                    "toTerritoryId": "toId_from_list",
                    "troops": int (between 1 and availableTroops),
                    "skipMove": false,
                    "message": "brief explanation of your move (max 15 words)"
                }
                OR
                { "action": "strategic", "skipMove": true, "message": "brief explanation of your move (max 15 words)" }
                """
        return pattern, json_expected