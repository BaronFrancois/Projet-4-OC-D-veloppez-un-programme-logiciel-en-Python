from models import Player, Tournament
from datetime import datetime


class View:
    def __init__(self, controller):
        self.controller = controller

    def display_menu(self):
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

    def get_user_choice(self):
        return input("Enter your choice: ")

    def create_player(self):
        last_name = input("Enter player's last name: ")
        first_name = input("Enter player's first name: ")
        birth_date = input("Enter player's date of birth (YYYY-MM-DD): ")
        chess_id = input("Enter player's national chess ID: ")

        return Player(last_name, first_name, birth_date, chess_id)

    def list_players(self, players):
        if not players:
            print("No players found.")
            return

        print("List of players:")
        for i, player in enumerate(sorted(players, key=lambda x: x.last_name),
                                   start=1):
            print(f"{i}. {player.last_name}, {player.first_name} "
                  f"({player.chess_id})")

    def modify_player(self, players):
        self.list_players(players)
        player_index = int(input("Enter the index of the player you want to "
                                 "modify: ")) - 1

        if player_index < 0 or player_index >= len(players):
            print("Invalid player index.")
            return

        player = players[player_index]
        print(f"Modifying player: {player.last_name}, {player.first_name} "
              f"({player.chess_id})")

        last_name = input(f"Enter new last name (leave blank to keep "
                          f"'{player.last_name}'): ") or player.last_name
        first_name = input(f"Enter new first name (leave blank to keep "
                           f"'{player.first_name}'): ") or player.first_name
        birth_date = input(
            f"Enter new date of birth (YYYY-MM-DD) "
            f"(leave blank to keep '{player.birth_date}'): "
        ) or player.birth_date
        chess_id = input(f"Enter new national chess ID (leave blank to keep "
                         f"'{player.chess_id}'): ") or player.chess_id

        player.last_name = last_name
        player.first_name = first_name
        player.birth_date = birth_date
        player.chess_id = chess_id

    def create_tournament(self):
        name = input("Enter tournament name: ")
        location = input("Enter tournament location: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        num_rounds = int(input("Enter number of rounds (default 4): ") or 4)

        return Tournament(name, location, start_date, end_date, num_rounds)

    def modify_tournament(self, tournaments):
        self.list_tournaments(tournaments)
        tournament_index = int(input("Enter the index of the tournament you "
                                     "want to modify: ")) - 1

        if tournament_index < 0 or tournament_index >= len(tournaments):
            print("Invalid tournament index.")
            return

        tournament = tournaments[tournament_index]
        print(f"Modifying tournament: {tournament.name} "
              f"({tournament.location})")

        name = input(f"Enter new name (leave blank to keep "
                     f"'{tournament.name}'): ") or tournament.name
        location = input(f"Enter new location (leave blank to keep "
                         f"'{tournament.location}'): ") or tournament.location
        start_date = input(
            f"Enter new start date (YYYY-MM-DD) "
            f"(leave blank to keep '{tournament.start_date}'): "
        ) or tournament.start_date
        end_date = input(
            f"Enter new end date (YYYY-MM-DD) "
            f"(leave blank to keep '{tournament.end_date}'): "
        ) or tournament.end_date
        num_rounds = int(
            input(
                f"Enter new number of rounds "
                f"(leave blank to keep {tournament.num_rounds}): "
            ) or tournament.num_rounds
        )

        tournament.name = name
        tournament.location = location
        tournament.start_date = start_date
        tournament.end_date = end_date
        tournament.num_rounds = num_rounds

    def list_tournaments(self, tournaments):
        if not tournaments:
            print("No tournaments found.")
            return

        print("List of tournaments:")
        for i, tournament in enumerate(tournaments, start=1):
            print(f"{i}. {tournament.name} ({tournament.location})")

    def register_players(self, tournament):
        print("Select players to register (enter 'done' when finished):")
        registered_players = []
        while True:
            player_id = input("Enter player's chess IDs by comma: ").strip()
            if player_id.lower() == 'done':
                break

            player = next((p for p in self.controller.players
                           if p.chess_id == player_id), None)
            if not player:
                print(f"Player with ID {player_id} not found.")
                continue

            registered_players.append({
                'last_name': player.last_name,
                'first_name': player.first_name,
                'birth_date': player.birth_date,
                'chess_id': player.chess_id,
                'score': 0
            })

        if len(registered_players) < 16:
            print("At least 16 players are required to launch a tournament "
                  "of 4 rounds.")
            return

        tournament.players = registered_players

    def launch_tournament(self, tournament):
        if len(tournament.players) < 16:
            print("At least 16 players are required to launch a tournament "
                  "of 4 rounds.")
            return

        for round_num in range(tournament.num_rounds):
            round_name = f"Round {round_num + 1}"
            print(f"\n{round_name}")

            matches = tournament.generate_swiss_system_matches()

            round_data = {
                'name': round_name,
                'start_datetime': datetime.now().isoformat(),
                'matches': matches,
            }

            tournament.rounds.append(round_data)

            print(f"\n{round_data['name']}")
            print(f"Start: {round_data['start_datetime']}")

            print("\nMatches:")
            for i, match in enumerate(round_data['matches'], start=1):
                player1 = match[0][0]
                player2 = match[1][0] if len(match) > 1 else None
                match_info = "Match {}: {} {} ({}) vs. {} {} ({})".format(
                    i, player1['first_name'],
                    player1['last_name'], player1['score'],
                    player2['first_name'],
                    player2['last_name'], player2['score']
                )
                print(match_info)
            tournament.play_round(round_num)

            print(f"\nEnd: {round_data['end_datetime']}")

        print("\nTournament finished.")
        winner = max(tournament.players, key=lambda x: x['score'])
        print(f"The winner is {winner['first_name']} {winner['last_name']} "
              f"({winner['chess_id']})")

    def show_ongoing_matches(self, tournament):
        if tournament.rounds:
            current_round = tournament.rounds[-1]
            print(f"\nCurrent round: {current_round['name']}")
            print("Matches:")
            for i, match in enumerate(current_round['matches'], start=1):
                print("Match {0}: {1} {2} vs. {3} {4}".format(
                    i, match[0][0]['first_name'],
                    match[0][0]['last_name'],
                    match[1][0]['first_name'],
                    match[1][0]['last_name']
                ))

        else:
            print("No ongoing matches found.")

    def enter_match_results(self, tournament):
        round_num = len(tournament.rounds) - 1
        tournament.play_round(round_num)

    def summary_rounds(self, tournament):
        for round_num, round_data in enumerate(tournament.rounds, start=1):
            print(f"\n{round_data['name']}")
            print(f"Start: {round_data['start_datetime']}")
            print(f"End: {round_data['end_datetime']}")

            print("\nMatches:")
            for i, match in enumerate(round_data['matches'], start=1):
                player1 = match[0][0]
                player2 = match[1][0] if len(match) > 1 else None
                print("Match {}: {} {} ({}), {} {} ({})".format(
                    i,
                    player1['first_name'], player1['last_name'], match[0][1],
                    player2['first_name'], player2['last_name'], match[1][1]
                ))
