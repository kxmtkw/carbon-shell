
echo ">> Installing up Carbon Shell..."

echo " :: Building environment " 
python3 -m venv .venv
source ./.venv/bin/activate

echo " :: Installing dependancies " 
pip install . > /dev/null 2>&1

echo " :: Linking hyprland " 
ln -s -i ~/.carbon/hypr ~/.config/hypr
touch ~/.carbon/hypr/hyprviz.conf
touch ~/.carbon/hypr/override.conf

echo " :: Copying shell configuration "
mkdir settings
cp -i ~/.carbon/defaults/config.toml ~/.carbon/settings/config.toml
cp -i ~/.carbon/defaults/colors.toml ~/.carbon/settings/colors.toml

echo ">> Carbon Shell installation complete!"

echo "Note: To use and start the shell, source ~/.carbon/env in your shell config." \
"Then run 'carbon.start' to start the shell."