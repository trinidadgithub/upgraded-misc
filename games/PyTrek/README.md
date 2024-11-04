This project is python port of the classic Star Trek game originally written for BASIC on the mainframe.

I have reviewed the C code for the Star Trek game. We can begin porting it to Python by first understanding the major components and data structures used in the C program. Here’s a brief overview of the key elements:
Key Features and Structure:

- Game Setup and Initialization:
        Functions like intro(), new_game(), and initialize() set up the game state and prompt the player.

- Game Loop:
        The game operates in a continuous loop, processing user commands and updating the game state accordingly.

- Core Mechanics:
        Various game functions handle ship navigation, combat with Klingons, damage control, and scanning sectors.

- Data Structures:
        Structures and arrays are used to represent the map, ship status, Klingon ships, and other game elements.

Plan for Porting:

- Initial Setup:
        Create Python classes or data structures to represent the ship, map, and Klingons.

- Functions and Flow:
        Convert key functions to Python, using standard Python syntax for reading input, printing outputs, and handling loops.

- Modular Approach:
        Implement individual game functions like new_game(), course_control(), and phaser_control() as Python functions or methods within classes.

- Testing and Iteration:
        Test each ported function to ensure it behaves as expected before integrating it into the main game loop.

**History:** Below is a history of the game ported from BASIC to C.  You can find this at [this repo here](https://github.com/EtchedPixels/FUZIX/blob/master/Applications/games/startrek.c).  Enjoy!
```bash

/*
 * startrek.c
 *
 * Super Star Trek Classic (v1.1)
 * Retro Star Trek Game 
 * C Port Copyright (C) 1996  <Chris Nystrom>
 *
 * Reworked for Fuzix by Alan Cox (C) 2018
 *	- Removed all floating point
 *	- Fixed multiple bugs in the BASIC to C conversion
 *	- Fixed a couple of bugs in the BASIC that either got in during it's
 *	  conversion between BASICs or from the original trek
 *	- Put it on a diet to get it to run in 32K. No features were harmed
 *	  in the making of this code smaller.
 *
 * TODO:
 *	- Look hard at all the rounding cases
 *	- Review some of the funnies in the BASIC code that appear to be bugs
 *	  either in the conversion or between the original and 'super' trek
 *	  Notably need to fix the use of shield energy directly for warp
 *	- Find a crazy person to draw ascii art bits we can showfile for things
 *	  like messages from crew/docking/klingons etc
 *	- I think it would make a lot of sense to switch to real angles, but
 *	  trek game traditionalists might consider that heresy.
 *
 * 
 * This program is free software; you can redistribute it and/or modify
 * in any way that you wish. _Star Trek_ is a trademark of Paramount
 * I think.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * This is a C port of an old BASIC program: the classic Super Star Trek
 * game. It comes from the book _BASIC Computer Games_ edited by David Ahl
 * of Creative Computing fame. It was published in 1978 by Workman Publishing,
 * 1 West 39 Street, New York, New York, and the ISBN is: 0-89489-052-3.
 * 
 * See http://www.cactus.org/~nystrom/startrek.html for more info.
 *
 * Contact Author of C port at:
 *
 * Chris Nystrom
 * 1013 Prairie Dove Circle
 * Austin, Texas  78758
 *
 * E-Mail: cnystrom@gmail.com, nystrom@cactus.org
 *
 * BASIC -> Conversion Issues
 *
 *     - String Names changed from A$ to sA
 *     - Arrays changed from G(8,8) to map[9][9] so indexes can
 *       stay the same.
 *
 * Here is the original BASIC header:
 *
 * SUPER STARTREK - MAY 16, 1978 - REQUIRES 24K MEMORY
 *
 ***        **** STAR TREK ****        ****
 *** SIMULATION OF A MISSION OF THE STARSHIP ENTERPRISE,
 *** AS SEEN ON THE STAR TREK TV SHOW.
 *** ORIGINAL PROGRAM BY MIKE MAYFIELD, MODIFIED VERSION
 *** PUBLISHED IN DEC'S "101 BASIC GAMES", BY DAVE AHL.
 *** MODIFICATIONS TO THE LATTER (PLUS DEBUGGING) BY BOB
 *** LEEDOM - APRIL & DECEMBER 1974,
 *** WITH A LITTLE HELP FROM HIS FRIENDS . . .
 *** COMMENTS, EPITHETS, AND SUGGESTIONS SOLICITED --
 *** SEND TO:  R. C. LEEDOM
 ***           WESTINGHOUSE DEFENSE & ELECTRONICS SYSTEMS CNTR.
 ***           BOX 746, M.S. 338
 ***           BALTIMORE, MD  21203
 ***
 *** CONVERTED TO MICROSOFT 8 K BASIC 3/16/78 BY JOHN BORDERS
 *** LINE NUMBERS FROM VERSION STREK7 OF 1/12/75 PRESERVED AS
 *** MUCH AS POSSIBLE WHILE USING MULTIPLE STATMENTS PER LINE
```

### Implementation
Currently, navigation and short range scans have been implemented.  Also, if you navigate to a Star Base, your ship will be repaired, refueled and resupplied.

### Next Steps

- **Implement Command Handling:** Add functionality to handle basic player commands (e.g., navigation, phaser control, long-range scans).

- **Combat Mechanics:** Implement functions for phaser control and firing photon torpedoes.

- **Damage and Repair System:** Create logic for handling damage to the ship and repairs.

- **Long-Range Scans:** Implement a function to show an overview of adjacent quadrants.

- **Game End Conditions:** Define victory and defeat conditions based on completing objectives or losing the ship.
