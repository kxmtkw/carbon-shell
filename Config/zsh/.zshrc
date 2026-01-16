
source ~/.zshac

zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors ''

autoload -Uz compinit
compinit


alias ls='ls --color'
alias la='ls --color --all'

alias grep='grep --color'

alias gs='git status'

ssh-add ~/.ssh/github >/dev/null 2>&1
