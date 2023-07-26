import pygame
import socket
import pickle

pygame.init()


# Define the Player class
class Player:
    def __init__(self, x, y, thickness, altitude):
        self.x = x
        self.y = y
        self.width = thickness
        self.height = altitude

    def draw(self, Window):
        pygame.draw.rect(Window, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def move_up(self):
        self.y -= 5

    def move_down(self):
        self.y += 5


# Define the Network class
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "124.253.61.13"
        self.port = 50000
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


width = 500
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(win: object, plr: object, plr2: object) -> object:
    win.fill((255, 255, 255))
    plr.draw(win)
    plr2.draw(win)
    pygame.display.update()
    return object


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    p = n.get_player()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p.move_left()
        elif keys[pygame.K_RIGHT]:
            p.move_right()
        elif keys[pygame.K_UP]:
            p.move_up()
        elif keys[pygame.K_DOWN]:
            p.move_down()

        redraw_window(window, p, p2)


if __name__ == '__main__':
    main()
