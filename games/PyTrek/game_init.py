# game_init.py

import random
import time

# Global variables for game state
energy0 = 3000  # Starting Energy
torps0 = 10     # Photon Torpedo capacity
map_size = 8
klingons_left = 0
starbases_left = 0

# Galaxy map: represents the 8x8 map in Python as a 2D list
galaxy_map = [[0 for _ in range(map_size)] for _ in range(map_size)]

def intro():
    """Display the introduction and seed the random number generator."""
    print("Welcome to the Super Star Trek game!")
    # Seed the random number generator with the current time
    random.seed(time.time())
    # Print other introductory messages here if needed

def new_game():
    """Initialize and start a new game."""
    global energy0, torps0, klingons_left, starbases_left, galaxy_map
    print("Initializing new game...")
    initialize()
    short_range_scan()  # This function will need to be added or imported

def initialize():
    """Set up the initial game state."""
    global klingons_left, starbases_left, galaxy_map
    klingons_left = 0
    starbases_left = 0
    for i in range(map_size):
        for j in range(map_size):
            r = random.randint(1, 100)
            klingons = 0
            if r > 98:
                klingons = 3
            elif r > 95:
                klingons = 2
            elif r > 80:
                klingons = 1

            klingons_left += klingons
            starbases = 1 if random.randint(1, 100) > 96 else 0
            starbases_left += starbases

            galaxy_map[i][j] = (klingons << 8) + (starbases << 4) + random.randint(1, 8)

    if starbases_left == 0:
        y, x = random.randint(0, map_size - 1), random.randint(0, map_size - 1)
        galaxy_map[y][x] += (1 << 4)
        starbases_left += 1

    print("Game setup complete.")


# Add this to game_init.py

def short_range_scan():
    """Perform a short-range scan of the current sector and print the results with aligned ASCII art."""
    global ship_y, ship_x, galaxy_map

    cell_width = 5  # Adjust to match the width of each cell in the row
    separator_length = map_size * cell_width

    print("\nShort Range Scan Report:")
    print("-" * separator_length)  # Print a separator line with the correct width

    for i in range(map_size):
        row_display = ""
        for j in range(map_size):
            if i == ship_y and j == ship_x:
                row_display += " >=> "  # ASCII art for the Federation Class heavy cruiser
            elif (galaxy_map[i][j] >> 8) & 0xF > 0:  # Check for Klingons
                row_display += " <K> "
            elif (galaxy_map[i][j] >> 4) & 0xF > 0:  # Check for Starbases
                row_display += " [B] "
            else:
                row_display += "  .  "  # Empty space with padding
        print(row_display)

    print("-" * separator_length)  # Print the closing separator line
    print("\nStatus: Short-range scan complete.\n")


# Global variables for ship position
ship_y = 0  # Initial y-coordinate of the ship
ship_x = 0  # Initial x-coordinate of the ship


def navigation():
    """Move the ship based on player input."""
    global ship_y, ship_x, galaxy_map, energy0

    if energy0 <= 0:
        print("Not enough energy to move.")
        return

    try:
        direction = int(input("Enter course (1-9): "))
        if direction < 1 or direction > 9:
            print("Invalid direction. Please enter a number from 1 to 9.")
            return

        distance = int(input("Enter warp factor (1-8): "))
        if distance < 1 or distance > 8:
            print("Invalid warp factor. Please enter a number from 1 to 8.")
            return

        # Map the direction to x, y changes
        dir_map = {
            1: (1, -1),  # down-left
            2: (1, 0),  # down
            3: (1, 1),  # down-right
            4: (0, -1),  # left
            5: (0, 0),  # stay (not used but placeholder)
            6: (0, 1),  # right
            7: (-1, -1),  # up-left
            8: (-1, 0),  # up
            9: (-1, 1),  # up-right
        }

        dy, dx = dir_map[direction]

        # Calculate new position
        new_y = ship_y + (dy * distance)
        new_x = ship_x + (dx * distance)

        # Check for boundaries
        if new_y < 0 or new_y >= map_size or new_x < 0 or new_x >= map_size:
            print("Cannot move outside the current sector boundaries.")
            return

        # Update ship position
        ship_y, ship_x = new_y, new_x
        energy0 -= distance * 10  # Deduct energy (adjust as needed)
        print(f"Ship moved to sector ({ship_y}, {ship_x}). Energy remaining: {energy0}.")

        # Check for docking and repair
        dock_and_repair()

    except ValueError:
        print("Invalid input. Please enter numeric values only.")

def dock_and_repair():
    """Repair the ship and replenish energy and torpedoes when docked at a base."""
    global ship_y, ship_x, galaxy_map, energy0, torps0

    if (galaxy_map[ship_y][ship_x] >> 4) & 0xF > 0:  # Check if there is a starbase at the current location
        print("\nDocked at a starbase. Repairs and resupply in progress...")
        energy0 = 3000  # Reset energy to maximum
        torps0 = 10  # Reset torpedoes to full capacity

        # Optionally, add a ship's damage system if needed and reset it here
        # Example: resetting a damage list where all damage is set to 0 (no damage)
        damage = [0] * 8  # Assuming 8 systems that can be damaged
        print("All systems have been repaired. Energy and torpedoes are replenished.\n")
    else:
        print("Not docked at a starbase. Repairs cannot be performed.\n")




