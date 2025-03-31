import curses
import pyfiglet
import time, sys

class Interface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.figlet = pyfiglet.Figlet(font='smkeyboard') # slant, drpepper, soft
        self.stdscr_y = 0
        self.stdscr_x = 0
        self.attempts = []


    def add_text(self, y:int=0, x:int=0, text:str=''):
        """Adds text to the 'current' screen position."""
        self.stdscr_x = 0
        if text:
            self.stdscr.addstr(self.stdscr_y+y, self.stdscr_x+x, text)
        self.stdscr_y += 1 + y
        self.stdscr_x += x

    def display_menu(self, title='Wordle'):
        """Displays the title screen."""
        ascii_art = self.figlet.renderText(title)

        for i, line in enumerate(ascii_art.splitlines()):
            self.add_text(text=line)

        self.add_text(text='')
        message = [
            'q - quit game',
            'r - reset game (round)',
        ]



        for i in range(len(message)):
            self.add_text(x=1, text=message[i])

        self.add_text(text='')
        self.add_text(text='Press any key to start game...')



    def display_game(self):
        """Displays the game screen."""
        ascii_art = self.figlet.renderText('Play')
        for i, line in enumerate(ascii_art.splitlines()):
            self.add_text(text=line)
        self.add_text(text='')
        # Refresh the screen to show the updated game state


    def display_attempts(self):
        """Displays the attempts."""
        if self.attempts:
            for i, attempt in enumerate(self.attempts):
                self.add_text(x=4, text=f'{i+1}: {attempt}')
            self.add_text(text='')

    def refresh(self):
        """Updates the screen."""
        self.stdscr.refresh()

    def clear(self):
        """Clear the screen."""
        self.stdscr.clear()

    def reset(self):
        """Clear & Update the screen."""
        self.stdscr.clear()
        self.stdscr_y = 0
        self.stdscr_x = 0
        self.stdscr.refresh()

    def exit_game(self):
        """Exits the game."""
        self.reset()
        self.add_text(text="Exiting game...")
        self.refresh()
        curses.napms(2000)
        sys.exit(0)

if __name__ == "__main__":
    pass