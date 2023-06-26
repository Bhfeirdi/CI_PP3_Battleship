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
    def __init__(self, player, computer, grid_size, mode):
        self.player = player
        self.computer = computer
        self.grid_size = grid_size
        self.player_grid = [['O'] * grid_size for _ in range(grid_size)]
        self.computer_grid = [['O'] * grid_size for _ in range(grid_size)]
        self.mode = mode
        self.last_hit = None
        self.tried_directions = []
        self.player_turn = True

        # Add ships to the players
        for i in range(1, 6):
            ship_locations = self.random_ship_location(i)
            self.player.add_ship(Ship(list(ship_locations)))

            ship_locations = self.random_ship_location(i)
            self.computer.add_ship(Ship(list(ship_locations)))

        if mode == 'medium':
            self.computer_guess = self.medium_mode_guess
        else:
            self.computer_guess = self.random_guess