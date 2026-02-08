
# EXTREMELY IMPORTANT, SHOULD PROBABLY MOVE THIS.
export CARBON="$HOME/.carbon"
export CARBONPY="$HOME/.carbon/.venv/bin/python3"

# ENV vars
export PATH="$HOME/.local/bin:$PATH"
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"

# SSH
ssh-add ~/.ssh/github >/dev/null 2>&1
