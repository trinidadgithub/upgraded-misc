# game_init.py

import random
import time

# Global variables for game state
energy0 = 3000  # Starting Energy
torps0 = 10  # Photon Torpedo capacity
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

def initialize():
    """Set up the initial game state with one Klingon and starbases in separate sectors."""
    global klingons_left, starbases_left, galaxy_map, klingon_ships
    klingons_left = 0
    starbases_left = 0
    klingon_ships = {}  # Initialize klingon_ships to store Klingon coordinates and stats

    # Step 1: Place a single Klingon in a random sector
    placed_klingon = False
    for i in range(map_size):
        for j in range(map_size):
            if not placed_klingon and random.randint(1, 100) > 80:
                galaxy_map[i][j] = (1 << 8) + random.randint(1, 8)  # Place one Klingon
                klingons_left += 1
                klingon_ships[(i, j)] = {"armor": 100, "hull": 300}  # Track the Klingon’s position and stats
                placed_klingon = True
                print(f"Debug: Placed Klingon at ({i + 1}, {j + 1})")

    # Step 2: Place Starbases in separate sectors from the Klingon
    for i in range(map_size):
        for j in range(map_size):
            if (galaxy_map[i][j] >> 8) & 0xF == 0:  # Only place starbase if no Klingon is present
                starbases = 1 if random.randint(1, 100) > 96 else 0
                if starbases:
                    galaxy_map[i][j] |= (1 << 4)  # Set the starbase flag
                    starbases_left += 1

    # Ensure there is at least one starbase
    if starbases_left == 0:
        while True:
            y, x = random.randint(0, map_size - 1), random.randint(0, map_size - 1)
            if (galaxy_map[y][x] >> 8) & 0xF == 0:  # Ensure no Klingon is in this sector
                galaxy_map[y][x] |= (1 << 4)  # Place the starbase
                starbases_left += 1
                print(f"Debug: Placed Starbase at ({y + 1}, {x + 1})")
                break

    print("Game setup complete with one Klingon and starbase(s).")
    print(f"Debug: Final klingon_ships content: {klingon_ships}")



def short_range_scan():
    """Perform a short-range scan of the current sector and print the results with aligned ASCII art and sector numbers."""
    global ship_y, ship_x, galaxy_map

    cell_width = 6  # Define width of each cell for alignment
    separator_length = (map_size + 1) * cell_width  # Adjust for row numbers

    print("\nShort Range Scan Report:")

    # Print column headers (1-based index)
    col_headers = "     " + "".join(f"{col+1:<{cell_width}}" for col in range(map_size))
    print(col_headers)
    print("-" * separator_length)  # Print a separator line for the map

    klingon_count = 0
    starbase_count = 0

    # Count total Klingons and starbases in each sector
    for i in range(map_size):
        for j in range(map_size):
            klingons_in_sector = (galaxy_map[i][j] >> 8) & 0xF
            starbases_in_sector = (galaxy_map[i][j] >> 4) & 0xF

            # Aggregate counts for HUD display
            if klingons_in_sector > 0:
                klingon_count += klingons_in_sector
            if starbases_in_sector > 0:
                starbase_count += starbases_in_sector

    # Display the map with row numbers and sector symbols
    for i in range(map_size):
        row_display = f"{i+1:<4}"  # Row number at the start (1-based index)
        for j in range(map_size):
            klingons_in_sector = (galaxy_map[i][j] >> 8) & 0xF
            starbases_in_sector = (galaxy_map[i][j] >> 4) & 0xF

            # Display appropriate symbols, ensuring each cell is `cell_width` characters wide
            if i == ship_y and j == ship_x:
                row_display += f"{' >=> ':<{cell_width}}"  # Federation Class heavy cruiser
            elif klingons_in_sector > 0:
                row_display += f"{' <K> ':<{cell_width}}"
            elif starbases_in_sector > 0:
                row_display += f"{' [B] ':<{cell_width}}"
            else:
                row_display += f"{' . ':<{cell_width}}"  # Empty space

        print(row_display)

    print("-" * separator_length)  # Print the closing line for the map

    # Return the counts for use in the HUD
    return klingon_count, starbase_count


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


# Initial player and Klingon ship stats
player_armor = 200
player_hull = 500

# Each Klingon ship will have its own armor and hull values
klingon_ships = {}  # A dictionary to track each Klingon's armor and hull

def initialize_klingon_ships():
    """Initialize armor and hull for each Klingon ship in the galaxy map."""
    global galaxy_map, klingon_ships
    for i in range(map_size):
        for j in range(map_size):
            klingons_in_sector = (galaxy_map[i][j] >> 8) & 0xF
            if klingons_in_sector > 0:
                klingon_ships[(i, j)] = {"armor": 100, "hull": 300}  # Initial stats for each Klingon

def apply_damage(target, damage):
    """Apply damage to the target's armor and hull."""
    if target["armor"] > 0:
        if damage <= target["armor"]:
            target["armor"] -= damage
            damage = 0
        else:
            damage -= target["armor"]
            target["armor"] = 0

    if damage > 0:  # Remaining damage applies to hull
        target["hull"] -= damage

    # Return whether the target was destroyed
    return target["hull"] <= 0

import math

def fire_phasers():
    """Player fires phasers at Klingon ships within range."""
    global energy0, galaxy_map, ship_y, ship_x, klingon_ships, klingons_left

    # Define the player’s attack range
    player_range = 5

    # Prompt for energy allocation and validate input
    try:
        phaser_energy = int(input("Enter energy allocation for phasers: "))
        if phaser_energy > energy0:
            print("Insufficient energy!")
            return
    except ValueError:
        print("Invalid energy amount.")
        return

    # Find Klingons within range and display debug information
    klingons_in_range = []
    for (k_y, k_x), stats in klingon_ships.items():
        distance = math.sqrt((ship_y - k_y) ** 2 + (ship_x - k_x) ** 2)
        print(f"Debug: Distance to Klingon at ({k_y + 1}, {k_x + 1}) from player at ({ship_y + 1}, {ship_x + 1}) is {distance:.2f}")
        if distance <= player_range:
            klingons_in_range.append((k_y, k_x, stats))

    if not klingons_in_range:
        print("No Klingon ships within range.")
        return

    # Distribute energy evenly to Klingons in range and deduct from player’s energy
    damage_per_klingon = phaser_energy // len(klingons_in_range)
    energy0 -= phaser_energy

    for k_y, k_x, stats in klingons_in_range:
        destroyed = apply_damage(stats, damage_per_klingon)
        if destroyed:
            print(f"Klingon at sector ({k_y + 1}, {k_x + 1}) destroyed!")
            galaxy_map[k_y][k_x] = 0  # Completely clear the cell in `galaxy_map`
            del klingon_ships[(k_y, k_x)]
            klingons_left -= 1  # Update the global count of Klingons
        else:
            print(f"Klingon at sector ({k_y + 1}, {k_x + 1}) took damage! Remaining armor: {stats['armor']}, Hull: {stats['hull']}")

    print(f"Phaser attack complete. Energy remaining: {energy0}")



def energy_status():
    """Return the current energy level."""
    return energy0


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


def print_sector_location():
    """Print the current sector location of the ship."""
    print(f"Captain, we are currently in sector ({ship_y + 1}, {ship_x + 1}).")


def display_dashboard(klingon_count, starbase_count):
    """Display the heads-up dashboard with ship status."""
    global ship_y, ship_x, energy0

    # Calculate the number of Klingons within phaser range
    klingons_in_range = count_klingons_in_phaser_range()

    # Construct each line of content
    title = "***  USS ENTERPRISE HUD ***"
    sector_info = f"Current Sector: (Y: {ship_y + 1}, X: {ship_x + 1})"
    energy_info = f"Energy Status: {energy0} / 3000 "
    klingon_info = f"Number of Klingons: {klingon_count}"
    starbase_info = f"Starbases in Sector: {starbase_count}     "
    range_info = f"|  Klingons within Phaser Range: {klingons_in_range}"

    # Calculate the width based on the longest row needed
    hud_width = max(len(title) + 4, 66)  # Ensures a minimum width for good alignment

    # Print the HUD with the exact width
    print("=" * hud_width)
    print(title.center(hud_width))
    print("=" * hud_width)
    print(f"|  {sector_info:<30} |  {energy_info:<20} |")
    print("-" * hud_width)
    print(f"|  {klingon_info:<30} |  {starbase_info:<20} |")
    print(range_info.center(hud_width) + " |")
    print("-" * hud_width + "\n")

def count_klingons_in_phaser_range(player_range=5):
    """Count Klingons within phaser range of the player."""
    global ship_y, ship_x, klingon_ships

    klingons_in_range = 0
    # print(f"Debug: Player position (Y: {ship_y + 1}, X: {ship_x + 1})")

    # Check if there are any Klingons in the `klingon_ships` dictionary
    #if not klingon_ships:
        # print("Debug: No Klingon ships detected in this sector.")
        # return 0

    # Proceed with counting Klingons in range if `klingon_ships` is not empty
    for (k_y, k_x), _ in klingon_ships.items():
        distance = math.sqrt((ship_y - k_y) ** 2 + (ship_x - k_x) ** 2)
        # print(
        #    f"Debug: Distance from player at ({ship_y + 1}, {ship_x + 1}) to Klingon at ({k_y + 1}, {k_x + 1}) is {distance:.2f} (player range: {player_range})")

        # if distance <= player_range:
        #    klingons_in_range += 1
        #    print(f"Debug: Klingon at ({k_y + 1}, {k_x + 1}) is within range.")
        # else:
        #    print(f"Debug: Klingon at ({k_y + 1}, {k_x + 1}) is out of range.")

    # print(f"Debug: Klingons within phaser range: {klingons_in_range}")
    return klingons_in_range

def apply_damage(klingon, damage):
    """Apply damage to a Klingon ship, first to armor, then to hull."""
    if klingon['armor'] > 0:
        klingon['armor'] -= damage
        if klingon['armor'] < 0:
            klingon['hull'] += klingon['armor']  # Carry over damage to hull
            klingon['armor'] = 0
    else:
        klingon['hull'] -= damage

    # Return True if the Klingon is destroyed
    return klingon['hull'] <= 0










