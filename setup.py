#!/usr/bin/env python

import os


if __name__ == '__main__':
    """Install the dependencies stored in requirements.txt using the "pip" installer."""
    print('Running pip install...')
    os.system('pip install -r requirements.txt')
