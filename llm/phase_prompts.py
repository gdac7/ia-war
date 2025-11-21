from dataclasses import dataclass

@dataclass
class PhasePrompt:
    @staticmethod
    def get_phase_prompt(phase):
        match phase:
            case "first_reinforcement":
                game_data_json = """{
                    "objectiveType": Your game objective type,
                    "objectiveDescription": Your Objective Description. You need to achieve this objective to win,
                    "freeTroops": Troops you can place on ANY territory,
                    "continentBonusTroops": {
                        "south_america": Bonus troops ONLY for South America territories,
                        "north_america": Bonus troops ONLY for North America territories,
                        "europe": Bonus troops ONLY for Europe territories,
                        "asia": Bonus troops ONLY for Asia territories,
                        "africa": Bonus troops ONLY for Africa territories,
                        "oceania": Bonus troops ONLY for Oceania territories
                    },
                    "totalAvailableTroops": Total troops to distribute (freeTroops + all bonuses),
                    "ownedTerritories": [
                        {"id": "territory_id", "territoryName": "name", "continent": "continent_name", "troops": current_troops}
                    ]
                }
                """
                pattern = """
                    first_reinforcement:
                        - Objective: Initial territory setup. You will place starting troops on your already-assigned territories;
                        - Troop rules:
                            1. freeTroops can be placed on ANY territory you own
                            2. continentBonusTroops can ONLY be placed on territories of that specific continent
                            3. Example: if continentBonusTroops.south_america = 2, those 2 troops can ONLY go to South America territories
                        - Constraints:
                            1. Territory must be owned by you
                            2. The SUM of all troops in placements MUST EQUAL totalAvailableTroops
                            3. Respect continent restrictions for bonus troops
                """
                json_expected = """
                {
                    "action": "first_reinforcement",
                    "placements": [
                        {"territoryId": "id of the territory that will be reinforced", "troops": number_of_troops},
                        {"territoryId": "another_territory_id", "troops": number_of_troops},
                    ]
                }
                """
            case "reinforcement":
                game_data_json = """{
                    "objectiveType": Your game objective type,
                    "objectiveDescription": Your Objective Description. You need to achieve this objective to win,
                    "freeTroops": Troops you can place on ANY territory,
                    "continentBonusTroops": {
                        "south_america": Bonus troops ONLY for South America territories,
                        "north_america": Bonus troops ONLY for North America territories,
                        "europe": Bonus troops ONLY for Europe territories,
                        "asia": Bonus troops ONLY for Asia territories,
                        "africa": Bonus troops ONLY for Africa territories,
                        "oceania": Bonus troops ONLY for Oceania territories
                    },
                    "totalAvailableTroops": Total troops to distribute (freeTroops + all bonuses),
                    "ownedTerritories": [
                        {
                            "id": territory identifier,
                            "territoryName": name of the territory,
                            "continent": which continent it belongs to,
                            "troops": current troops in this territory,
                            "enemyNeighbors": list of enemy territories adjacent to this one (for strategic decisions)
                        }
                    ]
                }
                """
                pattern = """
                    reinforcement:
                        - Objective: Place reinforcement troops to strengthen your position for upcoming attacks or defense;
                        - TROOP RULES:
                            1. freeTroops can be placed on ANY territory you own
                            2. continentBonusTroops can ONLY be placed on territories of that specific continent
                            3. Example: if continentBonusTroops.south_america = 2, those 2 troops can ONLY go to South America territories
                        - Constraints:
                            1. Territory must be owned by you
                            2. The SUM of all troops in placements MUST EQUAL totalAvailableTroops
                            3. Respect continent restrictions for bonus troops
                """
                json_expected = """
                {
                    "action": "reinforcement",
                    "placements": [
                        {"territoryId": "id of territory to reinforce", "troops": number_of_troops},
                        {"territoryId": "another_territory_id", "troops": number_of_troops},
                    ]
                }
                """
            case "attack":
                game_data_json = """{
                    "objectiveType": Your game objective type,
                    "objectiveDescription": Your Objective Description. You need to achieve this objective to win,
                    "territoriesCanAttackFrom": [
                        {
                            "id": territory identifier,
                            "territoryName": name of your territory,
                            "continent": which continent it belongs to,
                            "troops": current troops in this territory (must be >= 2 to attack),
                            "maxDice": maximum dice you can use from this territory (min of 3 or troops-1),
                            "enemyNeighbors": [
                                {"id": "enemy_id", "name": "enemy_name", "troops": enemy_troops, "owner": "owner_name", "continent": "continent_name"}
                            ]
                        }
                    ]
                }
                """
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
                game_data_json = """"""
                pattern = """"""
                json_expected = """"""

            
        return game_data_json, pattern, json_expected