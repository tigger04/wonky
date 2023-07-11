[ -n "$_os" ] || _os=$(uname)

# check if we have a good bash version - still loads partial colour codes if not

if [ ${#BASH_VERSINFO[@]} -gt 0 ] && [ ${BASH_VERSINFO[0]} -gt 5 ]; then
   export _bash_version_ok=true
else
   export _bash_version_ok=false
fi

. "$(dirname -- "${BASH_SOURCE[0]}")/colours.sh"

die() {

   local die_message="💀 $(basename "$0") died:"
   if [ $# -eq 0 ]; then
      read die_info < <(declare -p FUNCNAME)
      die_info="${die_info#declare -??}"
   else
      die_info="$*"
   fi

   echo -e "${bred}${die_message} ${die_info}${ansi_off}" >&2

   ~/bin/notify "$die_message" "$die_info" >/dev/null 2>&1 || :

   if [ -n "$debug" ]; then
      show_fail_source ${BASH_LINENO[0]} "${BASH_SOURCE[1]}"
      echo -ne "${ansi[off]}"
   fi >&2

   if [ $SHLVL -le 1 ]; then
      errortext "this shell will exit"
      confirm_cmd_execute exit 101
   else
      exit 100
   fi

}

show_fail_source() {

   show_fail_source_color="$yellow"
   printf '%s' "$show_fail_source_color$underline"
   nice_path "$2"
   printf '%s\n' "$not_underline"

   awk 'NR>L-4 && NR<L+4 { printf "%-5d%s\n",NR,$0 }' L=$1 "$2" |
      while read -r show_fail_source_line; do
         highlight_regex="^($1) "

         if [[ $show_fail_source_line =~ $highlight_regex ]]; then
            printf '%s%s%s\n' \
               "$invert" \
               "$show_fail_source_line" \
               "$ansi_off"
         else
            printf '%s%s\n' "$yellow" "$show_fail_source_line"
         fi
      done

}

nice_path() {
   if [[ "$1" == "$HOME/"* ]]; then
      printf "%s" "~${1#"$HOME"}"
   else
      printf "%s" "$1"
   fi
}

blockchart() {

   set -e
   [ ${BASH_VERSION:0:1} -ge 5 ]
   [ $# -gt 0 ]

   unset debug
   [[ "$1" == "-d" ]] && debug=true && shift

   if [[ "$1" == "-r" ]]; then
      bc_scheme=('🟩' '🟧' '🟥')
      shift
   else
      bc_scheme=('🟥' '🟨' '🟩')
   fi

   declare -i bc_metric_unadulterated=$(($1 + 0))

   bc_empty='\U2B1B'

   bc_precision=1000
   bc_metric_precision=$((bc_metric_unadulterated * bc_precision))
   bc_max=${2:-100}
   bc_maxblocks=${3:-10}

   # checks
   [ $bc_metric_unadulterated -le $bc_max ] || exit 1
   [ $bc_metric_unadulterated -ge 0 ] || exit 1

   bc_offset=$((bc_precision * bc_max / bc_maxblocks / 2))
   bc_metric=$((bc_metric_precision + bc_offset)) # for rounding

   bc_limits=($((0 * bc_max / 100))
      $((33 * bc_max / 100))
      $((66 * bc_max / 100))
   )

   bc_block_count=$((bc_metric * bc_maxblocks / bc_max / bc_precision))
   [ $bc_maxblocks -eq 1 ] && bc_block_count=1
   # unsure ^^
   bc_block_count_empty=$((bc_maxblocks - bc_block_count))

   declare -i bc_index=0
   bc_color="${bc_scheme[0]}"

   [ -n "$debug" ] && declare -p bc_max bc_maxblocks bc_block_count bc_metric bc_metric_precision bc_metric_unadulterated bc_offset bc_limits

   while [ $bc_index -lt ${#bc_limits[@]} ]; do
      if [ $bc_metric_unadulterated -ge ${bc_limits[$bc_index]} ]; then
         bc_color="${bc_scheme[$bc_index]}"
      fi
      bc_index+=1
   done

   while [ $((bc_block_count--)) -gt 0 ]; do
      echo -n "$bc_color"
   done

   while [ $((bc_block_count_empty--)) -gt 0 ]; do
      echo -ne "$bc_empty"
   done

}

cpu_usage() {
   top -b -n2 -p 1 | \grep "Cpu(s)" | tail -1 | awk -F'id,' -v prefix="$prefix" '{ split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf "%s%.1f%%\n",prefix, 100 - v }'
}

# [ ${BASH_VERSINFO[0]} -gt 5 ] || die "requires bash v5+"
# maybe we can do something for the slow learners .. maybe (experimental) so
# commenting this out for now
