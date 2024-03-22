import json
import os
from collections import defaultdict
from datetime import datetime
from random import shuffle, choice

if os.path.exists('players.json'):
    with open('players.json', 'r') as f:
        players = json.load(f)
else:
    players = []

if os.path.exists('tournaments.json'):
    with open('tournaments.json', 'r') as f:
        tournaments = json.load(f)
else:
    tournaments = []

def create_player():
    last_name = input("Enter player's last name: ")
    first_name = input("Enter player's first name: ")
    birth_date = input("Enter player's date of birth (YYYY-MM-DD): ")
    chess_id = input("Enter player's national chess ID: ")

    player = {
        'last_name': last_name,
        'first_name': first_name,
        'birth_date': birth_date,
        'chess_id': chess_id,
    }

    players.append(player)
    save_data()
    print("Player added successfully.")

def list_players():
    if not players:
        print("No players found.")
        return

    print("List of players:")
    for i, player in enumerate(sorted(players, key=lambda x: x['last_name'])):
        print(f"{i + 1}. {player['last_name']}, {player['first_name']} ({player['chess_id']})")

def modify_player():
    list_players()
    player_index = int(input("Enter the index of the player you want to modify: ")) - 1

    if player_index < 0 or player_index >= len(players):
        print("Invalid player index.")
        return

    player = players[player_index]
    print(f"Modifying player: {player['last_name']}, {player['first_name']} ({player['chess_id']})")

    last_name = input(f"Enter new last name (leave blank to keep '{player['last_name']}'): ") or player['last_name']
    first_name = input(f"Enter new first name (leave blank to keep '{player['first_name']}'): ") or player['first_name']
    birth_date = input(f"Enter new date of birth (YYYY-MM-DD) (leave blank to keep '{player['birth_date']}'): ") or player['birth_date']
    chess_id = input(f"Enter new national chess ID (leave blank to keep '{player['chess_id']}'): ") or player['chess_id']

    player['last_name'] = last_name
    player['first_name'] = first_name
    player['birth_date'] = birth_date
    player['chess_id'] = chess_id

    save_data()
    print("Player modified successfully.")

def create_tournament():
    name = input("Enter tournament name: ")
    location = input("Enter tournament location: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    num_rounds = int(input("Enter number of rounds (default 4): ") or 4)

    tournament = {
        'name': name,
        'location': location,
        'start_date': start_date,
        'end_date': end_date,
        'num_rounds': num_rounds,
        'current_round': 1,
        'rounds': [],
        'players': [],
    }

    tournaments.append(tournament)
    save_data()
    print("Tournament created successfully.")

def modify_tournament():
    list_tournaments()
    tournament_index = int(input("Enter the index of the tournament you want to modify: ")) - 1

    if tournament_index < 0 or tournament_index >= len(tournaments):
        print("Invalid tournament index.")
        return

    tournament = tournaments[tournament_index]
    print(f"Modifying tournament: {tournament['name']} ({tournament['location']})")

    name = input(f"Enter new name (leave blank to keep '{tournament['name']}'): ") or tournament['name']
    location = input(f"Enter new location (leave blank to keep '{tournament['location']}'): ") or tournament['location']
    start_date = input(f"Enter new start date (YYYY-MM-DD) (leave blank to keep '{tournament['start_date']}'): ") or tournament['start_date']
    end_date = input(f"Enter new end date (YYYY-MM-DD) (leave blank to keep '{tournament['end_date']}'): ") or tournament['end_date']
    num_rounds = int(input(f"Enter new number of rounds (leave blank to keep {tournament['num_rounds']}): ") or tournament['num_rounds'])

    tournament['name'] = name
    tournament['location'] = location
    tournament['start_date'] = start_date
    tournament['end_date'] = end_date
    tournament['num_rounds'] = num_rounds

    save_data()
    print("Tournament modified successfully.")

def register_players(tournament_index):
    tournament = tournaments[tournament_index]

    print("Select players to register (enter 'done' when finished):")
    registered_players = []
    while True:
        player_id = input("Enter player's chess IDs by comma: ").strip()
        if player_id.lower() == 'done':
            break

        player = next((p for p in players if p['chess_id'] == player_id), None)
        if not player:
            print(f"Player with ID {player_id} not found.")
            continue

        registered_players.append({
            'last_name': player['last_name'],
            'first_name': player['first_name'],
            'birth_date': player['birth_date'],
            'chess_id': player['chess_id'],
            'score': 0
        })

    if len(registered_players) < 16:
        print("At least 16 players are required to launch a tournament of 4 rounds.")
        return

    tournament['players'] = registered_players
    save_data()
    print("Players registered successfully.")

def generate_matches(players, avoid_duplicates=True):
    matches = []
    remaining_players = players.copy()
    shuffle(remaining_players)

    while remaining_players:
        player1 = remaining_players.pop(0)
        if remaining_players:
            player2 = remaining_players.pop(0)
            if avoid_duplicates and any(player1 in match and player2 in match for match in matches):
                remaining_players.append(player1)
                remaining_players.append(player2)
            else:
                matches.append([[player1, 0], [player2, 0]])
        else:
            matches.append([[player1, 0]])

    return matches


def generate_swiss_system_matches(players):
    players_by_score = sorted(players, key=lambda x: x['score'], reverse=True)
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

def launch_tournament(tournament_index):
    tournament = tournaments[tournament_index]

    if len(tournament['players']) < 16:
        print("At least 16 players are required to launch a tournament of 4 rounds.")
        return

    for round_num in range(tournament['num_rounds']):
        round_name = f"Round {round_num + 1}"
        print(f"\n{round_name}")

        matches = generate_swiss_system_matches(tournament['players'])

        round_data = {
            'name': round_name,
            'start_datetime': datetime.now().isoformat(),
            'matches': matches,
        }

        tournament['rounds'].append(round_data)
        save_data()

        play_round(tournament_index, round_num)

    print("\nTournament finished.")
    winner = max(tournament['players'], key=lambda x: x['score'])
    print(f"The winner is {winner['first_name']} {winner['last_name']} ({winner['chess_id']})")

def play_round(tournament_index, round_num):
    tournament = tournaments[tournament_index]
    round_data = tournament['rounds'][round_num]

    print(f"\n{round_data['name']}")
    print(f"Start: {round_data['start_datetime']}")

    print("\nMatches:")
    for i, match in enumerate(round_data['matches'], start=1):
        player1 = match[0][0]
        player2 = match[1][0] if len(match) > 1 else None
        print(f"Match {i}: {player1['first_name']} {player1['last_name']} ({player1['score']}) vs. {player2['first_name']} {player2['last_name']} ({player2['score']})")

    while True:
        match_num = input("Enter match number (or 'done' to finish round): ")
        if match_num.lower() == 'done':
            round_data['end_datetime'] = datetime.now().isoformat()
            save_data()
            print("Round finished.")
            break

        try:
            match_num = int(match_num)
        except ValueError:
            print("Invalid match number.")
            continue

        if not (1 <= match_num <= len(round_data['matches'])):
            print("Invalid match number.")
            continue

        match = round_data['matches'][match_num - 1]
        result = input(f"Enter result for match {match_num} ({match[0][0]['first_name']} {match[0][0]['last_name']} vs. {match[1][0]['first_name']} {match[1][0]['last_name']}) (1 for win, 2 for draw, 3 for loss): ")

        if result == '1':
            match[0][0]['score'] += 1
        elif result == '2':
            match[0][0]['score'] += 0.5
            match[1][0]['score'] += 0.5
        elif result == '3':
            match[1][0]['score'] += 1
        else:
            print("Invalid result.")
            continue

        save_data()

    print(f"\nEnd: {round_data['end_datetime']}")

def summary_rounds(tournament_index):
    tournament = tournaments[tournament_index]

    for round_num, round_data in enumerate(tournament['rounds'], start=1):
        print(f"\n{round_data['name']}")
        print(f"Start: {round_data['start_datetime']}")
        print(f"End: {round_data['end_datetime']}")

        print("\nMatches:")
        for i, match in enumerate(round_data['matches'], start=1):
            player1 = match[0][0]
            player2 = match[1][0] if len(match) > 1 else None
            print(f"Match {i}: {player1['first_name']} {player1['last_name']} ({match[0][1]}) vs. {player2['first_name']} {player2['last_name']} ({match[1][1]})")

def save_data():
    with open('players.json', 'w') as f:
        json.dump(players, f, indent=4)

    with open('tournaments.json', 'w') as f:
        json.dump(tournaments, f, indent=4)

def list_tournaments():
    if not tournaments:
        print("No tournaments found.")
        return

    print("List of tournaments:")
    for i, tournament in enumerate(tournaments):
        print(f"{i + 1}. {tournament['name']} ({tournament['location']})")

def main():
    while True:
        print("\nMenu:")
        print("1. Create tournament")
        print("2. Modify tournament")
        print("3. Create player")
        print("4. List players")
        print("5. Modify player")
        print("6. Register players for tournament")
        print("7. Launch tournament")
        print("8. See ongoing matches")
        print("9. Enter match results")
        print("10. Summary of rounds")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_tournament()
        elif choice == '2':
            modify_tournament()
        elif choice == '3':
            create_player()
        elif choice == '4':
            list_players()
        elif choice == '5':
            modify_player()
        elif choice == '6':
            list_tournaments()
            tournament_index = int(input("Enter tournament index: ")) - 1
            register_players(tournament_index)
        elif choice == '7':
            list_tournaments()
            tournament_index = int(input("Enter tournament index: ")) - 1
            launch_tournament(tournament_index)
        elif choice == '8':
            list_tournaments()
            tournament_index = int(input("Enter tournament index: ")) - 1
            tournament = tournaments[tournament_index]
            if tournament['rounds']:
                current_round = tournament['rounds'][-1]
                print(f"\nCurrent round: {current_round['name']}")
                print("Matches:")
                for i, match in enumerate(current_round['matches'], start=1):
                    print(f"Match {i}: {match[0][0]['first_name']} {match[0][0]['last_name']} vs. {match[1][0]['first_name']} {match[1][0]['last_name']}")
            else:
                print("No ongoing matches found.")
        elif choice == '9':
            list_tournaments()
            tournament_index = int(input("Enter tournament index: ")) - 1
            round_num = len(tournaments[tournament_index]['rounds']) - 1
            play_round(tournament_index, round_num)
        elif choice == '10':
            list_tournaments()
            tournament_index = int(input("Enter tournament index: ")) - 1
            summary_rounds(tournament_index)
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()