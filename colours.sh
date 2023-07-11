#!/usr/local/bin/bash

# did a script disable colours? fine, have a boring life :)
[ -n "$disable_colors" ] && return

# "normal" variables, should work with older versions of bash<5 :

# style_reset=$colour_reset
export not_italic=$'\e[23m'
export not_underline=$'\e[24m'
export not_bold=$'\e[22m'
export underline=$'\e[4m'
export italic=$'\e[3m'
export bold=$'\e[1m'
export bolditalic=$'\e[1m\e[3m'
export dim=$'\e[2m'
export blink=$'\e[5m' # oh god why does this even exist
export invert=$'\e[7m'

export strike=$'\e[9m' # problematic

# regular colors
export black=$'\e[0;30m'  # black
export red=$'\e[0;31m'    # red
export green=$'\e[0;32m'  # green
export yellow=$'\e[0;33m' # yellow
export blue=$'\e[0;34m'   # blue
export purple=$'\e[0;35m' # purple
export cyan=$'\e[0;36m'   # cyan
export white=$'\e[0;37m'  # white

# bold
export bblack=$'\e[1;30m'  # black
export bred=$'\e[1;31m'    # red
export bgreen=$'\e[1;32m'  # green
export byellow=$'\e[1;33m' # yellow
export bblue=$'\e[1;34m'   # blue
export bpurple=$'\e[1;35m' # purple
export bcyan=$'\e[1;36m'   # cyan
export bwhite=$'\e[1;37m'  # white

# underline
export ublack=$'\e[4;30m'  # black
export ured=$'\e[4;31m'    # red
export ugreen=$'\e[4;32m'  # green
export uyellow=$'\e[4;33m' # yellow
export ublue=$'\e[4;34m'   # blue
export upurple=$'\e[4;35m' # purple
export ucyan=$'\e[4;36m'   # cyan
export uwhite=$'\e[4;37m'  # white

# background
export on_black=$'\e[40m'  # black
export on_red=$'\e[41m'    # red
export on_green=$'\e[42m'  # green
export on_yellow=$'\e[43m' # yellow
export on_blue=$'\e[44m'   # blue
export on_purple=$'\e[45m' # purple
export on_cyan=$'\e[46m'   # cyan
export on_white=$'\e[47m'  # white

# high intensity
export iblack=$'\e[0;90m'  # black
export ired=$'\e[0;91m'    # red
export igreen=$'\e[0;92m'  # green
export iyellow=$'\e[0;93m' # yellow
export iblue=$'\e[0;94m'   # blue
export ipurple=$'\e[0;95m' # purple
export icyan=$'\e[0;96m'   # cyan
export iwhite=$'\e[0;97m'  # white

# bold high intensity
export biblack=$'\e[1;90m' # black
export grey="$biblack"
export bired=$'\e[1;91m'    # red
export bigreen=$'\e[1;92m'  # green
export biyellow=$'\e[1;93m' # yellow
export biblue=$'\e[1;94m'   # blue
export bipurple=$'\e[1;95m' # purple
export bicyan=$'\e[1;96m'   # cyan
export biwhite=$'\e[1;97m'  # white

# high intensity backgrounds
export on_iblack=$'\e[0;100m'  # black
export on_ired=$'\e[0;101m'    # red
export on_igreen=$'\e[0;102m'  # green
export on_iyellow=$'\e[0;103m' # yellow
export on_iblue=$'\e[0;104m'   # blue
export on_ipurple=$'\e[0;105m' # purple
export on_icyan=$'\e[0;106m'   # cyan
export on_iwhite=$'\e[0;107m'  # white

# reset
export ansi_off=$'\e[0m' # text reset
export nocolor="$ansi_off"
export nocolour="$ansi_off"

# point of no return! only reasonable version of bash get to have nice things
if [ -z "$_bash_version_ok" ]; then return; fi
# we let old shells politely out the door

declare -A blockmoji

blockmoji[red]='🟥'
blockmoji[green]='🟩'
blockmoji[blue]='🟦'
blockmoji[orange]='🟧'
blockmoji[yellow]='🟨'
blockmoji[purple]='🟪'
blockmoji[brown]='🟫'
blockmoji[black]='⬛'
blockmoji[white]='⬜'
blockmoji[Darwin]='🍏'
blockmoji[Linux]='🐧'

export blockmoji

# tbh these are mainly legacy for my old scripts anyway

declare -A ansi

# NOTE: using this in a prompt/readline situation where calculating the number of
#       chars is important it may be best to escape with \e and like so:
#
#       ansi[not_italic]=$'\e\e[23m'

ansi[not_italic]=$'\e[23m'
ansi[not_underline]=$'\e[24m'
ansi[not_bold]=$'\e[22m'
ansi[underline]=$'\e[4m'
ansi[italic]=$'\e[3m'
ansi[bold]=$'\e[1m'
ansi[bolditalic]=$'\e[1m\e[3m'
ansi[dim]=$'\e[2m'
ansi[strike]=$'\e9m'

# regular colors
ansi[black]=$'\e[0;30m'  # black
ansi[red]=$'\e[0;31m'    # red
ansi[green]=$'\e[0;32m'  # green
ansi[yellow]=$'\e[0;33m' # yellow
ansi[blue]=$'\e[0;34m'   # blue
ansi[purple]=$'\e[0;35m' # purple
ansi[cyan]=$'\e[0;36m'   # cyan
ansi[white]=$'\e[0;37m'  # white

# bold
ansi[bblack]=$'\e[1;30m'  # black
ansi[bred]=$'\e[1;31m'    # red
ansi[bgreen]=$'\e[1;32m'  # green
ansi[byellow]=$'\e[1;33m' # yellow
ansi[bblue]=$'\e[1;34m'   # blue
ansi[bpurple]=$'\e[1;35m' # purple
ansi[bcyan]=$'\e[1;36m'   # cyan
ansi[bwhite]=$'\e[1;37m'  # white

# underline
ansi[ublack]=$'\e[4;30m'  # black
ansi[ured]=$'\e[4;31m'    # red
ansi[ugreen]=$'\e[4;32m'  # green
ansi[uyellow]=$'\e[4;33m' # yellow
ansi[ublue]=$'\e[4;34m'   # blue
ansi[upurple]=$'\e[4;35m' # purple
ansi[ucyan]=$'\e[4;36m'   # cyan
ansi[uwhite]=$'\e[4;37m'  # white

# background
ansi[on_black]=$'\e[40m'  # black
ansi[on_red]=$'\e[41m'    # red
ansi[on_green]=$'\e[42m'  # green
ansi[on_yellow]=$'\e[43m' # yellow
ansi[on_blue]=$'\e[44m'   # blue
ansi[on_purple]=$'\e[45m' # purple
ansi[on_cyan]=$'\e[46m'   # cyan
ansi[on_white]=$'\e[47m'  # white

# high intensity
ansi[iblack]=$'\e[0;90m'  # black
ansi[ired]=$'\e[0;91m'    # red
ansi[igreen]=$'\e[0;92m'  # green
ansi[iyellow]=$'\e[0;93m' # yellow
ansi[iblue]=$'\e[0;94m'   # blue
ansi[ipurple]=$'\e[0;95m' # purple
ansi[icyan]=$'\e[0;96m'   # cyan
ansi[iwhite]=$'\e[0;97m'  # white

# bold high intensity
ansi[biblack]=$'\e[1;90m'  # black
ansi[bired]=$'\e[1;91m'    # red
ansi[bigreen]=$'\e[1;92m'  # green
ansi[biyellow]=$'\e[1;93m' # yellow
ansi[biblue]=$'\e[1;94m'   # blue
ansi[bipurple]=$'\e[1;95m' # purple
ansi[bicyan]=$'\e[1;96m'   # cyan
ansi[biwhite]=$'\e[1;97m'  # white

# high intensity backgrounds
ansi[on_iblack]=$'\e[0;100m'  # black
ansi[on_ired]=$'\e[0;101m'    # red
ansi[on_igreen]=$'\e[0;102m'  # green
ansi[on_iyellow]=$'\e[0;103m' # yellow
ansi[on_iblue]=$'\e[0;104m'   # blue
ansi[on_ipurple]=$'\e[0;105m' # purple
ansi[on_icyan]=$'\e[0;106m'   # cyan
ansi[on_iwhite]=$'\e[0;107m'  # white

# reset
ansi[off]=$'\e[0m' # text reset

export ansi
