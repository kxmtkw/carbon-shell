
# AutoComplete
source ~/.zshac

zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors ''

autoload -Uz compinit
compinit



# Prompt
autoload -U colors && colors

PROMPT='%F{cyan}[%n@%m]%f %F{white}%~%f
%F{green}>> %f'



# Aliases
alias ls='lsd'
alias la='lsd --all'
alias grep='grep --color'
alias gs='git status'
alias env='source ./.venv/bin/activate || echo No .venv found!'
alias denv='deactivate || echo No .venv activated!'



