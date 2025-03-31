import os, sys
import logging
from .logging_config import logger

def word_list_file_path(filename='en.txt'):
    """Create the file path to the wordlist filename."""
    if not filename.endswith('.txt'):
        filename += '.txt'

    folder_path='data/word_list'
    # relativ path 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    # join the path
    join_path = os.path.join(root_dir, folder_path)
    file_path = os.path.abspath(os.path.join(join_path, filename))
    
    logger.debug(f"Looking for word list at: {file_path}")
    
    if not os.path.isfile(file_path):
        logger.error(f"File {filename} not found in {folder_path}")
        raise FileNotFoundError(f"File {filename} not found in {folder_path}.")
    
    return file_path


def get_word_list(file_path:str):
    """Read the word list from a filepath and return the list."""
    word_list = []
    
    logger.debug(f"Reading word list from {file_path}")

    try:
        with open(file_path, 'r') as f:
            for line in f:
                word_list.append(line.strip().lower())
        logger.info(f"Loaded {len(word_list)} words from wordlist")
        return word_list
    except Exception as e:
        # Log error with full exception info (traceback)
        logger.error(f"Error reading word list: {str(e)}", exc_info=True)
        # Re-raise the exception in dev mode to get full traceback in console
        if logger.level == logging.DEBUG:
            raise


def get_word_list_length(word_list:list=[], length:int=5):
    """Returns word list of a specific length."""
    if not word_list:
        logger.warning("Empty word list provided to get_word_list_length")
        return False
    
    logger.debug(f"Filtering word list for words of length {length}")
    
    new_list = []
    for word in word_list:
        if len(word) == length:
            new_list.append(word)
    
    logger.info(f"Found {len(new_list)} words with length {length}")        
    return new_list