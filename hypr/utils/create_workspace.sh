#!/bin/sh

# Util to create a new workspace, only if the last workspace is not empty

total=$(hyprctl workspaces -j | jq 'length')
is_last_empty=$(hyprctl workspaces -j | jq 'if .[-1].windows == 0 then 1 else 0 end')

if (( is_last_empty == 0 )); then
    id=$(( total + 1 ))
    hyprctl dispatch workspace "$id"
fi