
echo ">> Setting up Carbon Shell..."

echo " :: Building python venv :: " 
python3 -m venv .venv
source ./.venv/bin/activate

echo " :: Installing dependancies :: " 
pip install .

echo ">> Carbon Shell setup complete!"

echo "Note: To use and start the shell, source ~/.carbon/env in your shell config." \
"Then run 'carbon.start' to start the shell."