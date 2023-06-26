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

    def random_ship_location(self, length):
        horizontal = random.choice([True, False])
        if horizontal:
            row = random.randint(0, self.grid_size-1)
            col = random.randint(0, self.grid_size-length)
            return [[row, col+i] for i in range(length)]
        else:
            row = random.randint(0, self.grid_size-length)
            col = random.randint(0, self.grid_size-1)
            return [[row+i, col] for i in range(length)]

    def display_grid(self):
        print(f"\n{self.player.name}'s Fleet Status:")
        for row in self.player_grid:
            print(" ".join(row))

        print(f"\n{self.computer.name}'s Fleet Status:")
        for row in self.computer_grid:
            print(" ".join(row))

    def medium_mode_guess(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.last_hit:
            for i in range(len(directions)):
                if i in self.tried_directions:
                    continue
                r, c = self.last_hit[0] + directions[i][0], self.last_hit[1] + directions[i][1]
                if r >= 0 and r < self.grid_size and c >= 0 and c < self.grid_size and self.player_grid[r][c] == 'O':
                    self.tried_directions.append(i)
                    return (r, c)
        self.last_hit = None
        self.tried_directions = []
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if self.player_grid[row][col] == 'O':
                return (row, col)

    def random_guess(self):
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)
        return (row, col)

    def guess(self, player, guesser, guess_row, guess_col):
        grid = self.player_grid if guesser == self.computer else self.computer_grid
        if guess_row < 0 or guess_row >= self.grid_size or guess_col < 0 or guess_col >= self.grid_size:
            print("Oops, that's off the board!.")
            return False
        elif grid[guess_row][guess_col] == 'X' or grid[guess_row][guess_col] == '1':
            print("You've already guessed that one!'.")
        else:
            hit = False
            for ship in player.ships:
                if [guess_row, guess_col] in ship.locations:
                    ship.hits += 1
                    hit = True
                    grid[guess_row][guess_col] = '1'
                    if guesser == self.computer:
                        self.last_hit = (guess_row, guess_col)
                    if ship.is_sunk():
                        print("Nailed it! You sank a battleship!")
                        if all(ship.is_sunk() for ship in player.ships):
                            print("Congratulations! You've sank all their battleships'!")
                            return True
                    break
            if not hit:
                print("That's a miss, try again!")
                grid[guess_row][guess_col] = 'X'
        return False