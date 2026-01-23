
# ENV vars
export PATH="$HOME/.local/bin:$PATH"
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"

export EDITOR=nano

# SSH
ssh-add ~/.ssh/github >/dev/null 2>&1
