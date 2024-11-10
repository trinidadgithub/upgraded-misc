# main.py

import os
from game_init import (
    intro,
    new_game,
    short_range_scan,
    navigation,
    fire_phasers,
    energy_status,
    display_dashboard
)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_ui():
    """Clear the screen and display the HUD and sector map in place."""
    clear_screen()  # Clear previous screen content
    klingon_count, starbase_count = short_range_scan()  # Display sector map and get counts
    display_dashboard(klingon_count, starbase_count)  # Display the HUD with updated info
    print_commands()  # Show available commands at the bottom of the screen


def print_commands():
    """Display available commands for the player."""
    print("\nAvailable commands:")
    print("  nav  - Navigate the ship")
    print("  pha  - Fire phasers at Klingon ships")
    print("  srs  - Perform a short-range scan of the current sector")
    print("  exit - Exit the game\n")


def main():
    intro()
    new_game()
    display_ui()  # Initial display

    running = True
    while running:
        command = input("Command? ").strip().lower()

        if command == "nav":
            navigation()
            print(f"Current energy level: {energy_status()}")
            display_ui()  # Refresh UI after navigation
        elif command == "pha":
            fire_phasers()
            print(f"Current energy level: {energy_status()}")
            display_ui()  # Refresh UI after phaser attack
        elif command == "srs":
            display_ui()  # Refresh UI for short-range scan
        elif command == "exit":
            print("Exiting the game. Goodbye!")
            running = False
        else:
            print("Invalid command.")
            print_commands()


if __name__ == "__main__":
    main()
