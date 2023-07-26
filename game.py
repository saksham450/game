from client.board import Board
from round import Round
import random


class Game(object):

    def __init__(self, game_id, players):
        """
        Initialize the game once the player threshold is met.
        :param game_id: int
        :param players: Player[]
        """
        self.game_id = game_id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        """
        Starts a new round with a new word.
        :return: None
        """
        try:
            round_word = self.get_word()
            self.round = Round(round_word, self.players[self.player_draw_ind], self)
            self.round_count += 1

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except IndexError:
            self.end_game()

    def player_guess(self, player, guess):
        """
        Makes the player guess the word.
        :param player: Player
        :param guess: str
        :return: bool
        """
        return self.round.guess(player, guess)

    def player_disconnected(self, player):
        """
        Call to clean up objects when player disconnects.
        :param player: Player
        :raises: Exception()
        """

        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat(f"Player {player.get_name()} disconnected.")
        else:
            raise Exception("Player not in game")

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self):
        """
        Returns a dictionary of player scores.
        :return: dict
        """
        scores = {player.name: player.get_score() for player in self.players}
        return scores

    def skip(self):
        """
        Increments the round skips. If skips are greater than
        the threshold, starts a new round.
        :return: bool
        """
        if self.round:
            new_round = self.round.skip()
            self.round.chat.update_chat(f"Player has voted to skip ({self.round.skips}/{len(self.players) - 2})")
            if new_round:
                self.round.chat.update_chat(f"Round has been skipped.")
                self.round_ended()
                return True
            return False
        else:
            raise Exception("No round started yet!")

    def round_ended(self):
        """
        Called when the round ends.
        :return: None
        """
        self.round.chat.update_chat(f"Round {self.round_count} has ended.")
        self.start_new_round()
        self.board.clear()

    def update_board(self, x, y, color):
        """
        Calls the update method on the board.
        :param x: int
        :param y: int
        :param color: 0-8
        :return: None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self):
        """
        Ends the game.
        :return: None
        """
        print(f"[GAME] Game {self.game_id} ended")
        for player in self.players:
            player.game = None

    def get_word(self):
        """
        Retrieves a word that has not yet been used.
        :return: str
        """
        with open("words.txt", "r") as f:
            words = []

            for line in f:
                word = line.strip()
                if word not in self.words_used:
                    words.append(word)

            r = random.randint(0, len(words) - 1)
            word = words[r].strip()
            self.words_used.add(word)

            return word
