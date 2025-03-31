# Wordle CLI (WIP)

A command-line implementation of the popular word-guessing game "Wordle". With some settings and feature, including en, de, ...

## Description

This project provides a CLI version of Wordle where players attempt to guess a hidden five-letter word within six attempts. After each guess, colored feedback is provided to indicate which letters are correct and in the correct position, which letters appear in the word but in a different position, and which letters are not in the word.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/wordle-cli.git
cd wordle-cli

# Install dependencies (if any)
pip install -r requirements.txt
```

## Usage

```bash
# Run the game
python -m src

# Run in developer mode (log)
python -m src --dev
```

## Features

- Command-line based Wordle gameplay
- Extensive English word dictionary
- Configurable logging for debugging
- Developer mode for testing and development

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
