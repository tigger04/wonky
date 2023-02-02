blockchart () {

    set -e
    [ ${BASH_VERSION:0:1} -ge 5 ]
    [ $# -gt 0 ]

    unset debug
    [[ "$1" == "-d" ]] && debug=true && shift

    if [[ "$1" == "-r" ]]; then
        bc_scheme=( '🟩' '🟨' '🟧' '🟥' )
        shift
    else
        bc_scheme=( '🟥' '🟧' '🟨' '🟩' )
    fi

    bc_metric_unadulterated=$(expr $1 + 0 )

    bc_empty='◼️'

    bc_precision=1000
    bc_metric_precision=$((bc_metric_unadulterated * bc_precision))
    bc_max=${2:-100}
    bc_maxblocks=${3:-10}

    # checks
    [ $bc_metric_unadulterated -le $bc_max ] || exit 1
    [ $bc_metric_unadulterated -ge 0 ] || exit 1

    bc_offset=$(( bc_precision * bc_max / bc_maxblocks / 2 ))
    bc_metric=$(( bc_metric_precision + bc_offset )) # for rounding

    bc_limits=( $(( 0 * bc_max / 100))
                $((25 * bc_max / 100))
                $((50 * bc_max / 100))
                $((75 * bc_max / 100))
              )

    bc_block_count=$(( bc_metric * bc_maxblocks / bc_max / bc_precision ))
    # [ $bc_block_count -eq 0 ] && bc_block_count=1
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

    while [ $((bc_block_count_empty--)) -gt 0 ] ; do
        echo -n "$bc_empty"
    done

}
