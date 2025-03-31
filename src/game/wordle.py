import random
import time, sys
from ..utils.utils import get_word_list, word_list_file_path


class Wordle:
    def __init__(self):
        """Initializes the game with a list of words."""
        self.word_list = get_word_list(word_list_file_path())
        
        self.options()
        self.reset()

    def options(self, language:str='en', word_length:int=5, attempts_max:int=6):
        """Sets the default options for the game."""
        self.language = language
        self.word_length = word_length
        self.attempts_max = attempts_max

    def reset(self):
        """Resets the game by selecting a new target word."""
        self.word = self.random_word(self.word_list)
        self.attempts = []
        self.feedback = []

    def random_word(self, word_list:list=None):
        """Return a random word from the word list."""
        return random.choice(word_list) if word_list else None

    
    def make_guess(self, guess):
        """Processes a guess and feedback."""
        if len(guess) != len(self.word):
            raise ValueError("Guess must be the same length as the target word.")
        elif not guess.isalpha():
            raise ValueError("Guess must only contain letters.")
        
        self.attempts.append(guess)

        self.feedback.append(self._generate_feedback(guess))

        return True

    def _generate_feedback(self, guess):
        """Generates feedback for a guess (e.g., correct letters and positions)."""
        feedback = []
        for g_char, w_char in zip(guess, self.word):
            if g_char == w_char:
                feedback.append("correct")
            elif g_char in self.word:
                feedback.append("present")
            else:
                feedback.append("absent")

        return feedback