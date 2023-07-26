import Player
import Game
import socket
from client.player import Player
import threading
import json


class Server(object):
    PLAYER = 8

    def __inint__(self):
        self.connection_queue = []
        self.game_id = 0


connection_queue = []


def player_thread(self, conn, player):
    """
    handles in game comunnication
    """
    while True:
        try:
            # recieve request
            data = conn.recv(1024)
            data = json.loads(data)
            # player is not a apart of it
            keys = [key for key in data.keys()]
            send_msg = {key:[] for key in keys}

            for key in keys:
                if key == -1: #get game, returns a list of players
                    if player.game: 
                        send_msg[-1] = player.game.players
                    else:
                        send_msg[-1] = []

            if player.game:
                if key == 0: #guess
                    correct = player.game.palyer_guess(player, data[0][0])
                    send_msg[0] = [correct] 
                elif key == 1: #skip
                    skip = player.game.skip()
                    send_msg[0] = [skip] 

                elif key == 2: #get chat
                    content = player.game.round.chat.get_chat()
                    send_msg[2] = content 
                elif key == 3: #get board  
                    brd = player.game.get_board()
                    send_msg[3] = brd
                
                elif key == 4: #get score
                    scores = player.game.get_player_scores()
                    send_msg[4] = scores
                elif key == 5: #get round
                        rnd = player.game.round_count
                        send_msg[5] = rnd
                elif key == 6: #get word
                    word = player.game.word
                    send_msg[6] = word
                elif key == 7: #get skips
                    key = player.ame.round.skips
                    send_msg[8] = key
                elif key == 8: #update board
                    x, y, color = data[8][:3]
                    self.game.update_board(x, y, color)
                elif key == 9: #get round time
                    t = self.gam.round.time
                    send_msg[9] = t

                else:
                    raise Exception("Not a valid request")



            conn.sendall(json.dumps(send_msg))

        except Exception as e:
            print(f"[EXECPTION] {player.get_name()} disconnected:", e)
            conn.close()
            # todo 

def handle_queue(self, player):

        self.connection_queue.append()

        if len(self.connection_queue) >= 8:
            game = Game(self.connection_queue[:], self.game_id)

            for p in self.connection_queue:
                p.set_game(game)

            self.game_id +=  1
            self.connection_queue = []
        

    
def authentication(self, conn, addr):
    """
    authentication here
    """
    try:
        data = conn.recv(16)
        name = str(data.decode())
        if not name:
            raise Exception("No name received")
        
        conn.sendall("1".encode)

        player = Player(addr, name)
        self.handle_queue(player)
        threading.Thread (target=self.player_thread, args=(conn, player))
    except Exception as e:
        print("[EXECEPTION]", e)
        conn.close()



def connection_thread(self):

    server = "124.253.63.136"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen()
    print("waiting for a connection, Server Started")

    while True:
        conn, addr = s.accept()
        print("[CONNECT] new connection!")

        self.authentication(conn, addr)

        threading.Thread (target=player_thread, args=(addr,))

        if __name__ == "__main__":
           s = Server()
           threading.Thread(target=connection_thread)






