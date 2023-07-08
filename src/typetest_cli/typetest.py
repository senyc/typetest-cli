#!/usr/bin/env python3

from contextlib import contextmanager
from typing import Final
import argparse
import glob
import math
import os
import random
import sys
import termios
import time
import tty

from rich.console import Console
from rich.live import Live

user_dir = os.path.expanduser('~')
here = os.path.abspath(os.path.dirname(__file__))

SOURCE_DIR: Final[str] = f'{here}/text'
EXTERN_DIR: Final[str] = f'{user_dir}.local/share/typetest-cli/text'

@contextmanager
def raw_mode(file):
    """Puts the terminal into raw mode, allowing for full reading of user's input.
    On exit, restores the terminal to the previous settings."""
    old_settings = termios.tcgetattr(file.fileno())
    try:
        tty.setraw(file.fileno())
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_settings)

def get_char() -> str:
    with raw_mode(sys.stdin):
        char = sys.stdin.read(1)
    return char

def displayed_text(source: str, user_input: str) -> str:
    final_text = ''
    for source_char, input_char in zip(source, user_input):
        if source_char == input_char:
            final_text += f'[green]{source_char}'
        else:
            final_text += (f'[red]{source_char}' if source_char != ' ' else '[red]_')
    return final_text + '[blue]' + (source[len(user_input)] if source[len(user_input)] != ' ' else '_') + '[white]' + source[len(user_input) + 1: len(source):]

def is_backspace(char: str) -> bool:
    return char == '\x7f'

def calc_wpm(time_seconds: float, letters: int) -> int:
    words = letters / 5
    minutes = time_seconds / 60
    return math.floor(words / minutes)

def is_quit(char: str) -> bool:
    return (char != '' and ord(char) == 3) or (char == '\n' or char == '\r')

def calc_correctness_percent(failures: int, letters: int) -> int:
    return round(((letters - failures) / letters) * 100)

def count_failures(source: str, user_input: str) -> int:
    failures = 0
    for source_letter, user_input_letter in zip(source, user_input):
        if user_input_letter != source_letter:
            failures += 1
    return failures

def get_random_file(*args):
    options = []
    for directory in args:
        files = glob.glob(f'{directory}/*')
        options.extend(files)
    return random.choice(options)

def main() -> None:
    parser = argparse.ArgumentParser(
        prog='typetest',
        description='Prints an interactable line of text for matching',
        epilog='Only prints out stats if the entire line is written out'
    )

    parser.add_argument('--hide-acc', '-a', action='store_true', help='hides the accuracy statistic')
    parser.add_argument('--hide-wpm', '-w', action='store_true', help='hides the word per minute statistic')
    parser.add_argument('--only-base', '-b', action='store_false', help='Only uses the base text')

    args = parser.parse_args()
    if not args.only_base:
        file = get_random_file(SOURCE_DIR, EXTERN_DIR)
    else:
        file = get_random_file(SOURCE_DIR)

    with open(file, encoding='utf-8', mode='r') as file:
        DATA = file.read().strip('\n').strip(' ')

    total_character_count = len(DATA)
    user_input = ''
    console = Console(soft_wrap=False, no_color=False)
    start = end = None

    with Live(console=console, auto_refresh=False) as display:
        while True:
            display.update(displayed_text(DATA, user_input), refresh=True)
            char = get_char()
            # Starts only after first character entered
            if start is None:
                start = time.time()
            if is_quit(char):
                return
            user_input = user_input[:-1] if is_backspace(char) else user_input + char
            if len(user_input) >= total_character_count:
                end = time.time()
                break

    # Validates the there is an endtime to display
    if not end:
        return

    if not args.hide_acc:
        print(calc_correctness_percent(count_failures(DATA, user_input), total_character_count), "percent correct")

    if not args.hide_wpm:
        print(calc_wpm(end - start, total_character_count), "words per minute")


if __name__ == '__main__':
    main()

