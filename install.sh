#!/usr/bin/env bash
mkdir ~/.carbon
git clone https://github.com/kxmtkw/carbon-shell.git ~/.carbon
cd ~/.carbon
python3 install.py < /dev/tty
