import time, sys, os
import signal
import curses
import traceback

from .game.wordle import Wordle
from .game.interface import Interface
from .utils.utils import get_word_list

import logging
from .utils.logging_config import logger

# Global variable to store the screen reference
stdscr_global = None

def main(stdscr):
    try:
        logger.info("Starting wordle game")
        # Store reference to stdscr globally so the signal handler can access it
        global stdscr_global
        stdscr_global = stdscr
        # Register signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        # Initialize the game and interface
        wordle = Wordle()
        interface = Interface(stdscr)
        logger.debug("Wordle and interface initialized")

        # Curses initialization
        curses.curs_set(False)  # Hide the cursor
        stdscr.keypad(True)     # Enable special keys like arrows
        stdscr.timeout(1)     # Set timeout to 500ms for getch()
        

        # Initial draw of the menu
        interface.reset()
        interface.display_menu()
        interface.refresh()
        
        logger.debug("Curses interface initialized")


        # MENU LOOP
        def menu_loop():
            """Menu loop for the game."""
            logger.debug("Entering menu loop")
            redraw_needed = False
            while True:
                # Only redraw if needed
                if redraw_needed:
                    logger.debug("Redrawing interface")
                    interface.display_menu()
                    redraw_needed = False

                # Wait for input (with timeout)
                user_input = interface.stdscr.getch()
                
                # No input within timeout
                if user_input == -1:
                    continue
                    
                if user_input == ord('q'):
                    logger.info("User selected menu quit")
                    interface.exit_game()
                elif user_input == ord('r'):
                    logger.info("User selected menu reset")
                    redraw_needed = False
                    wordle.reset()
                    interface.reset()
                    interface.add_text(text="Game reset!")
                    interface.refresh()
                    curses.napms(2000)
                elif user_input == ord('o'):
                    logger.info("User selected menu options")
                    redraw_needed = False
                    wordle.reset()
                else:
                    # Play the game
                    logger.info("Starting game loop")
                    redraw_needed = False
                    game_loop()
                    logger.debug("Returned to menu loop")

        # Game Loop
        def game_loop():
            logger.debug("Entering game loop")
            curses.curs_set(True)
            redraw_needed = True
            guess = ''
            max_input_length = 5  # Maximum guess length for Wordle

            while True:
                # Display the game state
                
                if redraw_needed:
                    interface.reset()
                    interface.display_game()
                    interface.display_attempts()
                    interface.add_text(text='Guess: ' + guess)
                    interface.refresh()
                    redraw_needed = False

                # Use short timeouts to regularly check for signals
                ch = interface.stdscr.getch()
                
                if ch == -1:  # No input, continue loop (allows signal processing)
                    continue
                
                elif ch == ord('\n'):  # Enter key
                    redraw_needed = True
                    if guess.lower().strip():
                        interface.attempts.append(guess)  # Store the guess
                    logger.debug(f"User entered guess: {guess}")

                    if guess == 'q':
                        logger.info("User quit during game")
                        curses.curs_set(False)
                        return
                    
                    # Process the guess logic
                    logger.debug("Processing guess")
                    # Reset for next input
                    guess = ''
                    redraw_needed = True
                    
                elif ch in (curses.KEY_BACKSPACE, curses.KEY_DC, 127, 8):  # Backspace
                    if guess:
                        guess = guess[:-1]
                        redraw_needed = True


                elif ch >= 32 and ch <= 126:  # Printable characters
                    # Only add character if below max length
                    if len(guess) < max_input_length:
                        guess += chr(ch)
                        redraw_needed = True
                    else:
                        # Optional: flash screen or beep to indicate max length reached
                        curses.flash()  # Visual indicator that max length is reached
                        pass


        # Start the menu loop
        menu_loop()
        logger.info("Game session ended")

    except Exception as e:
        # Log any uncaught exceptions with full stack trace
        logger.critical(f"Unhandled exception: {str(e)}", exc_info=True)
        if logger.level == logging.DEBUG:
            # In development mode, show the full traceback
            traceback.print_exc()
        else:
            # In production mode, show a user-friendly message
            print(f"An error occurred: {str(e)}")
        sys.exit(1)
        

def signal_handler(sig, frame):
    """Handle Ctrl+C by properly cleaning up curses"""
    logger.info("Game terminated by user (SIGINT)")
    if stdscr_global:
        curses.endwin()
    print('\nTerminated: Goodbye! Thanks for playing!\n')
    sys.exit(0)  # Make sure to use exit code 0 for clean termination
