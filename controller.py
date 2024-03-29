from models import Player, Tournament
from views import View


class Controller:
    def __init__(self):
        self.players = Player.load_players()
        self.tournaments = Tournament.load_tournaments()
        self.view = View(self)

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_user_choice()

            if choice == '1':
                self.create_tournament()
            elif choice == '2':
                self.modify_tournament()
            elif choice == '3':
                self.create_player()
            elif choice == '4':
                self.list_players()
            elif choice == '5':
                self.modify_player()
            elif choice == '6':
                self.register_players()
            elif choice == '7':
                self.launch_tournament()
            elif choice == '8':
                self.show_ongoing_matches()
            elif choice == '9':
                self.enter_match_results()
            elif choice == '10':
                self.summary_rounds()
            elif choice == '11':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_player(self):
        player = self.view.create_player()
        self.players.append(player)
        Player.save_players(self.players)

    def list_players(self):
        self.view.list_players(self.players)

    def modify_player(self):
        self.view.modify_player(self.players)
        Player.save_players(self.players)

    def create_tournament(self):
        tournament = self.view.create_tournament()
        self.tournaments.append(tournament)
        Tournament.save_tournaments(self.tournaments)

    def modify_tournament(self):
        self.view.modify_tournament(self.tournaments)
        Tournament.save_tournaments(self.tournaments)

    def register_players(self):
        self.view.list_tournaments(self.tournaments)
        tournament_index = int(input("Enter tournament index: ")) - 1
        self.view.register_players(self.tournaments[tournament_index])
        Tournament.save_tournaments(self.tournaments)

    def launch_tournament(self):
        self.view.list_tournaments(self.tournaments)
        tournament_index = int(input("Enter tournament index: ")) - 1
        self.view.launch_tournament(self.tournaments[tournament_index])
        Tournament.save_tournaments(self.tournaments)

    def show_ongoing_matches(self):
        self.view.list_tournaments(self.tournaments)
        tournament_index = int(input("Enter tournament index: ")) - 1
        self.view.show_ongoing_matches(self.tournaments[tournament_index])

    def enter_match_results(self):
        self.view.list_tournaments(self.tournaments)
        tournament_index = int(input("Enter tournament index: ")) - 1
        self.view.enter_match_results(self.tournaments[tournament_index])
        Tournament.save_tournaments(self.tournaments)

    def summary_rounds(self):
        self.view.list_tournaments(self.tournaments)
        tournament_index = int(input("Enter tournament index: ")) - 1
        self.view.summary_rounds(self.tournaments[tournament_index])


if __name__ == '__main__':
    controller = Controller()
    controller.run()
    print("\n")
