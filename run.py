import random
#use random to generate random numbers
class Player:
    def __init__(self, name):
        self.name = name
        self.ships = []
        self.stats = {"wins": 0, "losses": 0}

    def add_ship(self, ship):
        self.ships.append(ship)
# use player class to represent a player in the game. Each player has a name, a list of ships, and stats for wins and losses.
class Ship:
    def __init__(self, locations):
        self.locations = locations
        self.hits = 0
        
    def is_sunk(self):
        return self.hits == len(self.locations)
# use ship class to represent a ship. Each ship has a list of locations and a count of hits.
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
# use game class to represent the game itself. The game has a player, a computer opponent, a grid size, player grids, a game mode, and variables to track the last hit and tried directions.

        for i in range(1, 6):
            ship_locations = self.random_ship_location(i)
            self.player.add_ship(Ship(list(ship_locations)))
            
            ship_locations = self.random_ship_location(i)
            self.computer.add_ship(Ship(list(ship_locations)))

        if mode == 'medium':
            self.computer_guess = self.medium_mode_guess
        else:
            self.computer_guess = self.random_guess
# two difficulty settings built into the game

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
# generates random ship locations based on the grid size and ship length.

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
##implements medium difficulty guessing for the computer opponent.

    def random_guess(self):
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)
        return (row, col)
# generates random guesses for the computer opponent.

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
#checks if a guess is valid and updates the player and computer grids accordingly. It also checks if a ship is sunk and determines the game outcome.    

#functions as the entry point of the program. It prompts the user to enter their name, the grid size, and the game mode (easy or medium).
def main():
    while True:
        name = input("Enter your name:\n")
        player = Player(name)
        computer = Player("Computer")
        grid_size = int(input("Enter the grid size (at least 10 recommended):\n"))
        mode = input("Choose a mode (easy, medium):\n")

#function has two nested while loops to handle game rounds and play again functionality. Inside the loops, it creates a new game instance and prompts the user and computer for guesses.
        while True:
            game = Game(player, computer, grid_size, mode)

            while True:
                game.display_grid()
                if game.player_turn:
                    row = int(input("{} Guess Row (0 to {}): ".format(player.name, grid_size - 1)))
                    col = int(input("{} Guess Col (0 to {}): ".format(player.name, grid_size - 1)))
                    
                    if game.guess(game.computer, game.player, row, col):
                        game.display_grid()
                        player.stats["wins"] += 1
                        print("Game over. {} wins!".format(player.name))
                        break
                else:
                    row, col = game.computer_guess()
                    print("Computer is guessing ({}, {})".format(row, col))
                    if game.guess(game.player, game.computer, row, col):
                        game.display_grid()
                        computer.stats["wins"] += 1
                        print("Game over. Computer wins!")
                        break

                game.player_turn = not game.player_turn

            play_again = input("Do you want to play again? (yes/no):\n")
            if play_again.lower() != "yes":
                break
#prompt allows the player to choose whether to play again. If the player enters "yes," the inner loop repeats, starting a new game. If the player enters "no," the outer loop breaks, ending the program.

if __name__ == "__main__":
    main()