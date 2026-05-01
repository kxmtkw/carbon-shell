[ -d ~/.carbon ] && echo "~/.carbon already exists" && exit 1
git clone https://github.com/kxmtkw/carbon-shell.git ~/.carbon
python3 ~/.carbon/installation/install.py