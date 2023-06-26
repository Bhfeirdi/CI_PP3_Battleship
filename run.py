import random

class Player:
    def __init__(self, name):
        self.name = name
        self.ships = []
        self.stats = {"wins": 0, "losses": 0}