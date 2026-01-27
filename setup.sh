echo "Installing venv..."
python3 -m venv .venv
echo "Installed venv!"

echo "Setting up..."
chmod +x ./.venv/bin/activate
source ./.venv/bin/activate
pip install .
echo "Setup complete!"

echo "Installing Carbon shell..."
carbon install
echo "Installation complete"