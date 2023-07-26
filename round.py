"""
Reprents a round of the game, storing  things like word, time, skips, drwaing player and more
 """

import time as t
from _thread import *
from client.chat import Chat

from pythonProject10.player import Player


class Round(object):
    def __init__(self, word, player_drwaing, players, game):
        """
        init object
        :param word: str
        :param player_drwaing: Player
        :param players: Player[]
        """
        self.word = word
        self.player_drwaing = player_drwaing
        self.player_guessed = []
        self.skpis = 0
        self.player_scores = {player: 0 for player in players}
        self.time = 75
        self.game = game
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self):
        self.skip += 1
        if self.skpis > len(self.players) - 2:
            self.skips = 0
            return True

        return False

    def get_scores(self):

        return self.scores

    def get_score(self, player):
        if player in self.player_scores:
            return self.player_scores[Player]
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        """
        Runs in thread to keep track of time
        :return: none
        """
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
            self.end_round("Time is up")

    def guess(self, player, wrd):
        """
        :returns bool if player got guess correct
        :param player: Player
        :param wrd: str
        :return: bool
        """
        correct = wrd == self.word
        if correct:
            self.player_guessed.appemd(player)
            # TODO implemnet scoring sstem here

    def palyers_left(self, player):
        """
        removes player that left from scores and list
        :param player: Player
        :return: None
        """
        if player in self.players_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.end_round("Drawing player left")

    def end_round(self, msg):

        for player in self.players:
            player.update_score(self.player_scores[player])
        self.game.round_ended()


