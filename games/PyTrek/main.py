# main.py

from game_init import intro, new_game, short_range_scan, navigation


def main():
    """Main function to start and run the game."""
    # Display the introduction and seed the random number generator
    intro()

    # Start a new game
    new_game()

    # Initial short-range scan to hsow the game state
    short_range_scan()

    # Placeholder for the main game loop (to be implemented)
    running = True
    while running:
        # Take input for game commands (e.g., "nav", "srs", "pha", etc.)
        command = input("Command? ").strip().lower()

        if command == "exit":
            print("Exiting the game. Goodbye!")
            running = False
        elif command == "nav":
            navigation()
            short_range_scan()
        else:
            # For now, just echo the command
            print(f"Received command: {command}")
            print(f"Invalid command. Available commands: nav, exit.")


if __name__ == "__main__":
    main()
