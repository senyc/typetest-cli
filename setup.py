#!/usr/bin/env python3

from setuptools import setup
import os
import shutil

if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))
    user_dir = os.path.expanduser('~')
    text_path = f"{user_dir}/.local/share/typetest-cli/text"

    if not os.path.exists(f"{here}/text/"):
        print(f"Could not find text file, please make sure that it exists in this current directory {here}")
        exit

    if not os.path.exists(text_path):
        os.makedirs(text_path)

    for file in os.listdir(f"{here}/text/"):
        destination_path: str = f"{text_path}/{file}"
        if not os.path.exists(destination_path):
            current_file_path: str = f"{here}/text/{file}"
            shutil.copyfile(current_file_path, destination_path)

    setup(
        py_modules=['typetest'],
    )

