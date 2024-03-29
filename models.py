import json
import os
from collections import defaultdict
from datetime import datetime
from random import shuffle


class Player:
    def __init__(self, last_name, first_name, birth_date, chess_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id

    @staticmethod
    def load_players():
        if os.path.exists('players.json'):
            with open('players.json', 'r') as f:
                return [Player(**player) for player in json.load(f)]
        else:
            return []

    @staticmethod
    def save_players(players):
        with open('players.json', 'w') as f:
            json.dump([player.__dict__ for player in players], f, indent=4)


class Tournament:
    def __init__(self, name, location, start_date, end_date, num_rounds, current_round=1, rounds=None, players=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.current_round = current_round
        self.rounds = rounds if rounds is not None else []
        self.players = []


    @staticmethod
    def load_tournaments():
        if os.path.exists('tournaments.json'):
            with open('tournaments.json', 'r') as f:
                tournament_objects = []
                for tournament in json.load(f):
                    tournament_objects.append(Tournament(**tournament))
                return tournament_objects
        else:
            return []

    @staticmethod
    def save_tournaments(tournaments):
        with open('tournaments.json', 'w') as f:
            data = [tournament.__dict__ for tournament in tournaments]
            json.dump(data, f, indent=4)

    def generate_matches(self, avoid_duplicates=True):
        matches = []
        remaining_players = self.players.copy()
        shuffle(remaining_players)

        while remaining_players:
            player1 = remaining_players.pop(0)
            if remaining_players:
                player2 = remaining_players.pop(0)
                if avoid_duplicates and any(
                    player1 in match and player2 in match for match in matches
                ):
                    remaining_players.append(player1)
                    remaining_players.append(player2)
                else:
                    matches.append([[player1, 0], [player2, 0]])
            else:
                matches.append([[player1, 0]])

        return matches

    def generate_swiss_system_matches(self):
        players_by_score = sorted(
            self.players, key=lambda x: x['score'], reverse=True
        )
        matches = []
        score_groups = defaultdict(list)

        for player in players_by_score:
            score_groups[player['score']].append(player)

        for score, group in sorted(score_groups.items(), reverse=True):
            group_len = len(group)
            if group_len % 2 == 1:
                matches.append([[group.pop(), 0]])
            shuffle(group)
            for i in range(0, group_len, 2):
                player1 = group[i]
                if i + 1 < group_len:
                    player2 = group[i + 1]
                    matches.append([[player1, 0], [player2, 0]])

        return matches

    def play_round(self, round_num):
        round_data = self.rounds[round_num]

        for i, match in enumerate(round_data['matches'], start=1):
            player1 = match[0][0]
            player2 = match[1][0] if len(match) > 1 else None
            result = input(
                f"Enter result for match {i} ({player1['first_name']} "
                f"{player1['last_name']} vs. {player2['first_name']} "
                f"{player2['last_name']}) "
                "(1 for win, 2 for draw, 3 for loss): "
            )

            if result == '1':
                match[0][0]['score'] += 1
            elif result == '2':
                match[0][0]['score'] += 0.5
                match[1][0]['score'] += 0.5
            elif result == '3':
                match[1][0]['score'] += 1

        round_data['end_datetime'] = datetime.now().isoformat()
        self.save_tournaments([self])
        print("\n")
