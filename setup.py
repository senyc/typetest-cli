#!/usr/bin/env python3

from setuptools import setup
import os

if __name__ == '__main__':

    # Create directory for external text on install
    user_dir = os.path.expanduser('~')
    text_path = f"{user_dir}/.local/share/typetest-cli/text"

    try:
        if not os.path.exists(text_path):
            os.makedirs(text_path)
    except (PermissionError, OSError):
        # Skip directory creation in sandboxed environments (e.g., Nix builds)
        pass

    setup()

