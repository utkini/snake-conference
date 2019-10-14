from game.game_log import SnakeGameLog
from game.game_players_loader import FilePlayersLoader
from game.play import SnakeGame


def main():
    players = FilePlayersLoader().get_players()
    sg = SnakeGame(players)
    sg.run()
    SnakeGameLog(sg).save()


if __name__ == '__main__':
    main()
