import random

class Player:
    def __init__(self, name):
        self.name = name
        self.ships = []
        self.stats = {"wins": 0, "losses": 0}

    def add_ship(self, ship):
        self.ships.append(ship)

class Ship:
    def __init__(self, locations):
        self.locations = locations
        self.hits = 0
        
    def is_sunk(self):
        return self.hits == len(self.locations)

class Game: