
#  History

HISTFILE=$HOME/.history
HISTSIZE=100000
SAVEHIST=$HISTSIZE

setopt EXTENDED_HISTORY          # Write the history file in the ':start:elapsed;command' format.
setopt HIST_EXPIRE_DUPS_FIRST    # Expire a duplicate event first when trimming history.
setopt HIST_FIND_NO_DUPS         # Do not display a previously found event.
setopt HIST_IGNORE_ALL_DUPS      # Delete an old recorded event if a new event is a duplicate.
setopt SHARE_HISTORY             # Share history between all sessions.



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


# Window Title

precmd() {
  print -Pn "\e]0;%~\a"
}


# Aliases

# basic
alias ls='lsd'
alias la='lsd --all'
alias grep='grep --color'

# personal
alias env='source ./.venv/bin/activate || echo No .venv found!'
alias denv='deactivate || echo No .venv activated!'
alias fetch='fastfetch'

# git related
alias gs='git status'
alias ga='git add'
alias gb='git branch'
alias gr='git remote'
alias gp='git push'

# Prompt
eval "$(starship init zsh)"

