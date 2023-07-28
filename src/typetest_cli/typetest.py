#!/usr/bin/env python3

from contextlib import contextmanager
from itertools import zip_longest
from typing import Final
import argparse
import glob
import os
import random
import sys
import termios
import time
import tty

from rich.console import Console
from rich.live import Live

user_dir = os.path.expanduser("~")
here = os.path.abspath(os.path.dirname(__file__))

SOURCE_DIR: Final[str] = f"{here}/text"
EXTERN_DIR: Final[str] = f"{user_dir}/.local/share/typetest-cli/text"
MAX_SUBSEUQENT_ERRORS: Final[int] = 3
LETTERS_PER_WORD: Final[int] = 5


@contextmanager
def raw_mode(file):
    """Puts the terminal into raw mode, allowing for full reading of user input.
    On exit, restores the terminal to previous settings."""
    old_settings = termios.tcgetattr(file.fileno())
    try:
        tty.setraw(file.fileno())
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_settings)


def get_char() -> str:
    """Gets the next character input from the user"""
    with raw_mode(sys.stdin):
        char = sys.stdin.read(1)
    return char


def format_text(source: str, user_input: str) -> str:
    final_text = ""
    for source_char, input_char in zip(source, user_input):
        if source_char == input_char:
            final_text += f"[green]{source_char}[/]"
        else:
            final_text += f"[red]{source_char if source_char != ' ' else '_'}[/]"
    if len(user_input) < len(source):
        return final_text + f"[blue]{source[len(user_input)]}[/]{source[len(user_input) + 1:]}"
    return final_text


def calc_wpm(time_seconds: float, letters: int, letters_per_word: int) -> int:
    words = letters / letters_per_word
    minutes = time_seconds / 60
    return int(words // minutes)


def get_accuracy_percent(failures: int, letters: int) -> int:
    return int(((letters - failures) / letters) * 100)


def count_failures(source: str, user_input: str) -> int:
    failures = 0
    for source_letter, user_input_letter in zip_longest(source, user_input):
        if user_input_letter != source_letter:
            failures += 1
    return failures


def get_random_file(*args) -> str:
    options = []
    for directory in args:
        files = glob.glob(f"{directory}/*")
        options.extend(files)
    return random.choice(options)


def not_quit(char: str) -> bool:
    """Checks for SIGINT"""
    return ord(str(char)) != 3


def is_backspace(char: str) -> bool:
    return char == "\x7f"


def add_to(current_input: str, new_char: str) -> str:
    if is_backspace(new_char):
        if len(current_input) > 0:
            return current_input[:-1]
        else:
            return current_input
    return current_input + new_char


def is_input_error(char: str, DATA: str, input_index: int) -> bool:
    if is_backspace(char):
        return False
    return char != DATA[input_index]


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="typetest",
        description="Lightweight typing speed commandline tool. Can be exited with ctrl-c",
        epilog="Will only disply typing speed and accuracy upon completion of the text.",
    )

    parser.add_argument(
        "file_path", metavar="file_path", type=str, nargs="?", help="path to read file"
    )
    parser.add_argument(
        "--hide-acc", "-a", action="store_true", help="hides the accuracy statistic"
    )
    parser.add_argument(
        "--hide-wpm",
        "-w",
        action="store_true",
        help="hides the word per minute statistic",
    )
    parser.add_argument("--only-base", "-b", action="store_false", help="Only uses the base text")
    parser.add_argument(
        "--no-blocking",
        "-n",
        action="store_false",
        help="Do not block input after 3 failed attmpts",
    )

    args = parser.parse_args()

    if args.file_path and os.path.exists(args.file_path):
        file = args.file_path
    elif args.only_base:
        file = get_random_file(SOURCE_DIR)
    else:
        file = get_random_file(SOURCE_DIR, EXTERN_DIR)

    with open(file, encoding="utf-8", mode="r") as file:
        DATA = file.read().strip("\n").strip(" ")

    console = Console(soft_wrap=False, no_color=False)
    start = end = None
    user_input = ""
    subsequent_errors: int = 0

    with Live(console=console, auto_refresh=False) as display:
        display.update(DATA, refresh=True)
        while not_quit(char := get_char()):
            if start is None:
                start = time.time()

            if args.no_blocking:
                if is_input_error(char, DATA, len(user_input)):
                    subsequent_errors += 1
                    if subsequent_errors >= MAX_SUBSEUQENT_ERRORS:
                        continue
                else:
                    subsequent_errors = 0

            if len(user_input := add_to(user_input, char)) >= len(DATA):
                break

            display.update(format_text(DATA, user_input), refresh=True)
        end = time.time()
        display.update(format_text(DATA, user_input), refresh=True)

    if len(user_input) != len(DATA):
        return

    if not args.hide_acc:
        print(get_accuracy_percent(count_failures(DATA, user_input), len(DATA)), "percent correct")

    if not args.hide_wpm:
        print(calc_wpm(end - start, len(DATA), LETTERS_PER_WORD), "words per minute")


if __name__ == '__main__':
    main()
