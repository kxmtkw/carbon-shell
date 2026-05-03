[ -d ~/.carbon ] && echo "~/.carbon already exists. Delete it first before installing." && exit 1
git clone https://github.com/kxmtkw/carbon-shell.git ~/.carbon
cd ~/.carbon
python3 ~/.carbon/installation/install.py